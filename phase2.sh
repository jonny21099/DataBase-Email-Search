sort -u recs.txt | perl break.pl | db_load -T -c duplicates=1 -t hash re.idx
sort -u terms.txt | perl break.pl | db_load -T -c duplicates=1 -t btree te.idx
sort -u emails.txt | perl break.pl | db_load -T -c duplicates=1 -t btree em.idx
sort -u dates.txt | perl break.pl | db_load -T -c duplicates=1 -t btree da.idx
