from .forms import TuitionForm
from app.models import Tuition
from app.extensions import db


def add_tuition(form: TuitionForm, school_id: int) -> bool:
    try:
        tuition = Tuition(
            name=form.name.data, school_id=school_id, price=form.price.data
        )
        db.session.add(tuition)
        db.session.commit()
        return True
    except Exception as ex:
        db.session.rollback()
        print(f"Error while creating tuition {str(ex)}")
    return False
