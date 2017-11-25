'''
MIT License

Copyright (c) 2017 Stephen Gargan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Defines the validators used by commands. Validators are defined in the required and optional
methods of the command.
'''

import inspect

from decree.command import Command
from decree.exceptions import MissingRequiredError
from decree.exceptions import NotDefiningArgsException
from decree.exceptions import NotNoneError
from decree.exceptions import UnexpectedTypeError


class CommandValidatorEnricher(type):
    '''
    metaclass that automatically defines validators on the Command class as they are
    defined. This will allow custom Validators to be added from outside the decree
    module
    '''

    def __init__(cls, name, bases, clsdict):
        super(CommandValidatorEnricher, cls).__init__(name, bases, clsdict)

        for arg_name in cls.arg_method_names():
            CommandValidatorEnricher._define_arg_validator(arg_name, cls)

    def _define_arg_validator(arg_name, validator):
        '''
        defines an arg validator method with the given name on the Command object. The arg
        validator can be used during the command_args definition function adding a validator
        for that type to the map of validators in the command. It is only valid to call an
        arg definition function during command_args and so any attempt do sooutside of it
        will fail.
        '''
        def _create_arg_validator(command_class, name, **command_args):
            if not command_class.defining_args:
                raise NotDefiningArgsException()
            command_class.validators[name] = validator(name, **command_args)

        setattr(Command, arg_name, classmethod(_create_arg_validator))


class Validator(metaclass=CommandValidatorEnricher):
    '''
    Base validator class. Validators vet command arguments validating their
    type, presence and possible defaults.
    '''

    def __init__(self, name, default=None, allow_none=True):
        if not name:
            raise ValueError("validator requires a name")

        self.name = name
        self.allow_none = allow_none
        self.default = default

        if self.default:
            self.validate_type('default for {}'.format(name), default)

    def type_name(self):
        '''
        the name of the validator type, used to compare to the actual type of the command
        arg. Also used to create a method on the command object used to define args for the
        command.
        '''
        raise NotImplementedError('validator must implement type_name')

    @classmethod
    def arg_method_names(cls):
        return []

    def validate_type(self, name, value):
        actual_type = type(value).__name__
        if not actual_type == self.type_name():
            raise UnexpectedTypeError(name, self.type_name(), actual_type)
        return value

    def validate(self, args):
        present = self.name in args
        if present:
            value = args[self.name]
            if not (self.allow_none or value):
                raise NotNoneError(self.name)
            return self.validate_type(self.name, value)
        else:
            if not self.default:
                raise MissingRequiredError(self.name)
            return self.default


class IntValidator(Validator):
    def type_name(self):
        return "int"

    @classmethod
    def arg_method_names(cls):
        return ['int', 'integer']


class BooleanValidator(Validator):
    def type_name(self):
        return "bool"

    @classmethod
    def arg_method_names(cls):
        return ['bool', 'boolean']


class StringValidator(Validator):
    def type_name(self):
        return "str"

    @classmethod
    def arg_method_names(cls):
        return ['string', 'str']


class FloatValidator(Validator):
    def type_name(self):
        return "float"

    @classmethod
    def arg_method_names(cls):
        return ['float']


class DictValidator(Validator):
    def type_name(self):
        return "dict"

    @classmethod
    def arg_method_names(cls):
        return ['dict', 'map']


class SetValidator(Validator):
    def type_name(self):
        return "set"

    @classmethod
    def arg_method_names(cls):
        return ['set']


class ListValidator(Validator):
    def type_name(self):
        return "list"

    @classmethod
    def arg_method_names(cls):
        return ['list', 'array']


class ObjectValidator(Validator):

    def __init__(self, name, type=None, default=None, allow_none=True):
        super().__init__(name, default, allow_none)
        if not type:
            raise ValueError("Object validator requires a type argument")

        if inspect.isclass(type):
            self.type = type.__name__
        else:
            self.type = type

    def type_name(self):
        return self.type

    @classmethod
    def arg_method_names(cls):
        return ['object', 'type']
