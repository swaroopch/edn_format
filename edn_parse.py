
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
            | KEYWORD
            | WHITESPACE"""
    p[0] = p[1]


def p_vector(p):
    """vector : VECTOR_START expressions VECTOR_END"""
    p[0] = p[2]


def p_list(p):
    """list : LIST_START expressions LIST_END"""
    p[0] = tuple(p[2])


def p_set(p):
    """set : SET_START expressions MAP_OR_SET_END"""
    p[0] = set(p[2])


def p_map(p):
    """map : MAP_START expressions MAP_OR_SET_END"""
    terms = p[2]
    if len(terms) % 2 != 0:
        raise SyntaxError("Even number of terms required for map")
    p[0] = dict([terms[i:i+2] for i in range(0, len(terms), 2)]) # partition terms in pairs


def p_expression(p):
    """expression : vector
                  | list
                  | set
                  | map
                  | term"""
    p[0] = p[1]


def p_expressions_expressions_expression(p):
    """expressions : expressions expression"""
    p[0] = p[1] + [p[2]]


def p_expressions_expression(p):
    """expressions : expression"""
    p[0] = [p[1]]


def p_error(p):
    if p is None:
        print "Syntax Error! Reached EOF!"
    else:
        print "Syntax error! {}".format(p)


def parse(text):
    kwargs = {}
    if __debug__:
        kwargs = dict(debug=True)
    p = ply.yacc.yacc(**kwargs)

    return p.parse(text, lexer=lex())