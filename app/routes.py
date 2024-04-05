from flask import * 
from app import *
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit
from app.forms import *
from app.models import *

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Code was succesfully submitted")
        return redirect(url_for("index"))
    
    filter_form = FilterForm()
    if request.args.get("my") == "on":
        query = sa.select(Post).where(Post.author == current_user)
    else:
        query = sa.select(Post)
    posts = db.session.scalars(query).all()

    return render_template('index.html', title='Home', form=form, filter_form=filter_form, posts=posts)

@app.route("/admin")
@login_required
def explore():
    # a hack
    if current_user.username != "her":
        return redirect(url_for("index"))

    posts = db.session.scalars(sa.select(Post))
    return render_template("index.html", title="Admin", posts=posts)

@app.route("/submission/<int:idx>")
def submission(idx):
    res = db.session.scalar(sa.select(Post).where(Post.id == idx))
    if not res:
        abort(404)

    return render_template("submission.html", title="View Submission", code=res.body)

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
