import unittest
import pytest
from myparser import *

class InterprerTest(unittest.TestCase):
        def test_init(self):
                text = "1+1"
                i = Interpreter(text)
                assert(i._parser._current_token.value == 1)
                assert(i._parser._current_token.type == INTEGER)

        def text_interpret_multidigit(self):
                text = "10+1"
                i = Interpreter(text)
                result = i.interpret()
                assert(result == 11)

        def text_interpret_zero(self):
                text = "1-1"
                i = Interpreter(text)
                result = i.interpret()
                assert(result == 0)

        def text_interpret_negative(self):
                text = "6-7"
                i = Interpreter(text)
                result = i.interpret()
                assert(result == -1)

        def text_interpret_mul(self):
                text = "2*3"
                i = Interpreter(text)
                result = i.interpret()
                assert(result == 6)

        def text_interpret_div(self):
                text = "4/2"
                i = Interpreter(text)
                result = i.interpret()
                assert(result == 2)

        def text_interpret_multi_operands(self):
                text = "6-7+0+10"
                i = Interpreter(text)
                result = i.interpret()
                assert(result == 9)

                text = "6-7*2"
                i = Interpreter(text)
                result = i.interpret()
                assert(result == -8)

                text = "(3+2)*8"
                i = Interpreter(text)
                result = i.interpret()
                assert(result == 40)

                text = "(3*2)*8"
                i = Interpreter(text)
                result = i.interpret()
                assert(result == 48)

                text = "(((3)))"
                i = Interpreter(text)
                result = i.interpret()
                assert(result == 3)

                text = "5 - - - + - (3 + 4) - +2"
                i = Interpreter(text)
                result = i.interpret()
                assert(result == 10)
