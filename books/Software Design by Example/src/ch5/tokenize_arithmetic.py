from pprint import pprint

def tokenize(text: str):
    result = []
    current = ''

    def looking_for_number() -> bool:
        """
        Return true if 'result's last token is an operation
        """
        if not result:
            return False
        last_token = result[-1]
        # check if it is a number
        if last_token[0] == 'Number':
            return

    def add(token):
        nonlocal current
        if len(current) > 0:
            result.append(['Number', current])
            current = ''
        if token:
            result.append(token)

    for i, char in enumerate(text):
        if char == '(':
            add(['('])
        elif char == ')':
            add([')'])
        elif char == '+':
            add(['+'])
        elif char == '*':
            add(['*'])
        elif char == '/':
            add(['/'])
        elif char.isspace():
            continue
        # number can be '0-9',
        elif char.isdigit():
            current += char
        elif char == '.':
            if '.' not in current:
                current += char
            else:
                raise Exception(f'you promised valid string')
        elif char == '-':
            # now either this is the minus operation
            # or negative on a number
            #
            # If 'current' is empty => negative
            # If 'current' is not empty => minus operation
            if current:
                add(['-'])
            else:
                current += '-'
        else:
            raise Exception(f'provided text: {text} is supposed to be valid')

    add(None)
    return result
