
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
        self._current_char = None
        self._current_position = -1

    def advance(self):
        """read another unit of the input in the current state"""
        # check pointer bounds
        if (self._current_position + 1) == len(self._text):
            return Token(EOF, None)

        # advance pointer
        self._current_position+=1

        self._current_char = self._text[self._current_position]

    def get_next_token(self):
        """interpret current state into a token"""

        # get current char
        self.advance()

        # infer a symbol
        symbol = None

        if self._current_char == '+':
            symbol = PLUS
            token = Token(symbol, self._current_char)
        if self._current_char == '-':
            symbol = MINUS
            token = Token(symbol, self._current_char)
        if self._current_char.isdigit():
            symbol = INTEGER
            token = Token(symbol, int(self._current_char))
        if symbol == None:
            raise Exception("Can't parse symbol {symbol}".format(symbol=self._current_char))

        # return a token
        return token


# interpreter: sends string and judges order of token into actual actions
class Interpreter(object):
    def __init__(self, text):
        self._lexer = Lexer(text)
        self._current_token = self._lexer.get_next_token()

    def eat(self, symbol):
        """consume the lexer tape with an expected symbol. tape doesn't advance if symbol is unexpected"""
        if self._current_token.type == symbol:
            token = self._lexer.get_next_token()
            self._current_token = token
        else:
            raise Exception("Unexpected symbol {symbol}".format(symbol=symbol))

    def term(self):
        """return current token as a terminal (INTEGER) and consume the tape"""
        token = self._current_token.value
        self.eat(INTEGER)
        return token

    def expr(self):
        """the FSM that expects a sequence of terms"""

        result = self.term()
        while self._current_token.type in [PLUS, MINUS]:
            if self._current_token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            if self._current_token.type == MINUS:
                self.eat(MINUS)
                right = self._current_token.value
                result -= self.term()
        print(result)



# main: interactive prompt

if __name__ == "__main__":
    while True:
        text = str(raw_input("calc> "))
        try:
            i = Interpreter(text)
            i.expr()
        except Exception as e:
            pass
        if len(text) == 0:
            break
