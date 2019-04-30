import re
import numpy as np
import pandas as pd

def find_phrases(df, phrase, sender1, sender2):
    """
    args
        - df : pd.DataFrame, to be searched in
        - phrase : str, the phrase to be searched for
        - sender1 : str, name of the person in the chat
        - sender2 : str, name of the other person in the chat

    returns tuple of the form 
        - ((sender_name, count of phrase occurence))
    """
    s1_df = df[df['sender'] == sender1]
    s2_df = df[df['sender'] == sender2]
    s1_count = s1_df.message.str.count(phrase, flags=re.I).sum()
    s2_count = s2_df.message.str.count(phrase, flags=re.I).sum()
    return (sender1, s1_count), (sender2, s2_count)

def search_word_forms(df, word, sender1, sender2):
    """
    args
        - df : pd.DataFrame, to be searched in
        - word : str, the word whose forms we will generate and find
        - sender1 : str, name of the person in the chat
        - sender2 : str, name of the other person in the chat

    returns list of tuples the form 
        - (generated word, (sender_name, count of phrase occurence))
    """
    word_forms = get_word_forms(word)
    occurences = set()

    (s1_found, s2_found) = find_phrases(df, word, sender1, sender2)
    occurences.add((word, s1_found, s2_found))

    for form, words in word_forms.items():
        for a_word in words:
            (s1_found, s2_found) = find_phrases(df, a_word, sender1, sender2)
            occurences.add((a_word, s1_found, s2_found))
    return occurences