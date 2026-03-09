from flask import Flask, Blueprint
from .extensions import db, bcrypt, users_imgs, schools_imgs, login_manager, money_format
from .config import Config
from .login.routes import login
from .admin.routes import admin
from .page.routes import page
from .home.routes import home
from .schools.routes import schools
from .owner.routes import owner
from .groups.routes import groups
from .tuition.routes import tuition
from .scholarships.routes import scholarships
from .students.routes import students
from .payments.routes import payments
from app.models import *
from sqlalchemy import inspect, text
from flask_uploads import configure_uploads
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.jinja_env.filters['money'] = money_format

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    configure_uploads(app, [users_imgs, schools_imgs])

    app.register_blueprint(login)
    app.register_blueprint(admin)
    app.register_blueprint(page)
    app.register_blueprint(home)
    app.register_blueprint(schools)
    app.register_blueprint(owner)
    app.register_blueprint(groups)
    app.register_blueprint(tuition)
    app.register_blueprint(scholarships)
    app.register_blueprint(students)
    app.register_blueprint(payments)

    @app.context_processor
    def inject_current_year():
        return {"current_year": datetime.now().year}

    with app.app_context():
        create_db()
    return app


def create_db():
    inspector = inspect(db.engine)
    if not inspector.has_table(User.__tablename__):
        # Creating the db
        db.create_all()
        dummy_db_data()
        db.session.commit()


def dummy_db_data():
    # ADMIN USER
    email = "admin@gmail.com"
    password = "password"

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    person = Person()
    person.name = "Roberto"
    person.parent_last = "Aguilera"
    person.mother_last = "Alcantar"
    person.birthdate = datetime.now()
    person.email = email
    person.phone = "479-148-1494"
    person.address = "Calle #123"
    person.sex = True

    admin_user = User(
        email=email, password=hashed_password, role=UserRole.ADMIN, person=person
    )
    db.session.add(admin_user)
    # OWNER USER
    owner_mail = "owner@gmail.com"
    owner_user = User(
        email=owner_mail, password=hashed_password, role=UserRole.OWNER, person=person
    )
    owner = Owner(user=owner_user)

    school = School(name="My School", email="school@gmail.com", address="Address 123", owner=owner)
    db.session.add(school)
