from app.tools.TreeTagger import treetaggerwrapper
from app.tools.TreeTagger.TreeTaggerWord import *
from math import log

def lemmatisation(array_rss, k=1):
    occ = {}
    doc = {}
    for rss in array_rss:
        result, doc = lemmatisation_intern(rss, k, occ, doc)

    max_occ = max(result.values())
    nb_doc = len(array_rss)

    result = {}
    for key in result:
        tf = result[key] / max_occ
        idf = log(nb_doc / doc[key]) + 1
        score = tf * idf
        result[key] = score

    #Sorting the dictionary
    result = sorted(result, key=result.get, reverse=True)
    return result

def lemmatisation_intern(rss, k, result, doc):
    # Construction et configuration du wrapper
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR='TreeTagger',
                                          TAGINENC='utf-8',TAGOUTENC='utf-8')

    # Utilisation
    tags = tagger.TagText(rss)
    data = formatTTG(tags)

    liste = []

    i = 0
    while i <= len(data) - k:
        lemma = data[i].lemma
        for j in range(k - 1):
            lemma += " " + data[i + j + 1]
        if lemma not in result:
            result[lemma] = 0
            doc[lemma] = 1
            liste += [lemma]
        elif lemma not in liste:
            doc[lemma] += 1
            liste += [lemma]

        result[lemma] += 1
        i += 1
    return result, doc
