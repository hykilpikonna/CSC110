#!/usr/bin/env sh

# abort on errors
set -e

# navigate into the build output directory
cd notes

# if you are deploying to a custom domain
echo 'c110-notes.hydev.org' > CNAME

git init
git add -A
git commit -m 'deploy'

# if you are deploying to https://<USERNAME>.github.io/<REPO>
git push -f git@github.com:Hykilpikonna/CSC110.git master:gh-pages

cd -
