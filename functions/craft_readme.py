import pathlib
from datetime import date
from os import listdir
from os.path import isfile, join


mypath = pathlib.Path(__file__).parent.absolute() / ".." / "images"

block_titles = {
    'AS': 'Confronto tra i giorni precedenti al lockdown e oggi',
    'HS': 'Storici (andamento da febbraio 2020)',
    'PR': 'Predizioni per le prossime 2 settimane',
    'ST': 'Confronto tra nazioni europee',
}
kinds = {
    'intensive': 'dei casi di TERAPIA INTENSIVA',
    'new': 'dei nuovi casi positivi al tampone',
    'deaths': 'delle morti causate da COVID-19',
    'ospitalized': 'del numero di persone attualmente in ospedale causa COVID-19',
}


def get_title_plot(fname):
    parts = fname.split('_')
    reg = (parts[1] == 'national' and 'Italia') or parts[1]
    return f"\n{block_titles[parts[0]]} {kinds[parts[2]]} in {parts[1]}"


def write_rd2(last_day, d3):
    d3ago = f"```\nL'Italia 3 giorni fa\n    terapia_intensiva:      {d3['terapia_intensiva']}\n    nuovi_positivi:         {d3['nuovi_positivi']}\n    totale_ospedalizzati:   {d3['totale_ospedalizzati']}\n```\n"
    today = f"```\nL'Italia OGGI\n    terapia_intensiva:      {last_day['terapia_intensiva']}\n    nuovi_positivi:         {last_day['nuovi_positivi']}\n    totale_ospedalizzati:   {last_day['totale_ospedalizzati']}\n```\n"
    intro = f"\n# COVID-autumn-forecast\nAlcune Statistiche sul covid in Italia, Francia & Inghilterra\nultimo aggiornamento --> {date.today()}\nFonte dei dati sull' italia: [pcm-dpc covid repository](https://github.com/pcm-dpc/COVID-19/blob/master/dati-json/dpc-covid19-ita-regioni.json)\nAltre fonti: [Francia]('https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.json'),  [Regno Unito](https://api.coronavirus.data.gov.uk/v1)\n\n## Dati Generali\n```\nL'Italia il 15 marzo 2020\n    terapia_intensiva:      1672\n    nuovi_positivi:         3590\n    totale_ospedalizzati:   11335 \n```\n```\nL'Italia il 18 marzo 2020\n    terapia_intensiva:      2257\n    nuovi_positivi:         4207\n    totale_ospedalizzati:   16620 \n```\n{d3ago}{today}"
    document = [intro]
    plots = [
        f for f in listdir(mypath)
        if isfile(join(mypath, f)) and '.png' in f
    ]
    plots.sort()
    plots.reverse()

    tp = None

    # dinamically create report sections
    block = []
    for f in plots:
        if (f[:2] != tp):
            if (len(block) > 0):
                document.append("\n".join(block))
            tp = f[:2]
            block = [f"### {block_titles[tp]}\n"]
        block.append(f"{get_title_plot(f)}\n![{tp}](images/{f})")
    document.append("\n".join(block))

    # write file
    readme_path = pathlib.Path(__file__).parent.absolute() / ".." / "README.md"
    with open(readme_path, 'w') as fout:
        fout.write("\n\n".join(document))


def write_rd():
    doc = """
# COVID-autumn-forecast

Alcune Statistiche sul covid in Italia, Francia & Inghilterra
ultimo aggiornamento --> {}

Fonte dei dati sull' italia: [pcm-dpc covid repository](https://github.com/pcm-dpc/COVID-19/blob/master/dati-json/dpc-covid19-ita-regioni.json)


## Dati Generali

```
L'Italia il 15 marzo 2020
    terapia_intensiva:      1672
    nuovi_positivi:         3590
    totale_ospedalizzati:   11335 
```

```
L'Italia il 18 marzo 2020
    terapia_intensiva:      2257
    nuovi_positivi:         4207
    totale_ospedalizzati:   16620 
```

## Grafici

#### Stati Europei

Italia vs UK vs Francia: morti

![april vs september](images/gdeaths.png)

Italia vs UK vs Francia: nuovi casi

![april vs september](images/ginfections.png)

Italia vs Francia: terapia intensiva

![april vs september](images/gintensive.png)



#### Previsioni

Previsione a 2 settimane nel futuro del numero di casi in **terapia intensiva**. (modello `Yapprossimata=Ae^(Bx)`)

![april vs september](images/predictionint.png)

Previsione a 2 settimane nel futuro del numero di nuovi casi. (modello `Yapprossimata=Ae^(Bx)`)

![april vs september](images/prediction.png)

#### Aprile vs Settembre

Persone in ospedale causa covid: aprile e settembre

![april vs september](images/aprilseptember.png)

Morti in **Veneto** causa covid: aprile e settembre

![april vs september](images/aprilseptemberve.png)

Morti in **Trentino** causa covid: aprile e settembre

![april vs september](images/aprilseptembertr.png)

Terapia Intensiva in **Veneto** causa covid: aprile e settembre

![april vs september](images/aprilseptemberveintensive.png)

Terapia Intensiva in **Lazio** causa covid: aprile e settembre

![april vs september](images/aprilseptemberveintensila.png)


Terapia Intensiva in **Campania** causa covid: aprile e settembre

![april vs september](images/aprilseptemberveintensica.png)

Terapia Intensiva in **Emilia Romagna** causa covid: aprile e settembre

![april vs september](images/aprilseptemberveintensiem.png)

Terapia Intensiva in **Lombardia** causa covid: aprile e settembre

![april vs september](images/aprilseptemberveintensilo.png)


#### Storici

Storico dei ricoverati in terapia intensiva

![casi intensivi](images/intensive.png)

Storico dei nuovi casi registrati

![new cases](images/infections.png)


    """.format(date.today())

    readme_path = pathlib.Path(__file__).parent.absolute() / ".." / "README.md"

    with open(readme_path, 'w') as fout:
        fout.write(doc)
