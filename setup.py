"""
You don't want to write JavaScript? Me, too. But, Let me handle it with Python.
-----------
Powered by [Yamato Nagata](https://twitter.com/514YJ)

[GitHub](https://github.com/delta114514/JSRope)

"""

from setuptools import setup
from os import path

about = {}
with open("jsrope/__about__.py") as f:
    exec(f.read(), about)

here = path.abspath(path.dirname(__file__))

setup(name=about["__title__"],
      version=about["__version__"],
      url=about["__url__"],
      license=about["__license__"],
      author=about["__author__"],
      author_email=about["__author_email__"],
      description=about["__description__"],
      long_description=__doc__,
      install_requires=["jsbeautifier"],
      packages=["jsrope"],
      zip_safe=False,
      platforms="any",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Other Environment",
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules"
      ])
