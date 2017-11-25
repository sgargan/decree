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
'''
from pytest import raises

from decree.command import Command
from decree.exceptions import MissingRequiredError
from decree.exceptions import NotDefiningArgsException


def test_basic_run_with_no_args():
    class NoArgsCommand(Command):
        def execute(self):
            return 1234
    assert NoArgsCommand.run() == 1234


def test_basic_run_with_no_exec():
    class NoExecutesCommand(Command):
        pass
    assert NoExecutesCommand.run() is None


def test_run_with_required_args():
    class WithRequiredArgCommand(Command):
        @classmethod
        def command_args(cmd):
            cmd.int('someint')

        def execute(self):
            return self.someint
    assert WithRequiredArgCommand.run(someint=4321) == 4321

    with raises(MissingRequiredError):
        WithRequiredArgCommand.run()


def test_run_with_default_arg():

    class WithRequiredDefaultArgCommand(Command):
        @classmethod
        def command_args(cmd):
            cmd.int('someint', default=1234)

        def execute(self):
            return self.someint

    assert WithRequiredDefaultArgCommand.run() == 1234


def test_may_not_use_validators_outside_args_definition():

    class UsesValidatorOutsideCommandArgs(Command):
        @classmethod
        def command_args(cmd):
            pass

        def execute(self):
            self.__class__.int('someint')

    with raises(NotDefiningArgsException):
        UsesValidatorOutsideCommandArgs.run()


class BaseCommand(Command):
    @classmethod
    def command_args(cmd):
        cmd.int('someint', default=1234)

    def execute(self):
        return self.someint


class NestedCommand(BaseCommand):
    @classmethod
    def command_args(cmd):
        cmd.int('anotherint', default=2345)

    def execute(self):
        return [self.someint, self.anotherint]


class FurtherNestedCommand(NestedCommand):
    @classmethod
    def command_args(cmd):
        cmd.string('somestring', default='some arg')

    def execute(self):
        return [self.someint, self.anotherint, self.somestring]


class RedefiningCommand(BaseCommand):
    @classmethod
    def command_args(cmd):
        cmd.int('someint', default=3456)


def test_nested_command_has_parents_validators():
    assert NestedCommand.run() == [1234, 2345]
    assert FurtherNestedCommand.run() == [1234, 2345, 'some arg']


def test_args_can_be_redefined_in_subcommands():
    assert RedefiningCommand.run() == 3456
