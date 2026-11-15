import pytest
import uuid

from app.models.calculation import (
    Calculation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
)

def dummy_user_id():
    return uuid.uuid4()

def test_addition_get_result():
    inputs = [10, 5, 3.5]
    addition = Addition(user_id=dummy_user_id(), inputs=inputs)
    result = addition.get_result()
    assert result == sum(inputs), f"Expected {sum(inputs)}, got {result}"

def test_subtraction_get_result():
    inputs = [20, 5, 3]
    subtraction = Subtraction(user_id=dummy_user_id(), inputs=inputs)
    result = subtraction.get_result()
    assert result == 12, f"Expected 12, got {result}"

def test_multiplication_get_result():
    inputs = [2, 3, 4]
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=inputs)
    result = multiplication.get_result()
    assert result == 24, f"Expected 24, got {result}"

def test_division_get_result():
    inputs = [100, 2, 5]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    result = division.get_result()
    assert result == 10, f"Expected 10, got {result}"

def test_division_by_zero():
    inputs = [50, 0, 5]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        division.get_result()

#Tests for Polymorphic Factory Pattern

def test_calculation_factory_addition():
    inputs = [1, 2, 3]
    calc = Calculation.create(
        calculation_type='addition',
        user_id=dummy_user_id(),
        inputs=inputs,
    )

    assert isinstance(calc, Addition), \
        "Factory did not return an Addition instance."
    assert isinstance(calc, Calculation), \
        "Addition should also be an instance of Calculation."
    assert calc.get_result() == sum(inputs), "Incorrect addition results."

def test_calculation_factory_subtraction():
    inputs = [10, 4]
    calc = Calculation.create(
        calculation_type='subtraction',
        user_id=dummy_user_id(),
        inputs=inputs,
    )

    assert isinstance(calc, Subtraction), \
        "Factory did not return a Subtraction instance."
    assert calc.get_result() == 6, "Incorrect subtraction result."

def test_calculation_factory_multiplication():
    inputs = [3, 4, 2]
    calc = Calculation.create(
        calculation_type='multiplication',
        user_id=dummy_user_id(),
        inputs=inputs,
    )

    assert isinstance(calc, Multiplication), \
        "Factory did not return a Multiplication instance."
    assert calc.get_result() == 24, "Incorrect multiplication result."

def test_calculation_factory_division():
    inputs = [100, 2, 5]
    calc = Calculation.create(
        calculation_type='division',
        user_id=dummy_user_id(),
        inputs=inputs,
    )

    assert isinstance(calc, Division), \
        "Factory did not return a Division instance."
    assert calc.get_result() == 10, "Incorrect division result."

def test_calculation_factory_invalid_type():
    with pytest.raises(ValueError, match="Unsupported calculation type"):
        Calculation.create(
            calculation_type='modulus',
            user_id=dummy_user_id(),
            inputs=[10, 3],
        )

def test_calculation_factory_case_insensitive():
    inputs = [5, 3]
    for calc_type in['addition', 'Addition', 'ADDITION', 'AdDiTiOn']:
        calc = Calculation.create(
            calculation_type=calc_type,
            user_id=dummy_user_id(),
            inputs=inputs,
        )
        assert isinstance(calc, Addition), \
            f"Factory failed for case: {calc_type}"
        assert calc.get_result() == 8

#Tests for Input Validation

def test_invalid_inputs_for_addition():
    addition = Addition(user_id=dummy_user_id(), inputs="not-a-list")
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        addition.get_result()

def test_invalid_inputs_for_subtraction():
    subtraction = Subtraction(user_id=dummy_user_id(), inputs=[10])
    with pytest.raises(
        ValueError,
        match="Inputs must be a list with at least two numbers."
    ):
        subtraction.get_result()

def test_invalid_inputs_for_multiplication():
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=[5])
    with pytest.raises(
        ValueError, 
        match="Inputs must be a list with at least two numbers."
    ):
        multiplication.get_result()

def test_invalid_inputs_for_division():
    division = Division(user_id=dummy_user_id(), inputs=[10])
    with pytest.raises(
        ValueError,
        match="Inputs must be a list with at least two numbers."
    ):
        division.get_result()

def test_division_by_zero_in_middle():
    inputs = [10, 5, 0, 2]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        division.get_result()

def test_division_by_zero_at_end():
    inputs = [50, 5, 0]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        division.get_result()

#Tests demonstrating Polymorphic Behavior

def test_polymorphic_list_of_calculations():
    user_id = dummy_user_id()
    calculations = [
        Calculation.create('addition', user_id, [1, 2, 3]),
        Calculation.create('subtraction', user_id, [10, 3]),
        Calculation.create('multiplication', user_id, [2, 3, 4]),
        Calculation.create('division', user_id, [100, 5]),
    ]

    assert isinstance(calculations[0], Addition)
    assert isinstance(calculations[1], Subtraction)
    assert isinstance(calculations[2], Multiplication)
    assert isinstance(calculations[3], Division)

    results = [calc.get_result() for calc in calculations]
    assert results == [6, 7, 24, 20]

def test_polymorphic_method_calling():
    user_id = dummy_user_id()
    inputs = [10, 2]

    calc_types = ['addition', 'subtraction', 'multiplication', 'division']
    expected_results = [12, 8, 20, 5]

    for calc_type, expected in zip(calc_types, expected_results):
        calc = Calculation.create(calc_type, user_id, inputs)
        result = calc.get_result()
        assert result == expected, \
            f"{calc_type} failed: expected {expected}, got {result}"