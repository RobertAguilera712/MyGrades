from .forms import SchoolForm
from app.models import Person, User, School, UserRole, Owner
from app.extensions import hash_password, db, schools_imgs
from datetime import datetime


def add_school(form: SchoolForm) -> bool:
    try:
        person_data = form.owner.person.data
        person_data.pop("csrf_token", None)
        person_user = Person(**person_data)
        owner_user = User(
            email=form.owner.email.data,
            password=hash_password(form.owner.password.data),
            person=person_user,
            role=UserRole.OWNER,
        )
        owner = Owner(user=owner_user)
        school = School(
            name=form.name.data,
            email=form.email.data,
            address=form.address.data,
            owner=owner,
        )
        if form.image.data:
            image_filename = schools_imgs.save(form.image.data, name=f"{school.email}_{datetime.now().timestamp()}.")
            school.image_filename = image_filename
        db.session.add(school)
        db.session.commit()
        return True
    except Exception as ex:
        # TODO: ADD LOGGER
        print(f"Error while saving school {str(ex)}")
        db.session.rollback()
    return False
