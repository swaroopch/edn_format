
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name="edn_format",
      version="0.5.1",
      author="Swaroop C H",
      author_email="swaroop@swaroopch.com",
      description="EDN format reader and writer in Python",
      long_description=open('README.txt').read(),
      url="https://github.com/swaroopch/edn_format",
      install_requires=[
          "pytz==2012h",
          "pyRFC3339==0.1",
          "ply==3.4",
      ],
      license="LICENSE.txt",
      packages=['edn_format'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Software Development',
          'Programming Language :: Python',
          'Operating System :: OS Independent',
      ])
