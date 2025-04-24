"""cubicweb-spacyquery application packaging information"""

modname = "cubicweb_spacyquery"
distname = "cubicweb-spacyquery"

numversion = (0, 1, 3)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "Helpers for generating RQL query with spacy"
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/spacyquery"

__depends__ = {
    "cubicweb": ">= 4.9.1, < 5.0.0",
    "cubicweb-web": "> 1.3.3, < 2.0.0",
    "networkx": ">= 3.4.2, < 4.0.0",
    "pandas": ">= 2.2.3, < 3.0.0",
    "spacy": ">= 3.8.5, < 4.0.0",
    "spacy_download": ">=1.1.0, <2.0.0",
    "polib": ">= 1.2.0, < 2.0.0",
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python :: 3",
    "Programming Language :: JavaScript",
]
