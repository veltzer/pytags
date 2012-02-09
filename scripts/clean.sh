#!/bin/bash
find . \( -name "*.pyc" -or -name "*.pyo" \) -exec rm {} \;
