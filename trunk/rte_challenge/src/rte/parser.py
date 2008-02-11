#!/usr/bin/python

# File: parser.py
# Author: Rongzhou Shen
# Date: 11-02-2008
# Parses the RTE xml data into a list of TH dictionary objects

import cElementTree as ct

def parse(file_name):
    file = open(file_name)
    tree = ct.parse(file)

    th_list = []

    root = tree.getroot()
    th_pairs = root.findall("pair")
    for th_pair in th_pairs:
        th = {'id' : th_pair.get("id"),\
              'entailment' : th_pair.get("entailment"),\
              'task' : th_pair.get("task"),\
              'length' : th_pair.get("length")}
        text = th_pair.find("t").text
        th['text'] = text
        hypo = th_pair.find("h").text
        th['hypo'] = hypo

        th_list.append(th)

    return th_list

if __name__ == '__main__':
    parse("data/rte3_dev.xml")
