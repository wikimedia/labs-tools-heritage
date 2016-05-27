#!/usr/bin/env bash

# wait for db to come up before starting tests, as shown in https://github.com/docker/compose/issues/374#issuecomment-126312313
# uses bash instead of netcat, because netcat is less likely to be installed
# strategy from http://superuser.com/a/806331/98716
set -e

echoerr() { echo "$@" 1>&2; }

echoerr "wait-for-db: waiting for db:5432"

timeout 15 bash <<EOT
while ! (echo > /dev/tcp/db/5432) >/dev/null 2>&1;
    do sleep 1;
done;
EOT
RESULT=$?

if [ $RESULT -eq 0 ]; then
  # sleep another second for so that we don't get a "the database system is start up" error
  sleep 1
  echoerr "wait-for-db: done"
else
  echoerr "wait-for-db: timeout out after 10 seconds waiting for db:5432"
fi

exec "$@"
