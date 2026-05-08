#!/bin/bash

# Script to convert all .md files in a directory and its subdirectories to .pdf using pandoc and XeLaTeX

if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

DIR=$1

if [ ! -d "$DIR" ]; then
    echo "Directory $DIR does not exist"
    exit 1
fi

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "pandoc is not installed. Please install pandoc."
    exit 1
fi

# Check if xelatex is installed
if ! command -v xelatex &> /dev/null; then
    echo "xelatex is not installed. Please install a LaTeX distribution like TeX Live."
    exit 1
fi

# Find all .md files recursively and convert them
find "$DIR" -type f -name "*.md" | while read -r file; do
    # Get the base name without extension
    base="${file%.md}"
    # Output pdf path
    pdf="$base.pdf"
    echo "Converting $file to $pdf"
    # Convert using pandoc with xelatex engine
    pandoc "$file" --pdf-engine=xelatex -o "$pdf"
    if [ $? -eq 0 ]; then
        echo "Successfully converted $file"
    else
        echo "Failed to convert $file"
    fi
done

echo "Conversion complete."