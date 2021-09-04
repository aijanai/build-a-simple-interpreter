import unittest
import pytest
from myparser import *

class InterpreterTest(unittest.TestCase):
        def test_init(self):
                text = "1+1"
                i = Interpreter(text)
                assert(i._current_token.value == 1)
                assert(i._current_token.type == INTEGER)

        def test_eat_happy(self):
                text = "1+1"
                i = Interpreter(text)
                try:
                        i._eat(INTEGER)
                except:
                        pytest.fail("It shouldn't throw")

                assert(i._current_token.value == '+')
                assert(i._current_token.type == PLUS)

        def test_eat_wrong(self):
                text = "1+1"
                i = Interpreter(text)
                try:
                        i._eat(PLUS)
                except:
                        assert(i._current_token.value == 1)
                        assert(i._current_token.type == INTEGER)

                i = Interpreter(text)
                try:
                        i._eat(EOF)
                except:
                        assert(i._current_token.value == 1)
                        assert(i._current_token.type == INTEGER)

        def test_term_happy(self):
                text = "1+1"
                i = Interpreter(text)
                try:
                        res = i._term()
                        assert(res == 1)
                except:
                        pytest.fail("It shouldn't throw")

        def test_term_happy(self):
                text = "1+1"
                i = Interpreter(text)
                try:
                        res = i._term()
                        res = i._term()
                        pytest.fail("PLUS is not a term")
                except:
                        assert(res == 1)

        def test_expr_multidigit(self):
                text = "10+1"
                i = Interpreter(text)
                result = i.expr()
                assert(result == 11)

        def test_expr_zero(self):
                text = "1-1"
                i = Interpreter(text)
                result = i.expr()
                assert(result == 0)

        def test_expr_negative(self):
                text = "6-7"
                i = Interpreter(text)
                result = i.expr()
                assert(result == -1)

        def test_expr_mul(self):
                text = "2*3"
                i = Interpreter(text)
                result = i.expr()
                assert(result == 6)

        def test_expr_div(self):
                text = "4/2"
                i = Interpreter(text)
                result = i.expr()
                assert(result == 2)

        def test_expr_multi_operands(self):
                text = "6-7+0-10"
                i = Interpreter(text)
                result = i.expr()
                assert(result == -11)

                text = "6-7*2"
                i = Interpreter(text)
                result = i.expr()
                assert(result == -8)

                text = "(3+2)*8"
                i = Interpreter(text)
                result = i.expr()
                assert(result == 40)

                text = "(3*2)*8"
                i = Interpreter(text)
                result = i.expr()
                assert(result == 48)

                text = "(((3)))"
                i = Interpreter(text)
                result = i.expr()
                assert(result == 3)
