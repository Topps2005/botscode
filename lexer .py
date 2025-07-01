# src/tswana/lexer.py

from .tokens import Token, TokenType

KEYWORDS = {
    "lefa": TokenType.LEFA,
    "bala": TokenType.BALA,
    "fa": TokenType.FA,
    "jalo": TokenType.JALO,
    "fa_jalo": TokenType.FA_JALO,
    "a_teng": TokenType.A_TENG,
    "ema": TokenType.EMA,
    "tswele": TokenType.TSWELE,
    "letla": TokenType.LETLA,
    "boela": TokenType.BOELA
}

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.char = None
        self.line = 1
        self.column = 0
        self.advance()

    def advance(self):
        self.pos += 1
        self.column += 1
        if self.pos < len(self.text):
            self.char = self.text[self.pos]
        else:
            self.char = None

    def generate_tokens(self):
        while self.char is not None:
            if self.char.isspace():
                if self.char == '\n':
                    self.line += 1
                    self.column = 0
                self.advance()
            elif self.char.isdigit():
                yield self.generate_number()
            elif self.char.isalpha() or self.char == '_':
                yield self.generate_identifier()
            elif self.char == '+':
                yield Token(TokenType.PLUS, '+', self.line, self.column)
                self.advance()
            elif self.char == '-':
                yield Token(TokenType.MINUS, '-', self.line, self.column)
                self.advance()
            elif self.char == '*':
                yield Token(TokenType.STAR, '*', self.line, self.column)
                self.advance()
            elif self.char == '/':
                yield Token(TokenType.SLASH, '/', self.line, self.column)
                self.advance()
            elif self.char == '=':
                self.advance()
                if self.char == '=':
                    self.advance()
                    yield Token(TokenType.EQEQ, '==', self.line, self.column)
                else:
                    yield Token(TokenType.EQ, '=', self.line, self.column)
            else:
                raise Exception(f"Illegal character: {self.char}")

        yield Token(TokenType.EOF, None, self.line, self.column)

    def generate_number(self):
        number = ''
        while self.char is not None and self.char.isdigit():
            number += self.char
            self.advance()
        return Token(TokenType.NUMBER, int(number), self.line, self.column)

    def generate_identifier(self):
        id_str = ''
        while self.char is not None and (self.char.isalnum() or self.char == '_'):
            id_str += self.char
            self.advance()
        tok_type = KEYWORDS.get(id_str, TokenType.IDENTIFIER)
        return Token(tok_type, id_str, self.line, self.column)
