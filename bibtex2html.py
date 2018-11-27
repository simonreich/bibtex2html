#! /usr/bin/env python3
# -*- coding: UTF-8 -*-


"""
Copyright (C) 2009-2018 Gustavo de Oliveira. 
Copyright (C) 2018 Simon Reich

Licensed under the GPLv2 (see the license file).

This program reads a BibTeX file and converts it to a list of references in
HTML format.

To use this program you need Python installed on your computer.

To run the program, in a command-line interface enter the command

    python bibtex2html.py bibtex.bib template.html output.html

Here, `bibtex.bib` is the BibTeX file that you want to convert, and
`template.html` is any template file containing the following placeholders:

    <!--NUMBER_OF_REFERENCES-->
    <!--NEWER-->
    <!--OLDER-->
    <!--DATE-->
    <!--LIST_OF_REFERENCES-->

These placeholders will be replaced by the program, and the result will be
written to the file `output.html`.
"""


import sys
from datetime import date
import calendar


def cleanup_author(s):
    """Clean up and format author names.

    cleanup_author(str) -> str
    """

    dictionary = {'\\"a': '&auml;', '\\"A': '&Auml;', '\\"e': '&euml;', 
    '\\"E': '&Euml;', '\\"i': '&iuml;', '\\"I': '&Iuml;', '\\"o': '&ouml;', 
    '\\"O': '&Ouml;', '\\"u': '&uuml;', '\\"U': '&Uuml;', "\\'a": '&aacute;',
    "\\'A": '&Aacute;', "\\'e": '&eacute;', "\\'i": '&iacute;', 
    "\\'I": '&Iacute;', "\\'E": '&Eacute;', "\\'o": '&oacute;', 
    "\\'O": '&Oacute;', "\\'u": '&uacute;', "\\'U": '&Uacute;', 
    '\\~n': '&ntilde;', '\\~N': '&Ntilde;', '\\~a': '&atilde;', 
    '\\~A': '&Atilde;', '\\~o': '&otilde;', '\\~O': '&Otilde;', 
    '.': ' ', "\\'\\": '', '{': '', '}': '', ' And ': ' and '}

    for k, v in dictionary.items():
        s = s.replace(k, v)

    s = s.strip()

    before, sep, after = s.rpartition(' and ')
    before = before.replace(' and ', ', ')
    s = before + sep + after

    return s


def cleanup_title(s):
    """Clean up and format article titles.

    cleanup_title(str) -> str
    """

    s = s.lower()
    s = s.capitalize()

    return s


def cleanup_page(s):
    """Clean up the article page string.

    cleanup_pages(str) -> str
    """

    s = s.replace('--', '-')

    return s



# Get the BibTeX, template, and output file names
bibfile = sys.argv[1]
templatefile = sys.argv[2]
outputfile = sys.argv[3]


# Open, read and close the BivTeX and template files
with open(templatefile, 'r') as f:
    template = f.read()

with open(bibfile, 'r') as f:
    datalist = f.readlines()


# Discard unwanted characteres and commented lines
datalist = [s.strip(' \n\t') for s in datalist]
datalist = [s for s in datalist if s[:2] != '%%']


# Convert a list into a string
data = ''
for s in datalist: data += s


# Split the data at the separators @ and put it in a list
biblist = data.split('@')
# Discard empty strings from the list
biblist = [s for s in biblist if s != '']


# Create a list of lists containing the strings "key = value" of each bibitem
listlist = []
for s in biblist:
    type, sep, s = s.partition('{')
    id, sep, s = s.partition(',')
    s = s.rpartition('}')[0]
    keylist = ['type = ' + type.lower(), 'id = ' + id]

    number = 0
    flag = 0
    i = 0
    while len(s) > 0:
        if s[i] == '{':
            number += 1
            flag = 1
        elif s[i] == '}':
            number -= 1

        if number == 0 and flag == 1:
            keylist.append(s[:i+1])
            s = s[i+1:]
            flag = 0
            i = 0
            continue

        i += 1

    keylist = [t.strip(' ,\t\n') for t in keylist]
    listlist.append(keylist)
 

# Create a list of dicts containing key : value of each bibitem
dictlist = []
for l in listlist:
    keydict = {}
    for s in l:
        key, sep, value = s.partition('=')
        key = key.strip(' ,\n\t{}')
        key = key.lower()
        value = value.strip(' ,\n\t{}')
        keydict[key] = value

    dictlist.append(keydict)


# Backup all the original data
full_dictlist = dictlist


# Keep only articles in the list
#dictlist = [d for d in dictlist if d['type'] == 'article']
# keep only articles that have author and title
dictlist = [d for d in dictlist if 'author' in d and 'title' in d]
dictlist = [d for d in dictlist if d['author'] != '' and d['title'] != '']


