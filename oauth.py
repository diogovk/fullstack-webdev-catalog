from app import flow
import requests
import json


# Loads facebook credentials for this server from json file
with open('fb_client_secret_webcatalog.json') as json_file:
    json_data = json.load(json_file)
    facebook_app_secret = json_data["app_secret"]
    facebook_app_id = json_data["app_id"]


def google_oauth(token, session):
    """
    Authenticates with google using a short-lived token, and getting a long
    one in the process.
    The login information and long lived token are stored in the session.

    Returns: http response with "ok" in case of success, or and http error
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

    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        return ('Current user is already connected', 200)

    session['credentials'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    session['username'] = data['name']
    session['email'] = data['email']
    session['provider'] = 'google'
    return ('ok', 200)


def facebook_oauth(token, session):
    """
    Authenticates with facebook using a short-lived token, and getting a long
    one in the process.
    The login information and long lived token are stored in the session.

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
    params = {
            'access_token': access_token,
            'fields': 'name,id,email'
            }
    # Gets user information from facebook api, and store it in the session
    api_url = 'https://graph.facebook.com/v2.4/me'
    answer = requests.get(api_url, params=params)
    data = answer.json()
    session['provider'] = 'facebook'
    session['username'] = data['name']
    session['email'] = data['email']
    session['facebook_id'] = data["id"]
    return ("ok", 200)


def google_revoke_token(token):
    url = "https://accounts.google.com/o/oauth2/revoke"
    answer = requests.get(url, params={"token": token})
    if answer.status_code != 200:
        # Most likely the token was invalid
        return False
    return True


def facebook_revoke_token(token):
    pass
