#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# Graph-based Ranker
# Based on TextRank

import itertools
import networkx as nx

from operator import itemgetter

import argparse
import sys, os
reload(sys).setdefaultencoding("utf-8")

class GraphRank:
	''' Rank list w.r.t. similarity/distance using graph '''
	
	def __init__(self, metric='levenshtein'):
		''' Constructor '''
		self.metric = metric
		
	def get_metric(self, n1, n2):
		''' compute required metric between 2 nodes '''
		if self.metric == 'levenshtein':
			return self.levenshtein(n1, n2)
		
	def levenshtein(self, str1, str2):
		"compute the Levenshtein distance between two string"
		if len(str1) > len(str2):
			str1, str2 = str2, str1
		dists = range(len(str1) + 1)
		for ind2, ch2 in enumerate(str2):
			newdists = [ind2 + 1]
			for ind1, ch1 in enumerate(str1):
				if ch1 == ch2:
					newdists.append(dists[ind1])
				else:
					newdists.append(1 + min((dists[ind1], dists[ind1+1], newdists[-1])))
			dists = newdists
		return dists[-1]
		
	def unique_list(self, ilist):
		''' List unique elements, preserving order '''
	
		seen = set()
		for e in ilist:
			if e not in seen:
				seen.add(e)
		return seen
		
	def build_graph(self, nodes):
		''' Build a graph from list of nodes '''
		
		# initialize an undirected graph
		gr = nx.Graph() 
		gr.add_nodes_from(nodes)
		
		# generate node pairs
		npairs = list(itertools.combinations(nodes, 2))
		
		#add edges to the graph (weighted by self.get_metric)
		for pair in npairs:
			(n1, n2) = pair
			val = self.get_metric(n1, n2)
			gr.add_edge(n1, n2, weight=val)

		return gr
		
	def rank_list(self, ilist):
		''' rank items in the list '''
		# get unique list
		ulist = list(self.unique_list(ilist))
		# build graph
		graph = self.build_graph(ulist)
		# rank using Page Rank
		ranks = nx.pagerank(graph, weight='weight')
		# sort by rank
		slist = sorted(ranks, key=ranks.get, reverse=True)
		
		return slist
