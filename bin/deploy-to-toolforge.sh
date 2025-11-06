#!/bin/bash

set -e
user="";
if [ -n "$1" ]; then
    user="$1"@
fi
ssh "$user"login.toolforge.org <<'ENDSSH'
become heritage
cd heritage
. bin/defaults.sh

echo "Pulling changes from Git..."
git pull
git log "@{1}.." --oneline --reverse -C --no-merges

echo "Updating dependencies..."
toolforge jobs run build-python --command "./bin/build-python.sh" --image "$TOOLFORGE_PYTHON_IMAGE" --wait
toolforge jobs run build-php --command "./bin/build-php.sh" --image "$TOOLFORGE_PHP_IMAGE" --wait
echo "Dependencies updated"

echo "Updating the Server Admin Log..."
dologmsg "$($VIRTUAL_ENV_PATH/bin/$PYWIKIBOT_BIN bin/deploy_message_from_git_log.py)"
echo "Deploy done."
ENDSSH