# Get a list of the article years and the min and max values
years = [int(d['year']) for d in dictlist if 'year' in d]
years.sort()
older = years[0]
newer = years[-1]


###########################################################################
# Set the fields to be exported to html (following this order)
mandatory = ['author', 'title', 'year']
optional = ['journal', 'eprint', 'volume', 'pages', 'url', 'doi', 'abstract', 'note', 'address', 'annote', 'booktitle', 'chapter', 'crossref', 'edition', 'editor', 'howpublished', 'institution', 'key', 'month', 'number', 'organization', 'publisher', 'school', 'series', 'type']

###########################################################################


# Clean up data
for i in range(len(dictlist)):
    dictlist[i]['author'] = cleanup_author(dictlist[i]['author'])
    dictlist[i]['title'] = cleanup_title(dictlist[i]['title'])


# Write down the list html code
counter = 0
html = ''
html += '\n\n<ul>\n'
for y in reversed(range(older, newer + 1)):
    if y in years:
        #html += '\n<h3 id="y{0}">{0}</h3>\n\n<ul>\n'.format(y)
        for d in dictlist:
            # generate bibtex text
            bibtex = "@" + str(d['type']) + '{' + str(d['id']) + ',<br />'
            for key in sorted(d):
                if (str(key) != 'type') and (str(key) != 'id') and (str(key) != 'file'):
                    value = d[key]
                    bibtex += '&nbsp;&nbsp;' + str(key) + ' = {' + str(value) + '},<br />'
            bibtex += '}'
            if 'year' in d and int(d['year']) == y:
                mandata = [d[key] for key in mandatory]
                html += '<li><b>{1}</b>,<br /> {0} ({2}).<br />'.format(*mandata)

                if d['type'] == 'thesis': html += 'Thesis'
                if d['type'] == 'phdthesis': html += 'Ph.D. Thesis'
                if 'journal' in d: html += 'In {0}'.format(d['journal'])
                if 'eprint' in d: html += 'In {0}'.format(d['eprint'])
                if 'booktitle' in d: html += 'In {0}'.format(d['booktitle'])
                if 'volume' in d: html += '. Volume {0}'.format(d['volume'])
                if 'chapter' in d: html += '. Chapter {0} ch'.format(d['chapter'])
                if 'pages' in d: 
                    a = cleanup_page(d['pages'])
                    if str(d['pages']).isdigit():
                        html += ', p. {0}'.format(a)
                    else:
                        html += ', pp. {0}'.format(a)
                if 'month' in d: 
                    try:
                        month = calendar.month_name[int(d['month'])]
                    except:
                        month = str(d['month']).capitalize()
                    html += ', {0}'.format(month)
                if 'edition' in d: html += '. Edition {0}'.format(d['edition'])
                if 'number' in d: html += '. Number {0}'.format(d['number'])
                if 'editor' in d: html += '. Editor {0}'.format(d['editor'])
                if 'institution' in d: html += '. {0}'.format(d['institution'])
                if 'address' in d: html += '. {0}'.format(d['address'])
                if 'organization' in d: html += '. {0}'.format(d['organization'])
                if 'publisher' in d: html += '. {0}'.format(d['publisher'])
                if 'school' in d: html += '. {0}'.format(d['school'])
                if 'series' in d: html += '. Series {0}'.format(d['series'])
                if 'note' in d: html += ' ({0})'.format(d['note'])
                html += '<br />'
                if 'file' in d: html += '<a href="{0}">[pdf]</a> '.format(d['file'])
                if 'url' in d: html += '<a href="{0}">[url]</a> '.format(d['url'])
                if 'doi' in d: html += '<a href="https://doi.org/{0}">[doi]</a> '.format(d['doi'])
                html += '<br />'
                if 'abstract' in d: html += '<button class="collapsible">[↓ Abstract]</button><div class="content"><p>{0}</p></div>'.format(d['abstract'])
                html += '<button class="collapsible">[↓ BibTeX]</button><div class="content"><p>' + bibtex +'</p></div>'

                html += '</li>\n'
                counter += 1

html += '</ul>\n'


# Fill up the empty fields in the template
a, mark, b = template.partition('<!--LIST_OF_REFERENCES-->')
a = a.replace('<!--NUMBER_OF_REFERENCES-->', str(counter), 1)
a = a.replace('<!--NEWER-->', str(newer), 1)
a = a.replace('<!--OLDER-->', str(older), 1)
now = date.today()
a = a.replace('<!--DATE-->', date.today().strftime('%d %b %Y'))


# Join the header, list and footer html code
final = a + html + b

# Write the final result to the output file
with open(outputfile, 'w', encoding="UTF8") as f:
    f.write(final)
