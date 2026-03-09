from .forms import GroupForm
from app.models import Group
from app.extensions import db

def add_group(form: GroupForm, school_id: int) -> bool:
    try:
        group = Group(name = form.name.data, school_id=school_id)
        db.session.add(group)
        db.session.commit()
        return True
    except Exception as ex:
        db.session.rollback()
        print(f"Error while creating group {str(ex)}")
    return False

