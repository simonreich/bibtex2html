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
import bibtexparser


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

    # replace entry in names from dictionary
    for k, v in dictionary.items():
        s = s.replace(k, v)

    # split string of authors into single authors
    authors = s.split('and')
    ret = ""
    counter = 0
    for author in authors:
        names = []
        # split author into first and second name
        if author.find(','):
            names = author.split(',')
            names.reverse()
        else:
            names = author.split()
        # this takes care of middle names
        names1 = []
        for name in names:
            t = name.split()
            names1.extend(t)
        names = names1

        # add a dot, if only intial char of name
        counter1 = 0
        for name in names:
            name = name.strip()
            if len(name) == 1:
                name += '.'
            names[counter1] = name
            counter1 += 1

        # join to single name
        author = ' '.join(names)

        # either add ',' or ', and' between names
        ret += author
        if counter < len(authors)-2:
            ret += ', '
        elif counter < len(authors)-1:
            ret += ', and '

        counter += 1

    return ret


def cleanup_page(s):
    """Clean up the article page string.

    cleanup_pages(str) -> str
    """

    s = s.replace('--', '-')

    return s


if __name__ == '__main__':
    # Get the BibTeX, template, and output file names
    bibfile = sys.argv[1]
    templatefile = sys.argv[2]
    outputfile = sys.argv[3]
    
    
    # Open, read and close the BivTeX and template files
    with open(templatefile, 'r') as f:
        template = f.read()
    
    with open(bibfile, 'r') as f:
        datalist = f.read()
    
    bib_database = bibtexparser.loads(datalist)
    

    # Set the fields to be exported to html (following this order)
    mandatory = ['author', 'title', 'year']
    optional = ['journal', 'eprint', 'volume', 'pages', 'url', 'doi', 'abstract', 'note', 'address', 'annote', 'booktitle', 'chapter', 'crossref', 'edition', 'editor', 'howpublished', 'institution', 'key', 'month', 'number', 'organization', 'publisher', 'school', 'series', 'type']
    
    
    # Get a list of the article years and the min and max values
    years = []
    for bib in bib_database.entries[:]:
        years.append(int(bib['year']))
    years.sort()
    older = years[0]
    newer = years[-1]
    
    
    # Write down the list html code
    counter = 0
    htmlYear = '\n\n<ul>'
    htmlNoYear = '\n\n<ul>'

    for y in reversed(range(older, newer + 1)):
        if y in years:
            htmlYear += '\n\n<h3 id="publications-year-{0}">{0}</h3>\n\n<ul>\n'.format(y)
            for bib in bib_database.entries[:]:
                html = ''

                # generate html
                if 'year' in bib and int(bib['year']) == y:
                    mandata = [bib[key] for key in mandatory]
                    mandata[0] = cleanup_author(mandata[0])
                    html += '<li><b>{1}</b>,<br /> {0} ({2}).<br />'.format(*mandata)
    
                    if bib['ENTRYTYPE'] == 'thesis': html += 'Thesis'
                    if bib['ENTRYTYPE'] == 'phdthesis': html += 'Ph.D. Thesis'
                    if bib['ENTRYTYPE'] == 'mastersthesis': html += 'Master\'s Thesis'
                    if bib['ENTRYTYPE'] == 'misc' and str(bib['note']).lower() == 'bachelor\'s thesis': html += 'Bachelor\'s Thesis'
                    elif bib['ENTRYTYPE'] == 'misc': html += 'Misc'
                    if 'journal' in bib: html += 'In {0}'.format(bib['journal'])
                    if 'eprint' in bib: html += 'In {0}'.format(bib['eprint'])
                    if 'booktitle' in bib: html += 'In {0}'.format(bib['booktitle'])
                    if 'volume' in bib: html += '. Volume {0}'.format(bib['volume'])
                    if 'chapter' in bib: html += '. Chapter {0} ch'.format(bib['chapter'])
                    if 'pages' in bib: 
                        a = cleanup_page(bib['pages'])
                        if str(bib['pages']).isdigit():
                            html += ', p. {0}'.format(a)
                        else:
                            html += ', pp. {0}'.format(a)
                    if 'month' in bib: 
                        try:
                            month = calendar.month_name[int(bib['month'])]
                        except:
                            month = str(bib['month']).capitalize()
                        html += ', {0}'.format(month)
                    if 'edition' in bib: html += '. Edition {0}'.format(bib['edition'])
                    if 'number' in bib: html += '. Number {0}'.format(bib['number'])
                    if 'editor' in bib: html += '. Editor {0}'.format(bib['editor'])
                    if 'institution' in bib: html += '. {0}'.format(bib['institution'])
                    if 'address' in bib: html += '. {0}'.format(bib['address'])
                    if 'organization' in bib: html += '. {0}'.format(bib['organization'])
                    if 'publisher' in bib: html += '. {0}'.format(bib['publisher'])
                    if 'school' in bib: html += '. {0}'.format(bib['school'])
                    if 'series' in bib: html += '. Series {0}'.format(bib['series'])
                    if 'note' in bib: html += ' ({0})'.format(bib['note'])
                    html += '<br />'
                    if 'file' in bib: html += '<a href="{0}">[pdf]</a> '.format(bib['file'])
                    if 'url' in bib: html += '<a href="{0}">[url]</a> '.format(bib['url'])
                    if 'doi' in bib: html += '<a href="https://doi.org/{0}">[doi]</a> '.format(bib['doi'])
                    html += '<br />'
                    if 'abstract' in bib: html += '<button class="collapsible">[↓ Abstract]</button><div class="content"><p>{0}</p></div>'.format(bib['abstract'])
                    # generate bibtex text
                    bibtex_dict = bib_database.entries_dict[bib['ID']]
                    bibtex = '@' + str(bib['ENTRYTYPE']) + '{' + bib['ID'] + ',<br />\n'
                    counter1 = 0
                    bibtexDoNotPrint = ['ID', 'ENTRYTYPE', 'file']
                    for key, value in sorted(bibtex_dict.items()):
                        if str(key) not in bibtexDoNotPrint:
                            bibtex += '&nbsp;&nbsp;' + str(key) + " = {" + str(value) + '}'
                            if counter1 < len(bibtex_dict)-1:
                                bibtex += ',<br />\n'
                            elif counter1 == len(bibtex_dict)-1:
                                bibtex += '<br />\n'
                        counter1 += 1
                    bibtex += '}'

                    html += '<button class="collapsible">[↓ BibTeX]</button><div class="content"><p>' + bibtex +'</p></div>'
                    html += '</li><br />\n'

                    htmlYear += html + '\n'
                    htmlNoYear += html + '\n'

                    counter += 1
    
            htmlYear += '</ul>\n'
    htmlNoYear += '</ul>\n'
    
    
    # Fill up the empty fields in the template
    template = template.replace('<!--LIST_OF_REFERENCES-->', htmlYear)
    template = template.replace('<!--LIST_OF_REFERENCES_NOYEAR-->', htmlNoYear)
    template = template.replace('<!--NUM_OF_REFERENCES-->', str(counter))
    template = template.replace('<!--NEWER-->', str(newer))
    template = template.replace('<!--OLDER-->', str(older))
    now = date.today()
    template = template.replace('<!--DATE-->', date.today().strftime('%d %b %Y'))
    
    # Write the final result to the output file
    with open(outputfile, 'w', encoding="UTF8") as f:
        f.write(template)
