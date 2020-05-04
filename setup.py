try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("requirements.txt") as f:
    requirements = f.read().strip().split("\n")


setup(name="edn_format",
      version="0.7.2",
      author="Swaroop C H",
      author_email="swaroop@swaroopch.com",
      description="EDN format reader and writer in Python",
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url="https://github.com/swaroopch/edn_format",
      install_requires=requirements,
      license="Apache 2.0",
      packages=['edn_format'],
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Software Development',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
      ])
