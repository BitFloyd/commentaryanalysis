from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import OrderedDict
from matplotlib import pylab
from corpusFromCommentary import getWordsFromCorpus
import math
from scipy import stats
import numpy as np

def remove_stopwords_from_corpus_words(words):

    stop_words = stopwords.words('english')
    stop_words = [i.upper() for i in stop_words]
    stop_words.append('.')

    filtered_words = [word for word in words if word not in stop_words]

    return filtered_words

def get_frequency_distribution_of_words(words):

    fqdist = FreqDist(words)

    return fqdist

def normalized_sorted_frequency_distribution(words):

    fqdist = FreqDist(words)
    N = fqdist.N()
    sorted_keys_of_fqdist = sorted(fqdist, key=fqdist.get, reverse=True)

    normalized_fqdist = OrderedDict()

    for key in sorted_keys_of_fqdist:
        normalized_fqdist[key] = (fqdist[key]/(N+0.0))

    return normalized_fqdist

def plot_frequency_distribution(fqdist,n=20):

    fqdist.plot(n)

    return True

def plot_normalized_frequency_distribution(n_fqdist, n=20):

    text_type=unicode
    pylab.grid(True, color="silver")
    pylab.title('Normalized Word Frequency Distribution. TOP {n} Samples'.format(n=n))

    freqs = n_fqdist.values()[0:n+1]
    samples = n_fqdist.keys()[0:n+1]

    pylab.stem(freqs)
    pylab.xticks(range(len(samples)), [text_type(s) for s in samples], rotation=90)
    pylab.xlabel("Samples")
    pylab.ylabel("Normalized Word Frequency")
    pylab.show()

    return True

def plot_zipf_law_on_corpus(corpus):

    words = getWordsFromCorpus(corpus)
    words = remove_stopwords_from_corpus_words(words)
    fdist = FreqDist(words)
    words = fdist.most_common()

    x = [math.log(i[1]) for i in words]
    y = [math.log(i) for i in range(1, len(x)+1)]

    (m, b) = pylab.polyfit(x, y, 1)
    yp = pylab.polyval([m, b], x)

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)


    pylab.plot(x, y,'r')
    pylab.plot(x,yp,'b')

    pylab.ylim([min(y), max(y)])
    pylab.xlim([min(x), max(x)])
    pylab.text(x=1,y=1,s = "Best Fit Line (Blue) \nslope = {slope}".format(slope=np.round(slope,2)))
    pylab.grid(True)
    pylab.ylabel('Counts of words (log)')
    pylab.xlabel('Ranks of words (log)')
    pylab.title('ZIPF LAW TEST ON CORPUS. IDEALLY SLOPE OF THE LINE MUST BE = -1 for IDEAL ZIPF CASE')
    pylab.show()

