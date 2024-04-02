# README for the FYS4565 code library

This folder contains several Python3 modules and Jupyter notebook examples.
The modules are in the `FYS4565_codelibrary` subfolder, and the examples are in the `examples` subfolder.
The `docs` subfolder contains the tools to generate the code documentation, discussed below.

## Installation

To use, install with `pip` using:
```
pip install --user git+https://github.com/AcceleratorPhysicsUiO/FYS4565_codelibrary.git
```
You can later remove (or remove before re-installing in order to get a newer version) by
```
pip uninstall FYS4565_codelibrary
```

Alternatively, you can copy the `FYS4565_codelibrary` sub-folder from this repository into your project (the folder with content, not just the contents).

After installing, you can use the library by importing its modules, i.e.
`from FYS4565_codelibrary import Util`

## Sphinx code documentation

For documentation of the modules and their functions/classes, please see: https://acceleratorphysicsuio.github.io/FYS4565_codelibrary/

### Manually generating code documentation

The code library is documented using Sphinx. The configuration for this is contained in the `docs` subfolder.
Note that the code documentation is automatically generated at every commit to the `main` branch and published to the above mentioned github pages website.

To manually update the docs locally, enter the `docs` folder and run e.g. `make html` or `make latex` or `make singlehtml`.
The updated documentation will appear in `docs/build/html` or `docs/build/latex` or `docs/build/singlehtml.
The generate a PDF from LaTeX, please run `make` inside the `docs/build/latex`.

The Sphinx installation is controlled by `docs/source/conf.py` and `docs/source/index.rst`.

Sphinx was initially initialized by `sphinx-quickstart -q -p "FYS4565 code library" -a "Kyrre Sjobak & Erik Adli" --no-batchfile --ext-autodoc  --sep .` inside the docs folder.
I found the blog posts https://eikonomega.medium.com/getting-started-with-sphinx-autodoc-part-1-2cebbbca5365 and https://brendanhasz.github.io/2019/01/05/sphinx.html to be very helpful.
