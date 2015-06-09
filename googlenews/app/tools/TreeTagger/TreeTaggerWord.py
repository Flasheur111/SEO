import app.tools.TreeTagger.treetaggerwrapper

class TreeTaggerWord:
    def __init__(self, triplet):
        self.word, self.postag, self.lemma = triplet

def formatTTG(output, treetagger, stop_words):
    words = []
    stop_words += ['\'', '"', '.', ',', '!', '?', ':', '.', '/', '\\', '-', '+', '(', '{', '[', ']', '}', ')', '#', '@', '«', '»', '@card@', '>', '<', '–', '|', '%', '...', '©']
    for w in output:
        split = w.split("\t")
        if len(split) != 3:
            newtags = treetagger.TagText(w.replace('.', ' '))
            for newtag in newtags:
                split = newtag.split("\t")
                if len(split) == 3:
                    treeTaggerWord = TreeTaggerWord(newtag.split("\t"))
                    if treeTaggerWord.lemma not in stop_words:
                        words.append(treeTaggerWord)
                else:
                    words.append(TreeTaggerWord([newtag, newtag, newtag]))
        else:
            treeTaggerWord = TreeTaggerWord(w.split("\t"));
            if treeTaggerWord.lemma not in stop_words:
                words.append(treeTaggerWord)
    return words
