# pylint: disable-msg=W0622
"""cubicweb-fresh application packaging information"""

modname = "fresh"
distname = "cubicweb-fresh"

numversion = (1, 11, 1)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "Logilab"
author_email = "contact@logilab.fr"
description = "expense tracking application built on the CubicWeb framework"
web = "http://www.cubicweb.org/project/%s" % distname
classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]

__depends__ = {
    "cubicweb[s3]": ">=4.10.0,<5.0.0",
    "cubicweb-api": ">=0.16.1,<0.17.0",
    "cubicweb-expense": ">=1.0.0,<2.0.0",
    "cubicweb-workcase": ">=1.0.0,<2.0.0",
    "cubicweb-searchui": ">=1.0.0,<2.0.0",
    "cubicweb-prometheus": ">=0.5.0,<0.6.0",
    "cubicweb-signedrequest": ">=3.2.2,<4.0.0",
    "cubicweb-sentry": ">=1.0.0,<2.0.0",
    "cubicweb-card": ">=2.0.0,<3.0.0",
    "cubicweb-oauth2": ">=1.0.0,<2.0.0",
    "cubicweb-web": ">=1.0.0,<2.0.0",
    "reportlab": ">=3.6.0,<3.7.0",
    "cwclientlib": ">=1.3.0,<1.4.0",
}
