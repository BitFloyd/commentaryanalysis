import os
from cleanSRT import read_and_clean_srt_into_sentences
from nltk.corpus.reader.plaintext import PlaintextCorpusReader


def textFileFromListCommentary(filepath,list_commentary):

    assert (os.path.exists(os.path.split(filepath)[0]))

    with open(filepath,'w') as f:
        for item in list_commentary:
            f.write("%s\n" % item)

    return True

def checkSRTOrTXT(filename):

    if(len(filename)<=4):
        return False

    elif filename[-4:]=='.txt' or filename[-4:]=='.srt':
        return True

    else:
        return False

def corpusFileName(CorpusDir, i):

    filename, file_extension = os.path.splitext(i)

    new_filename = os.path.join(CorpusDir,filename+'.corpusfile')

    return new_filename

def createCorpusFilesFromSRTDir(SRTDir,CorpusDir):

    assert os.path.exists(SRTDir)
    assert os.path.exists(CorpusDir)

    list_SRT_files = os.listdir(SRTDir)

    # Get only the list of srt or txt files in the directory
    list_SRT_files = [i for i in list_SRT_files if checkSRTOrTXT(i)]

    list_abs_SRT_files = [os.path.join(SRTDir,i) for i in list_SRT_files]

    list_abs_corpus_files = [corpusFileName(CorpusDir, i) for i in list_SRT_files]

    for sub_file, corpus_file in zip(list_abs_SRT_files, list_abs_corpus_files):

        dict_commentary = read_and_clean_srt_into_sentences(sub_file)
        textFileFromListCommentary(corpus_file, dict_commentary.values())

    return True

def getCorpusFromCorpusDir(CorpusDir):

    corpus = PlaintextCorpusReader(CorpusDir,'.*')

    return corpus

def getCorupsFromCorpusFile(CorpusFile):

    CorpusDir,CorpusFile = os.path.split(CorpusFile)

    corpus = PlaintextCorpusReader(CorpusDir,CorpusFile)

    return corpus

def getCorpusFromSRTDir(SRTDir,CorpusDir):

    createCorpusFilesFromSRTDir(SRTDir,CorpusDir)
    corpus = getCorpusFromCorpusDir(CorpusDir)

    return corpus

def getWordsFromCorpus(corpus):

    return corpus.words()
