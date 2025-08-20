from .tokenizer import *
from ..ch4.matcher import *

class Parser():
    def __init__(self):
        pass

    def parse(self, text: str):
        tokens = Tokenizer().tok(text)
        return self._parse(tokens)

    def _parse(self, tokens):
        if not tokens:
            return Null()

        car = tokens[0]
        cdr = tokens[1:]
        pattern = car[0]
        if pattern == 'Any':
            handler = self._parse_Any
        elif pattern == 'Lit':
            handler = self._parse_Lit
        elif pattern == 'EitherStart':
            handler = self._parse_EitherStart
        else:
            assert False, f'Unknown token type {pattern}'

        return handler(car[1:], cdr)

    def _parse_Any(self, arg, rest_tokens):
        return Any(rest=self._parse(rest_tokens))

    def _parse_Lit(self, arg, rest_tokens):
        text = arg[0]
        return Lit(chars=text, rest=self._parse(rest_tokens))

    def _parse_EitherStart(self, arg, rest_tokens):
        args = [] # with store the options of Either

        for i in range(len(rest_tokens)):
            token = rest_tokens[i]
            if token[0] == 'EitherEnd':
                either_end_index = i
                break
            else:
                pattern = self._parse([token])
                args.append(pattern)

        return Either(*args, rest=self._parse(rest_tokens[either_end_index+1:]))
