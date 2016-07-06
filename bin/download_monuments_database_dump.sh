#!/bin/bash
# Downloads the monuments database dump from Tool Labs

wget --timestamping https://tools.wmflabs.org/heritage/monuments_db.sql.gz -P ./conf/
