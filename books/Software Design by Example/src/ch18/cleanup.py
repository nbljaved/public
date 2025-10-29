def _cleanup(self):
    new_seq = {
        o: i for i, o in enumerate(self._index.values())
    }
    keep = {self._get_block_id(o) for o in new_seq}

    renaming = {o: i for i, o in enumerate(list(sorted(keep)))}
    garbage_ids = {
        i for i in range(len(self._blocks))
        if i not in renaming
    }

    self._delete_blocks(garbage_ids)
    self._rename_blocks(renaming)

    new_index = {
        k: new_seq[self._index[k]] for k in self._index
    }
    self._index = new_index
    self._next = len(self._index)
