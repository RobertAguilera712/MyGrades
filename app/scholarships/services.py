from .forms import SchoolarshipForm
from app.models import Scholarship
from app.extensions import db


def add_scholarship(form: SchoolarshipForm, school_id: int) -> bool:
    try:
        scholarship = Scholarship(
            name=form.name.data,
            discount=form.discount.data,
            type=form.type.data,
            school_id=school_id,
        )
        db.session.add(scholarship)
        db.session.commit()
        return True
    except Exception as ex:
        db.session.rollback()
        print(f"Error while saving scholarship {str(ex)}")
    return False
