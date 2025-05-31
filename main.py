import pickle
from itertools import product

with open("zalizniak_lemmas_cleaned.pkl", "rb") as f:
    zalizniak_lemmas = pickle.load(f)


def is_real_russian_word(word: str) -> bool:
    return word in zalizniak_lemmas


class SpellingBeeGame:
    def __init__(self, center_letter, other_letters):
        self.center_letter = center_letter.lower()
        self.letters = set(letter.lower() for letter in other_letters + [center_letter])
        self.valid_words = self._generate_valid_words()
        self.found_words = set()

    def _generate_valid_words(self):
        valid = set()
        letters_list = list(self.letters)
        for r in range(4, 8):
            for tup in product(letters_list, repeat=r):
                word = ''.join(tup)
                if self.center_letter in word and is_real_russian_word(word):
                    valid.add(word)
        return valid

    def is_valid(self, word):
        word = word.lower()
        if self.center_letter not in word:
            return False, "В слове должна быть центральная буква."
        if word in self.found_words:
            return False, "Это слово уже было использовано."
        if word not in self.valid_words:
            return False, "Слово не подходит."
        return True, ""

    def submit_word(self, word):
        word = word.lower()
        valid, message = self.is_valid(word)
        if valid:
            self.found_words.add(word)
            return True, ""
        else:
            return False, message

    def get_found_words(self):
        return sorted(self.found_words)

    def get_score(self):
        score = 0
        for word in self.found_words:
            length = len(word)
            if length == 4:
                score += 1
            elif length == 5:
                score += 5
            elif length == 6:
                score += 6
            elif length == 7:
                score += 7
            elif length >= 8:
                score += length * 2
        return score

    def get_total_words(self):
        return len(self.valid_words)

    def get_remaining(self):
        return self.get_total_words() - len(self.found_words)
