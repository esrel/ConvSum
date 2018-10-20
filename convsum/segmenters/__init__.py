from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str
from typing import Text, List, Dict, Any

import logging


class Segmenter(object):
    """
    Topic, etc. segmentation class template
    """
    name = None
    languages = []
    requires = []
    provides = []
    defaults = []

    def segment(self, text):
        raise NotImplementedError("Segmenter needs 'segment' method.")