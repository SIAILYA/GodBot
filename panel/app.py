from flask import Flask, render_template

from panel.data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init(r"C:\Yandex\Flask-YaL\db\jobs.sqlite")
    app.run()


@app.route('/')
def main_page():
    return render_template('main_page.html', title='Привет. Я бот!')


if __name__ == '__main__':
    main()
