
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name="edn_format",
      version="0.5.3",
      author="Swaroop C H",
      author_email="swaroop@swaroopch.com",
      description="EDN format reader and writer in Python",
      long_description=open('README.md').read(),
      url="https://github.com/swaroopch/edn_format",
      install_requires=[
          "pytz==2013.9",
          "pyRFC3339==0.2",
          "ply==3.4",
      ],
      license="Apache 2.0",
      packages=['edn_format'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Software Development',
          'Programming Language :: Python',
          'Operating System :: OS Independent',
      ])
