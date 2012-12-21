
tokens = ('STRING',
          'NIL',
          'BOOLEAN',
          'NUMBER')


t_STRING = r'"[^"]*"'
t_NIL = r'nil'
t_ignore = " \t"


def t_BOOLEAN(t):
    r"""(true)|(false)"""
    if t.value == "false":
        t.value = False
    elif t.value == "true":
        t.value = True
    return t


def t_NUMBER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)