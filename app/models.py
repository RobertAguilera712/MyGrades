from .extensions import db, login_manager, users_imgs, schools_imgs, get_current_time
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from flask_login import UserMixin
from flask import url_for
from sqlalchemy import or_
from datetime import timedelta, datetime
from enum import Enum


class UserRole(Enum):
    ADMIN = 0
    OWNER = 1
    EMPLOYEE = 2
    STUDENT = 3


class ScholarshipType(Enum):
    QUANTITY = 0
    PERCENTAGE = 1


class PaymentType(Enum):
    CASH = 0
    DIGITAL = 1



class RowStatus(Enum):
    INACTIVE = 0
    ACTIVE = 1


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(45), nullable=False)
    parent_last = db.Column(db.String(45), nullable=False)
    mother_last = db.Column(db.String(45), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    curp = db.Column(db.String(18), nullable=True)
    sex = db.Column(db.Boolean, nullable=False)
    phone = db.Column(db.String(12), nullable=True)
    address = db.Column(db.String(256), nullable=False)
    estatus = db.Column(db.Enum(RowStatus), nullable=False, default=RowStatus.ACTIVE)

    @hybrid_property
    def full_name(self):
        return f"{self.name} {self.parent_last} {self.mother_last}"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    image_filename = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(RowStatus), nullable=False, default=RowStatus.ACTIVE)
    person = db.relationship("Person", lazy=True, uselist=False)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    role = db.Column(db.Enum(UserRole), nullable=False)

    @hybrid_property
    def image_url(self):
        url = (
            url_for(
                "_uploads.uploaded_file",
                setname=users_imgs.name,
                filename=self.image_filename,
                _external=True,
            )
            if self.image_filename != None and len(self.image_filename) > 0
            else url_for("static", filename="img/users/default.png", _external=True)
        )
        return url


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(45), nullable=False)
    image_filename = db.Column(db.String(255))
    address = db.Column(db.String(256), nullable=False)
    owner = db.relationship("Owner", lazy=True, uselist=False, backref="school")
    students_query = db.relationship("Student", lazy="dynamic", backref="school")
    employees_query = db.relationship("Employee", lazy="dynamic", backref="school")
    groups_query = db.relationship("Group", lazy="dynamic", backref="school")
    tutions_query = db.relationship("Tuition", lazy="dynamic", backref="school")
    scholarships_query = db.relationship("Scholarship", lazy="dynamic", backref="school")
    sells_query = db.relationship("Sell", lazy="dynamic", backref="school")
    estatus = db.Column(db.Enum(RowStatus), nullable=False, default=RowStatus.ACTIVE)

    ## CHANGE FOR SHCOOL IMAGE SET
    @hybrid_property
    def image_url(self):
        url = (
            url_for(
                "_uploads.uploaded_file",
                setname=schools_imgs.name,
                filename=self.image_filename,
                _external=True,
            )
            if self.image_filename != None and len(self.image_filename) > 0
            ## SET DEFAULT IMAGE FOR SCHOOL
            else url_for("static", filename="img/users/default.png", _external=True)
        )
        return url

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship("User", lazy=True, uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    school_id = db.Column(db.Integer, db.ForeignKey("school.id"))
    estatus = db.Column(db.Enum(RowStatus), nullable=False, default=RowStatus.ACTIVE)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship("User", lazy=True, uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    school_id = db.Column(db.Integer, db.ForeignKey("school.id"))
    estatus = db.Column(db.Enum(RowStatus), nullable=False, default=RowStatus.ACTIVE)

class Group(db.Model):
    # Can have a classroom
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True)
    students_query = db.relationship("Student", lazy="dynamic", backref="group")
    school_id = db.Column(db.Integer, db.ForeignKey("school.id"))
    estatus = db.Column(db.Enum(RowStatus), nullable=False, default=RowStatus.ACTIVE)


class Tuition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    payment_period = db.Column(db.Integer, nullable=False, default=30) # Period in the days the tuition must be paid
    students_query = db.relationship("Student", lazy="dynamic", backref="tuition")
    school_id = db.Column(db.Integer, db.ForeignKey("school.id"))
    estatus = db.Column(db.Enum(RowStatus), nullable=False, default=RowStatus.ACTIVE)


class Scholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    discount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.Enum(ScholarshipType), nullable=False)
    students_query = db.relationship("Student", lazy="dynamic", backref="scholarship")
    school_id = db.Column(db.Integer, db.ForeignKey("school.id"))
    estatus = db.Column(db.Enum(RowStatus), nullable=False, default=RowStatus.ACTIVE)



class Student(db.Model):
    # Can have grades, it needs subjects and have a grade for each one, consider failed, partials and all that stuff, pretty complex
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship("User", lazy=True, uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    school_id = db.Column(db.Integer, db.ForeignKey("school.id"))
    tuition_id = db.Column(db.Integer, db.ForeignKey("tuition.id"))
    scholarship_id = db.Column(db.Integer, db.ForeignKey("scholarship.id"))
    sells_query = db.relationship("Sell", lazy="dynamic", backref="student")
    estatus = db.Column(db.Enum(RowStatus), nullable=False, default=RowStatus.ACTIVE)

    @hybrid_property
    def last_payment_date(self):
        return self.sells_query.all()[-1].date

    @hybrid_property
    def next_payment_date(self):
        return self.last_payment_date + timedelta(days=self.tuition.payment_period)


# THIS TABLE RECORDS ALL THE DATA RELATED TO THE TUITION PAYMENTS STUDENTS DO
class Sell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment = db.Column(db.Numeric(10, 2), nullable=False)
    payment_type = db.Column(db.Enum(PaymentType), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=get_current_time)
    details = db.relationship("SellDetails", lazy=True, backref="sell")
    school_id = db.Column(db.Integer, db.ForeignKey("school.id"))
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    status = db.Column(db.Enum(RowStatus), nullable=False, default=RowStatus.ACTIVE)

    @hybrid_property
    def subtotal(self):
        return sum([i.price * i.quantity for i in self.details])

    @hybrid_property
    def total(self):
        return self.subtotal

    @hybrid_property
    def change(self):
        return float(self.payment) - self.total




class SellDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sell_id = db.Column(db.Integer, db.ForeignKey("sell.id"))
    tuition = db.relationship("Tuition", lazy=True, uselist=False)
    tuition_id = db.Column(db.Integer, db.ForeignKey("tuition.id"))
    schoolarship = db.relationship("Scholarship", lazy=True, uselist=False)
    scholarship_id = db.Column(db.Integer, db.ForeignKey("scholarship.id"))
    quantity = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(RowStatus), nullable=False, default=RowStatus.ACTIVE)
