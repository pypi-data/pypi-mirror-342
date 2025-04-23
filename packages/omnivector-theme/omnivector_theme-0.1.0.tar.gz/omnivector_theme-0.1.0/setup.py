from pathlib import Path

import setuptools

VERSION = "0.1.0" 

NAME = "omnivector-jupyterhub-theme"



setuptools.setup(
    name=NAME,
    version=VERSION,
    description="Jupyter hub theme.",
    url="https://github.com/omnivector-solutions/jupyterhub-theme",
    project_urls={
        "Source Code": "https://github.com/omnivector-solutions/jupyterhub-theme",
    },
    author="Omnivector",
    author_email="bruno@vantagecompute.ai",
    license="Apache License 2.0",
)