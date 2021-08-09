#!/usr/bin/env bash

executable_path="$(pwd)/kavosdraugas-sales-notifier.py"
requirements_path="$(pwd)/requirements.txt"

echo 'Python interpreter path:'
read -e python_path

sed -i.tmp -e 's|{EXECUTABLE_PATH}|'"$executable_path"'|g' com.kavosdraugas-sales-notifier.plist
sed -i '' -e 's|{PYTHON_PATH}|'"$python_path"'|g' com.kavosdraugas-sales-notifier.plist

if [ "${python_path}" != '' ]
then
    $python_path -m pip install -r $requirements_path
fi

cp com.kavosdraugas-sales-notifier.plist ~/Library/LaunchAgents/

mv com.kavosdraugas-sales-notifier.plist.tmp com.kavosdraugas-sales-notifier.plist

launchctl load -w ~/Library/LaunchAgents/com.kavosdraugas-sales-notifier.plist