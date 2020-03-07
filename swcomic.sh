#!/bin/bash


tmp_col_file=".tmp_collections.json"
col_file=".collections.json"

# Get collections
wget -q https://raw.githubusercontent.com/shuweilee/swcomic/master/"${col_file}" -O "${tmp_col_file}"

# Failure check
if [[ $? -ne 0 ]];then
    echo "Get collection failed"
    exit 1
fi

# Check new epsode
python3 comic.py

# Update collection
git status -s | grep "${col_file}"
if [[ $? -ne 0 ]];then
    echo "No update"
    exit 0
fi

git add "${col_file}"
git commit -m "Update collections"
git push swcomic master

rm "${tmp_col_file}"
