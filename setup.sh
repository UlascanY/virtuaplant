#!/bin/sh

sudo apt-get install python3-pip python3-dev python3-pygame python3-gi python3-gi-cairo gir1.2-gtk-3.0 libgirepository1.0-dev gcc libcairo2-dev pkg-config python-is-python3
echo "packages installed"

#adding directory to PATH 
export PATH="$HOME/.local/bin:$PATH"

pip install -r requirements.txt
echo "requirements installed"