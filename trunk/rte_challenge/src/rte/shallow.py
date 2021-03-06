#!/usr/bin/python

# File: shallow.py
# Author: Rongzhou Shen
# Date: 11-02-2008
# TODO: A simple baseline RTE system using a simple word overlap between
# the text and the hypothesis for inference.
# Note: This module is intended for finding the features for the TH
# pairs that are inferred correctly using the shallow semantics
# approach.

from parser import parse
from nltk.wordnet import *

def entail(text, hyp):
    entailment = "YES"
    hyp_tokens = hyp.split()
    text_tokens = text.split()

    for token in hyp_tokens:
        if token not in text_tokens:
            synsets = get_synsets(token)
            if len(synsets) == 0:
                entailment = "NO"
            for word in synsets:
                if word not in text_tokens:
                    entailment = "NO"

    return entailment

def get_synsets(word):
    syns = []
    if N.has_key(word):
        synsets = N[word].synsets()
        for s in synsets:
            syns.extend(s.words)
    if V.has_key(word):
        synsets = V[word].synsets()
        for s in synsets:
            syns.extend(s.words)
    return syns

def evaluate(th_list):
    num_correct = 0
    for th_pair in th_list:
        correct = th_pair['entailment']
        text = th_pair['text']
        hyp = th_pair['hypo']
        predict = entail(text, hyp)
        if predict == correct:
            num_correct += 1
        else:
            print "Wrong ID: %s; Task: %s" % (th_pair['id'], th_pair['task'])

    print num_correct / 800.0

if __name__ == '__main__':
    th_list = parse("data/rte3_dev.xml")
    evaluate(th_list)
