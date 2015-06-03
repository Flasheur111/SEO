from TreeTagger import treetaggerwrapper
from TreeTagger.TreeTaggerWord import *
from math import log

def lemmatisation(array_rss, k):
    occ = {}
    doc = {}
    for rss in array_rss:
        result, doc = lemmatisation_intern(rss, k, occ, doc)

    max_occ = max(result.values())
    nb_doc = len(array_rss)
    for key in result:
        tf = result[key] / max_occ
        #print "NbDoc: " + str(nb_doc) + " Doc: " + str(doc[key])
        idf = log(nb_doc / doc[key]) + 1
        score = tf * idf
        #Faire quelquechose avec !!!
        #To delete
        print(key + ' ' + str(tf) + ' ' + str(idf))

def lemmatisation_intern(rss, k, result, doc):
    # Construction et configuration du wrapper
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR='TreeTagger',
                                          TAGINENC='utf-8',TAGOUTENC='utf-8')

    # Utilisation
    print('rss is ' + rss)
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


lemmatisation(['What I did for love ?'], 1)
