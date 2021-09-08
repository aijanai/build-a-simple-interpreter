import unittest
import pytest
from myparser import *

class ParserTest(unittest.TestCase):
        def test_init(self):
                text = "1+1"
                i = Parser(text)
                assert(i._current_token.value == 1)
                assert(i._current_token.type == INTEGER)

        def test_eat_happy(self):
                text = "1+1"
                i = Parser(text)
                try:
                        i._eat(INTEGER)
                except:
                        pytest.fail("It shouldn't throw")

                assert(i._current_token.value == '+')
                assert(i._current_token.type == PLUS)

        def test_eat_wrong(self):
                text = "1+1"
                i = Parser(text)
                try:
                        i._eat(PLUS)
                except:
                        assert(i._current_token.value == 1)
                        assert(i._current_token.type == INTEGER)

                i = Parser(text)
                try:
                        i._eat(EOF)
                except:
                        assert(i._current_token.value == 1)
                        assert(i._current_token.type == INTEGER)

        def test_term_happy(self):
                text = "1+1"
                i = Parser(text)
                try:
                        res = i._term()
                        assert(res == 1)
                except:
                        pytest.fail("It shouldn't throw")

        def test_term_happy(self):
                text = "1+1"
                i = Parser(text)
                try:
                        res = i._term()
                        res = i._term()
                        pytest.fail("PLUS is not a term")
                except:
                        assert(res.value == 1)

        def test_expr_multidigit(self):
                text = "10+1"
                i = Parser(text)
                result = i.expr()
                #assert(result == 11)
                assert(type(result) == BinOp)
                assert(result.op == PLUS)

        def test_expr_zero(self):
                text = "1-1"
                i = Parser(text)
                result = i.expr()
                #assert(result == 0)
                assert(type(result) == BinOp)
                assert(result.op == MINUS)

        def test_expr_negative(self):
                text = "6-7"
                i = Parser(text)
                result = i.expr()
                #assert(result == -1)
                assert(type(result) == BinOp)
                assert(result.op == MINUS)

        def test_expr_mul(self):
                text = "2*3"
                i = Parser(text)
                result = i.expr()
                #assert(result == 6)
                assert(type(result) == BinOp)
                assert(result.op == MUL)

        def test_expr_div(self):
                text = "4/2"
                i = Parser(text)
                result = i.expr()
                #assert(result == 2)
                assert(type(result) == BinOp)
                assert(result.op == DIV)

        def test_expr_multi_operands(self):
                text = "6-7+0+10"
                i = Parser(text)
                result = i.expr()
                #assert(result == 9)
                assert(type(result) == BinOp)
                assert(result.op == PLUS)

                text = "6-7*2"
                i = Parser(text)
                result = i.expr()
                #assert(result == -8)
                assert(type(result) == BinOp)
                assert(result.op == MINUS)

                text = "(3+2)*8"
                i = Parser(text)
                result = i.expr()
                #assert(result == 40)
                assert(type(result) == BinOp)
                assert(result.op == MUL)

                text = "(3*2)*8"
                i = Parser(text)
                result = i.expr()
                #assert(result == 48)
                assert(type(result) == BinOp)
                assert(result.op == MUL)

                text = "(((3)))"
                i = Parser(text)
                result = i.expr()
                assert(type(result) == NumOp)
                assert(result.value == 3)
