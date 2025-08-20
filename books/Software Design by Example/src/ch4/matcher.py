Pattern = type('Pattern')
class Pattern:
    def __init__(self, rest: Pattern | None = None):
        """
        Subclasses of Pattern can take two arguments:
        1. set of characters, a str etc.
        2. rest (the next Pattern)
        """
        # NOTE: How we can pass the argument has None and it is handled by the
        # Null Object pattern
        self.rest : Pattern = rest if rest is not None else Null()

    def match(self, text: str) -> bool:
        """
        Returns boolean indicating if Pattern matches `text`.
        """
        length_of_matched_text = self._match(text, start=0)
        return len(text) == length_of_matched_text

    def __eq__(self, other):
        return (other is not None
                and self.__class__ == other.__class__
                and self.rest == other.rest)

class Null(Pattern):
    """
    Null Object Pattern
    Null() is the placeholder object instead of 'None'
    """
    def __init__(self):
        """
        Null objects must be at the end of the matching chain, i.e., their 'rest'
        must be None, so we remove the 'rest' parameter from the class’s
        constructor and pass 'None' up to the parent constructor every time.
        """
        self.rest = None # base case

    def _match(self, text, start):
        """
        Since Null objects don’t match anything, Null._match immediately returns
        whatever starting point it was given.

        Every other matcher can now pass responsibility down the chain without
        having to test whether it’s the last matcher in line or not.
        """
        return start

class Lit(Pattern):
    def __init__(self, chars: str, rest=None):
        super().__init__(rest)
        self.chars = chars

    def _match(self, text: str, start=0):
        end = len(self.chars) + start
        if text[start:end] != self.chars:
            # failed
            #
            # this is the position to next search,
            # (therefore None means failed)
            return None
        # passed
        return self.rest._match(text, start=end)

    def __eq__(self, other):
        return super().__eq__(other) and (self.chars == other.chars)
    
class Any(Pattern):
    def __init__(self, rest=None):
        super().__init__(rest)

    def _match(self, text: str, start=0):
        """
        Here '*' can match 0 or more of the characters
        in text[start:].
        Here, we implement lazy matching, '*' will match
        the shortes string so that the 'rest' of Pattern can
        successfully match 'text'.
        """
        n = len(text)
        # length matched = from 0 -> len(text[start:])
        #
        # NOTE1: i=n+1 => * matched the complete text[start:]
        #       and the 'rest' will have to match the empty string.
        for i in range(start, n+1):
            # i the index where 'rest' will start matching from,
            # i.e. 'rest' tries to match text[i:]
            #
            # if self.rest.match(text[i:]):
            #     return n
            # OR
            j = self.rest._match(text, start=i)
            if j == n: # NOTE2: why we test for this (hint we don't rely on 'rest')
                # success
                return n # NOTE3

        # fail
        return None
class Either(Pattern):
    def __init__(self, *patterns, rest=None):
        super().__init__(rest)
        self.patterns = patterns

    def _match(self, text, start=0):
        # NOTE: what if patterns are empty ?
        if not self.patterns:
            return self.rest._match(text, start)

        # Try each pattern
        for pattern in self.patterns:
            j = pattern._match(text, start)
            if j is None:
                continue
            if len(text) == self.rest._match(text, start=j):
                # pass
                return len(text)
        # fail
        return None
