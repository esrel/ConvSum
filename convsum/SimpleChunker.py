# -*- coding: utf-8 -*-
#!/usr/bin/env python

import nltk
import sys, os
import argparse
reload(sys).setdefaultencoding("utf-8")

class SimpleChunker:
	''' Simple RegEx Chunker '''
	
	grammar = r"""
		NP:	{<DET.*>?<ADJ>*<NOM|NPR>+<ADJ>*(<PRE.*>*<ADJ>*<NOM|NPR>+<ADJ>*)*}
	"""
	
	chunks = ['NP'] # chunks to get
	
	def __init__(self):
		'''constructor'''

	def get_chunks(self, sent, join=False):
		''' Chunk sentence '''
		# convert sentence to NLTK format
		isent   = [(w[0], w[1]) for w in sent]
		chunker = nltk.RegexpParser(self.grammar)
		chtree  = chunker.parse(isent)

		chunks  = []
		for stree in chtree.subtrees():
			if stree.label() in self.chunks:
				if join:
					chunks.append(' '.join([w[0] for w in stree.leaves()]))
				else:
					chunks.append([w[0] for w in stree.leaves()])
		return chunks

#----------------------------------------------------------------------#
if __name__ == "__main__":
	
	'''
	NP chunk a sentence
	'''

	argpar = argparse.ArgumentParser(description='Simple RegEx Chunker')
	argpar.add_argument('-f', '--ifile', type=file)
	args = argpar.parse_args()

	chunker = SimpleChunker()

	if not args.ifile:
		sent = [
			['credo', 'VER:pres', 'credere'], 
			['di', 'PRE', 'di'], 
			['aver', 'VER:infi', 'avere'], 
			['chiarito', 'VER:pper', 'chiarire'], 
			['tutto', 'ADV', 'tutto'], 
			['ha', 'VER:pres', 'avere'], 
			['dichiarato', 'VER:pper', 'dichiarare'], 
			["l'", 'DET:def', 'il'], 
			['ex', 'ADJ', 'ex'], 
			['capo', 'NOM', 'capo'], 
			['della', 'PRE:det', 'del'], 
			['segreteria', 'NOM', 'segreteria'], 
			['politica', 'ADJ', 'politico'], 
			['del', 'PRE:det', 'del'], 
			['campidoglio', 'NOM', 'campidoglio'], 
			['intanto', 'ADV', 'intanto'], 
			["l'", 'DET:def', 'il'], 
			['assessore', 'NOM', 'assessore'], 
			["all'", 'PRE:det', 'al'], 
			['urbanistica', 'NOM', 'urbanistica'], 
			['senza', 'CON', 'senza'], 
			['del', 'PRE:det', 'del'], 
			['campidoglio', 'NOM', 'campidoglio'], 
			['vergine', 'ADJ', 'vergine'], 
			['ha', 'VER:pres', 'avere'], 
			['presentato', 'VER:pper', 'presentare'], 
			['le', 'DET:def', 'il'], 
			['dimissioni', 'NOM', 'dimissione'],
			['e', 'CON', 'e'],
			['del', 'PRE:det', 'del'], 
			['referendum', 'NOM', 'referendum'], 
			['di', 'PRE', 'di'], 
			['giugno', 'NOM', 'giugno'],
			['e', 'CON', 'e'],
			['tribunale', 'NOM', 'tribunale'], 
			['a', 'PRE', 'a'], 
			['Roma', 'NPR', 'Roma'], 
			['fino', 'CON', 'fino'],
		]

		print chunker.get_chunks(sent, join=True)
