# Contributing to edn\_format #

## Setup ##

1. Make sure you have a working Python installation (2 or 3). Use either
   [Virtualenv][], Vagrant, or a similar tool to create an isolated
   environment:
    ```bash
    # 1. One-time: Install Vagrant
    #
    # macOS
    # Install Homebrew from https://brew.sh
    # brew cask install virtualbox vagrant
    #
    # All OSes
    # Install from https://www.vagrantup.com/downloads.html

    # 2. One-time: Install Vagrant plugin
    vagrant plugin install vagrant-vbguest

    # 3. This is all you need
    vagrant up

    # 4. To access the dev environment via ssh
    vagrant ssh
    cd /vagrant
    ```

2. Install `edn_format`’s dependencies: `pip install -r requirements.txt`
3. Install `flake8`: `pip install flake8`

[Virtualenv]: https://virtualenv.pypa.io/en/stable/#virtualenv

## Tests ##

Run unit tests with:

    python tests.py

Check Python warnings with:

    python -Wall -c 'import edn_format'

Run a linter over the code with:

    flake8 --max-line-length=100 --exclude=parsetab.py .

## Release a new version ##

To release a new version:

1. Ensure you have [setup GPG](https://help.github.com/en/articles/generating-a-new-gpg-key) and [`twine`](https://pypi.org/project/twine/)
2. Bump up the version number in `setup.py`, e.g. `0.6.3`
3. Create a git tag: `git tag -s v0.6.3 -m 'Version 0.6.3'` (use [signed tags](https://help.github.com/en/articles/signing-tags))
4. Verify git tag: `git tag -v v0.6.3`
5. Push git tag: `git push origin master --tags`
6. Clean your `dist/` directory if it already exists
7. Package the release: `python setup.py sdist bdist_wheel`
8. Check the package: `twine check dist/*`
9. Upload the package: `twine upload dist/*`
