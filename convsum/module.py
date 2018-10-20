from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str
from typing import Text, List, Dict, Any

from convsum import utils

import logging


class UnsupportedLanguageError(Exception):
    """
    Raised when a module is created, but the language is not supported.
    """

    def __init__(self, module, language):
        self.module = module
        self.language = language
        super(UnsupportedLanguageError, self).__init__(module, language)

    def __str__(self):
        return "module {} does not support language {}".format(self.module, self.language)


class Module(object):

    # Module name
    name = ""

    # Defaults parameters
    defaults = {}

    # List of required attributes: should match 'provides' from the modules upstream the pipeline
    requires = []

    # List of provided attributes: should match 'required' from the modules downstream the pipeline
    provides = []

    # List of languages supported by the module
    languages = []

    def __init__(self, module_config=None):
        if not module_config:
            module_config = {}

        module_config["name"] = self.name
        self.module_config = utils.update_config(self.defaults, module_config)

