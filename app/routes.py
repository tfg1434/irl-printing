from flask import * 
from app import *
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User
from urllib.parse import urlsplit
from app.forms import LoginForm, RegistrationForm

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None:
            flash("invalid username")
            return redirect(url_for("login"))
        login_user(user, remember=True)

        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc == "":
            next_page = url_for("index")
        return redirect(next_page)

    return render_template('login.html',  title='Sign In', form=form)

@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a user!")
        return redirect(url_for("login"))
    
    return render_template("register.html", title="Register for a new account", form=form)
