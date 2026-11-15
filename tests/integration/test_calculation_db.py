import pytest
import uuid
from sqlalchemy.exc import IntegrityError
from app.models.calculation import (
    Calculation, 
    Addition,
    Subtraction,
    Multiplication,
    Division,
)

def test_insert_calculation_saves_to_db(db_session, test_user):
    user_id = test_user.id
    calc = Calculation.create("addition", user_id, [10, 5])
    calc.result = calc.get_result()
    db_session.add(calc)
    db_session.commit()
    calc_id = calc.id
    db_session.expunge_all()

    saved = db_session.query(Calculation).filter_by(id=calc_id).first()
    assert saved is not None
    assert isinstance(saved, Addition)
    assert saved.inputs == [10, 5]
    assert saved.result == 15
    assert saved.user_id == user_id


def test_insert_subtraction_saves_to_db(db_session, test_user):
    user_id = test_user.id
    calc = Calculation.create("subtraction", user_id, [10, 5])
    calc.result = calc.get_result()
    db_session.add(calc)
    db_session.commit()
    calc_id = calc.id
    db_session.expunge_all()

    saved = db_session.query(Calculation).filter_by(id=calc_id).first()
    assert saved is not None
    assert isinstance(saved, Subtraction)
    assert saved.inputs == [10, 5]
    assert saved.result == 5
    assert saved.user_id == user_id


def test_insert_multiplication_saves_to_db(db_session, test_user):
    user_id = test_user.id
    calc = Calculation.create("multiplication", user_id, [10, 5])
    calc.result = calc.get_result()
    db_session.add(calc)
    db_session.commit()
    calc_id = calc.id
    db_session.expunge_all()

    saved = db_session.query(Calculation).filter_by(id=calc_id).first()
    assert saved is not None
    assert isinstance(saved, Multiplication)
    assert saved.inputs == [10, 5]
    assert saved.result == 50
    assert saved.user_id == user_id


def test_insert_division_saves_to_db(db_session, test_user):
    user_id = test_user.id
    calc = Calculation.create("division", user_id, [10, 5])
    calc.result = calc.get_result()
    db_session.add(calc)
    db_session.commit()
    calc_id = calc.id
    db_session.expunge_all()

    saved = db_session.query(Calculation).filter_by(id=calc_id).first()
    assert saved is not None
    assert isinstance(saved, Division)
    assert saved.inputs == [10, 5]
    assert saved.result == 2
    assert saved.user_id == user_id


def test_calculation_with_invalid_user_id(db_session):
    fake_user_id = uuid.uuid4()
    calc = Calculation.create("addition", fake_user_id, [10, 5])
    db_session.add(calc)
    
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
    assert db_session.query(Calculation).filter_by(user_id=fake_user_id).first() is None
