from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from convsum.segmenters import Segmenter
from convsum.utils import update_config,add_logging_arguments,configure_colored_logging

from nltk.tokenize.texttiling import TextTilingTokenizer

import logging
import argparse

logger = logging.getLogger(__name__)


class TextTilingSegmenter(Segmenter):
    """
    Class for Topic Segmentation using TextTiling
    """
    name = 'TextTilingSegmenter'
    languages = ['en', 'it']
    defaults = {'w': 20, 'k': 10}
    segmenter = None

    def __init__(self, language='en', **kwargs):
        """
        :param language:
        :param kwargs:
        """
        update_config(self.defaults, kwargs)
        self.segmenter = TextTilingTokenizer(w=self.defaults.get('w'), k=self.defaults.get('k'))
        logger.debug('Segmenter parameters: {}'.format(self.defaults))

    def segment(self, text):
        """
        :param text:
        :return:
        """
        if len(text.split()) <= self.defaults.get('w'):
            logger.debug('Text too short: {} tokens'.format(len(text.split())))
            return [text]
        else:
            return self.segmenter.tokenize(text)


def create_argument_parser():
    parser = argparse.ArgumentParser(description='Topic Segmentation using TextTiling')
    parser.add_argument('-d', '--data',     type=str)
    parser.add_argument('-l', '--language', type=str)
    add_logging_arguments(parser)
    return parser


if __name__ == "__main__":
    parser = create_argument_parser()
    args = parser.parse_args()
    configure_colored_logging(args.loglevel)

    segmenter = TextTilingSegmenter(args.language)

    with open(args.data) as fh:
        text = fh.read()
        print(text)
        topics = segmenter.segment(text)
        print(topics)
