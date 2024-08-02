#!/bin/bash

echo "Creating output directories..."
mkdir -p data/1_interim/records/md
mkdir -p data/1_interim/records/json

echo "Converting .doc to .md..."
for file in data/0_raw/records/*.doc; do
    filename=$(basename "${file}")
    echo " - Converting $filename to .md..."

    textutil -convert docx "$file" -output "data/1_interim/${filename}x"
    pandoc -o "data/1_interim/records/md/${filename%doc}md" "data/1_interim/${filename}x"
    rm "data/1_interim/${filename}x"
done
echo "Done converting .doc to .md"