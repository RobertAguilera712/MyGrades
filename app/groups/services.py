from .forms import GroupForm
from app.models import Group
from app.extensions import db

def edit_group(form: GroupForm, group: Group) -> bool:
    try:
        group.name = form.name.data
        db.session.commit()
        return True
    except Exception as ex:
        db.session.rollback()
        ## TODO: ADD LOGGER
        print(f"Error while editing group {str(ex)}")
    return False



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

