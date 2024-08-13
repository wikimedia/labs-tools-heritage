#!/bin/bash
set -e
user="";
if [ -n "$1" ]; then
    user="$1"@
fi
ssh "$user"login.toolforge.org <<'ENDSSH'
become heritage
cd heritage
echo "Pulling changes from Git..."
git pull
git log "@{1}.." --oneline --reverse -C --no-merges
echo "Updating dependencies..."
./bin/build.sh
echo "Updating the Server Admin Log..."
dologmsg "$(python bin/deploy_message_from_git_log.py)"
echo "Deploy done."
ENDSSH
