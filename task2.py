from trie import Trie


class ReverseTrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0


class Homework(Trie):
    def __init__(self):
        super().__init__()

        # Додаткове префіксне дерево для перевернутих слів.
        # Воно потрібне, щоб швидко шукати слова за суфіксом.
        self.reversed_root = ReverseTrieNode()

        # Зберігаємо слова, щоб не рахувати дублікати повторно
        self.words = set()

    def put(self, key, value=None):
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

        # Спочатку додаємо слово у звичайний Trie
        super().put(key, value)

        # Якщо слово вже було, не додаємо його повторно у підрахунок
        if key in self.words:
            return

        self.words.add(key)

        # Додаємо слово у reverse trie у перевернутому вигляді
        node = self.reversed_root
        node.count += 1

        for char in reversed(key):
            if char not in node.children:
                node.children[char] = ReverseTrieNode()

            node = node.children[char]
            node.count += 1

    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            raise TypeError("Pattern must be a string")

        # Порожній суфікс формально підходить для всіх слів
        if pattern == "":
            return len(self.words)

        node = self.reversed_root

        for char in reversed(pattern):
            if char not in node.children:
                return 0

            node = node.children[char]

        return node.count

    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise TypeError("Prefix must be a string")

        # Порожній префікс існує, якщо у дереві є хоча б одне слово
        if prefix == "":
            return len(self.words) > 0

        node = self.root

        for char in prefix:
            if char not in node.children:
                return False

            node = node.children[char]

        return True


if __name__ == "__main__":
    trie = Homework()

    words = ["apple", "application", "banana", "cat"]

    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert trie.count_words_with_suffix("e") == 1      # apple
    assert trie.count_words_with_suffix("ion") == 1    # application
    assert trie.count_words_with_suffix("a") == 1      # banana
    assert trie.count_words_with_suffix("at") == 1     # cat
    assert trie.count_words_with_suffix("x") == 0

    # Перевірка наявності префікса
    assert trie.has_prefix("app") == True              # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True              # banana
    assert trie.has_prefix("ca") == True               # cat

    print("Усі тести пройдено успішно!")