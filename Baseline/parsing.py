#!/usr/bin/python

from bs4 import Beautifulsoup
import subprocess
from collections import defaultdict

def stanford_parse(parser_path, file_path, filename):
    result = subprocess.call(['java', '-cp', parser_path, '-Xmx10g', 'edu.stanford.nlp.pipeline.StanfordCoreNLP',
                          '-annotators', 'tokenize,ssplit,pos,lemma,parse', '-file',
                          file_path + filename, '-outputFormat', 'xml', '-outputDirectory',
                          file_path])
    print "DONE!"

def xml_parse(file_path, filename, dic=None): # dependencies for custom txt file; basic-dependencies otherwise.
    with open(file_path + filename, 'r') as f:
        xml = f.read()
    soup = BeautifulSoup(xml, 'xml')
    sents_xml = soup.find("sentences").find_all("sentence")
    sents = []
    for sent_xml in sents_xml:
        sent = defaultdict(list)
        words = [word_xml.contents[0] for word_xml in sent_xml.find("tokens").find_all("word")]
        lemmas = [lemma_xml.contents[0] for lemma_xml in sent_xml.find("tokens").find_all("lemma")]
        deps = [dep_xml.contents[0] for dep_xml in sent_xml.find("dependencies").find_all("dependent")]
        rels = [rel_xml.attrs["type"] for rel_xml in sent_xml.find("dependencies").find_all("dep")]
        govs = [gov_xml.contents[0] for gov_xml in sent_xml.find("dependencies").find_all("governor")]
        if dic != None: # dic: container for token->lemma mapping.
            for word,lemma in zip(words,lemmas):
                dic[word] = lemma
        sent['words'], sent['lemma'] = words, lemmas
        sent['dep_triples'] = zip(deps, rels, govs)
        sents.append(sent)
    return sents