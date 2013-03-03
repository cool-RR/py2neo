#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2011-2013, Nigel Small
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__    = "Nigel Small <nasmall@gmail.com>"
__copyright__ = "2011-2013, Nigel Small"
__license__   = "Apache License, Version 2.0"
__package__   = "py2neo"
__version__   = "1.5-alpha"


def node(**properties):
    """ Return a new abstract node.
    """
    return neo4j.Node.abstract(**properties)


def rel(start_node, type, end_node, **properties):
    """ Return a new abstract relationship.
    """
    return neo4j.Relationship.abstract(start_node, type, end_node, **properties)


from . import neo4j
