:: SCRIPT BEHAVIOUR
:: run main.py --> get date --> commit --> push


:: DEPENDENCIES NEEDED TO RUN main.py
:: - numpy
:: - pandas
:: - matplotlib
:: - requests

python main.py -S

git add -A

set date=%date:~-4%_%date:~3,2%_%date:~0,2%

git commit -m "auto update: %date%"

git push

