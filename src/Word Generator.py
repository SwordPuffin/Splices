#The program used to generate words.txt
#Made by Nathan Perlman

#You can use this program for yourself, I don't really care.

import nltk
import re
import enchant

# nltk.download('brown')
from nltk.corpus import brown

dictionary = enchant.Dict("en_US")

fdist = nltk.FreqDist(brown.words())
most_common_words = fdist.most_common(100000)

with open('words.txt', 'w') as f:
    for word, freq in most_common_words:
        word = re.sub(r'\d+', '', word)
        word = re.sub(r'[^a-zA-Z0-9]', '', word)
        if(len(word) > 1  and len(word) < 10 and dictionary.check(word)):
            #Must have the forward slashes to designate the start and end of the word. EX. /fast/.
            f.write('/'+ word.lower() + '/\n')
