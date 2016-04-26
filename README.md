# Siptrack Contributed tools

Any tools people can use to work with [Siptrack](https://github.com/sii/siptrackweb). 

# How to get started with Siptrack

## Create virtualenv for siptrack

Create a virtualenv for siptrack in ``~/.venv/siptrack`` and activate it in your shell.

    virtualenv ~/.venv/siptrack
    . ~/.venv/siptrack/bin/activate

## Download siptrack client library

    git clone https://github.com/sii/siptrack
    cd siptrack

## Install Siptrack client library in your virtualenv

    python setup.py install

Now you should be able to run any of the tools here that require the siptrack library. 

Also configure the file ``siptrack_sample.cfg`` to point to your own siptrack and the base view you normally use. 
