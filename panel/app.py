from flask import Flask, render_template, redirect
from flask_login import login_user, LoginManager

from panel.data import db_session
from panel.data.db_session import create_session
from panel.data.forms.login_form import LoginForm
from panel.data.models.all_users import User
from panel.data.models.panel_user import PanelUser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'our secret key'
login_manager = LoginManager()
login_manager.init_app(app)


# TODO:
#  3. Сделать грамотную систему прав в панели, чтобы юзер мог иметь доступ только к определенным беседам
#  (надо связывать с таблицей)
#  4. Сделать регистрацию пользователей -
#  один/несколько способов ( на сайте, логин/пароль присылается ВК/ссылка на редактирование присылается ВК (как
#  ссылку генерировать, отслеживать?))
#  5. Сделать красивый шаблон отображения информации о беседе (ПРИВАТНОСТЬ ОТОБРАЖЕНИЯ ЗАДАЕТСЯ В НАСТРОЙКАХ!!!!)


def main():
    db_session.global_init()
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
            (PanelUser.login == login_form.login.data) | (PanelUser.email == login_form.login.data)).first()
        if user and user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            return redirect("/panel")
        return render_template('login_page.html',
                               title='Что-то не то...',
                               message="Псс... Неправильный логин или пароль!",
                               form=login_form)
    return render_template('login_page.html', title='Логинься уже...', form=login_form)


@app.route('/panel')
def panel():
    session = create_session()
    # TODO: Сделать панель
    return render_template('general_panel.html', title='Панель моя панель',
                           user_conferences=session.query(User).filter(User.user_id == 223632391).first().conferences)


@app.route('/login')
def login():
    pass


if __name__ == '__main__':
    main()
