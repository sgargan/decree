from pytest import raises

from decree.exceptions import MissingRequiredError
from decree.exceptions import NotNoneError
from decree.exceptions import UnexpectedTypeError
from decree.validators import BooleanValidator
from decree.validators import DictValidator
from decree.validators import FloatValidator
from decree.validators import IntValidator
from decree.validators import ListValidator
from decree.validators import ObjectValidator
from decree.validators import SetValidator
from decree.validators import StringValidator
from decree.validators import Validator


class SomeClass():
    def __eq__(self, other):
        return type(other) == type(self)


args = {'somebool': True,
        'someint': 1234,
        'somefloat': 1.234,
        'somestring': 'blah',
        'somelist': [1, 2, 3, 4],
        'somedict': {1: 2, 3: 4},
        'someset': set([1, 2, 3, 4]),
        'not_none': None,
        'someclass': SomeClass()}


def test_validator_requires_name():
    with raises(ValueError, match='validator requires a name'):
        BooleanValidator(None).validate(args)


def test_validator_must_implement_type_name():
    class TypeNameNotImplemented(Validator):
        pass

    with raises(NotImplementedError, match='validator must implement type_name'):
        TypeNameNotImplemented('someint').validate(args)


def test_boolean_validator():
    assert BooleanValidator('somebool').validate(args)
    with raises(UnexpectedTypeError,
                match="Expected 'someint' to be of type 'bool' but was 'int'"):
        BooleanValidator('someint').validate(args)


def test_int_validator():
    assert IntValidator('someint').validate(args) == 1234
    with raises(UnexpectedTypeError,
                match="Expected 'somestring' to be of type 'int' but was 'str'"):
        IntValidator('somestring').validate(args)


def test_string_validator():
    assert StringValidator('somestring').validate(args) == 'blah'
    with raises(UnexpectedTypeError,
                match="Expected 'someint' to be of type 'str' but was 'int'"):
        StringValidator('someint').validate(args)


def test_float_validator():
    assert FloatValidator('somefloat').validate(args) == 1.234
    with raises(UnexpectedTypeError,
                match="Expected 'someint' to be of type 'float' but was 'int'"):
        FloatValidator('someint').validate(args)


def test_list_validator():
    assert ListValidator('somelist').validate(args) == [1, 2, 3, 4]
    with raises(UnexpectedTypeError,
                match="Expected 'someint' to be of type 'list' but was 'int'"):
        ListValidator('someint').validate(args)


def test_dict_validator():
    assert DictValidator('somedict').validate(args) == {1: 2, 3: 4}
    with raises(UnexpectedTypeError,
                match="Expected 'someint' to be of type 'dict' but was 'int'"):
        DictValidator('someint').validate(args)


def test_set_validator():
    assert SetValidator('someset').validate(args) == set([1, 2, 3, 4])
    with raises(UnexpectedTypeError,
                match="Expected 'someint' to be of type 'set' but was 'int'"):
        SetValidator('someint').validate(args)


def test_object_validator():
    assert ObjectValidator('someclass', type='SomeClass').validate(
        args) == SomeClass()
    with raises(UnexpectedTypeError,
                match="Expected 'someint' to be of type 'SomeClass' but was 'int'"):
        assert ObjectValidator('someint', type='SomeClass').validate(args)


def test_object_validator_requires_type():
    with raises(ValueError, match="Object validator requires a type argument"):
        assert ObjectValidator('someint')


def test_object_validator_passing_class_as_type():
    assert ObjectValidator('someclass', type=SomeClass).validate(
        args) == SomeClass()
    with raises(UnexpectedTypeError,
                match="Expected 'someint' to be of type 'SomeClass' but was 'int'"):
        assert ObjectValidator('someint', type=SomeClass).validate(args)


def test_required():
    with raises(MissingRequiredError,
                match="Argument 'notpresent' not present in command args"):
        IntValidator('notpresent').validate(args)


def test_required_with_default():
    IntValidator('notpresent', default=1234).validate(args) == 1234


def test_not_none():
    with raises(NotNoneError, match="Argument 'not_none' may not be None"):
        IntValidator('not_none', allow_none=False).validate(args)


def test_default():
    assert IntValidator('notpresent', default=1234).validate(args) == 1234

    with raises(UnexpectedTypeError,
                match="Expected 'default for someint' to be of type 'int' but was 'str'"):
        IntValidator('someint', default='not an int')
