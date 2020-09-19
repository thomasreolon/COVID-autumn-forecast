import pathlib
import requests
import json
import sys

SCRAPE_FLAGS = ['-d', '-D', '--scrape', '--download', '-s', '-S']
TODO = {
    'IT',
    'FR',
    'UK',
}
# current path
funct_folder = pathlib.Path(__file__).parent.absolute()

# ITALY DATA
try:
    if 'IT' not in TODO:
        raise Exception('skip')
    if len(sys.argv) > 1 and sys.argv[1] in SCRAPE_FLAGS:

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
    print("ITALY EXCEPTION: ", e)


# FRANCE DATA
try:
    if 'FR' not in TODO:
        raise Exception('skip')
    URL_FRANCE = 'https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.json'
    FRANCE_FILE = funct_folder / ".." / "data/france.json"
    resp = requests.get(URL_FRANCE)
    data = json.loads(resp.content)

    results, prev = {}, 0
    for v in data:
        try:
            if 'source' in v and v['source']['nom'] == 'Ministère des Solidarités et de la Santé':
                data = v['date']
                if 'deces' in v:
                    decessi = v['deces']
                else:
                    decessi = 0
                tmp = {
                    "data": data,
                    "terapia_intensiva": v['reanimation'],
                    "totale_ospedalizzati": v['hospitalises'],
                    "deceduti": decessi,
                    "nuovi_positivi": v['casConfirmes']-prev
                }
                prev = v['casConfirmes']
            results[data] = tmp
        except:
            pass

    results = [x[1] for x in results.items()]

    with open(FRANCE_FILE, 'w') as fout:
        json.dump(results, fout)
except Exception as e:
    print("FRANCE EXCEPTION: ", e)


# UK DATA
try:
    if 'UK' not in TODO:
        raise Exception('skip')

    UK_FILE = funct_folder / ".." / "data/uk.json"
    STRUCTURE = {
        "data": "date",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumDeathsByDeathDate": "cumDeaths28DaysByDeathDate"
    }

    # get data
    endpoint = (
        'https://api.coronavirus.data.gov.uk/v1/data?'
        'filters=areaType=overview&'
        'structure=' + json.dumps(STRUCTURE)
    )
    response = requests.get(endpoint, timeout=10)
    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: { response.text }')
    data = json.loads(response.content)

    res = []
    for v in data['data']:
        deaths = v['cumDeathsByDeathDate']
        if not deaths:
            deaths = 0
        res.append({
            'data': v['data'],
            'nuovi_positivi': v['newCasesByPublishDate'],
            'deceduti': deaths,
        })
    res.sort(key=lambda x: x['data'])
    del res[-1]
    with open(UK_FILE, 'w') as fout:
        json.dump(res, fout)

except Exception as e:
    print("UK EXCEPTION: ", e)
