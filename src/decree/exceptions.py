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

Defines exceptions raised by decree.
'''


class ValidationError(Exception):
    '''Base validation Error'''
    pass


class NotDefiningArgsException(Exception):
    '''Error raised if a validator method is called outside of the command_args function'''

    def __init__(self):
        super().__init__("Validations can only be defined during command_args")


class MissingRequiredError(ValidationError):
    '''Error raised when a required command arg is missing'''

    def __init__(self, name):
        super().__init__("Argument '{}' not present in command args".format(name))


class NotNoneError(ValidationError):
    '''Error raised when None is passed for an arg which may not be None'''

    def __init__(self, name):
        super().__init__("Argument '{}' may not be None".format(name))


class UnexpectedTypeError(ValidationError):
    '''Error raised when the type of a command arg is not as expected'''

    def __init__(self, name, expected_type, actual_type):
        super().__init__("Expected '{}' to be of type '{}' but was '{}'".format(
            name, expected_type, actual_type
        ))
