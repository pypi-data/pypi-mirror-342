# -*- coding: utf-8 -*-

"""Tuning parameter needed because Cytoscape occasionally returns before it's done with an operation
"""

"""Copyright 2020-2022 The Cytoscape Consortium

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the 
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit 
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the 
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# print(f'Starting {__name__} module')

from os import environ

CATCHUP_FILTER_SECS = int(environ.get('PY4CYTOSCAPE_CATCHUP_FILTER_SECS', '0')) # '1'
MODEL_PROPAGATION_SECS = int(environ.get('PY4CYTOSCAPE_MODEL_PROPAGATION_SECS', '2'))
CATCHUP_NETWORK_SECS = int(environ.get('PY4CYTOSCAPE_CATCHUP_NETWORK_SECS', '4')) # How long to sleep between network operation retries
CATCHUP_NETWORK_TIMEOUT_SECS = int(environ.get('PY4CYTOSCAPE_CATCHUP_NETWORK_TIMEOUT_SECS', '60')) # How long to keep retrying network operation
CATCHUP_NETWORK_MERGE_SECS = int(environ.get('PY4CYTOSCAPE_CATCHUP_NETWORK_MERGE_SECS', '1')) # How long to sleep waiting for merge to complete Network table

def set_catchup_filter_secs(delay_secs):
    global CATCHUP_FILTER_SECS
    CATCHUP_FILTER_SECS = delay_secs

def set_model_propagation_secs(delay_secs):
    global MODEL_PROPAGATION_SECS
    MODEL_PROPAGATION_SECS = delay_secs

def set_catchup_network_secs(delay_secs):
    global CATCHUP_NETWORK_SECS
    CATCHUP_NETWORK_SECS = delay_secs

def set_catchup_network_timeout_secs(delay_secs):
    global CATCHUP_NETWORK_TIMEOUT_SECS
    CATCHUP_NETWORK_TIMEOUT_SECS = delay_secs

def set_catchup_network_merge_secs(delay_secs):
    global CATCHUP_NETWORK_MERGE_SECS
    CATCHUP_NETWORK_MERGE_SECS = delay_secs


