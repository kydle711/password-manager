def _is_int(int_input):
    try:
        int(int_input)
        return True
    except ValueError:
        return False
