from app.tools.TreeTagger import treetaggerwrapper
from app.tools.TreeTagger.TreeTaggerWord import *
from math import log
from operator import itemgetter
import stop_words
import platform

if platform.architecture()[0] == '32bit':
    treetagger_path = 'app/tools/TreeTagger/32'
else:
    treetagger_path = 'app/tools/TreeTagger/64'


def lemmatization_full_article(article_rss, lang='fr', nb_keyword=6):
    titles = lemmatization(article_rss.keys(), lang)
    contents = lemmatization(article_rss.values(), lang)

    return titles[:nb_keyword], contents[:nb_keyword]

def lemmatization(array_rss, lang):
    if len(array_rss) == 0:
        return {}
    occ = [{}, {}, {}]
    doc = [{}, {}, {}]
    for rss in array_rss:
        occ, doc = lemmatization_intern(lang, rss, occ, doc)

    if len(occ[0].values()) == 0:
        return {}

    result = {}
    nb_doc = len(array_rss)
    for i in range(3):
        max_occ = max(occ[i].values())

        for key in occ[i]:
            tf = occ[i][key] / max_occ
            idf = log(nb_doc / doc[i][key] + 1)
            score = tf * idf
            result[key] = score

    #Sorting the dictionary
    sorted_list = [key[0] for key in sorted(result.items(), key=itemgetter(1), reverse=True)]
    return sorted_list

def lemmatization_intern(lang, rss, result, doc):
    # Construction et configuration du wrapper
    tagger = treetaggerwrapper.TreeTagger(TAGLANG=lang, TAGDIR=treetagger_path,
                                          TAGINENC='utf-8', TAGOUTENC='utf-8')

    # Utilisation
    tags = tagger.TagText(rss)
    data = formatTTG(tags, tagger, stop_words.get_stop_words(language=lang))

    for k in [1, 2, 3]:
        i = 0
        liste = []
        while i <= len(data) - k:
            lemma = getLemma(data[i])

            for j in range(k - 1):
                lemma += " " + getLemma(data[i + j + 1])
            if lemma not in result:
                result[k-1][lemma] = 0
                doc[k-1][lemma] = 1
                liste += [lemma]
            elif lemma not in liste:
                doc[k-1][lemma] += 1
                liste += [lemma]

            result[k-1][lemma] += 1
            i += 1
    return result, doc

def getLemma(data):
    lemma = data.lemma
    if lemma == '<unknown>':
        lemma = data.word
    return lemma