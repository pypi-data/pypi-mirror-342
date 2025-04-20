def true_false(question, valid_keys):
    err_str = []
    if not isinstance(valid_keys, (list, tuple)):
        err_str.append('The second argument must be a '
        'tuple or list.')
        err_str.append('AttributeError: El segundo argumento tiene que '
        'una tuple o list.')
        raise AttributeError('\n'.join(err_str))
    if isinstance(valid_keys, (list, tuple)) and len(valid_keys) != 2:
        err_flag = 'Attribute' if len(valid_keys) == 2 else 'Index'
        err_str.append('The 2nd argument must be a tuple '
        'or list with two elements.')
        err_str.append(err_flag + 'Error: El 2° argumento debe ser '
        'una tuple o list de 2 elementos.')
        if len(valid_keys) != 2:
            raise IndexError('\n'.join(err_str))
        else:
            raise ValueError('\n'.join(valid_keys))
    if any(not isinstance(k, str) for k in valid_keys):
        err_str.append('Both elements of the second argument '
        'must be strings.')
        err_str.append('ValueError: Los dos elementos del 2° argumento '
        'tienen que ser str.')
        raise ValueError('\n'.join(err_str))
    first_chars = (valid_keys[0][0] + valid_keys[1][0]).lower()
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
    from sys import stdin
    from tty import setraw
    import termios
    title_key = lambda _k: f'\033[1m{_k[0]}\033[0m{_k[1:]}'
    words_question = [f'{title_key(k)}' for k in valid_keys]
    print (f'{question} {" o ".join(words_question)}')
    fd = stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    first_letter = [k[0].lower() for k in valid_keys]

    try:
        setraw(fd)
        while True:
            char = stdin.read(1).lower()
            if char in first_letter:
                return char == first_letter[0]
                break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
