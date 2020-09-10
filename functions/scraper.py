import pathlib
import requests
import json
import sys

SCRAPE_FLAGS = ['-d', '-D', '--scrape', '--download', '-s', '-S']

try:
    if len(sys.argv) > 1 and sys.argv[1] in SCRAPE_FLAGS:
        # current path
        funct_folder = pathlib.Path(__file__).parent.absolute()

        # constants
        URL_REGIONAL = 'https://github.com/pcm-dpc/COVID-19/raw/master/dati-json/dpc-covid19-ita-regioni.json'
        URL_NATIONAL = 'https://github.com/pcm-dpc/COVID-19/raw/master/dati-json/dpc-covid19-ita-andamento-nazionale.json'
        FNAME_REGIONAL = funct_folder / ".." / "data/regional_data.json"
        FNAME_NATIONAL = funct_folder / ".." / "data/national_data.json"

        # download data
        urls = [(URL_REGIONAL, FNAME_REGIONAL), (URL_NATIONAL, FNAME_NATIONAL)]
        for url, fname in urls:
            resp = requests.get(url)
            data = json.loads(resp.content)
            with open(fname, 'w') as fout:
                json.dump(data, fout)
except Exception as e:
    print("exception: ", e)
