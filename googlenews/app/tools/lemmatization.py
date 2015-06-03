from TreeTagger import treetaggerwrapper
from TreeTagger.TreeTaggerWord import *
from math import log

def lemmatisation(array_rss, k):
    result = {}
    doc = {}
    for rss in array_rss:
        result, doc = lemmatisation(rss, k, occ, doc)

    max_occ = max(result.values())
    nb_doc = len(array_rss)
    for key in result:
        tf = result[key] / max_occ
        idf = log(nb_doc / doc[key]) + 1
        score = tf * idf
        #Faire quelquechose avec !!!
        #To delete
        print key + ' ' + str(tf) + ' ' + str(idf)

def lemmatisation(input, k, result, doc):
    # Construction et configuration du wrapper
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR='TreeTagger',
                                          TAGINENC='utf-8',TAGOUTENC='utf-8')

    # Utilisation
    tags = tagger.TagText(input)
    data = formatTTG(tags)

    liste = []

    i = 0
    while i <= len(data) - k:
        lemma = data[i].lemma + data[i + 1].lemma + data[i + 3].lemma
        if not result.has_key(lemma):
            result[lemma] = 0
            doc[lemma] = 1
        elif lemma not in liste:
            doc[lemma] += 1
            liste += [lemma]

        result[lemma] += 1
        i += 1
    return result
