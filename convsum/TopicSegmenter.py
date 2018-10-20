# -*- coding: utf-8 -*-
#!/usr/bin/env python

from nltk.tokenize.texttiling import TextTilingTokenizer
from nltk.corpus import stopwords

import re
import argparse
import sys, os
reload(sys).setdefaultencoding("utf-8")

class TopicSegmenter:
	''' Class for Topic Segmentation using TextTiling '''

	def __init__(self, w=20, k=10, sw_lst=None, lang='english'):
		''' Constructor '''
		self.w = w
		self.k = k

		if sw_lst and type(sw_lst) == list:
			self.stopwords = sw_lst
		else:
			self.stopwords = stopwords.words(lang)

	def topicSegment(self, text, join=False):
		''' meta function for TextTiling '''
		tt = TextTilingTokenizer(w=self.w, k=self.k, stopwords=self.stopwords)

		# normalize spaces
		text = re.sub(' +',' ', text)

		return tt.tokenize(text)

#----------------------------------------------------------------------#
if __name__ == "__main__":

	argpar = argparse.ArgumentParser(description='Topic Segmentation using TextTiling')
	argpar.add_argument('-f', '--ifile', type=file)
	argpar.add_argument('-l', '--lang',  type=str, default='english')
	args = argpar.parse_args()

	text = args.ifile.read()

	tsc = TopicSegmenter(lang=args.lang)
	topics = tsc.topicSegment(text)
	for t in topics:
		for s in t.split('\n'):
			print s

