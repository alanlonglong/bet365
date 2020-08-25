# bet365

Load football.sql with mysql -u root -p football < football.sql

Modify .ini file to contain your MySQL password and a comma separated list of competitions

Requirements: 
https://github.com/ultrafunkamsterdam/undetected-chromedriver (this allows you to use selenium undetected)
You will need Mysqldb. On mac with python3, you should be able to get all that you need with: conda install mysqlclient
You will need both Chrome and the Chromedriver (https://chromedriver.chromium.org/) and be sure to put the newly downloaded chromedriver on your path (https://www.kenst.com/2015/03/including-the-chromedriver-location-in-macos-system-path/)

Run from command line: python bet365football.py
with the python file in the same locatoin as the .ini file.
