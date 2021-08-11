#!/usr/bin/env bash

# create a path for Python executable script file and requirements file
executable_path="$(pwd)/kavosdraugas-sales-notifier.py"
requirements_path="$(pwd)/requirements.txt"

# ask user to enter path to Python interpreter
echo 'Python interpreter path:'
read -e python_path

# replace executable and python placeholders with real values
# here backup file is creaeted to not change one in project folder
sed -i.tmp -e 's|{EXECUTABLE_PATH}|'"$executable_path"'|g' com.kavosdraugas-sales-notifier.plist
sed -i '' -e 's|{PYTHON_PATH}|'"$python_path"'|g' com.kavosdraugas-sales-notifier.plist

# install requirements if needed
if [ "${python_path}" != '' ]
then
    $python_path -m pip install -r $requirements_path
fi

# copy created process configuration file into new location
cp com.kavosdraugas-sales-notifier.plist ~/Library/LaunchAgents/

# change edited plist file with pre-edited backup
mv com.kavosdraugas-sales-notifier.plist.tmp com.kavosdraugas-sales-notifier.plist

# load plist
launchctl load -w ~/Library/LaunchAgents/com.kavosdraugas-sales-notifier.plist