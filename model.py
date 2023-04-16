import numpy as np
from gensim.models import Word2Vec


class Analyzer:
    def __init__(self):
        # Word2Vec 모델 로딩
        self.model = None
        self.model_url = 'soccer-player-intimacy/FastText-KCC150.model'
        self.positiveWords = []
        self.negativeWords = []
        self.loaded = False
        self.positiveWords_url = 'soccer-player-intimacy/src/positive_words.txt'
        self.negativeWords_url = 'soccer-player-intimacy/src/negative_words.txt'
        self.setPositiveWords(self.positiveWords_url)
        self.setNegativeWords(self.negativeWords_url)
        self.loadModel(self.model_url)

    def loadModel(self, url):
        self.model = Word2Vec.load(url)
        self.loaded = True

    def setPositiveWords(self, src):
        with open(src, 'r', encoding='utf-8') as f:
            word = f.readline().strip()
            while word:
                self.positiveWords.append(word)
                word = f.readline().strip()
            f.close()

    def setNegativeWords(self, src):
        with open(src, 'r', encoding='utf-8') as f:
            word = f.readline().strip()
            while word:
                self.negativeWords.append(word)
                word = f.readline().strip()
            f.close()

    def analyzePositiveOrNagative(self, nouns):
        nouns_vectors = [self.model.wv.get_vector(
            noun) for noun in nouns if noun in self.model.wv.key_to_index]
        if len(nouns_vectors) > 0:
            sentiment_vector = np.mean(nouns_vectors, axis=0)

            # 해당 벡터가 긍정어에 속하는지 부정어에 속하는지 판단
            positive_sim = [self.model.wv.similarity(
                word, sentiment_vector) for word in self.positive_words]
            negative_sim = [self.model.wv.similarity(
                word, sentiment_vector) for word in self.negative_words]

            if (len(positive_sim) == 0) or (len(negative_sim) == 0):
                print("비교 불가 길이 : positive_sim: %d / negative_sim: %d" %
                      len(positive_sim), len(negative_sim))
            else:
                if np.amax(positive_sim) > np.amax(negative_sim):
                    return 1
                else:
                    return 0
        return 0


def main():
    analyzer = Analyzer()
    # task1 = asyncio.ensure_future(analyzer.loadModel(analyzer.model_url))
    # await task1


if __name__ == '__main__':
    main()
    # loop = asyncio.get_event_loop()
    # print("test3")
    # loop.run_until_complete(main())
    # print("test4")
    pass
