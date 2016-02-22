from app import flow
import requests


def google_oauth(token, session):
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
