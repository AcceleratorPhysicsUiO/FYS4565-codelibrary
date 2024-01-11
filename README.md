# README for the FYS4565 code library

This folder contains several Python3 modules and Jupyter notebook examples.

## Generating code documentation

The code library is documented using Sphinx. This is contained in the `docs` subfolder.

To update the docs, enter the `docs` folder and run e.g. `make html` or `make latex` or `make singlehtml`.
The updated documentation will appear in `docs/build/html` or `docs/build/latex` or `docs/build/singlehtml.
The generate a PDF from LaTeX, please run `make` inside the `docs/build/latex`.

The Sphinx installation is controlled by `docs/source/conf.py` and `docs/source/index.rst`.

Sphinx was initially initialized by `sphinx-quickstart -q -p "FYS4565 code library" -a "Kyrre Sjobak & Erik Adli" --no-batchfile --ext-autodoc  --sep .` inside the docs folder.
I found the blog posts https://eikonomega.medium.com/getting-started-with-sphinx-autodoc-part-1-2cebbbca5365 and https://brendanhasz.github.io/2019/01/05/sphinx.html to be very helpful.
