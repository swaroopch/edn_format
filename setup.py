
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name="edn_format",
<<<<<<< HEAD
      version="0.5.13",
=======
      version="0.5.10",
>>>>>>> 5dfb4eb53ca57d4bf354232cacd2ebe90179844c
      author="Swaroop C H",
      author_email="swaroop@swaroopch.com",
      description="EDN format reader and writer in Python",
      long_description=open('README.md').read(),
      url="https://github.com/swaroopch/edn_format",
      install_requires=[
<<<<<<< HEAD
          "pytz==2016.10",
          "pyRFC3339==0.2",
          "ply==3.10",
=======
          "pytz==2015.4",
          "pyRFC3339==1.0",
          "ply==3.6",
          "pytest",
          "pytest-xdist"
>>>>>>> 5dfb4eb53ca57d4bf354232cacd2ebe90179844c
      ],
      license="Apache 2.0",
      packages=['edn_format'],
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Software Development',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
      ])
