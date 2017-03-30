import flask
import flask_login
import app

from .forms import LoginForm
from .models import User


@app.main.route('/')
@app.main.route('/index')
@flask_login.login_required
def index():
    user = flask.g.user
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
    ]
    return flask.render_template(
            'index.html',
            title='Home',
            user=user,
            posts=posts)


@app.main.route('/login', methods=['GET', 'POST'])
@app.oid.loginhandler
def login():
    if flask.g.user is not None and flask.g.user.is_authenticated:
        return flask.redirect(flask.url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flask.session['remember_me'] = form.remember_me.data
        return app.oid.try_login(
                form.openid.data, ask_for=['nickname', 'email'])
    return flask.render_template(
            'login.html',
            title='Sign In',
            form=form,
            providers=app.main.config['OPENID_PROVIDERS'])


@app.oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flask.flash('Invalid login. Please try again')
        return flask.redirect(flask.url_for('login'))

    user = User.query.filter_by(email=resp.email).first()

    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]

        user = User(nickname=nickname, email=resp.email)
        app.db.session.add(user)
        app.db.session.commit()

    remember_me = False
    if 'remember_me' in flask.session:
        remember_me = flask.session['remember_me']
        flask.session.pop('remember_me', None)

    flask_login.login_user(user, remember=remember_me)
    return flask.redirect(
            flask.request.args.get('next') or flask.url_for('index'))


@app.main.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))


@app.lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.main.before_request
def before_request():
    flask.g.user = flask_login.current_user
