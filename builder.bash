#!/bin/bash

echo "Give name for python tool"
read TOOL
echo "Give path to repo to sync with"
read path

echo "Here we go..."


#move all the needed files in to the current dir and remove old git files
rm -rf python_project_planer/.git
mv python_project_planer/* python_project_planer/.[!.]* .
rm -rf python_project_planer/

mv py_project $TOOL

echo "#" $TOOL > README.md

pip3 install -r $TOOL/requirements.txt

#initialise empty git
git init

#add file structure to the new git 
git add .
git commit -m "first commit"

#install the wanted hooks
pre-commit install 

git add .
git commit -m "installed pre-commit hooks" 

#add remote location 
git remote add origin $path

#create a master branch by pushing file structure as a start
git push -u origin master

