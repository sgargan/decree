# -*- coding: utf-8 -*-
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

Defines the base Command object which is the core of Interact.
'''


class CommandArgDefiner(type):
    '''
    metaclass invoked every time Command is subclassed, calling the subclasses' command_args
    function to define its arguments. Each command inherits its parent commands argument validators
    which it can override if it wishes. The full set of validators is stored in the command
    class and called each time the command is executed
    '''
    def __init__(cls, name, bases, clsdict):
        super(CommandArgDefiner, cls).__init__(name, bases, clsdict)

        cls.validators = {}

        # get the validators from the first command found in the hierachy
        # if present they will also contain the validators from its parent
        for base in bases:
            if base.validators:
                cls.validators = base.validators.copy()
                break

        try:
            cls.defining_args = True
            cls.command_args()
        finally:
            cls.defining_args = False


class Command(metaclass=CommandArgDefiner):
    '''
    Base Command object.
    '''
    @classmethod
    def command_args(cmd):
        '''
        Used to define arguments for the command. Validators are created when the command is
        defined and are used each time the command is run to validate the the keyword args
        supplied to run. Run will raise a ValidationError if the required args are missing
        or incorrect
        def command_args(cmd):
            cmd.int('someint', default=6)
            cmd.object('someobject', type=SomeObject)

        Args:
           cmd: the class of the command, arg defining methods can be called on this
        '''
        pass

    @classmethod
    def run(cls, **command_args):
        '''
        runs the command, validating the arguments and calling
        the overridden execute method.

        Args:
         command_args: arbitrary keyword args which get validated by name
        '''
        instance = cls()
        return instance.run_instance(**command_args)

    def run_instance(self, **command_args):
        '''
        runs an instance of a command, validating the arguments and calling
        the overridden execute method.

        Args:
         command_args: arbitrary keyword args which get validated by name
        '''
        self._validate_args(command_args)
        self.validate()
        return self.execute()

    def _validate_args(self, command_args):
        '''
        Iterates each of the validators defined during the command's command_args method.
        It uses them to vet the keyword command_args supplied to run. As each argument is
        vetted its is added as an attribute on the command instance so that it is easily accessible
        during the command execution.
        '''
        self.raw_args = command_args
        for validator in self.__class__.validators.values():
            validated_arg = validator.validate(command_args)
            self.__dict__[validator.name] = validated_arg

    def validate(self):
        '''
        validate method called after args have been vetted to allow custom argument
        validation and should raise an Exception to indicate a validation issue
        '''
        pass

    def execute(self):
        '''
        execute command called when the arguments have been vetted and ay custom validation
        has passed.
        '''
        pass
