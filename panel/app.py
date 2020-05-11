import logging

import vk_api
from flask import Flask, render_template, redirect
from flask_login import login_user, LoginManager, current_user, login_required, logout_user
from flask_ngrok import run_with_ngrok
from flask_restful import Api

from bot.api import VkApi
from panel.api import UsersResource, UsersListResource
from panel.data import db_session
from panel.data.db_session import create_session
from panel.data.forms.login_form import LoginForm
from panel.data.forms.manage import ManageForm
from panel.data.models.all_conferences import Conference
from panel.data.models.all_users import User
from panel.data.models.conference_user import ConferenceUser
from panel.data.models.panel_user import PanelUser

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'our secret key'
login_manager = LoginManager()
login_manager.init_app(app)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

api.add_resource(UsersResource, '/api/user/<key>/<int:user_id>')
api.add_resource(UsersListResource, '/api/conf_users/<key>/<int:conference_id>')


def main():
    print('Web-panel is started!')
    db_session.global_init()
    address = run_with_ngrok(app)
    app.run()


@app.route('/')
def main_page():
    return render_template('main_page.html', title='Привет. Я бот!')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(PanelUser).get(user_id)


@app.route('/panel_login', methods=['GET', 'POST'])
def panel_login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        session = create_session()
        user = session.query(PanelUser).filter(
            (PanelUser.login == login_form.login.data) |
            (PanelUser.user_id == login_form.login.data)).filter(
            PanelUser.password == login_form.password.data).first()
        if user:
            login_user(user, remember=login_form.remember_me.data)
            return redirect("/panel")
        return render_template('login_page.html',
                               title='Что-то не то...',
                               message="Псс... Неправильный логин или пароль!",
                               form=login_form)
    return render_template('login_page.html', title='Логинься уже...', form=login_form)


@login_required
@app.route('/panel')
def panel():
    session = create_session()
    if current_user.is_authenticated:
        return render_template('general_panel.html', title='Панель моя панель',
                               user_conferences=session.query(User).filter(
                                   User.user_id == current_user.user_id).first().conferences)
    return redirect('/panel_login')


@login_required
@app.route('/manage/<int:conference_id>')
def manage(conference_id):
    def users_dict(users):
        res = {}
        for u in users:
            res.update({u.user_id: {'name': u.name, 'surname': u.surname}})
        return res

    session = create_session()
    if conference_id in [c.conference_id for c in
                         session.query(User).filter(User.user_id == current_user.user_id).first().conferences]:
        users_ids = [u.user_id for u in session.query(ConferenceUser).filter(ConferenceUser.conference_id ==
                                                                             conference_id).all()]
        return render_template('manage_conf.html',
                               title='Управление беседой',
                               conference=session.query(Conference).filter(Conference.conference_id ==
                                                                           conference_id).first(),
                               conf_users=session.query(ConferenceUser).filter(ConferenceUser.conference_id ==
                                                                               conference_id).all(),
                               users=users_dict([session.query(User).filter(User.user_id == user_id).first() for user_id
                                                 in users_ids]))
    else:
        return redirect('/no-access')


@login_required
@app.route('/edit/<int:conference_id>', methods=['GET', 'POST'])
def edit_conference(conference_id):
    session = create_session()
    form = ManageForm()
    user = session.query(ConferenceUser).filter(ConferenceUser.conference_id == conference_id,
                                                ConferenceUser.user_id == current_user.user_id).first()
    conference = session.query(Conference).filter(Conference.conference_id == conference_id).first()
    if form.validate_on_submit():
        if user.is_admin or user.title_change:
            if form.title.data:
                try:
                    VkApi().set_title(conference_id - 2000000000, form.title.data)
                except vk_api.exceptions.ApiError as e:
                    return redirect(f'/failed/{e}')
                conference.title = form.title.data
        if user.is_admin:
            if form.hello_msg.data:
                conference.hello_message = form.hello_msg.data
            conference.auto_kick = form.auto_kick.data
            conference.archived = form.archived.data
        session.commit()
        return redirect(f'/manage/{conference_id}')
    return render_template('edit.html', title='Настройки беседы', form=form, user=user, conference=conference)


@login_required
@app.route('/kick/<int:conference_id>/<int:user_id>')
def kick(conference_id, user_id):
    def user_kick(peer_id, user_id):
        if user_id > 0:
            user = session.query(User).filter(User.user_id == user_id).first()
            conference = session.query(Conference).filter(Conference.conference_id == peer_id).first()
            conference_user = session.query(ConferenceUser).filter(ConferenceUser.conference_id == peer_id,
                                                                   ConferenceUser.user_id == user_id).first()

            conference_user.set_defaults()
            conference_user.is_leave = True
            conference_user.kicks += 1
            session.commit()

    session = create_session()
    curr_user = session.query(ConferenceUser).filter(ConferenceUser.conference_id == conference_id,
                                                     ConferenceUser.user_id == current_user.user_id).first()

    kicked_user = session.query(ConferenceUser).filter(ConferenceUser.conference_id == conference_id,
                                                       ConferenceUser.user_id == user_id).first()

    if not kicked_user.kick_immunity and curr_user.kick:
        try:
            VkApi().kick_user(chat_id=conference_id - 2000000000, member_id=user_id)
            user_kick(conference_id, user_id)
            return redirect(f'/manage/{conference_id}')
        except vk_api.exceptions.ApiError as e:
            return redirect(f'/failed/{e}')


@app.route('/failed/<e>')
def failed(e):
    return render_template('failed.html', msg=e, msglines=e.split('\n'), title='Сбой в программе...')


@app.route('/top')
def top():
    session = create_session()
    return render_template('top.html', title='Топ бесед',
                           conferences=session.query(Conference).filter(Conference.archived == False).order_by(
                               -Conference.msg_count).all())


@app.route('/no-access')
def no_access():
    return render_template('no_access.html', title='Нет прав...')


@app.route('/creators')
def creators():
    return render_template('creators.html', title='Создатели')


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', title='Found not')


if __name__ == '__main__':
    main()
