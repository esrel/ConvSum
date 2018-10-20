#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# Wrapper for TreeTagger

from subprocess import Popen, PIPE
import argparse
import sys, os
reload(sys).setdefaultencoding("utf-8")

class TreeTagger:
	''' TreeTagger Wrapper '''
	
	def __init__(self, tbin, tmod, lemma=False, teos='<eos>'):
		"Set paths & vars"
		if lemma:
			#self.cmd = tbin + " -token -lemma -no-unknown -eos-tag '" + teos + "' " + tmod
			self.cmd = [tbin, '-token', '-lemma', '-no-unknown', '-eos-tag', teos, tmod]
		else:
			#self.cmd = tbin + " -token -eos-tag '" + teos + "' " + tmod
			self.cmd = [tbin, '-token', '-eos-tag', teos, tmod]
		
		self.eos = teos
		
	def list2text(self, sents):
		"convert list of list into token per line format"
		txt = ""
		for s in sents:
			txt += "\n".join(s)
			txt += "\n" + self.eos + "\n"
			
		return txt
		
	def text2list(self, text):
		"convert token-per-line text to list of lists"
		lst  = []
		sent = []
		for line in text.split("\n"):
			if line.strip() != self.eos:
				sent.append(line.strip().split())
			else:
				lst.append(sent)
				sent = []
			
		return lst

	def tag(self, sents):
		"tag a list of sentences (list of words)"
		txt = self.list2text(sents)
		p = Popen(self.cmd, shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
		(stdout, stderr) = p.communicate(txt)
		
		return self.text2list(stdout)
		

#----------------------------------------------------------------------#
if __name__ == "__main__":
	
	''' TreeTagger'''

	argpar = argparse.ArgumentParser(description='TreeTagger')
	argpar.add_argument('-f', '--ifile', type=file)
	argpar.add_argument('-b', '--tbin',  type=str)
	argpar.add_argument('-m', '--tmod',  type=str)
	argpar.add_argument('-e', '--teos',  type=str,  default='<eos>')
	argpar.add_argument('--lemma', action='store_true', help='output lemma')
	args = argpar.parse_args()

	tt = TreeTagger(args.tbin, args.tmod, args.lemma, args.teos)

	text = args.ifile.read()
	toks = [sent.split() for sent in text.split("\n")]
	print tt.tag(toks)

	
