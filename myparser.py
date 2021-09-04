
EOF, INTEGER, PLUS, MINUS = 'EOF', 'INTEGER', 'PLUS', 'MINUS'
# token: models content and type of data
class Token(object):

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "TOKEN({type}, {value})".format(type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()



# lexer: parses string and returns tokens

class Lexer(object):

    def __init__(self, text):
        self._text = text
        self._current_position = 0
        self._current_char = self._text[self._current_position]
        self._text_len = len(self._text)
        self._current_token = None

    def _advance(self):
        """read another unit of the input in the current state"""
        # advance pointer
        self._current_position+=1

        # check pointer bounds
        if self._current_position +1 > self._text_len :
            self._current_char = None
            self._current_position = self._text_len
        else:
            self._current_char = self._text[self._current_position]


    def _parse_integer(self):
        """parse multi digit integer"""
        number = ''
        while self._current_char is not None and self._current_char.isdigit() :
            number += self._current_char
            self._advance()
        return int(number)

    def get_next_token(self):
        """interpret current state into a token"""

        # infer a symbol
        symbol = None

        current_char = self._current_char

        if current_char is None:
            return Token(EOF, current_char)
        if current_char == '+':
            symbol = PLUS
            self._advance()
            return Token(symbol, current_char)
        if current_char == '-':
            symbol = MINUS
            self._advance()
            return Token(symbol, current_char)
        if current_char.isdigit():
            number = self._parse_integer()
            symbol = INTEGER
            return Token(symbol, int(number))
        if symbol == None:
            raise Exception("Can't parse symbol {symbol}".format(symbol=self._current_char))



# interpreter: sends string and judges order of token into actual actions
class Interpreter(object):
    def __init__(self, text):
        self._lexer = Lexer(text)
        self._current_token = self._lexer.get_next_token()

    def _eat(self, symbol):
        """consume the lexer tape with an expected symbol. tape doesn't advance if symbol is unexpected"""
        if self._current_token.type == symbol:
            token = self._lexer.get_next_token()
            self._current_token = token
        else:
            raise Exception("Unexpected symbol {symbol}".format(symbol=symbol))

    def _term(self):
        """return current token as a terminal (INTEGER) and consume the tape"""
        token = self._current_token
        self._eat(INTEGER)
        return token.value

    def expr(self):
        """the FSM that expects a sequence of terms"""

        result = self._term()
        while self._current_token.type in [PLUS, MINUS]:
            if self._current_token.type == PLUS:
                self._eat(PLUS)
                result = result + self._term()
            if self._current_token.type == MINUS:
                self._eat(MINUS)
                result = result - self._term()
        return result



# main: interactive prompt

if __name__ == "__main__":
    while True:
        text = ''
        try:
            text = str(input("calc> "))
            i = Interpreter(text)
            result = i.expr()
            print(result)
        except Exception as e:
            pass
        if len(text) == 0:
            break
