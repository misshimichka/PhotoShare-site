import os
import math

from flask import Flask, render_template, redirect
from werkzeug.exceptions import abort

from data import db_session
from data.users import User
from data.images import Image
import datetime
from forms.registerForm import RegisterForm
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from forms.loginForm import LoginForm
from forms.changeInfoForm import ChangeInfoForm
from forms.photoForm import PhotoForm
import base64

from change_image import change_size

app = Flask(__name__)
app.config['SECRET_KEY'] = 'My_Photo_Project'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/photos.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return render_template("index.html", user=current_user)


@app.route("/profile")
def profile():
    db_sess = db_session.create_session()
    result = db_sess.query(User).filter(User.id == current_user.id).first()
    f = open(f"static/img/images/{current_user.id}.jpg", mode="wb")
    if result.avatar is None:
        return render_template("profile.html", name=current_user.name, about=current_user.about,
                               image=f"static/img/img1.jpg")
    f.write(base64.b64decode(result.avatar))
    return render_template("profile.html", name=current_user.name, about=current_user.about,
                           image=f"static/img/images/{current_user.id}.jpg")


@app.route("/main")
@app.route("/main/<int:page_id>")
def main_page(page_id=1):
    import os
    import glob

    files = glob.glob('static/img/images/*')
    for f in files:
        os.remove(f)

    db_sess = db_session.create_session()
    photos = db_sess.query(Image).all()

    x = []
    for i in photos[(page_id - 1) * 3: page_id * 3]:
        f = open(f"static/{photos.index(i)}.jpg", mode="wb")
        f.write(base64.b64decode(i.image))
        change_size(f"static/{photos.index(i)}.jpg")
        user = db_sess.query(User).filter(User.id == i.user_id).first()
        x.append((f"{photos.index(i)}.jpg", i.about, i.name, user.name, i.id))
    return render_template("main_page.html", photos=x, page=page_id, len=math.ceil(len(photos) / 3))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/profile")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
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
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/change_info", methods=["GET", "POST"])
@login_required
def change_info():
    import os
    import glob

    files = glob.glob('static/img/images/*')
    for f in files:
        os.remove(f)

    form = ChangeInfoForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        image = Image()
        current_user.name = form.name.data
        current_user.about = form.about.data
        image.user_id = current_user.id
        form.image.data.save(f"static/img/images/{current_user.id}.jpg")
        f = open(f"static/img/images/{current_user.id}.jpg", mode="rb").read()
        image.image = base64.b64encode(f)
        current_user.avatar = base64.b64encode(f)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/profile')
    return render_template('change_info.html', title='Добавление работы',
                           form=form)


@app.route('/add_photo', methods=['GET', 'POST'])
@login_required
def add_photo():
    import os
    import glob

    files = glob.glob('static/*.jpg')
    for f in files:
        os.remove(f)

    form = PhotoForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        image = Image()
        image.name = form.name.data
        image.about = form.about.data
        form.image.data.save(f"static/{form.image.data.filename}")
        f = open(f"static/{form.image.data.filename}", mode="rb").read()
        image.image = base64.b64encode(f)
        image.user_id = current_user.id
        db_sess.merge(current_user)
        db_sess.add(image)
        db_sess.commit()
        return redirect('/main')
    return render_template('add_photo.html',
                           form=form)


@app.route("/dev")
def dev():
    return render_template("developer.html")


@app.route("/delete_photo/<int:image_id>")
@app.route("/delete_photo")
def delete_photo(image_id=1):
    db_sess = db_session.create_session()
    result = db_sess.query(Image).filter(Image.id == image_id, Image.user_id == current_user.id).first()
    if result:
        db_sess.delete(result)
        db_sess.commit()
    return redirect("/main")


# @app.route('/jobs/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_jobs(id):
#     form = JobForm()
#     if request.method == "GET":
#         db_sess = db_session.create_session()
#         jobs = db_sess.query(Jobs).filter(Jobs.id == id,
#                                           Jobs.user == current_user
#                                           ).first()
#         if jobs:
#             form.job.data = jobs.job
#             form.team_leader_id.data = jobs.team_leader
#             form.work_size.data = jobs.work_size
#             form.collaborators.data = jobs.collaborators
#             form.is_finished.data = jobs.is_finished
#         else:
#             abort(404)
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         jobs = db_sess.query(Jobs).filter(Jobs.id == id,
#                                           Jobs.user == current_user).first()
#         if jobs:
#             jobs.job = form.job.data
#             jobs.team_leader = form.team_leader_id.data
#             jobs.work_size = form.work_size.data
#             jobs.collaborators = form.collaborators.data
#             jobs.is_finished = form.is_finished.data
#             db_sess.commit()
#             return redirect('/')
#         else:
#             abort(404)
#     return render_template('job.html',
#                            title='Редактирование новости',
#                            form=form
#                            )
#
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    main()
