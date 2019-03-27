# commentaryanalysis
A package to create and analyze a corpus from a set of closed caption files from hockey videos.


IMPORTANT: 
---------
This is written in Py 2.7. 

The srt files are generated from the TS files using the following script.

```

import os
path_to_TS = '/usr/local/data/sejacob/HOCKEY_VIDEOS/TS'
path_to_Sub = '/usr/local/data/sejacob/HOCKEY_VIDEOS/Subtitles'
list_of_TS_files_abs_path = [os.path.join(path_to_TS,i) for i in os.listdir(path_to_TS)]
list_of_Sub_files_abs_path = []

for i  in os.listdir(path_to_TS):
    filename, file_extension = os.path.splitext(i)
    list_of_Sub_files_abs_path.append(os.path.join(path_to_Sub,filename+'.srt'))

commands = []

for i, j in zip(list_of_TS_files_abs_path,list_of_Sub_files_abs_path):
    commands.append('ffmpeg -f lavfi -i movie={ts_file}[out+subcc]  -map 0:1  {sub_file}'.format(ts_file=i,sub_file=j))

for command in commands:
    os.system(command)
```

INSTALLATION:
-------------
Download the source files

Navigate to the folder where setup.py lies in your terminal

Do: pip install -e .

(This will create a package in your python environment called commentaryanalysis using a symlink. So anytime we make changes in this code, you can just pull the repo to ths same spot and the python package will be updated automatically without re-installing it)

USAGE:
------
```
from commentaryanalysis.corpusFromCommentary import *
from commentaryanalysis.wordFrequencies import *

SRTDir='/usr/local/data/sejacob/HOCKEY_VIDEOS/Subtitles'
CorpusDir='/usr/local/data/sejacob/HOCKEY_VIDEOS/CorpusFiles'
corpus = getCorpusFromSRTDir(SRTDir,CorpusDir)
words_from_corpus = getWordsFromCorpus(corpus)
filtered_words = remove_stopwords_from_corpus_words(words_from_corpus)
normalized_fqdist = normalized_sorted_frequency_distribution(filtered_words)
plot_normalized_frequency_distribution(normalized_fqdist,n=35)
```
