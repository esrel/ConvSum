#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# Extractive Summarization using
# TextTiling & MMR


from collections import Counter
from TopicSegmenter import *
from MaximalMarginalRelevance import *
from TreeTagger import *
from GraphRank import *
from SentiLex import *
from SimpleChunker import *

import json
import re, math
import argparse
import sys, os
reload(sys).setdefaultencoding("utf-8")


class Config:
	''' Configuration for classes '''
	
	# General:

	#####
	# Tree Tagger: POS-tags & Lemmas
	# path to treetagger executable
	tt_bin = 'bin/treetagger/bin/tree-tagger'
	# path to par file
	tt_par = 'bin/treetagger/lib/italian.par'
	# to lemmatize or not
	tt_lem = True
	
	#####
	# Lexicon-based Sentiment Analysis: SentiLex
	# path to polarity lexicon
	plex = 'resources/it-lexicon.tsv'
	# path to polarity shifter lexicon
	slex = 'resources/it-shifters.tsv'
	# path to intensifier lexicon
	ilex = 'resources/it-intensifiers.tsv'
	# lexicon token separator
	tsep = '+'
	# lexicon discountinuous token separator
	dsep = '..'
	
	#####
	# Topic Segmenter
	ts_w = 20 # 'virtual' sentence window (words)
	ts_k = 10 # comparison block size (sentences)
	
	#####
	# Maximal Marginal Relevance
	# summary length as % of text sentence
	mmr_len = 7
	# MMR lambda: 0.7 from the paper to get most important parts
	mmr_lmb = 0.7


def list2text(lst):
	text = ''
	for sent in lst:
		text += ' '.join(sent) + '\n'
	return text

#----------------------------------------------------------------------#
if __name__ == "__main__":
	
	''' Extractive Summarizer '''

	argpar = argparse.ArgumentParser(description='Extractive Summarization')
	argpar.add_argument('-f', '--ifile', type=file)
	argpar.add_argument('-l', '--lang',  type=str, default='english')
	argpar.add_argument('-m', '--mode',  type=str, default='sum', choices=['sum', 'seg'])
	argpar.add_argument('-n', '--knum',  type=int, default=5, help='number of keyphrases')
	argpar.add_argument('--keyphrases', action='store_true', help='extract keyphrases')
	argpar.add_argument('--sentiment',  action='store_true', help='tag polarity words')
	argpar.add_argument('--time',       action='store_true', help='text contains time')
	args = argpar.parse_args()

	# Get configuration
	cfg = Config()
	
	# Initiate classes
	mmr = MaximalMarginalRelevance()
	tt  = TreeTagger(cfg.tt_bin, cfg.tt_par, lemma=cfg.tt_lem)
	#tr  = TextRank(args.lang)
	gr  = GraphRank()
	io  = IoUtilities()
	lt  = LexTagger(cfg.tsep, cfg.dsep)
	sl  = SentiLex()

	# read file
	if args.time:
		text = args.ifile.read()
		text = text.strip()
		time = [sent.split()[0:2] for sent in text.split("\n") if len(sent.strip().split()) > 2]
		text = "\n".join([' '.join(sent.split()[2:]) for sent in text.split("\n")])
	else:
		text = args.ifile.read()
		text = text.strip()
		
	# segment into topics
	tlist  = []
	if args.mode == 'seg':
		ts = TopicSegmenter(w=cfg.ts_w, k=cfg.ts_k, lang=args.lang)
		topics = ts.topicSegment(text)
		for t in topics:
			tlist.append([sent.split() for sent in t.split("\n") if sent])
	else:
		tlist.append([sent.split() for sent in text.split("\n") if sent])
		
	# Check if length of times list and number of sentences are the same
	if args.time and len(time) != sum([len(t) for t in tlist]):
		print 'ERROR: Check if each line contains start end times...'
		exit()
		
	# POS-tag and lemmatize
	if args.keyphrases or args.sentiment:
		 tagged = [tt.tag(slist) for slist in tlist]
		 
	# Setup for Sentiment Analysis
	if args.sentiment:
		# make dictionaries
		pdict = sl.mkLex(io.readColumns(open(cfg.plex)))
		sdict = sl.mkLex(io.readColumns(open(cfg.slex)))
		idict = sl.mkLex(io.readColumns(open(cfg.ilex)))
		# make lists of lexicon entries
		plist = lt.readLex(pdict.keys())
		slist = lt.readLex(sdict.keys())
		ilist = lt.readLex(idict.keys())

	# for each topic segment produce required representation
	out  = [] # output list
	scnt = 0  # sentence counter
	for k,t in enumerate(tlist):
		seg = {}
		
		# add topic ID
		seg['topic_id'] = k
		
		# add topic start & end times
		if args.time:
			seg['start'] = time[scnt][0]
			seg['end']   = time[scnt + len(t) - 1][1]
			scnt += len(t)

		# summarize
		topic = t[:]
		summary = mmr.summarize(topic, cfg.mmr_lmb, cfg.mmr_len)
		
		# sort summary sentences w.r.t. order of appearance & extract:
		# - summary sentence indices
		# - tagged summary sentences
		indices = []
		sorted_summary = []
		tagged_summary = []
		for i,s in enumerate(t):
			if s in summary:
				indices.append(i)
				sorted_summary.append(s)
				
				if args.keyphrases or args.sentiment:
					tagged_summary.append(tagged[k][i])
		
		seg['summary'] = list2text(sorted_summary)
		
		# get segment polarity
		if args.sentiment:
			# get sentiment per sentence
			scores = []
			for s in tagged[k]:
				lemmas = [w[2] for w in s]
				txt = {} # aggregate of all tags
				
				puncts = sl.getPunctIndex(lemmas)
				for p in puncts:
					txt[p] = {'type':'punct'}
				
				txt = sl.tag_doc(lt, lemmas, sdict, slist, 'sword', txt)
				txt = sl.tag_doc(lt, lemmas, idict, ilist, 'iword', txt)
				txt = sl.tag_doc(lt, lemmas, pdict, plist, 'pword', txt)
				
				scores.append(sl.scoreText(txt))
				
			seg['polarity_score'] = sum(scores)
			seg['polarity'] = sl.num2nom(sum(scores))
			
		
		# extract key phrases
		if args.keyphrases:
			# chunk summary sentences & extract NPs
			chunker = SimpleChunker()
			nps = []
			for s in tagged_summary:
				nps += chunker.get_chunks(s, join=True)
				
			# rank NPs
			ranked = gr.rank_list(nps)
			seg['keyphrases'] = ranked[0:args.knum]

		out.append(seg)
		
	# Print JSON to stdout
	print json.dumps(out)
	



