#!/bin/sh
sphinx-apidoc -F -o docs necbaas && \
    (cd docs && make html)
