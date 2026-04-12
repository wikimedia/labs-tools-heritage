#!/bin/bash
set -ex

LOCAL_PORT="${LOCAL_PORT:-3306}"
REMOTE_PORT="${REMOTE_PORT:-3306}"

SERVICE="${SERVICE:-analytics}"

if [ -z "${WIKI_DB}" ]; then
    echo "ERROR: WIKI_DB environment variable is required" >&2
    exit 1
fi

REMOTE_HOST="$WIKI_DB.$SERVICE.db.svc.wikimedia.cloud"

HOST="${HOST:-login.toolforge.org}"

# Copy the mounted SSH properties, to set the right permissions
if [ -d "/root/ssh/" ]; then
    ls -l /root/ssh/
    rm -rf /root/.ssh
    mkdir -m 700 /root/.ssh
    cp -R /root/ssh/* /root/.ssh/
    chmod 600 /root/.ssh/*
fi

# You may not need to set the user if mounting an SSH config
if [ -z "${SSH_USER}" ]; then
    SSH_HOST="$HOST";
else
    SSH_HOST="$SSH_USER@$HOST";
fi

ssh \
    -v \
    -o StrictHostKeyChecking=accept-new \
    -L *:$LOCAL_PORT:$REMOTE_HOST:$REMOTE_PORT \
    -N "$SSH_HOST"
