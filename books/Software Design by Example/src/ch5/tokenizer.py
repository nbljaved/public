class Tokenizer():
    def __init__(self):
        self._setup()

    def _setup(self):
        # NOTE: We are defining the class attributes in a function
        #       other than __init__ !
        self.result = []
        self.current = ""

    def _add(self, thing):
        """
        Adds the current thing to the list of tokens.
        Examples of 'thing': ['Any'], ['EitherStart'], ['EitherEnd']

        As a special case, self._add(None) means “add the literal but nothing
        else”
        """
        if len(self.current) > 0:
            self.result.append(['Lit', self.current])
            self.current = ''
        if thing is not None:
            self.result.append(thing)

    def tok(self, text: str):
        """
        Main method of our tokenizer
        """
        # This method calls self._setup() at the start so that the tokenizer can
        # be re-used
        self._setup()

        for c in text:
            if c == '*':
                self._add(['Any'])
            elif c == '{':
                self._add(['EitherStart'])
            elif c == '}':
                self._add(['EitherEnd'])
            elif c == ',':
                self._add(None)
            elif c.isascii():
                self.current += c
            else:
                raise NotImplementedError(f'what is {c} ?')
        # NOTE: We do this to add the final 'current' to the 'result'.
        return self.result
