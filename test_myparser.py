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
                l.advance()
                assert(l._current_position == 1)
                assert(l._current_char == '+')
                l.advance()
                assert(l._current_position == 2)
                assert(l._current_char == '1')
                l.advance()
                assert(l._current_position == 3)
                assert(l._current_char == None)
                l.advance()
                assert(l._current_position == 3)
                assert(l._current_char == None)

        def test_advance_single(self):
                text = "1"
                l = Lexer(text)
                assert(l._current_position == 0)
                assert(l._current_char == '1')
                l.advance()
                assert(l._current_position == 1)
                assert(l._current_char == None)

        def test_get_next_token_1plus1(self):
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

        def test_get_next_token_1minus1(self):
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

 #       def test_get_next_token
