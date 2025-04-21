def true_false(question, options, mark=False):
    err_str = []
    if not isinstance(options, (list, tuple)):
        err_str.append('The second argument must be a '
        'tuple or list.')
        err_str.append('AttributeError: El segundo argumento tiene que '
        'una tuple o list.')
        raise AttributeError('\n'.join(err_str))
    if isinstance(options, (list, tuple)) and len(options) != 2:
        err_flag = 'Attribute' if len(options) == 2 else 'Index'
        err_str.append('The 2nd argument must be a tuple '
        'or list with two elements.')
        err_str.append(err_flag + 'Error: El 2° argumento debe ser '
        'una tuple o list de 2 elementos.')
        if len(options) != 2:
            raise IndexError('\n'.join(err_str))
        else:
            raise ValueError('\n'.join(options))
    if any(not isinstance(k, str) for k in options):
        err_str.append('Both elements of the second argument '
        'must be strings.')
        err_str.append('ValueError: Los dos elementos del 2° argumento '
        'tienen que ser str.')
        raise ValueError('\n'.join(err_str))
    first_chars = (options[0][0] + options[1][0]).lower()
    if first_chars[0] == first_chars[1] or not first_chars.isalnum():
        err_str.append('The first characters of the elements in the '
        'second argument must be different and alphanumeric.')
        err_str.append('ValueError: Los primeros caracteres de los elementos '
        'del segundo argumento deben ser diferente y alfanuméricos.')
        raise ValueError('\n'.join(err_str))
    del (first_chars)
    if not isinstance(question, str):
        err_str.append('The first argument must be a string.')
        err_str.append('AttributeError: El primer argumento tiene que '
        'ser str.')
        raise AttributeError('\n'.join(err_str))
    if not isinstance(mark, bool):
        err_str.append('This argument expects a boolean value '
        '(True or False).')
        err_str.append('AttributeError: Se esperaba un argumento buleano '
        '(True o False).')
        raise AttributeError('\n'.join(err_str))
    from sys import stdin
    from tty import setraw
    import termios
    title_key = lambda _k: f'\033[1m{_k[0]}\033[0m{_k[1:]}'
    words_question = (
            [f'{title_key(k)}' for k in options]
            if mark else options.copy()
            )
    print (f'{question} {" o ".join(words_question)}')
    fd = stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    first_letter = [k[0].lower() for k in options]

    try:
        setraw(fd)
        while True:
            char = stdin.read(1).lower()
            if char in first_letter:
                return char == first_letter[0]
                break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
if __name__ == 'main__':
    print ('Do you wish to continue?', ['Yes', 'no'], True)
