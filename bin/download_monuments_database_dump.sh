#!/bin/bash
# Downloads the monuments database dump from Tool Labs

URL=https://tools.wmflabs.org/heritage/monuments_db.sql.gz

wget --timestamping $URL -P ./conf/
