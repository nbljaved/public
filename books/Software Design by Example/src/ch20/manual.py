def make_possibilities(manifest):
    available = []
    for package, versions in manifest.items():
        available.append([(package, v) for v in versions])

    accum = []
    _make_possible(available, [], accum)
    return accum

def _make_possible(remaining, current, accum):
    if not remaining:
        accum.append(current)
        return

    head, tail = remaining[0], remaining[1:]
    for h in head:
        _make_possible(tail, current + [h], accum)
