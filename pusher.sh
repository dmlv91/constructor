#!/bin/bash

# get current branch
curr=$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')
echo "Current branch is: '$curr'"

# git pull
echo "Pulling latest changes from the '$curr' branch"
git pull origin "$curr"

# get the commit from user input
message="$1"

# If no commit message is passed, use current date time in the commit message
if [[ -z "${message// }" ]]
    then
        message="$(date '+%Y-%m-%d %H:%M:%S')
fi

# stage all changes
echo "Adding all changed files to commit"
git add .

# commit changes
git commit -m "$message"
echo "Changes commited with message: '$message'"

# git push
git push origin "$curr"
echo "Changes pushed to '$curr' branch"
