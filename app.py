import os


from flask import redirect, url_for

from core import app
from auth.views import auth_bp
from main.views import main_bp


def init_vk_credentials(app):
    """Парсит необходимые для работы вк апи данные."""
    app.vk = {
        'client_id': '7583966',
        # Чтобы не распространяться ключем приложения, берем его из переменной окружения.
        'client_secret': os.getenv('vk_client_secret', None),
        'authorization_base_url': 'https://oauth.vk.com/authorize',
        'token_url': 'https://oauth.vk.com/access_token',
        'redirect_uri': 'http://127.0.0.1:5000/auth/callback'
    }
    assert app.vk['client_secret'], 'Не задана переменная окружения vk_client_secret.'

def run_app(app):
    app.secret_key = b'\x93 \xe7\xaed\x19\xbc\xdc\xfe\x1c^\xe4\xe3QB\x7f'

    # Для локального использования отключаем необходимость https.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    init_vk_credentials(app)

    app.run(debug=True)

@app.route('/')
def redirect_view():
    return redirect(url_for('main.views.main_view'))

if __name__ == '__main__':
    run_app(app)
