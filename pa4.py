Python 3.12.0 (tags/v3.12.0:0fb18b0, Oct  2 2023, 13:03:39) [MSC v.1935 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> # Classmates consulted for this assignment:
... #   none
... #
... # Other sources consulted for this assignment:
... #   none
... 
... 
... # Task 1: Word counting across files
... # ----------------------------------
... # Write a function that takes as arguments the path to a folder containing 
... # .txt files, the path to an output .txt file, and the path to a file 
... # containing a list of words to ignore, and creates a file at the output path 
... # that reports how many times each word that is not in the ignore list occurs 
... # across all of the .txt files in the input folder. 
... # You can assume that the input folder path will end in a /. You can also 
... # assume that every word in each .txt file in the input folder should be 
... # counted. 
... # See the README for considerations about case and punctuation, and for the
... # expected format of the output file.
... import glob
... def count_words_across_files(input_folder_path, output_filepath, 
...                              words_to_ignore_path="input/stopwords.txt"):
...     """This function first takes the file containing the words we don't want
...     to count and makes a list of those words, then it uses every file in the
...     input filepath to generate a list of all the words in that folder's files.
...     Then it counts how many times each word we are interested in has occurred,
...     then sorts that counter and creates file with all the sorted words and
...     their counts.
...     """
...     words_to_ignore = get_ignore_words(words_to_ignore_path)
...     word_counter = count_words(input_folder_path, words_to_ignore)
...     sorted_counter = sort_counter(word_counter)
...     create_output_one(sorted_counter, output_filepath)
... 
... def get_ignore_words(words_to_ignore_path):
...     """Takes a path to a file containing the words that we should not count
...     and makes a list of those words, which is returned
    """
    with open(words_to_ignore_path) as in_file:
        ignore_list = list()
        for line in in_file:
            line = line.strip("\n")
            ignore_list.append(line)
    return ignore_list

def count_words(input_folder_path, words_to_ignore):
    """makes a list of each filepath in the input folderpath, then iterates 
    through each of those files. Each iteration, it cleans every line of the 
    file into a list of just the words, then for each word that is not in 
    words_to_ignore it updates the counter for that word
    """
    folder_path_ext = input_folder_path + "*.txt" 
    filepaths = glob.glob(folder_path_ext)
    words_list = list()
    for filepath in filepaths:
        with open(filepath, encoding="utf-8") as in_file:
            for line in in_file:
                line_words = process_text(line)
                for word in line_words:
                    if word not in words_to_ignore:
                        words_list.append(word)
    word_counter = dict()
    for word in words_list:
        word_counter[word] = word_counter.get(word, 0) + 1
    return word_counter

def process_text(text):
    """This function breaks a string into a list of individual lowercase words,
    removing any spaces, newline characters, or external punctuations, 
    then returns the list of words
    """
    text = text.lower()
    word_list = text.split()
    punctuation = "!?\".,()-@#$%^&;:*_"
    for i in range(len(word_list)):
        word_list[i] = word_list[i].strip("\n")
        word_list[i] = word_list[i].strip(punctuation)
    while "" in word_list:
        word_list.remove("")
    return word_list

def cust_sort(tuple):
    """sorts by the value indescending order, then key alphabetically"""
    return (-tuple[1], tuple[0])
    
def sort_counter(word_counter):
    """makes a dictionary into a list of key:value tuples, which is then
    sorted as a list
    """
    count_list = list(word_counter.items())
    count_list = sorted(count_list, key = cust_sort)
    return count_list

def create_output_one(counter_list, output_filepath):
    """Takes a list of key:value tuples and puts them in the indicated
    output filepath, properly formatted
    """
    with open(output_filepath, "w") as out_file:
        for tuple in counter_list:
            line = tuple[0]+"\t"+str(tuple[1])+"\n"
            out_file.write(line)
            
# Task 2: Flesch scoring sentences in a file
# ------------------------------------------
# Write a function that reads a list of sentences from a file and produces
# a CSV file that reports each sentence, its number of words, its number
# of syllables, and its Flesch reading ease score, rounded to 2dp. 
# Your function should take as arguments the path to an input plain text
# file, the path to the CSV file to output, and the path to a JSON file
# representing the CMU Pronunciation Dictionary.
# See the README for the expected format of the CSV file.
import csv
import json
import re
def flesch_score_sentences(sentences_filepath, csv_filepath, 
                           cmudict_filepath="input/cmudict-0.7b.json"):
    """Takes a .txt file with a sentence on each line and outputs a .csv file
    where each row is the original sentence, the number of words in the
    sentence, the number of syllables in the sentence, and the sentence's
    flesch score
    """
    list_of_rows = process_input(sentences_filepath, cmudict_filepath)
    create_output_two(list_of_rows, csv_filepath)

def process_input(sentences_filepath, cmudict_filepath):
    """takes an input file path with a sentence on each line, and builds
    a list of lists, where each list inside the overall list contains the data
    for each row in the csv file we hope to output.
    """
    with open(cmudict_filepath, encoding="utf-8") as in_file:
        cmu_dict = json.load(in_file)
    with open(sentences_filepath, encoding="utf-8") as in_file:
        csv_rows = list()
        for line in in_file:
            row = list()
            #add sentence with no newline char to row list first
            row.append(line.strip("\n"))
            num_senten = len(line.split(". "))
            #find then add number of words to row list
            words = process_text(line)
            num_words = len(words)
            row.append(num_words)
            #find then add number of syllables to row list
            num_syl = 0
            for word in words:
                num_syl += count_syllables(word, cmu_dict)
            row.append(num_syl)
            #calculate flesch score with above values and add to row list
            flesch = (206.835 - 1.015 * num_words / num_senten - 84.6 * num_syl / num_words)
            row.append(round(flesch, 2))
            csv_rows.append(row)

    return csv_rows

def create_output_two(list_of_rows, csv_filepath):
    """takes a list of lists and creates an output csv file at the indicated
    filepath, where each row is the sentence, number of words, number of 
    syllables, and flesch score for each sentence in the original input file.
    """
    with open(csv_filepath, "w", newline="") as out_file:
        writer = csv.writer(out_file)
        headers = ["SENTENCE", "WORDS", "SYLLABLES", "FLESCH_SCORE"]
        writer.writerow(headers)
        writer.writerows(list_of_rows)

def count_syllables(word, cmu_dict):
    """This function checks if the input word exists as a key in the given
    dictionary, and if it does then it iterates through each string 
    contained in that keys associated list.  For each string, it checks if 
    the string ends in a 0, 1, or 2, and when it finds any of those digits 
    it adds one to our syllable counter since that string must represent a 
    vowel phone.  We then return the number of vowel phones found, which is
    the same as the number of syllables. If the input word does not exist 
    as a key in the given dictionary, then it uses the provided 
    estimate_syllables function to return an estimate for the input word's
    number of syllables.    
    """
    word = word.upper()
    syllable_count = 0
    if word in cmu_dict.keys():
        for string in cmu_dict[word]:
            if string[-1].isdigit():
                syllable_count += 1
    else:
        syllable_count = estimate_syllables(word)

    return syllable_count

def estimate_syllables(word):
    """Returns an estimate of the number of syllables in a provided 
    English word.
    
    Assumptions
    -----------
    1. each sequence of at least one vowel character (a, e, i, o, u) 
       corresponds to a single syllable.
    2. a y that it not at the beginning of a word or after a vowel 
       character adds a syllable.
    3. word endings -es, -ed, and -e (but not -le) do not add syllables, 
       unless they are the only syllable in the word.

    Note: this does not account for OCP effects with -es and -ed.
    """
    syllables = len(re.findall(r"[aeiou]+", word, flags=re.I))
    
    syllables += len(re.findall(r"[^aeiou]y", word, flags=re.I))
    
    if syllables > 1 and re.search(r"(?:e[sd]|(?<!l)e)$", word, flags=re.I):
        syllables -= 1
    
    return syllables
    
# Task 3: N-gram extraction by UPOS
# ---------------------------------
# Write a function that extracts all of the N-grams with provided Universal
# Dependencies Part-of-Speech (UPOS) tags from a UPOS-tagged plain text file
# and saves them in a CSV file. Your function should take as arguments a
# tuple of N string labels for UPOS tags, the path to a plain text file
# where each word is followed by an underscore and its UPOS tag, and the
# path to the CSV file to create.
# See the README for the expected CSV format and futher considerations.
def extract_upos_ngrams_to_csv(upos_ngram, tagged_filepath, csv_filepath):
    header = header_row(len(upos_ngram))
    pattern = upos_ngram_pattern(upos_ngram)
    tagged_ngrams = find_matches_in_file(pattern, tagged_filepath)
    ngrams = list()
    for tagged_ngram in tagged_ngrams:
        temp = strip_tags(tagged_ngram)
        temp = temp.split()
        ngrams.append(temp)
    create_output_three(header, upos_ngram, ngrams, csv_filepath)

def header_row(n):
    """Makes a header row for a CSV file to report on UPOS tags and words for
    N-grams, of the format UPOS_1, ..., UPOS_N, WORD_1, ..., WORD_N

    Arguments
    ---------
    n: int; the size of the N-grams to be reported

    Returns
    -------
    header_row: list(str); a list of 2N labels to act as column headings, 
                UPOS_1, ..., UPOS_N, WORD_1, ..., WORD_N
    """
    header_row = list()
    for i in range(1, n+1):
        header_row.append("UPOS_"+str(i))
    for i in range(1, n+1):
        header_row.append("WORD_"+str(i))
    return header_row    

def upos_ngram_pattern(upos_ngram):
    """Creates a pattern for finding a sequence of N words with a provided
    sequence of N UPOS tags, where the tag of each word follows an _ after
    the word, and tagged words are separated by a single space.

    Arguments
    ---------
    upos_ngram: tuple(str); the sequence of N UPOS tags that the extracted
                N words are required to have (in ALL CAPS)

    Returns
    -------
    pattern: str; a regular expression that matches an N-gram of words with
             the required tags
    """
    pattern = r"\S+_{1}"
    for upos in upos_ngram:
        pattern += str(upos)
        if upos != upos_ngram[-1]:
            pattern += "\s{1}\S+_{1}"

    return pattern

def find_matches_in_file(pattern, filepath):
    """Finds all matches of a regular expression pattern in a file, assuming
    that matches never span multiple lines.

    Arguments
    ---------
    pattern: str; a regular expression to search for in the file
    filepath: str; the path to the input file

    Returns
    -------
    matches: list(str); a list of the matches in the file
    """
    matches = list()
    with open(filepath, encoding = "utf-8") as in_file:
        for line in in_file:
            line_matches = re.findall(pattern, line)
            for match in line_matches:
                matches.append(match)
    return matches

def strip_tags(tagged_words):
    """Strips UPOS tags from words of the format word_UPOS.

    Arguments
    ---------
    tagged_words: str; UPOS-tagged text, where each word is followed by
                  an _ and then its UPOS tag

    Returns
    -------
    words: str; the words from the text, without their tags
    """
    tag_pattern = r"_\S+\b"
    words = re.sub(tag_pattern, "", tagged_words)
    return words

def create_output_three(header, upos_ngram, ngrams, csv_filepath):
    """Takes a desired header of len 2n, the tags for our N-grams, list of
    N-grams stored in lists, and a desired output filepath for a csv.  The 
    function starts each row of the output as UPOS1,...,UPOSN, then each 
    word of the N-gram.  It then creates the csv file using the list of rows
    created.
    """
    rows = []
    for ngram in ngrams:
        tmp_list = list(upos_ngram)
        for word in ngram:
            tmp_list.append(word)
        rows.append(tmp_list)
    with open(csv_filepath, "w", newline="") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(header)
