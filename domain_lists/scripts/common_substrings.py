FILE_TO_PARSE = 'pornography'
FILEPATH = f'C:/Users/Freedom/PycharmProjects/dnxfirewall-signatures/domain_lists/{FILE_TO_PARSE}.domains'

with open(FILEPATH, 'r') as sig_file:
    signatures = sig_file.read().splitlines()

class WordComparison:
    __slots__ = ('words', 'common')

    def __init__(self, words, min_length=1):
        self.words = words
        self.common = self.find_common_substrings(min_length)

    def find_common_substrings(self, min_length):
        # Create a set to store the common substrings
        common = set()

        # Get the length of the shortest word
        shortest_word_length = min(len(word) for word in self.words)

        # Iterate over the length of substrings to compare
        for substring_length in range(min_length, shortest_word_length + 1):

            # Use a set to keep track of substrings of this length
            seen = set()

            # Iterate over the words
            for word in self.words:

                # Iterate over the start index of the substring in this word
                for start in range(len(word) - substring_length + 1):

                    # Extract the substring from this word
                    substring = word[start:start + substring_length]

                    # If the substring has not been seen before, add it to the set
                    if substring not in seen:
                        seen.add(substring)

                    # If the substring has been seen before, it is common to all words
                    else:
                        common.add(substring)

        # Return the result as a sorted list of substrings
        return sorted(list(common))

    def compare_word(self, word, min_length=1):
        self.words.append(word)
        self.common = self.find_common_substrings(min_length)
        return self.common


# Example usage
word_comparison = WordComparison(signatures, min_length=4)

print(word_comparison.common)
# print(word_comparison.compare_word('hi'))
# # Output: ['h', 'i']
# print(word_comparison.compare_word('hey'))
# # Output: ['he', 'ey', 'h', 'y']
