class TreeTaggerWord:
    def __init__(self, triplet):
        self.word, self.postag, self.lemma = triplet

def formatTTG(output):
    words = []
    for w in output:
        words.append(TreeTaggerWord(w.split("\t")))
    return words
