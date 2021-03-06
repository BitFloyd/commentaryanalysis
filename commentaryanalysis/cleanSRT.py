from datetime import datetime
import re
from collections import OrderedDict
from contractions import CONTRACTION_MAP
import unicodedata

def remove_control_characters(s):
    s = unicode(s,'utf-8')
    return_unicode = "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")
    return_string = return_unicode.encode('ascii','ignore')

    return return_string


def remove_HTML_tags(s):
    s = s.replace('<font face="Monospace">{\\an7}','')
    s = s.replace('</font>','')
    return s


def readSRTFile(sub_file):

    # Takes an SRT file and returns the lines as a list starting with the line containing '1'
    # that indicates the start of the commentary

    with open(sub_file) as f:
        lines = f.readlines()

    lines = [remove_control_characters(i) for i in lines]
    lines = [remove_HTML_tags(i) for i in lines]
    lines = [i.rstrip() for i in lines]
    lines = [i.lstrip() for i in lines]

    if(len(lines)==0):
        return lines

    while lines[0] != '1':
        lines.pop(0)

    return lines


def parseTimeString(line):

    Tstring1, Tstring2 = line.split('-->')

    Tstring1 = Tstring1.strip()
    Tstring2 = Tstring2.strip()

    T1 = datetime.strptime(Tstring1, '%H:%M:%S,%f')
    T2 = datetime.strptime(Tstring2, '%H:%M:%S,%f')

    T1 = T1.time()
    T2 = T2.time()

    return T1, T2


def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9.\s]' if not remove_digits else r'[^a-zA-z\s]'
    text_removed = re.sub(pattern, '', text)
    return text_removed


def isNotAd(line):
    words = line.split(' ')

    uppercase = 0
    lowercase = 0

    for word in words:
        if (word.isupper()):
            uppercase+=1
        else:
            lowercase+=1

    if(uppercase>lowercase):
        return  True
    else:
        return False


def isMatchMoment(line):

    if(line[0]=='[' and line[-1]==']'):
        return True

    else:
        return False


def addLine(line):

    line_contractions_expanded = expand_contractions(line)
    line_sp_removed = remove_special_characters(line_contractions_expanded)
    line_to_upper = line_sp_removed.upper()
    line_to_upper = line_to_upper.strip()

    return line_to_upper


def stripMatchMomentBracks(line):

    line_stripped = line[1:-1].strip()

    return line_stripped


def checkifLineHasAlphaNum(line):

    line_sp_removed = remove_special_characters(line)

    return any(c.isalpha() or c.isdigit() for c in line_sp_removed)


def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
            if contraction_mapping.get(match) \
            else contraction_mapping.get(match.lower())
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)


    return expanded_text


def cleanSRTFile(lines):

    time_commentary_dict = OrderedDict()

    # time_commentary_dict is a dictionary.
    # It is indexed by a tuple of time between when the commentary has happened.
    # For example:
    # (T1,T2) : LINE SPOKEN AT THAT TIME
    # T1 and T2 are time objects.

    comm_line = 1
    T1 = None
    T2 = None

    last_added_line = None

    while len(lines):

        line = lines[0]
        if(line == str(comm_line)):
            lines.pop(0)
            comm_line+=1
            continue

        elif(not checkifLineHasAlphaNum(line)):
            lines.pop(0)
            continue

        elif('-->' in line):
            T1, T2 = parseTimeString(line)
            lines.pop(0)
            continue

        elif(line == last_added_line):
            lines.pop(0)
            continue

        elif(line==''):
            lines.pop(0)
            continue

        elif(line.isupper()):
            last_added_line = line
            line_to_be_added = addLine(line)
            time_commentary_dict[(T1, T2)] = line_to_be_added
            lines.pop(0)
            continue

        elif('>>' in line and ':' in line):

            colon_split = line.split(':')

            line_to_check = colon_split[1]

            if(isNotAd(line_to_check)):

                last_added_line = line
                line_to_be_added = addLine(line_to_check)
                time_commentary_dict[(T1, T2)] = line_to_be_added
                lines.pop(0)
                continue

            else:
                lines.pop(0)
                continue

        elif(isMatchMoment(line)):
            last_added_line = line
            line_match_brack_stripped = stripMatchMomentBracks(line)

            line_to_be_added = addLine(line_match_brack_stripped)

            time_commentary_dict[(T1, T2)] = line_to_be_added

            lines.pop(0)
            continue

        elif(isNotAd(line)):
            last_added_line = line

            line_to_be_added = addLine(line)

            time_commentary_dict[(T1, T2)] = line_to_be_added


            lines.pop(0)
            continue

        else:
            lines.pop(0)
            continue

    return time_commentary_dict


def order_time_commentary_dict_into_sentences(time_commentary_dict):

    time_commentary_dict_sentences = OrderedDict()

    time_start = None
    time_end = None
    sentence_running = ''

    for time, line in time_commentary_dict.iteritems():

        if time_start is None:
            time_start = time[0]

        line_split = line.split('.')

        for value in line_split[0:-1]:
            sentence_running += value
            sentence_running += '.'
            time_end = time[1]
            time_commentary_dict_sentences[(time_start, time_end)] = sentence_running
            sentence_running = ''

        sentence_running = line_split[-1]

        if line_split[-1] == '':
            time_start = None
        else:
            sentence_running += ' '

        if len(line_split) >1 :
            time_start = time[0]

    if sentence_running.rstrip().lstrip() != '':
        time_commentary_dict_sentences[time_start, time_end] = sentence_running.rstrip() +'.'

    return time_commentary_dict_sentences


def read_and_clean_srt(sub_file):
    """Arguments: path to the subtitle file
       Returns: time_commentary_dict: A dictionary indexed by a tuple of time objects. Ex: (T1,T2): COMMENTARY HERE
                list_time_indexes: A list of time indexes in order of appearance in the SUB FILE
                list_commentary: A list of commentary strings in order of appearance in the SUB FILE

        Notes: The commentary file is cleaned for ads, commentator names, contractions are expanded and all words
               changed to uppercase for uniformity"""
    lines = readSRTFile(sub_file)
    time_commentary_dict = cleanSRTFile(lines)

    return time_commentary_dict


def read_and_clean_srt_into_sentences(sub_file):
    """Arguments: path to the subtitle file
       Returns: time_commentary_dict: A dictionary indexed by a tuple of time objects. Ex: (T1,T2): COMMENTARY HERE
                list_time_indexes: A list of time indexes in order of appearance in the SUB FILE
                list_commentary: A list of commentary strings in order of appearance in the SUB FILE

        Notes: The commentary file is cleaned for ads, commentator names, contractions are expanded and all words
               changed to uppercase for uniformity"""
    lines = readSRTFile(sub_file)
    time_commentary_dict = cleanSRTFile(lines)
    time_commentary_dict_sentences = order_time_commentary_dict_into_sentences(time_commentary_dict)

    return time_commentary_dict_sentences



