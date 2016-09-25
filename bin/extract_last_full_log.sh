#!/bin/bash
#
# Script to make a local copy of the last complete log

# make a local copy of the logs
cp /data/project/heritage/logs/update_monuments.log ./raw.log;

# cut log at last complete
last_complete=$(grep --binary-files=text -n "Done with the update!" raw.log | tail -n1 | cut -f1 -d:);
# echo "last_complete: $last_complete";
head -n "$last_complete" raw.log > tmp.log;

# keep only last log
log_length=$(wc -l tmp.log | cut -f1 -d' ');
# echo "log_length: $log_length";
last_start=$(grep --binary-files=text -n "Starting full monument update" tmp.log | tail -n1 | cut -f1 -d:);
# echo "last_start: $last_start";
cut_line=$((log_length - last_start + 1));
tail -n "$cut_line" tmp.log > update_monuments.log;

# output info on isolated log
log_length=$(wc -l update_monuments.log | cut -f1 -d' ');
start_time=$(head -n1 update_monuments.log | cut -f1 -d' ');
end_time=$(tail -n1 update_monuments.log | cut -f1 -d' ');
echo "update_monuments.log: ($start_time -- $end_time) $log_length lines";

# clean up
rm raw.log;
rm tmp.log;
