import requests

from flask.blueprints import Blueprint
from flask import session, redirect, url_for, render_template, make_response


main_bp = Blueprint(__name__, 'main', template_folder='templates', static_folder='static', url_prefix='/main')

@main_bp.route('/')
def main_view():
    """Представление главной страницы сайта"""
    if not 'vk_token' in session:
        return redirect(url_for('auth.views.login_view'))
    context = {}
    # Получаем список друзей.
    vk_response = requests.get(f'https://api.vk.com/method/friends.get?'
                               f'order=random'
                               f'&count=5'
                               f'&fields=nickname,domain,photo_200'
                               f'&access_token={session["vk_token"]}&'
                               f'v=5.122')
    try:
        context['items'] = vk_response.json()['response']['items']
    except KeyError:
        context.setdefault('errors', []).append('Ошибка при загрузке пяти рандомных друзей.')

    # Получаем информацию об аккаунте.
    vk_response_user_info = requests.get(f'https://api.vk.com/method/users.get?'
                               f'access_token={session["vk_token"]}'
                               f'&v=5.122')
    print(vk_response_user_info.json())
    try:
        context['user'] = vk_response_user_info.json()['response'][0]
    except KeyError:
        context.setdefault('errors', []).append('Ошибка при загрузке аккаунта пользователя.')

    print(context)

    return make_response(render_template('main_page.html', **context))
