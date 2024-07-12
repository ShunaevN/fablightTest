import datetime
from dotenv import dotenv_values
from flask import Flask, render_template, abort, redirect, request
from flask_login import LoginManager, login_user, \
    login_required, logout_user, current_user

from data import db_session
from data.users import User
from forms.user import RegisterForm
from forms.login import LoginForm
from forms.change_user import UserForm
from flask_restful import abort

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

config = dotenv_values(".env")

app.config['SECRET_KEY'] = config["SECRET_KEY"]

app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=int(config["PERMANENT_SESSION_LIFETIME"])
)


@login_manager.user_loader
def load_user(user_id):
    """ get user from database by id """
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def main():
    """
        start app endpoint with rendering index.html
        and creating database connection
    """
    db_session.global_init("db/users.db")
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        if current_user.is_admin:
            users = db_sess.query(User).all()
            return render_template("index.html", users=users)
        return render_template("index.html", users=[])
    else:
        return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    """ endpoint of user's registration """
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ endpoint of user's login """
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/users',  methods=['GET', 'POST'])
@login_required
def add_user():
    """ add new user endpoint"""
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        users = User()
        users.email = form.email.data
        users.name = form.name.data
        if form.password.data == form.password_again.data:
            users.set_password(form.password.data)
        db_sess.add(users)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Добавление пользователя',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    """ logout user endpoint """
    logout_user()
    return redirect("/")


@app.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """ edit user by id endpoint """
    form = UserForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        users = db_sess.query(User).filter(User.id == id).first()
        if users:
            form.name.data = users.name
            form.email.data = users.email
            form.is_admin.data = users.is_admin
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        users = db_sess.query(User).filter(User.id == id).first()
        if users:
            users.name = form.name.data
            users.email = form.email.data
            users.is_admin = form.is_admin.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('users.html',
                           title='Редактирование пользователя',
                           form=form
                           )


@app.route('/user_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def user_delete(id):
    """ delete user from database by id """
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.id == id).first()
    if users:
        db_sess.delete(users)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)
