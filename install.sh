#!/usr/bin/env bash

# Set working directory to current repository
cd /vagrant

# Update apt packages list
sudo env DEBIAN_FRONTEND=noninteractive apt-get update

# Install C++ compiler and Python dependencies
# https://github.com/pyenv/pyenv/wiki/Common-build-problems
sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y make build-essential \
    libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl libncurses5-dev \
    libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev git

# Install pyenv
# https://github.com/pyenv/pyenv-installer
curl -sL https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Install Python 3
pyenv install 3.7.2
pyenv global 3.7.2
pyenv shell 3.7.2
pip install -U pip  # always ensure latest version

# Install dependencies - Python libraries
pip install -r requirements.txt
pip install flake8

# Run tests
python tests.py
