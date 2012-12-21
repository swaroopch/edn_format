
import ply.yacc
from edn_lex import tokens

if tokens: pass # Dummy statement to indicate that 'tokens' is used.

start = 'expression'


def p_term_string(p):
    """term : STRING"""
    p[0] = p[1]


def p_term_number(p):
    """term : NUMBER"""
    p[0] = p[1]


def p_term_boolean(p):
    """term : BOOLEAN"""
    p[0] = p[1]


def p_term_nil(p):
    """term : NIL"""
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


def p_expression_vector(p):
    """expression : vector"""
    p[0] = p[1]


def p_expression_set(p):
    """expression : set"""
    p[0] = p[1]


def p_expression_term(p):
    """expression : term"""
    p[0] = p[1]


def p_error(p):
    print "Syntax error! : {}".format(p)


def parse(text):
    kwargs = {}
    if __debug__:
        kwargs = dict(debug=True)
    p = ply.yacc.yacc(**kwargs)
    return p.parse(text)