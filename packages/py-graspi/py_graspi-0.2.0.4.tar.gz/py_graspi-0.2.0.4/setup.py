from setuptools import setup, find_packages

setup(
    name="py_graspi",
    author="Olga Wodo",
    author_email="olgawodo@buffalo.edu",
    version="0.2.0.4",
    description="Graph-based descriptor extraction tool for microstructures",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=["Programming Language :: Python"],
    url="https://github.com/owodolab/py-graspi",
    download_url='https://github.com/owodolab/py-graspi/archive/refs/tags/v_2.0.31.tar.gz',
    # need to get this link from the GitHub repo "Releases" section
    install_requires=[
        "igraph",
        "matplotlib",
        "numpy",
        "contourpy",
        "cycler",
        "fonttools",
        "kiwisolver",
        "packaging",
        "pillow",
        "psutil",
        "pyparsing",
        "python-dateutil",
        "six",
        "texttable",
        "fpdf",
    ],
    python_requires=">=3.7"

)
