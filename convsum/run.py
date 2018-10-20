from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str
from typing import Text, List, Dict, Any

import json
import spacy

import logging
import argparse

from convsum.utils import configure_colored_logging,add_logging_arguments

logger = logging.getLogger(__name__)


class ConversationSummarizer:

    abs_domains = ['shopping']
    pipe_config = {
        "language": "en",
        "nlp": "spacy",
        "topic_segmentation": "nltk",
        "topic_classification": None,

    }

    def __init__(self, config_file=None):
        """
        :param language:
        """
        #self.pipe_config.update(json.load(open(config_file)))

    def summarize(self, conversation):
        """
        Summarize conversation
        :param conversation:
        :return:
        """
        # Parse conversation format
        # {"ID": 00, "speakers": [], "turns": [{"start": 0, "end":0, "text": "", "speaker": ""}]}
        logger.info("NLP ...")

        # NLP: tokenization, lemmatization, chunking, POS-tagging, NER, etc.


        # Topic Segmentation: Segment conversation into topics
        logger.info("Topic Segmentation: ... ")
        topics = []
        #
        logger.info("Topic Segmentation: found {} topics".format(len(topics)))

        # Topic Classification: Classify topical segments into domains
        logger.info("Topic Classification ...")
        # Summarize topical segments w.r.t. domain
        for t in topics:
            domain = t.get('domain')
            if domain in self.abs_domains:
                # abstractive summarization
                pass
            else:
                # extractive summarization
                pass


def create_argument_parser():
    parser = argparse.ArgumentParser(description='Lexicon Tagger')
    #parser.add_argument('-l', '--lexicon', type=str)
    #parser.add_argument('-d', '--data',    type=str)
    utils.add_logging_arguments(parser, default=logging.INFO)
    return parser


if __name__ == "__main__":
    parser = create_argument_parser()
    args = parser.parse_args()

    utils.configure_colored_logging(args.loglevel)

    nlp = spacy.load('en')

    txt = "Mexico has agreed that 75% of its automotive content will be manufactured within the trade bloc " \
          "(which for now just includes itself and the US but could include Canada if another deal is reached). " \
          "That's up from the current 62.5% and that potentially means more business for small- and medium-sized " \
          "parts and equipment manufacturers in the US automotive industry. Mexico has also agreed that 40 to 45% " \
          "of the automobile content produced will be done so by workers making at least $16 an hour. " \
          "That's also good news for small businesses in the US, particularly those that are already paying in " \
          "excess of this minimum wage and that are losing business from cheaper producers south of the border."
    doc = nlp(txt)

    #print(doc.print_tree())
    print(doc.sentiment, doc.cats)

    for s in doc.sents:
        print(s)

    print(doc)

    summarizer = ConversationSummarizer()
    summarizer.summarize(txt)