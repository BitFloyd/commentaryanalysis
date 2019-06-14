import tensorflow as tf
import tensorflow_hub as hub
from commentaryanalysis.corpusFromCommentary import *


def getUniversalSentenceEncodingsFromCorpus(corpus):

    sents = getSentsFromCorups(corpus)
    module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3"
    embed = hub.Module(module_url)
    messages = []

    for line in sents:
        sent = ''
        for word in line[:-1]:
            sent = sent + ' ' + word

        sent += '.'

        messages.append(sent)

    
    message_embeddings = getUniversalSentenceEncodingsFromListOfLines(messages)

    return message_embeddings


def getUniversalSentenceEncodingsFromListOfLines(list_of_lines):

    module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3"
    embed = hub.Module(module_url)

    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        message_embeddings = session.run(embed(list_of_lines))

    return message_embeddings