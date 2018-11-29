# Bibtex2html

This program reads a BibTeX file and converts it to a list of references in
HTML format.

To use this program you need Python and Python's bibtexparser installed on your computer.

## File description

* `bibtex2html.py`: the bibtex2html program.
* `example.bib`: example of BibTeX file.
* `template.html`: example of template file.

## Usage

To run the program, in a command-line interface enter the command

    python bibtex2html.py bibtex.bib template.html output.html

Here, `bibtex.bib` is the BibTeX file that you want to convert, and
`template.html` is any template file containing the following placeholders:

    <!--NUM_OF_REFERENCES-->
    <!--NEWER-->
    <!--OLDER-->
    <!--DATE-->
    <!--LIST_OF_REFERENCES-->
    <!--LIST_OF_REFERENCES_NOYEAR-->

These placeholders will be replaced by the program, and the result will be
written to the file `output.html`.

## License

Copyright (C) 2009-2018 Gustavo de Oliveira. Licensed under the GPLv2 (see the [license](LICENSE.txt) file).

Copyright (C) 2018 Simon Reich. Licensed under the GPLv2 (see the [license](LICENSE.txt) file).
