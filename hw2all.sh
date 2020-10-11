echo '\i ./testCases/tc1.sql; \q' | psql -d <DB NAME>
python3 checkdb.py database=testCases/tc1.txt


echo '\i./testCases/tc2.sql; \q' | psql -d <DB NAME>
python3 checkdb.py database=testCases/tc2.txt


echo '\i ./testCases/tc3.sql; \q' | psql -d <DB NAME>
python3 checkdb.py database=testCases/tc3.txt


echo '\i ./testCases/tc4.sql; \q' | psql -d <DB NAME>
python3 checkdb.py database=testCases/tc4.txt


echo '\i ./testCases/tc5.sql; \q' | psql -d <DB NAME>
python3 checkdb.py database=testCases/tc5.txt

echo '\i ./testCases/tc6.sql; \q' | psql -d <DB NAME>
python3 checkdb.py database=testCases/tc6.txt

