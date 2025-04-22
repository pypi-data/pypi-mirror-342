#!/bin/bash

# Optional: Run tests again or build
./build.sh

# Push to PyPI
twine upload ../dist/*

