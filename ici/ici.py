#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import re
import sys
import urllib2
import getopt
import logging
from xml.dom import minidom
from collections import namedtuple


KEY = 'E0F0D336AF47D3797C68372A869BDBC5'
URL = 'http://dict-co.iciba.com/api/dictionary.php'
TAG = namedtuple('TAG', ['value', 'color', 'newline'], verbose=False, rename=False)
TAG_DICT = {
    'ps': TAG('[%s]', 'green', False),
    'fy': TAG('%s', 'green', False),
    'orig': TAG('%s', 'red', False),
    'trans': TAG('%s', 'white', True),
    'pos': TAG('%s'.ljust(12), 'red', False),
    'acceptation': TAG('%s', 'white', True)
}


logger = logging.getLogger(__name__)


def get_response(words):
    try:
        response = urllib2.urlopen(URL + '?key=' + KEY + '&w=' + words)
    except urllib2.URLError:
        logger.error('哎哟,好像出错了')
        return
    return response


def read_xml(xml):
    dom = minidom.parse(xml)
    return dom.documentElement

from termcolor import colored

ex_count = 0

def show(node):
    global ex_count
    if not node.hasChildNodes():
        if node.nodeType == node.TEXT_NODE and node.data != '\n':
            tag_name = node.parentNode.tagName
            content = node.data.replace('\n', '')
            if tag_name in TAG_DICT.keys():
                tag = TAG_DICT[tag_name]
                if tag_name == 'orig':
                    ex_count = ex_count+1
                    print colored(str(ex_count)+'. ', 'yellow'),
                    print_tag(tag, content)
                else:
                    print_tag(tag, content)
    else:
        for e in node.childNodes:
            show(e)

def print_tag(tag, content):
    if not sys.platform == 'win32':
        if tag.newline:
            print colored(tag.value % content, tag.color)
        else:
            print colored(tag.value % content, tag.color) ,
    else:
        try:
            print(tag.value.decode('ascii') % content)
        except UnicodeEncodeError as e:
            pass


def main():
    try:
        options, args = getopt.getopt(sys.argv[1:], ["help"])
    except getopt.GetoptError as e:
        pass

    match = re.findall(r'[\w.]+', " ".join(args).lower())
    words = "_".join(match)
    response = get_response(words)
    if not response:
        return
    root = read_xml(response)
    show(root)


if __name__ == '__main__':
    main()
