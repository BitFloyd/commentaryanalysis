from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import OrderedDict
from matplotlib import pylab

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