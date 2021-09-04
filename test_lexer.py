import unittest
import pytest
from myparser import *

class LexerTest(unittest.TestCase):
        def test_init(self):
                text = "1+1"
                l = Lexer(text)
                assert(l._text == text)
                assert(l._current_position == 0)
                assert(l._current_char == '1')
                assert(l._current_token == None)
                assert(l._text_len == len(text))

        def test_advance_happy(self):
                text = "1+1"
                l = Lexer(text)
                assert(l._current_position == 0)
                assert(l._current_char == '1')
                l._advance()
                assert(l._current_position == 1)
                assert(l._current_char == '+')
                l._advance()
                assert(l._current_position == 2)
                assert(l._current_char == '1')
                l._advance()
                assert(l._current_position == 3)
                assert(l._current_char == None)
                l._advance()
                assert(l._current_position == 3)
                assert(l._current_char == None)

        def test_advance_single(self):
                text = "1"
                l = Lexer(text)
                assert(l._current_position == 0)
                assert(l._current_char == '1')
                l._advance()
                assert(l._current_position == 1)
                assert(l._current_char == None)

        def test_get_next_token_plus(self):
                text_1plus1 = "1+1"
                l = Lexer(text_1plus1)

                t = l.get_next_token()
                assert(t.value == 1)
                assert(t.type == INTEGER)
                t = l.get_next_token()
                assert(t.value == '+')
                assert(t.type == PLUS)
                t = l.get_next_token()
                assert(t.value == 1)
                assert(t.type == INTEGER)
                t = l.get_next_token()
                assert(t.value == None)
                assert(t.type == EOF)

        def test_get_next_token_whitespace(self):
                text_1plus1 = "1 + 1"
                l = Lexer(text_1plus1)

                t = l.get_next_token()
                assert(t.value == 1)
                assert(t.type == INTEGER)
                t = l.get_next_token()
                assert(t.value == '+')
                assert(t.type == PLUS)
                t = l.get_next_token()
                assert(t.value == 1)
                assert(t.type == INTEGER)
                t = l.get_next_token()
                assert(t.value == None)
                assert(t.type == EOF)

                text_1plus1 = "1 +1"
                l = Lexer(text_1plus1)

                t = l.get_next_token()
                assert(t.value == 1)
                assert(t.type == INTEGER)
                t = l.get_next_token()
                assert(t.value == '+')
                assert(t.type == PLUS)
                t = l.get_next_token()
                assert(t.value == 1)
                assert(t.type == INTEGER)
                t = l.get_next_token()
                assert(t.value == None)
                assert(t.type == EOF)

                text_1plus1 = "1+ 1"
                l = Lexer(text_1plus1)

                t = l.get_next_token()
                assert(t.value == 1)
                assert(t.type == INTEGER)
                t = l.get_next_token()
                assert(t.value == '+')
                assert(t.type == PLUS)
                t = l.get_next_token()
                assert(t.value == 1)
                assert(t.type == INTEGER)
                t = l.get_next_token()
                assert(t.value == None)
                assert(t.type == EOF)

        def test_get_next_token_minus(self):
                text_1minus1 = "1-1"
                l = Lexer(text_1minus1)

                t = l.get_next_token()
                assert(t.value == 1)
                assert(t.type == INTEGER)
                t = l.get_next_token()
                assert(t.value == '-')
                assert(t.type == MINUS)
                t = l.get_next_token()
                assert(t.value == 1)
                assert(t.type == INTEGER)
                t = l.get_next_token()
                assert(t.value == None)
                assert(t.type == EOF)

        def test_get_next_token_mul(self):
                text_2x3 = "2*3"
                l = Lexer(text_2x3)

                t = l.get_next_token()
                assert(t.value == 2)
                assert(t.type == INTEGER)
                t = l.get_next_token()
                assert(t.value == '*')
                assert(t.type == MUL)
                t = l.get_next_token()
                assert(t.value == 3)
                assert(t.type == INTEGER)
                t = l.get_next_token()
                assert(t.value == None)
                assert(t.type == EOF)

        def test_get_next_token_div(self):
                text_4div2 = "4/2"
                l = Lexer(text_4div2)

                t = l.get_next_token()
                assert(t.value == 4)
                assert(t.type == INTEGER)
                t = l.get_next_token()
                assert(t.value == '/')
                assert(t.type == DIV)
                t = l.get_next_token()
                assert(t.value == 2)
                assert(t.type == INTEGER)
                t = l.get_next_token()
                assert(t.value == None)
                assert(t.type == EOF)

        def test_parse_integer(self):
                text_multi = '1111'
                l = Lexer(text_multi)

                t = l.get_next_token()
                assert(t.value == 1111)
                assert(t.type == INTEGER)

        def test_get_next_token_multidigit(self):
                text_multi = '111+222'
                l = Lexer(text_multi)

                t = l.get_next_token()
                assert(t.value == 111)
                assert(t.type == INTEGER)
                t = l.get_next_token()
                assert(t.value == '+')
                assert(t.type == PLUS)
                t = l.get_next_token()
                assert(t.value == 222)
                assert(t.type == INTEGER)
                t = l.get_next_token()
                assert(t.value == None)
                assert(t.type == EOF)

        def test_get_next_token_invalid(self):
                text_multi = '@'
                l = Lexer(text_multi)

                try:
                        t = l.get_next_token()
                        pytest.fail("It shouldn't parse @")
                except:
                        assert(l._current_char == '@')
