'''
    Script for cleaning maintenance work order short text (adapted from notebook W3-1)
'''

# Ensure that packages are installed
import os
os.system('pip install regex nltk')

import regex
import nltk
# Load the NLTK stopwords
nltk.download("stopwords")
from nltk.corpus import stopwords

word_normalisation_dictionary = {
    "#": "number",
    "@": "at",
    "u/s": "unserviceable",
    "changeout": "change out",
    "c/o": "change out",
    "c/out": "change out",
    "rplc": "replace",
    "p/p": "pump",
    "stn": "station",
    "repl": "replace",
    "&": "and",
    "rpl": "replace",
}


# Remove all characters except for alphanumerical and reserved special characters e.g. @, -, #, /, and .
# Note: We're using regular expressions here, so some characters need to be 'escaped' as they are special 'metacharacters'
# Refer to this for further information: https://www3.ntu.edu.sg/home/ehchua/programming/howto/Regexe.html
chars_to_keep = "&\.\#\@\/-"
fnc_rmv_chars = lambda text: regex.sub(rf"[^a-zA-Z0-9 {chars_to_keep}]", "", text)

# Remove duplicate reserved special characters (like ##, @@@, etc.)
# This way if we want to normalise # to number and we have ## we wont' get numbernumber

fnc_rmv_dupe_chars = lambda text: regex.sub(rf"([{chars_to_keep}])\1+", r"\1", text)

# Break any erroneous hyphenated or compound abbreviations
# We want to keep things like 'o-ring' and 'c/o' but fix things like 'CV001-replace' → 'CV001 - replace'
# and 'change-out' → 'change out', 'Plate/Lower' → 'plate / lower', 'inspect/replace' → 'inspect / replace'

fnc_fix_compound_hyphen = lambda text: regex.sub(r"(?<=\w{3,})-(?=\w{3,})", " - ", text)
fnc_fix_compound_fwd_slash = lambda text: regex.sub(
    r"(?<=\w{3,})\/(?=\w{3,})", " / ", text
)
fnc_fix_compound_chars = lambda text: fnc_fix_compound_fwd_slash(
    fnc_fix_compound_hyphen(text)
)

# Removing superfluous whitespace (e.g. more than 1 whitespace between words)
# Doing this means we do not have tokens that are whitespace e.g. 'replace   engine' → ['replace', '', '', 'engine']
# We also 'strip' leading and ending whitespace e.g. ' replace engine ' → 'replace engine'

fnc_rmv_whitespace = lambda text: regex.sub(r" {2,}", " ", text).strip()

# Removing stopwords (cautiously)
# Note: stopwords are unigrams, so we can simply split our text on whitespace and check whether each token
# is in a stopword list; if it is, skip it, otherwise keep it.

# Recall that some stopwords are meaningful for us, hence we will filter the list down first.

stopwords_to_keep = [
    "on",
    "off",
    "over",
    "under",
    "no",
    "not",
    "don",
    "don't",
    "aren",
    "aren't",
    "no",
    "not",
    "didn't",
    "doesn",
    "doesn't",
    "hadn",
    "hadn't",
    "hasn",
    "hasn't",
    "haven",
    "haven't",
    "isn",
    "isn't",
    "won",
    "won't",
    "wouldn",
    "wouldn't",
]
filtered_stopwords = [
    word for word in stopwords.words("english") if word not in stopwords_to_keep
]

fnc_rmv_stopwords = lambda text: " ".join(
    [token for token in text.split(" ") if token not in filtered_stopwords]
)

# Normalising noisy words with a controlled dictionary
# Note this could be performed entirely with more complex regular expressions
def dictionary_normalisation(text: str, norm_dict: dict) -> str:
    for noisy_word, clean_word in norm_dict.items():
        if noisy_word in chars_to_keep:
            text = text.replace(noisy_word, f" {clean_word} ")
        text = regex.sub(rf"(?<!-)\b{noisy_word}\b(?!-)", f" {clean_word} ", text)

    return text


# Putting them all together. Note the order of these operations is important.
# We don't want to try and remove stopwords or normalise words when they have special characters, or extra whitespace etc.
def clean_text(text: str, norm_dict: dict = word_normalisation_dictionary) -> str:
    """Cleans and normalises a given text. Steps performed include: remove casing,
    removing special characters, removing duplicate non-alphanumerical characters, fix erroneous compound chars,
    removing stopwords, normalising terms using a dictionary, and remvoing superfluous whitespace"""
    text = text.lower()
    text = fnc_rmv_chars(text)
    text = fnc_rmv_dupe_chars(text)
    text = fnc_fix_compound_chars(text)
    text = fnc_rmv_stopwords(text)
    text = dictionary_normalisation(text, norm_dict)
    text = fnc_rmv_whitespace(text)

    return text