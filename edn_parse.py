
import ply.yacc
from edn_lex import tokens, lex

if tokens: pass # Dummy statement to indicate that 'tokens' is used.

start = 'expression'


def p_term_leaf(p):
    """term : CHAR
            | STRING
            | NUMBER
            | BOOLEAN
            | NIL
            | KEYWORD"""
    p[0] = p[1]


def p_terms_terms_term(p):
    """terms : terms term"""
    p[0] = p[1] + [p[2]]


def p_terms_term(p):
    """terms : term"""
    p[0] = [p[1]]


def p_vector(p):
    """vector : VECTOR_START terms VECTOR_END"""
    p[0] = p[2]


def p_set(p):
    """set : SET_START terms MAP_OR_SET_END"""
    p[0] = set(p[2])


def p_expression(p):
    """expression : vector
                  | set
                  | term"""
    p[0] = p[1]


def p_error(p):
    print "Syntax error! : {}".format(p)


def parse(text):
    kwargs = {}
    if __debug__:
        kwargs = dict(debug=True)
    p = ply.yacc.yacc(**kwargs)

    return p.parse(text, lexer=lex())