# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from .. import tokens
from . import expressions as zexpr
from .. import errors

class AlgebraicParser: # tremend descenso recursivo
    def __init__(self, tokens, debug=False):
        self.tokens = tokens
        self.debug = debug
        self.current = 0
    def parse(self):
        return self.parse_logic()
    def is_at_end(self):
        return self.current >= len(self.tokens)
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.tokens[self.current-1]
    def peek(self):
        if self.current+1 < len(self.tokens):
            return self.tokens[self.current+1]
        return None
    def eat(self, tipo):
        if not self.is_at_end() and self.tokens[self.current].type == tipo:
            self.advance()
            return True
        return False
    def prev(self):
        return self.tokens[self.current-1]
    def eat_more(self, *types):
        if not self.is_at_end() and self.tokens[self.current].type in types:
            self.advance()
            return True
        return False
    def parse_logic(self):
        fnode = self.parse_comp()
        while self.eat_more(tokens.TokenType.AND, tokens.TokenType.OR, tokens.TokenType.XOR):
            if self.peek().type==tokens.TokenType.SEMICOLON:
                return fnode
            op = self.prev().lexem
            snode = self.parse_comp()
            fnode = zexpr.Binary(fnode, op, snode)
        return fnode
    def parse_comp(self):
        fnode = self.parse_expr()
        while self.eat_more(tokens.TokenType.EQUAL_EQUAL, tokens.TokenType.BANG_EQUAL, tokens.TokenType.LESS, tokens.TokenType.GREATER, tokens.TokenType.LESS_EQUAL, tokens.TokenType.GREATER_EQUAL):
            if self.peek().type==tokens.TokenType.SEMICOLON:
                return fnode
            op = self.prev().lexem
            snode = self.parse_expr()
            fnode = zexpr.Binary(fnode, op, snode)
        return fnode
    def parse_expr(self):
        fnode = self.parse_term()
        while self.eat_more(tokens.TokenType.PLUS, tokens.TokenType.MINUS):
            if self.peek().type==tokens.TokenType.SEMICOLON:
                return fnode
            op = self.prev().lexem
            snode = self.parse_term()
            fnode = zexpr.Binary(fnode, op, snode)
        return fnode
    def parse_term(self):
        fnode = self.parse_factor()
        while self.eat_more(tokens.TokenType.STAR, tokens.TokenType.SLASH):
            if self.peek().type==tokens.TokenType.SEMICOLON:
                return fnode
            op=self.prev().lexem
            snode = self.parse_factor()
            fnode = zexpr.Binary(fnode, op, snode)
        return fnode

    def parse_factor(self):
        if self.eat_more(tokens.TokenType.MINUS, tokens.TokenType.BANG):
            op = self.prev().lexem
            return zexpr.Unary(op, self.parse_factor())
        elif self.eat(tokens.TokenType.LPAREN): # ya me olvidaba de esto
            expr = self.parse_logic()
            if not self.eat(tokens.TokenType.RPAREN):
                raise SyntaxError("Expected closing parenthesis")
            return expr
        elif self.eat_more(tokens.TokenType.STRING, tokens.TokenType.FLOAT, tokens.TokenType.BOOL, tokens.TokenType.NULL):
            return zexpr.Literal(self.prev().value)
        elif self.eat(tokens.TokenType.IDENTIFIER):
            if self.eat(tokens.TokenType.DOT):
                if self.eat(tokens.TokenType.IDENTIFIER):
                    return zexpr.MIdentifier(self.tokens[self.current-3].lexem, self.prev().lexem)
                else:
                    raise SyntaxError("Expected identifier after a dot")
            return zexpr.Identifier(self.prev().lexem)
        else:
            raise SyntaxError("Unexpected Token")


# monte eso a escondidas a 4 am
# código clandestino


