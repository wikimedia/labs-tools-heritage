#!/bin/bash
user="";
if [ -n "$1" ]; then
  user="$1"@
fi
ssh "$user"tools-login.wmflabs.org <<'ENDSSH'
become heritage
cd heritage
git pull
git log @{1}.. --oneline  --reverse -C --no-merges
echo "Deploy done."
ENDSSH
