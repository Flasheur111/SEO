from app.tools.TreeTagger import treetaggerwrapper
from app.tools.TreeTagger.TreeTaggerWord import *
from math import log
from operator import itemgetter

def lemmatisation_full_article(article_rss, k=1, lang='fr', nb_keyword=3):
    titles = lemmatisation(article_rss.keys(), lang, k)
    contents = lemmatisation(article_rss.values(), lang, k)

    titles_keywords = {}
    contents_keywords = {}
    for i in range(nb_keyword):
        if i < len(titles):
            titles_keywords[titles[i][0]] = titles[i][1]
        if i < len(contents):
            contents_keywords[contents[i][0]] = contents[i][1]
    return titles_keywords, contents_keywords

def lemmatisation(array_rss, lang, k=1):
    if len(array_rss) == 0:
        return {}
    occ = {}
    doc = {}
    for rss in array_rss:
        occ, doc = lemmatisation_intern(lang, rss, k, occ, doc)

    if len(occ.values()) == 0:
        return {}

    max_occ = max(occ.values())
    nb_doc = len(array_rss)

    result = {}
    for key in occ:
        tf = occ[key] / max_occ
        idf = log(nb_doc / doc[key]) + 1
        score = tf * idf
        result[key] = score

    #Sorting the dictionary
    sorted_list = sorted(result.items(), key=itemgetter(1), reverse=True)
    return sorted_list

def lemmatisation_intern(lang, rss, k, result, doc):
    # Construction et configuration du wrapper
    tagger = treetaggerwrapper.TreeTagger(TAGLANG=lang,TAGDIR='app/tools/TreeTagger',
                                          TAGINENC='utf-8',TAGOUTENC='utf-8')

    # Utilisation
    tags = tagger.TagText(rss)
    data = formatTTG(tags, tagger, get_stop_words(language=lang))
    liste = []

    data_clear = []
    stop_words = get_stop_words(lang)

    i = 0
    while i <= len(data) - k:
        lemma = getLemma(data[i])

        for j in range(k - 1):
            lemma += " " + getLemma(data[i + j + 1])
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

def getLemma(data):
    lemma = data.lemma
    if lemma == '<unknown>':
        lemma = data.word
    return lemma