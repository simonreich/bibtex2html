# -*- coding: utf-8 -*-
"""
This file is part of bibtex2html.
    bibtex2html is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    bibtex2html is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with bibtex2html.  If not, see <http://www.gnu.org/licenses/>.
"""



import calendar
import bibtexparser



class parser:
    def __init__(self, _filenameBib, _debug=False):
        self.debug = _debug
        self.filenameBib = _filenameBib


    def cleanup_authors(self, _s):
        """Clean up and format author names.
 
        cleanup_authors(str) -> str
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
            _s = _s.replace(k, v)
 
        # split string of authors into single authors
        authors = _s.split('and')
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



    def cleanup_string(self, _s):
        """Clean up and format author names.
 
        cleanup_string(str) -> str
        """
 
        dictionary = {'\\"a': '&auml;', '\\"A': '&Auml;', '\\"e': '&euml;', 
        '\\"E': '&Euml;', '\\"i': '&iuml;', '\\"I': '&Iuml;', '\\"o': '&ouml;', 
        '\\"O': '&Ouml;', '\\"u': '&uuml;', '\\"U': '&Uuml;', "\\'a": '&aacute;',
        "\\'A": '&Aacute;', "\\'e": '&eacute;', "\\'i": '&iacute;', 
        "\\'I": '&Iacute;', "\\'E": '&Eacute;', "\\'o": '&oacute;', 
        "\\'O": '&Oacute;', "\\'u": '&uacute;', "\\'U": '&Uacute;', 
        '\\~n': '&ntilde;', '\\~N': '&Ntilde;', '\\~a': '&atilde;', 
        '\\~A': '&Atilde;', '\\~o': '&otilde;', '\\~O': '&Otilde;', 
        '.': ' ', "\\'\\": '', '{': '', '}': ''}
 
        # replace entry in names from dictionary
        for k, v in dictionary.items():
            _s = _s.replace(k, v)
 
        return _s



    def cleanup_page(self, _s):
        """Clean up the article page string.
 
        cleanup_pages(str) -> str
        """
 
        _s = _s.replace('--', '-')
 
        return _s



    def getBib(self):
        """Loads the bibtex file and creates a dictionary, which can be parsed
 
        getBib() -> dict
        """
        # Open, read and close the BibTeX
        with open(self.filenameBib, 'r') as f:
            datalist = f.read()
        
        bib_database = bibtexparser.loads(datalist)

        # Add to each bib entry a key called 'bibtex'. which holds the raw bibtex code as read from file.
        for bib in bib_database.entries[:]:
            bibtex_dict = bib_database.entries_dict[bib['ID']]
            bibtex = '@' + str(bib['ENTRYTYPE']) + '{' + bib['ID'] + ',\n'
            counter1 = 0
            bibtexDoNotPrint = ['ID', 'ENTRYTYPE', 'file']
            for key, value in sorted(bibtex_dict.items()):
                if str(key) not in bibtexDoNotPrint:
                    bibtex += '' + str(key) + " = {" + str(value) + '}'
                    if counter1 < len(bibtex_dict)-1:
                        bibtex += ',\n'
                    elif counter1 == len(bibtex_dict)-1:
                        bibtex += '\n'
                counter1 += 1
            bibtex += '}'
            bib_database.entries_dict[bib['ID']]['bibtex'] = bibtex

        # This fields will be cleaned up by cleanup_authors
        cleanupAuthors = ['author', 'editor']

        # This fields will be cleaned up by cleanup_string
        cleanupString = ['title', 'year', 'journal', 'eprint', 'volume', 'pages', 'abstract', 'note', 'address', 'annote', 'booktitle', 'chapter', 'crossref', 'edition', 'howpublished', 'institution', 'key', 'month', 'number', 'organization', 'publisher', 'school', 'series', 'type']

        # This fields will be cleanup by cleanup_page
        cleanupPage = ['pages']

        # Cleanup all fields
        for bib in bib_database.entries[:]:
            for field in cleanupAuthors:
                if field in bib:
                    bib[field] = self.cleanup_authors(bib[field])

            for field in cleanupString:
                if field in bib:
                    bib[field] = self.cleanup_string(bib[field])

            for field in cleanupPage:
                if field in bib:
                    bib[field] = self.cleanup_page(bib[field])

        return bib_database

        
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
                        mandata[0] = cleanup_authors(mandata[0])
                        html += '<li><b>{1}</b>,<br /> {0} ({2}).<br />'.format(*mandata)
        
                        if bib['ENTRYTYPE'] == 'thesis': html += 'Thesis'
                        if bib['ENTRYTYPE'] == 'phdthesis': html += 'Ph.D. Thesis'
                        if bib['ENTRYTYPE'] == 'mastersthesis': html += 'Master\'s Thesis'
                        if bib['ENTRYTYPE'] == 'misc' and str(cleanup_string(bib['note'])).lower() == 'bachelor\'s thesis': html += 'Bachelor\'s Thesis'
                        elif bib['ENTRYTYPE'] == 'misc': html += 'Misc'
                        if 'journal' in bib: html += 'In: {0}'.format(cleanup_string(bib['journal']))
                        if 'eprint' in bib: html += 'In: {0}'.format(cleanup_string(bib['eprint']))
                        if 'booktitle' in bib: html += 'In: {0}'.format(cleanup_string(bib['booktitle']))
                        if 'volume' in bib: html += '. Volume {0}'.format(cleanup_string(bib['volume']))
                        if 'chapter' in bib: html += '. Chapter {0} ch'.format(cleanup_string(bib['chapter']))
                        if 'pages' in bib: 
                            a = cleanup_page(cleanup_string(bib['pages']))
                            if str(bib['pages']).isdigit():
                                html += ', p. {0}'.format(a)
                            else:
                                html += ', pp. {0}'.format(a)
                        if 'month' in bib: 
                            try:
                                month = calendar.month_name[int(bib['month'])]
                            except:
                                month = str(cleanup_string(bib['month'])).capitalize()
                            html += ', {0}'.format(month)
                        if 'edition' in bib: html += '. Edition {0}'.format(cleanup_string(bib['edition']))
                        if 'number' in bib: html += '. Number {0}'.format(cleanup_string(bib['number']))
                        if 'editor' in bib: html += '. Editor {0}'.format(cleanup_string(bib['editor']))
                        if 'institution' in bib: html += '. {0}'.format(cleanup_string(bib['institution']))
                        if 'address' in bib: html += '. {0}'.format(cleanup_string(bib['address']))
                        if 'organization' in bib: html += '. {0}'.format(cleanup_string(bib['organization']))
                        if 'publisher' in bib: html += '. {0}'.format(cleanup_string(bib['publisher']))
                        if 'school' in bib: html += '. {0}'.format(cleanup_string(bib['school']))
                        if 'series' in bib: html += '. Series {0}'.format(cleanup_string(bib['series']))
                        if 'note' in bib: html += ' ({0})'.format(cleanup_string(bib['note']))
                        html += '.<br />'
                        if 'file' in bib: html += '<a href="{0}">[pdf]</a> '.format(bib['file'])
                        if 'link' in bib: html += '<a href="{0}">[url]</a> '.format(bib['link'])
                        if 'doi' in bib: html += '<a href="https://doi.org/{0}">[doi]</a> '.format(bib['doi'])
                        html += '<br />'
                        if 'abstract' in bib: html += '<button class="collapsible">[↓ Abstract]</button><div class="content"><p>{0}</p></div>'.format(cleanup_string(bib['abstract']))
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
