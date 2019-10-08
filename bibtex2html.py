#! /usr/bin/env python3
# -*- coding: UTF-8 -*-


"""
Copyright (C) 2009-2018 Gustavo de Oliveira. 
Copyright (C) 2018-2019 Simon Reich

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
from bibtex2parser import bibtex2parser



def main():
    # Get the BibTeX, template, and output file names
    bibfile = sys.argv[1]
    templatefile = sys.argv[2]
    outputfile = sys.argv[3]
    
    # Open, read and close the template file
    with open(templatefile, 'r') as f:
        template = f.read()

    # Load parser
    cParser = bibtex2parser.parser(bibfile)
    bibDatabase = cParser.getBib()
        
    # Set the fields to be exported (following this order)
    mandatory = ['author', 'title', 'year']
    optional = ['journal', 'eprint', 'volume', 'pages', 'url', 'doi', 'abstract', 'note', 'address', 'annote', 'booktitle', 'chapter', 'crossref', 'edition', 'editor', 'howpublished', 'institution', 'key', 'month', 'number', 'organization', 'publisher', 'school', 'series', 'type']
    
    # Get a list of the article years and the min and max values
    years = []
    for bib in bibDatabase.entries[:]:
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
            for bib in bibDatabase.entries[:]:
                html = ''

                # generate html
                if 'year' in bib and int(bib['year']) == y:
                    mandata = [bib[key] for key in mandatory]
                    mandata[0] = mandata[0]
                    html += '<li><b>{1}</b>,<br /> {0} ({2}).<br />'.format(*mandata)
    
                    if bib['ENTRYTYPE'] == 'thesis': html += 'Thesis'
                    if bib['ENTRYTYPE'] == 'phdthesis': html += 'Ph.D. Thesis'
                    if bib['ENTRYTYPE'] == 'mastersthesis': html += 'Master\'s Thesis'
                    if bib['ENTRYTYPE'] == 'misc' and str(bib['note']).lower() == 'bachelor\'s thesis': html += 'Bachelor\'s Thesis'
                    elif bib['ENTRYTYPE'] == 'misc': html += 'Misc'
                    if 'journal' in bib: html += 'In: {0}'.format(bib['journal'])
                    if 'eprint' in bib: html += 'In: {0}'.format(bib['eprint'])
                    if 'booktitle' in bib: html += 'In: {0}'.format(bib['booktitle'])
                    if 'volume' in bib: html += '. Volume {0}'.format(bib['volume'])
                    if 'chapter' in bib: html += '. Chapter {0} ch'.format(bib['chapter'])
                    if 'pages' in bib: 
                        fieldPages = bib['pages']
                        if str(bib['pages']).isdigit():
                            html += ', p. {0}'.format(fieldPages)
                        else:
                            html += ', pp. {0}'.format(fieldPages)
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
                    html += '.<br />'
                    if 'file' in bib: html += '<a href="{0}">[pdf]</a> '.format(bib['file'])
                    if 'link' in bib: html += '<a href="{0}">[url]</a> '.format(bib['link'])
                    if 'doi' in bib: html += '<a href="https://doi.org/{0}">[doi]</a> '.format(bib['doi'])
                    html += '<br />'
                    if 'abstract' in bib: html += '<button class="collapsible">[↓ Abstract]</button><div class="content"><p>{0}</p></div>'.format(bib['abstract'])
                    # generate bibtex text
                    fieldBibtex = bib['bibtex']
                    count = fieldBibtex.count('\n') - 1
                    fieldBibtex = fieldBibtex.replace('\n', '<br />\n&nbsp;&nbsp;', count)
                    count = fieldBibtex.rfind('\n')
                    fieldBibtex = fieldBibtex[:count] + '\n<br />' + fieldBibtex[count+1:]
                    html += '<button class="collapsible">[↓ BibTeX]</button><div class="content"><p>' + fieldBibtex +'</p></div>'
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



if __name__ == '__main__':
    # execute only if run as a script
    main()