class ZynkLParser:
    def __init__(self, tokens, debug=False):
        self.debug = debug
        self.tokens = tokens
        self.current = 0
    def is_at_end(self):
        return self.current >= len(self.tokens)
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.tokens[self.current-1]
    def peek(self):
        if self.current+1 <= len(self.tokens):
            return self.tokens[self.current+1]
        return None
    def eat(self, tipe):
        if self.actual().type == tipe:
            self.advance()
            return True
        return False
    def prev(self):
        return self.tokens[self.current-1]
    def eat_more(self, *types):
        if self.actual().type in types:
            self.advance()
            return True
        return False
    def actual(self):
        if self.is_at_end():
            return None
        return self.tokens[self.current]
    def parse_import(self):
        if self.eat_more(tokens.TokenType.IDENTIFIER, tokens.TokenType.STRING):
            first = self.algebraic([self.prev()])
            if self.eat(tokens.TokenType.AS):
                if self.eat_more(tokens.TokenType.IDENTIFIER, tokens.TokenType.STRING):
                    return zexpr.ImportExpr(first, self.algebraic([self.prev()]))
                else:
                    raise SyntaxError("Expected Identifier/String after as")
            else:
                return zexpr.ImportExpr(first, first) 
        else:
            raise SyntaxError("Expected Identifier/String After Import")
    def parse_identifier(self):
        first = self.prev()
        if self.eat(tokens.TokenType.DOT):
            if self.eat(tokens.TokenType.IDENTIFIER):
                return zexpr.MIdentifier(first.lexem, self.prev().lexem)
            else:
                raise SyntaxError("Expected Identifier After dot")
        else:
            return zexpr.Identifier(self.prev().lexem)
    def algebraic(self, toks):
        psd = AlgebraicParser(toks, self.debug)
        return psd.parse()
    def parse(self):
        statements = []
        while not self.is_at_end():
            stmt = self.parse_stmt()
            if stmt is not None:
                statements.append(stmt)
        return statements
    def parse_stmt(self):
        tok = self.actual()
        self.advance()
        if tok is None:
            return None
        elif tok.type == tokens.TokenType.IMPORT:
            return self.parse_import()
        elif tok.type == tokens.TokenType.IDENTIFIER:
            first = self.parse_identifier()
            if self.eat(tokens.TokenType.EQUAL):
                expression = self.parse_expression()
                return zexpr.VarAssign(first.name, expression)
            else:
                raise SyntaxError("Unexpected Token after Identifier")
        elif tok.type == tokens.TokenType.IF:
           return self.parse_if()
        elif tok.type == tokens.TokenType.CALL:
            return self.parse_call()

        elif tok.type == tokens.TokenType.WHILE:
            return self.parse_while()

        elif tok.type == tokens.TokenType.FOR:
            return self.parse_for()

        elif tok.type == tokens.TokenType.FUNC:
            return self.parse_func()
        elif tok.type == tokens.TokenType.VAR:
            if self.eat(tokens.TokenType.IDENTIFIER):
                name = self.prev().lexem
                if self.eat(tokens.TokenType.EQUAL):
                    value = self.parse_expression()
                    return zexpr.VarDef(name, value)
                else:
                    return zexpr.VarDef(name, zexpr.Literal(None))
            else:
                raise SyntaxError("Expected identifier after 'var'")
        elif tok.type == tokens.TokenType.LBRACE:
            self.advance()
            return self.parse_block()
        elif tok.type == tokens.TokenType.SEMICOLON:
            self.advance()
            return None
        elif tok.type == tokens.TokenType.PRINT:
            expression = self.parse_expression()
            return zexpr.PrintStmt(expression)
        elif tok.type == tokens.TokenType.INPUT:
            expr = self.algebraic(self.until_to())
            if self.prev().type == tokens.TokenType.TO:
                to = self.actual().lexem
                if not self.peek().type == tokens.TokenType.SEMICOLON:
                    raise SyntaxError("Expected Semicolon")
                return zexpr.InputStmt(expr, to)
            return zexpr.InputStmt(expr, None)
        elif tok.type == tokens.TokenType.EOF:
            return None
    def parse_call(self):
        if not self.eat(tokens.TokenType.IDENTIFIER):
            raise SyntaxError("Expected Identifier")
        idtf = self.parse_identifier()
        if not self.eat(tokens.TokenType.LPAREN):
            raise SyntaxError("Expected Paren")
        args = self.get_args()
        args = [self.algebraic(arg) for arg in args]
        if self.eat(tokens.TokenType.TO):
            to = self.actual().lexem
        else:
            to = None
        if not self.eat(tokens.TokenType.SEMICOLON):
            raise SyntaxError("Expected Semicolon")
        return zexpr.CallFunc(idtf, args, to)
    def until_to(self):
        until = []
        while not self.is_at_end():
            if self.eat_more(tokens.TokenType.TO, tokens.TokenType.SEMICOLON):
                break
            if self.eat(tokens.TokenType.EOF):
                raise SyntaxError("Unexpected EOF")
            until.append(self.actual())
            self.advance()
        return until
    def parse_expression(self):
        expr = []
        while not self.is_at_end():
            if self.eat(tokens.TokenType.SEMICOLON):
                break
            elif self.eat(tokens.TokenType.EOF):
                raise SyntaxError("Unexpected EOF")
            else:
                expr.append(self.actual())
                self.advance()
        return self.algebraic(expr)
    def parse_block(self):
        block = []
        while not self.is_at_end():
            if self.eat(tokens.TokenType.RBRACE):
                break
            elif self.eat(tokens.TokenType.EOF):
                raise SyntaxError("Unexpected EOF")
            else:
                block.append(self.actual())
                self.advance()
        subparse = ZynkLParser(block, self.debug)
        return subparse.parse()
    def parse_if(self):
        if not self.eat(tokens.TokenType.LPAREN):
            raise SyntaxError("Expected Paren after if")
        condition = self.parsinp()
        if not self.eat(tokens.TokenType.LBRACE):
            raise SyntaxError("Expected Brace after condition")
        then = self.parse_block()
        if self.eat(tokens.TokenType.ELSE):
            if not self.eat(tokens.TokenType.LBRACE):
                raise SyntaxError("Expected Brace after else")
            else_branch = self.parse_block()
        else:
            else_branch = None
        return zexpr.IfExpr(condition, then, else_branch)
    def parse_while(self):
        if not self.eat(tokens.TokenType.LPAREN):
            raise SyntaxError("Expected Paren after while")
        condition = self.parsinp()
        if not self.eat(tokens.TokenType.LBRACE):
            raise SyntaxError("Expected Brace after condition")
        body = self.parse_block()
        return zexpr.WhileExpr(condition, body)
    def parse_for(self):
        if not self.eat(tokens.TokenType.LPAREN):
            raise SyntaxError("Expected Paren after for")
        args = self.get_args()
        name = args[0][0].lexem
        if args[0][1].lexem != "=":
            raise SyntaxError("Expected Equal")
        args[0] = zexpr.VarDef(name, self.algebraic(args[0][2:]))
        args[1] = self.algebraic(args[1])
        args[2] = zexpr.VarAssign(name, self.algebraic(args[2]))
        if not self.eat(tokens.TokenType.LBRACE):
            raise SyntaxError("Expected Brace after condition")
        body = self.parse_block()
        return zexpr.ForExpr(args[0], args[2], args[1], body)
    def parse_func(self):
        funcname = self.actual().lexem
        self.advance()
        if not self.eat(tokens.TokenType.LPAREN):
            raise SyntaxError("Expected Paren after Function Name")
        args = self.get_args()
        if not self.eat(tokens.TokenType.LBRACE):
            raise SyntaxError("Expected Brace after Params")
        body = self.parse_block()
        return zexpr.FuncDef(funcname, args, body)
    def parsinp(self):
        expr = []
        while not self.is_at_end():
            if self.eat(tokens.TokenType.RPAREN):
                break
            elif self.eat(tokens.TokenType.EOF):
                raise SyntaxError("Unexpected EOF")
            else:
                expr.append(self.actual())
                self.advance()
        return self.algebraic(expr)
    def get_args(self):
        args = []
        arg = []
        while not self.is_at_end():
            if self.eat(tokens.TokenType.RPAREN):
                args.append(arg)
                break
            elif self.eat(tokens.TokenType.COMMA):
                args.append(arg)
                arg = []
            arg.append(self.actual())
            self.advance()
        return args
