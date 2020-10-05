import pathlib
from datetime import date


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
