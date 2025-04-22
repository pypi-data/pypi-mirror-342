try:
    from sys import stdin
    from tty import setraw
    import termios
    from localized_errors import get_error
    _has_termios = True
except ImportError:
    raise IndentationError('This function is available only on '
    'Unix-based systems.')

def display_errors(_question, _options, _mark=False):
    if not isinstance(_options, (list, tuple)):
        raise AttributeError(get_error("invalid_type_options"))
    if isinstance(_options, (list, tuple)) and len(_options) != 2:
        raise IndexError(get_error('wrong_len_options'))
    if any(not isinstance(k, str) for k in _options):
        raise ValueError(get_error('options_not_str'))
    first_chars = (_options[0][0] + _options[1][0]).lower()
    if first_chars[0] == first_chars[1] or not first_chars.isalnum():
        raise ValueError(get_error('options_same_char'))
    del (first_chars)
    if not isinstance(_question, str):
        raise AttributeError(get_error('invalid_type_question'))
    if not isinstance(_mark, bool):
        raise AttributeError(get_error('invalid_type_mark'))

def true_false(question, options, mark=False):
    display_errors(question, options, mark)
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
if __name__ == '__main__':
    print (true_false('Do you wish to continue?', ['Yes', 'no'], True))
