from datetime import datetime
from app.extensions import hash_password, users_imgs, db
from app.models import (
    Person,
    Student,
    User,
    UserRole,
    Tuition,
    Sell,
    PaymentType,
    SellDetails,
    Scholarship,
    ScholarshipType,
)
from .forms import StudentForm


def get_sell(
    tuition: Tuition, scholarship: Scholarship, school_id: int
) -> Sell:
    details = SellDetails()
    discount = (
        scholarship.discount
        if scholarship.type == ScholarshipType.QUANTITY
        else tuition.price * scholarship.discount / 100
    )
    details.discount = discount
    details.price = tuition.price
    details.quantity = 1
    details.scholarship_id = scholarship.id
    details.tuition_id = tuition.id

    sell = Sell()
    sell.payment = tuition.price - discount
    sell.payment_type = PaymentType.CASH
    sell.school_id = school_id
    sell.details.append(details)
    return sell


def add_student(form: StudentForm, school_id: int) -> bool:
    try:
        person_data = form.user.person.data
        person_data.pop("csrf_token", None)
        person_user = Person(**person_data)
        student_user = User(
            email=form.user.email.data,
            password=hash_password(form.user.password.data),
            person=person_user,
            role=UserRole.STUDENT,
        )

        tuition = Tuition.query.get(form.tuition.data)
        scholarship = Scholarship.query.get(form.scholarship.data)

        student = Student(
            user=student_user,
            tuition = tuition,
            scholarship = scholarship,
            school_id=school_id,
            group_id=form.group.data,
        )

        sell = get_sell(tuition, scholarship, school_id)
        student.sells_query.append(sell)

        # TODO: ADD USER IMAGE PIC
        # if form.user.image.data:
        #     image_filename = users_imgs.save(
        #         form.image.data, name=f"{student_user.email}_{datetime.now().timestamp()}."
        #     )
        #     student_user.image_filename = image_filename
        db.session.add(student)
        db.session.commit()
        return True
    except Exception as ex:
        # TODO: ADD LOGGER
        print(f"Error while saving student {str(ex)}")
        db.session.rollback()
    return False
