from TreeTagger import treetaggerwrapper
from TreeTagger.TreeTaggerWord import *

# Construction et configuration du wrapper
tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR='TreeTagger',
  TAGINENC='utf-8',TAGOUTENC='utf-8')

# Utilisation
tags = tagger.TagText(u"Ceci est un très court texte à étiqueter.")
data = formatTTG(tags)

print data[0].word
print data[0].postag
print data[0].lemma
