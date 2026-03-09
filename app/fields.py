from wtforms import (
    SelectField,
)
from app.models import (
    Group,
    Scholarship,
    Student,
    Tuition,
)
from wtforms.widgets import html_params, Select
from markupsafe import Markup
from flask import session

# TODO: Filter groups and tuition that belong to the current school the user is logged in


class GroupsField(SelectField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = []  # Initialize empty to avoid None

    def iter_choices(self):
        school_id = session.get("school_id", None)
        groups = [
            (g.id, f"{g.id} {g.name}")
            for g in Group.query.filter_by(school_id=school_id).all()
        ]
        for value, label in groups:
            yield (value, label, self.coerce(value) == self.data, {})

    def pre_validate(self, form):
        # Skip the parent class validation since we load dynamically
        school_id = session.get("school_id", None)
        groups = [
            (g.id, f"{g.id} {g.name}")
            for g in Group.query.filter_by(school_id=school_id).all()
        ]
        valid_values = {value for value, _ in groups}
        if self.data not in valid_values:
            self.errors.append("Selecciona una opción válida")


class TuitionField(SelectField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = []  # Initialize empty to avoid None

    def iter_choices(self):
        school_id = session.get("school_id", None)
        tuitions = [
            (t.id, f"{t.id} {t.name}")
            for t in Tuition.query.filter_by(school_id=school_id).all()
        ]
        for value, label in tuitions:
            yield (value, label, self.coerce(value) == self.data, {})

    def pre_validate(self, form):
        # Skip the parent class validation since we load dynamically
        school_id = session.get("school_id", None)
        tuitions = [
            (t.id, f"{t.id} {t.name}")
            for t in Tuition.query.filter_by(school_id=school_id).all()
        ]
        valid_values = {value for value, _ in tuitions}
        if self.data not in valid_values:
            self.errors.append("Selecciona una opción válida")


class ScholarshipsField(SelectField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = []  # Initialize empty to avoid None

    def iter_choices(self):
        school_id = session.get("school_id", None)
        scholarships = [
            (s.id, f"{s.id} {s.name}")
            for s in Scholarship.query.filter_by(school_id=school_id).all()
        ]
        scholarships.insert(0, (0, f"Seleccionar {self.label.text}"))
        for value, label in scholarships:
            yield (value, label, self.coerce(value) == self.data, {})

    def pre_validate(self, form):
        # Skip the parent class validation since we load dynamically
        school_id = session.get("school_id", None)
        scholarships = [
            (s.id, f"{s.id} {s.name}")
            for s in Scholarship.query.filter_by(school_id=school_id).all()
        ]
        scholarships.insert(0, (0, f"Seleccionar {self.label.text}"))
        valid_values = {value for value, _ in scholarships}
        if self.data not in valid_values:
            self.errors.append("Selecciona una opción válida")


class StudentsField(SelectField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = []  # Initialize empty to avoid None

    def iter_choices(self):
        school_id = session.get("school_id", None)
        students = [
            (s.id, f"{s.group.name} {s.user.person.full_name}")
            for s in Student.query.filter_by(school_id=school_id).all()
        ]
        students.insert(0, (0, f"Seleccionar {self.label.text}"))
        for value, label in students:
            yield (value, label, self.coerce(value) == self.data, {})

    def pre_validate(self, form):
        # Skip the parent class validation since we load dynamically
        school_id = session.get("school_id", None)
        students = [
            (s.id, f"{s.group.name} {s.user.person.full_name}")
            for s in Student.query.filter_by(school_id=school_id).all()
        ]
        valid_values = {value for value, _ in students}
        if self.data not in valid_values:
            self.errors.append("Selecciona una opción válida")
