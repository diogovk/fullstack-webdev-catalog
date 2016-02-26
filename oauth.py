from app import flow
import urlparse
import requests
import json
from models import User


# Loads facebook credentials for this server from json file
with open('fb_client_secret_webcatalog.json') as json_file:
    json_data = json.load(json_file)
    facebook_app_secret = json_data["app_secret"]
    facebook_app_id = json_data["app_id"]


def google_oauth(token, session):
    """
    Authenticates with google using a short-lived token, and getting a long
    one in the process.
    The following will be stored in session:
    * user_id - Local ID of the user
    * username - Name of the user
    * access_token - Long lived token received from google
    * email - User's email
    * provider - The login provider (google)
    * gplus_id - ID of the user in google

    Returns: http response with "ok" in case of success, or an http error
             in the case of an error.
    """
    try:
        credentials = flow.step2_exchange(token)
    except FlowAExchangeError:
        return ('Failed to upgrade the authorization token (step2)', 401)

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    answer = requests.get(url)
    result = answer.json()
    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        return (result.get('error'), 500)

    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return ("Token's used ID doesn't match given user", 401)

    # Verify that the access token is valid for this app.
    if result['issued_to'] != flow.client_id:
        return ("Token's client ID does not match app's", 401)

    stored_access_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        return ('Current user is already connected', 200)

    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    session['user_id'] = User.get_or_create(data['email']).id
    session['username'] = data['name']
    session['email'] = data['email']
    session['provider'] = 'google'
    return ('ok', 200)


def facebook_oauth(token, session):
    """
    Authenticates with facebook using a short-lived token, and getting a long
    one in the process.
    The following will be stored in session:
    * user_id - Local ID of the user
    * username - Name of the user
    * access_token - Long lived token received from google
    * email - User's email
    * provider - The login provider (facebook)
    * facebook_id - The user ID in Facebook

    Returns: http response with "ok" in case of success, or and http error in
             the case of an error.
    """
    if 'provider' in session:
        return ("you're already logged in", 200)
    params = {
            'client_id': facebook_app_id,
            'client_secret': facebook_app_secret,
            'fb_exchange_token': token,
            'grant_type': 'fb_exchange_token'
            }
    # Get long-lived access token from facebook
    token_exchange_url = "https://graph.facebook.com/oauth/access_token"
    answer = requests.get(token_exchange_url, params=params)
    access_token = urlparse.parse_qs(answer.text)["access_token"][0]
    session['access_token'] = access_token
    params = {
            'access_token': access_token,
            'fields': 'name,id,email'
            }
    # Gets user information from facebook api, and store it in the session
    api_url = 'https://graph.facebook.com/v2.4/me'
    answer = requests.get(api_url, params=params)
    data = answer.json()
    session['user_id'] = User.get_or_create(data['email']).id
    session['provider'] = 'facebook'
    session['username'] = data['name']
    session['email'] = data['email']
    session['facebook_id'] = data["id"]
    return ("ok", 200)


def google_revoke_token(token):
    """ Uses google api to revoke a access_token.
    Return the http status code received from server"""
    url = "https://accounts.google.com/o/oauth2/revoke"
    answer = requests.get(url, params={"token": token})
    return answer.status_code


def facebook_revoke_token(facebook_id, token):
    """ Uses facebook api to revoke a access_token
    Return the http status code received from server"""
    url = "https://graph.facebook.com/%s/permissions" % facebook_id
    answer = requests.delete(url, params={"access_token": token})
    return answer.status_code
