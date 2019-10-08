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

    python bibtex2md.py bibtex.bib outputFolder

Here, `bibtex.bib` is the BibTeX file that you want to convert.

These placeholders will be replaced by the program, and the result will be
written to files in `outputFolder`.
"""



import sys
from datetime import date
import calendar
from bibtex2parser import bibtex2parser



def main():
    # Get the BibTeX, template, and output file names
    bibfile = sys.argv[1]
    folderOut = sys.argv[2]

    # Load parser
    cParser = bibtex2parser.parser(bibfile)
    bibDatabase = cParser.getBib()
        
    # Set the fields to be exported
    fieldMandatory = ['author', 'title', 'year', 'journal', 'eprint', 'volume', 'pages', 'url', 'doi', 'abstract', 'note', 'address', 'annote', 'booktitle', 'chapter', 'crossref', 'edition', 'editor', 'howpublished', 'institution', 'key', 'month', 'number', 'organization', 'publisher', 'school', 'series', 'type', 'id', 'entrytype', 'bibtex']
    fieldMandatory = sorted(fieldMandatory)

    # Parse database
    for bib in bibDatabase.entries[:]:
        md = '---\n'

        # generate md
        for field in fieldMandatory:
            if field in bib:
                if field == 'bibtex':
                    # generate bibtex html text
                    fieldBibtex = bib['bibtex']
                    count = fieldBibtex.count('\n') - 1
                    fieldBibtex = fieldBibtex.replace('\n', '<br />\n&nbsp;&nbsp;', count)
                    count = fieldBibtex.rfind('\n')
                    fieldBibtex = fieldBibtex[:count] + '\n<br />' + fieldBibtex[count+1:]
                    md += field.lower() + ': \'' + str(fieldBibtex) + '\'\n'
                elif field == 'pages':
                    fieldPages = bib['pages']
                    if str(bib['pages']).isdigit():
                        md += field.lower() + ': \'p. ' + str(fieldPages) + '\'\n'
                    else:
                        md += field.lower() + ': \'pp. ' + str(fieldPages) + '\'\n'
                elif field == 'month':
                    try:
                        month = calendar.month_name[int(bib['month'])]
                    except:
                        month = str(bib['month']).capitalize()
                    md += field.lower() + ': ' + str(month) + '\'\n'
                else:
                    md += field.lower() + ': \'' + bib[field] + '\'\n'
        md += '---\n'

        # generate filename
        filenameOut = folderOut + '/' + bib['ID'] + '.md'
    
        # Write the final result to the output file
        with open(filenameOut, 'w', encoding="UTF8") as f:
            f.write(md)



if __name__ == '__main__':
    # execute only if run as a script
    main()
