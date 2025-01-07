from typing import Any, Iterable
from collections.abc import MutableMapping


def character_to_key(char: str) -> int:
    """
    Given a character return a number between [0, 26] inclusive.

    Letters a-z should be given their position in the alphabet 0-25, regardless
    of case:
        a/A -> 0
        z/Z -> 25

    Any other character should return 26.
    """
    try:
        position = ord(char.lower()) - 97
    except AttributeError:
        raise ValueError('The input should be a single character or symbol.')
    return position if 0 <= position <= 25 else 26


class NotSet:
    """
    Sentinel
    """


class Trie(MutableMapping):
    """
    Implementation of a trie class where each node in the tree can
    have up to 27 children based on next letter of key.
    (Using rules described in character_to_key.)

    Must implement all required MutableMapping methods,
    as well as wildcard_search.
    """

    def __init__(self):
        self.sub_trie = [NotSet] * 27
        self.value = NotSet
        self.length = 0
        self.char = ''
        self.prefix = ''

    def __getitem__(self, key: str) -> Any:
        """
        Given a key, return the value associated with it in the trie.

        If the key has not been added to this trie, raise `KeyError(key)`.
        If the key is not a string, raise `ValueError(key)`
        """
        # check if key valid
        if not isinstance(key, str):
            raise KeyError(key)

        # base step: value found/not found
        if len(key) == 0:
            if self.value is NotSet:
                raise KeyError(key)
            return self.value

        # recursive step:
        idx_subtrie = character_to_key(key[0])
        remaining_str = key[1:]
        if self.sub_trie[idx_subtrie] is NotSet:
            # raise eror if key not found
            raise KeyError(key)
        return self.sub_trie[idx_subtrie][remaining_str]

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Given a key and value, store the value associated with key.

        Like a dictionary, will overwrite existing data if key already exists.

        If the key is not a string, raise `ValueError(key)`
        """
        # check if key valid
        if not isinstance(key, str):
            raise KeyError(key)

        # base step: insert/overwrite the value
        if len(key) == 0:
            # set new value
            self.value = value
            # update trie length
            self.length = len(self)
            return

        # recersive step:
        idx_subtrie = character_to_key(key[0])
        char = key[0].lower() if idx_subtrie < 26 else "_"
        remaining_str = key[1:]
        if self.sub_trie[idx_subtrie] is NotSet:
            # create a new branch if needed
            self.sub_trie[idx_subtrie] = Trie()
            self.sub_trie[idx_subtrie].char = char
        self.sub_trie[idx_subtrie][remaining_str] = value
        # update trie length
        self.length = len(self)
        return

    def __delitem__(self, key: str) -> None:
        """
        Remove data associated with `key` from the trie.

        If the key is not a string, raise `ValueError(key)`
        """
        # check if key valid
        if not isinstance(key, str):
            raise ValueError(key)

        # base step: value found/not found
        if len(key) == 0:
            # del value
            self.value = NotSet
            # update trie length
            self.length = len(self)
            return

        # recursive step:
        idx_subtrie = character_to_key(key[0])
        remaining_str = key[1:]
        if self.sub_trie[idx_subtrie] is NotSet:
            # key is already not in trie
            raise KeyError(key)
        del self.sub_trie[idx_subtrie][remaining_str]
        # update trie length
        self.length = len(self)
        return

    def __len__(self) -> int:
        """
        Return the total number of entries currently in the trie.
        """
        sub_trie_length = sum(sub_trie.length for sub_trie in self.sub_trie
                              if sub_trie is not NotSet)
        self_lenght = 1 if self.value is not NotSet else 0
        return sub_trie_length + self_lenght

    def __iter__(self) -> Iterable[tuple[str, Any]]:
        """
        Return an iterable of (key, value) pairs for every entry in the trie in
        alphabetical order.
        """
        return self.generator()

    def generator(self, prefix='') -> Iterable[tuple[str, Any]]:
        '''
        A generator function that return a iterable of all the key-value pairs
        in the current sub-trie.
        '''
        prefix += self.char
        if self.char:
            if self.value is not NotSet:
                yield (prefix, self.value)
        for sub_trie in self.sub_trie:
            if sub_trie is not NotSet:
                yield from sub_trie.generator(prefix)

    def wildcard_search(self, key: str,
                        pointer=0, prefix='') -> Iterable[tuple[str, Any]]:
        """
        Search for keys that match a wildcard pattern where a '*' can represent
        any character.

        For example:
            - c*t would match 'cat', 'cut', 'cot', etc.
            - ** would match any two-letter string.

        Returns: Iterable of (key, value) pairs meeting the given condition.
        """
        # check if key valid
        if not isinstance(key, str):
            raise ValueError(key)
        prefix += self.char
        # base step: value found
        if len(key) == pointer:
            if self.value is not NotSet:
                yield (prefix, self.value)
            return
        # recursive step:
        if key[pointer] == "*":
            for sub_trie in self.sub_trie:
                if sub_trie is not NotSet:
                    yield from sub_trie.wildcard_search(key, pointer+1, prefix)
        else:
            idx = character_to_key(key[pointer])
            if self.sub_trie[idx] is not NotSet:
                yield from self.sub_trie[idx].wildcard_search(key, pointer+1,
                                                              prefix)

    def __repr__(self):
        return f"Keys starting with '{self.char}', number: {self.length} "
