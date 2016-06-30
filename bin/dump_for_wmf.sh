#!/usr/bin/bash

# Dump for wlm.wikipedia.org
#mysqldump --skip-add-locks --complete-insert --default-character-set=utf8 p_erfgoed_p monuments_all admin_tree|gzip>./public_html/monuments.sql.gz
cd ~/temp || exit
php ../tools/export_as_text.php admin_tree > ./admin_tree_tmp.txt
php ../tools/export_as_text.php monuments_all > ./monuments_all_tmp.txt
tar -czf ../public_html/export.tar.gz admin_tree_tmp.txt monuments_all_tmp.txt
rm ./*.txt
cd ..
rm /home/project/e/r/f/erfgoed/temp/countries.ser
