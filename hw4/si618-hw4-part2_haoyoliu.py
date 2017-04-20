from mrjob.job import MRJob
from mrjob.step import MRStep
import re

WORD_RE = re.compile(r"[\w']+")

class MRMostUsedWord(MRJob):
    def mapper_get_words(self, _, line):
        words = WORD_RE.findall(line)
        for word in words:
            yield (word.lower(), 1)

    def combiner_count_words(self, word, counts):
        yield (word, sum(counts))

    def reducer_count_words(self, word, counts):
        yield None, (word, sum(counts))

    def reducer_find_max_word(self, _, word_count_pairs):
        yield sorted(word_count_pairs, key=lambda x: x[1], reverse=True)[0]

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper_get_words,
                combiner=self.combiner_count_words,
                reducer=self.reducer_count_words,
            ),
            MRStep(reducer=self.reducer_find_max_word)
        ]

if __name__ == '__main__':
    MRMostUsedWord.run()
