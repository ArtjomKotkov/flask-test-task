import requests

from requests_oauthlib import OAuth2Session
from flask.blueprints import Blueprint
from flask import session, redirect, request, url_for, jsonify, render_template

from core import app

auth_bp = Blueprint(__name__, 'auth', template_folder='templates', static_folder='static', url_prefix='/auth')

@auth_bp.route('/logout')
def logout_view():
    del session['vk_token']
    session.modified = True
    return redirect(url_for('main.views.main_view'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        scope = ['friends']
        vk = OAuth2Session(client_id=app.vk['client_id'], redirect_uri=app.vk['redirect_uri'], scope=scope)
        authorization_url, state = vk.authorization_url(app.vk['authorization_base_url'])
        session['state'] = state
        return redirect(authorization_url)
    if not 'vk_token' in session:
        return render_template('auth_page.html')
    return redirect(url_for('main.views.main_view'))


@auth_bp.route('/callback')
def callback_view():

    code = request.args.get('code')

    token_response = requests.get(app.vk['token_url'], params=dict(
        client_id=app.vk['client_id'],
        client_secret=app.vk['client_secret'],
        redirect_uri=app.vk['redirect_uri'],
        code=code
    ))

    try:
        session['vk_token'] = token_response.json()['access_token']
    except KeyError:
        return redirect(url_for('main.views.main_view'))
    return redirect(url_for('main.views.main_view'))