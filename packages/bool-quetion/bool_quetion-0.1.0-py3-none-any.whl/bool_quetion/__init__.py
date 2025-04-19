def true_false(question, valid_keys):
    err_flag = False
    if not isinstance(valid_keys, (list, tuple)):
        print ('The second argument must be a tuple or list.')
        print ('El segundo argumento tiene que una tuple o list.')
        err_flag = True
    if isinstance(valid_keys, (list, tuple)) and len(valid_keys) != 2:
        print ('The 2nd argument must be a tuple or list with two elements.')
        print ('El 2° argumento debe ser una tuple o list de 2 elementos.')
        err_flag = True
    if any(not isinstance(k, str) for k in valid_keys):
        print ('Both elements of the second argument must be strings.')
        print ('Los dos elementos del 2° argumento tienen que ser str.')
        err_flag = True
    if not isinstance(question, str):
        print ('The first argument must be a string.')
        print ('El primer argumento tiene que ser str.')
        err_flag = True
    if err_flag:
        raise ValueError('Error')
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

if __name__ == '__main__':
    yes_or_no = true_false('Do you want to continue?', ['Yes', 'No'])
    print (yes_or_no)
