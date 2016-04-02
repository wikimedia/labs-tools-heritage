#!/bin/bash
ssh  tools-login.wmflabs.org <<'ENDSSH'
become heritage
cd heritage
git pull
git log @{1}.. --oneline  --reverse -C --no-merges
echo "Deploy done."
ENDSSH
