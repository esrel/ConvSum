#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# MMR: Maximal Marginal Relevance
# (Jaime Carbonell and Jade Goldstein, SIGIR, 1998)
#
# Based on Jeremy Trione
# Based on Karan Singla
# Modified by Evgeny A. Stepanov

from collections import Counter

import re, math
import argparse
import sys, os
reload(sys).setdefaultencoding("utf-8")

class MaximalMarginalRelevance:
	''' Extractive Summarization using Maximal Marginal Relevance '''

	def __init__(self):
		''' Constructor '''
	
	def text2vec(self, text):
		''' Convert text to word counts '''
		return Counter(text)
		
	def flatten_list(self, ilist):
		''' flatten 2D list '''
		flist = []
		for l in ilist:
			flist += l
		return flist
	
	def cosine_similarity(self, vec1, vec2):
		'''Simple Cosine Similarity'''
		intersection = set(vec1.keys()) & set(vec2.keys())
		numerator    = sum([vec1[x] * vec2[x] for x in intersection])

		vec1_sum     = sum([vec1[x]**2 for x in vec1.keys()])
		vec2_sum     = sum([vec2[x]**2 for x in vec2.keys()])
		denominator  = math.sqrt(vec1_sum) * math.sqrt(vec2_sum)

		if not denominator:
			return 0.0
		else:
			return float(numerator)/denominator

	def summarize(self, sents, lbda, slen):
		'''Maximal Marginal Relevance'''
		
		summ = []
		
		# Create full text
		ftext  = self.flatten_list(sents)
		
		tlen   = len(ftext)
		argmax = 0
		
		# % of the conversation
		summ_rate = tlen * float(slen)/100
		summ_dict = {}
		
		conv_vec = self.text2vec(ftext) # conversation vector

		while len(self.flatten_list(summ)) < summ_rate:
			for i in range(len(sents)):
				sent_vec = self.text2vec(sents[i])
				summ_vec = self.text2vec(self.flatten_list(summ))
		
				conv_sent_cossim = self.cosine_similarity(sent_vec, conv_vec)
				sent_summ_cossim = self.cosine_similarity(sent_vec, summ_vec)
				
				conv_score = float(lbda) * conv_sent_cossim;
				summ_score = (1 - float(lbda)) * sent_summ_cossim 
				
				mmr_score = conv_score -  summ_score
				
				if mmr_score >= argmax:
					argmax = mmr_score

				summ_dict[mmr_score] = sents[i]		
		
			summ.append(summ_dict[argmax])
			sents.remove(summ_dict[argmax])
			summ_dict = {}
			argmax = 0
			
		return summ
		
#----------------------------------------------------------------------#
if __name__ == "__main__":
	
	'''
	Requres tokenized & sentence split text
	sentence/utterance per line
	'''

	argpar = argparse.ArgumentParser(description='Extractive Summarization using Maximal Marginal Relevance')
	argpar.add_argument('-f', '--ifile', type=file)
	argpar.add_argument('-p', '--lbda',  type=float, default=0.7)
	argpar.add_argument('-s', '--slen',  type=int,   default=7)
	args = argpar.parse_args()

	mmr = MaximalMarginalRelevance(lbda=args.lbda)

	text = args.ifile.read()
	toks = [sent.split() for sent in text.split("\n")]

	summ = mmr.summarize(toks, args.lbda, args.slen)
	
	for sent in summ:
		print ' '.join(sent)






