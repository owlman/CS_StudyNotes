#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
    Created on 2015-11-20
    
    @author: lingjie
    @name:   example_NLTK_URL_analyzing
'''

import urllib2
import nltk
from bs4 import BeautifulSoup
Hint: 􀁉􀁕􀁕􀁑􀀛􀀐􀀐􀁕􀁂􀁓􀁕􀁂􀁓􀁖􀁔􀀏􀁐􀁓􀁈􀀐􀁎􀁂􀁓􀁕􀁊􀁏􀀐􀀱􀁐􀁓􀁕􀁆􀁓􀀴􀁕􀁆􀁎􀁎􀁆􀁓􀀐􀁑􀁚􀁕􀁉􀁐􀁏􀀏􀁕􀁙􀁕􀀁
http://Snowball.tartarus.org/algorithms/english/stemmer.html
def URL_analyzing(url):
    response = urllib2.urlopen(url)
    html = response.read()
        
    #clean = nltk.clean_html(html)
    # but the function raise NotImplementedError 
	#("To remove HTML markup, use BeautifulSoup's get_text() function")
    soup = BeautifulSoup(html,"lxml")
    clean = soup.get_text()
    tokens = [tok for tok in clean.split()]
    # print tokens[:100]
    Freq_dist_nltk=nltk.FreqDist(tokens) 
    print Freq_dist_nltk 
    Freq_dist_nltk.plot(50, cumulative=False)
    
def main():
    URL_analyzing("http://python.org/")

if __name__ == "__main__":
    main()
    