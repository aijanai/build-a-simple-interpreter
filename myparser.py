
EOF, INTEGER, PLUS, MINUS, MUL, DIV, LPAR, RPAR= 'EOF', 'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAR', 'RPAR'
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
        if self._current_position >= self._text_len :
            self._current_char = None
            self._current_position = self._text_len
        else:
            self._current_char = self._text[self._current_position]

    def __skip_whitespace(self):
        while self._current_char.isspace():
            self._advance()

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

        while True:
            current_char = self._current_char

            if current_char is None:
                return Token(EOF, current_char)

            if current_char.isspace():
                self.__skip_whitespace()
                continue

            if current_char == '/':
                symbol = DIV
                self._advance()
                return Token(symbol, current_char)

            if current_char == '*':
                symbol = MUL
                self._advance()
                return Token(symbol, current_char)

            if current_char == '+':
                symbol = PLUS
                self._advance()
                return Token(symbol, current_char)

            if current_char == '-':
                symbol = MINUS
                self._advance()
                return Token(symbol, current_char)

            if current_char == '(':
                symbol = LPAR
                self._advance()
                return Token(symbol, current_char)

            if current_char == ')':
                symbol = RPAR
                self._advance()
                return Token(symbol, current_char)

            if current_char.isdigit():
                number = self._parse_integer()
                symbol = INTEGER
                return Token(symbol, int(number))

            raise Exception("Can't parse symbol {symbol}".format(symbol=self._current_char))



# parser: sends string and judges order of token into actual actions
class Parser(object):
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
        if token.type == LPAR:
            self._eat(LPAR)
            result = self.expr()
            self._eat(RPAR)
            return result
        if token.type == INTEGER:
           self._eat(INTEGER)
           return NumOp(token)
        raise Exception(f"Unexpected term {token.type}")

    def _factor(self):
        """factor: term((MUL|DIV) term)*"""
        result = self._term()

        while self._current_token.type in [DIV, MUL]:
            if self._current_token.type == DIV:
                self._eat(DIV)
                result = BinOp(result, DIV, self._term())
                continue
            if self._current_token.type == MUL:
                self._eat(MUL)
                result = BinOp(result, MUL, self._term())
                continue
        return result

    def expr(self):
        """
        the FSM that expects a sequence of terms

        expr: factor ((PLUS|MINUS) factor)*
        factor: term((MUL|DIV) term)*
        term: (INTEGER|LPAR expr RPAR)
        """

        result = self._factor()
        while self._current_token.type in [PLUS, MINUS]:
            if self._current_token.type == PLUS:
                self._eat(PLUS)
                result = BinOp(result, PLUS, self._factor())
                continue
            if self._current_token.type == MINUS:
                self._eat(MINUS)
                result = BinOp(result, MINUS, self._factor())
                continue
        return result

# base node
class AST(object):
    pass

# operation node
class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

# value node
class NumOp(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

# provides basic visitor method
class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_'+type(node).__name__
        visitor = getattr(self, method, self.default_visitor)
        return visitor(node)

    def default_visitor(self, node):
        raise Exception(f"Unsupported {node}")

# provides implementations of Visitor pattern
class Interpreter(NodeVisitor):
    def __init__(self, text):
        self._parser = Parser(text)

    def visit_NumOp(self, node):
        return node.value

    def visit_BinOp(self, node):
        if node.op == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        if node.op == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        if node.op == MUL:
            return self.visit(node.left) * self.visit(node.right)
        if node.op == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def interpret(self):
        tree = self._parser.expr()
        return self.visit(tree)

class ReversePolishNotationPrinter(Interpreter):

    def visit_BinOp(self, node):
        result = ''
        if node.op == MINUS:
            result = f"{result} {self.visit(node.left)} {self.visit(node.right)} -"
        if node.op == PLUS:
            result = f"{result} {self.visit(node.left)} {self.visit(node.right)} +"
        if node.op == MUL:
            result = f"{result} {self.visit(node.left)} {self.visit(node.right)} *"
        if node.op == DIV:
            result = f"{result} {self.visit(node.left)} {self.visit(node.right)} /"
        return result.strip()

class LISPNotationPrinter(Interpreter):

    def visit_BinOp(self, node):
        result = ''
        if node.op == MINUS:
            result = f"({result} - {self.visit(node.left)} {self.visit(node.right)})"
        if node.op == PLUS:
            result = f"({result} + {self.visit(node.left)} {self.visit(node.right)})"
        if node.op == MUL:
            result = f"({result} * {self.visit(node.left)} {self.visit(node.right)})"
        if node.op == DIV:
            result = f"({result} / {self.visit(node.left)} {self.visit(node.right)})"
        return result.strip()

# main: interactive prompt
if __name__ == "__main__":
    while True:
        text = ''
        try:
            text = str(input("calc> "))
            i = Interpreter(text)
            result = i.interpret()
            print(result)
        except EOFError as e:
                break
        except Exception as e:
            if len(text) == 0:
                break
            print(e)
