import pandas as pd
import numpy as np
from functions.dataset import *
from functions.plot import plot_linear, plot, plot_multiple, plot_prediction, plot_comparison
from functions.craft_readme import write_rd
from functions import scraper

FOLDER = "./data/"

# load datasets
ndf = load_file(FOLDER+'national_data.json')
rdf = load_file(FOLDER+'regional_data.json')
ukdf = load_file(FOLDER+'uk.json')
frdf = load_file(FOLDER+'france.json')
dark = 'dark_background'

# plot hospitalized people in april vs september
DAYS, YLIM = 23, 20000
XLABEL, YLABEL = '{} days'.format(DAYS), 'people in hospital'
september = ndf.get_after('2020-08-22').get_hospitalized()[-DAYS:]
s_xlabels = ndf.get_after('2020-08-22').get_dates()[-DAYS:]

# plot_linear(september, xlabel=XLABEL, ylabel=YLABEL, xlabels=s_xlabels)


# plot intensive care for the whole dataset
intensive, dates = ndf.get_intensive(), ndf.get_dates()
plot(intensive, dates, xlabel='giorni', ylabel='terapia intensiva',
     style=dark, save='intensive.png')

# comparison: april vs september
april = ndf.get_previous('2020-03-19').get_hospitalized()[:DAYS]
a_xlabels = ndf.get_previous('2020-03-19').get_dates()[:DAYS]
plot_multiple([april, september], ylim=YLIM, xlabel=XLABEL, save='aprilseptember.png',
              ylabel=YLABEL, xlabels=[a_xlabels, s_xlabels], style=dark)

# exponential fit for september
y = ndf.get_after('2020-08-31').get_new_cases()
labels = ndf.get_after('2020-08-31').get_dates()
plot_prediction(y, xlabels=labels, ylabel='new cases', save='prediction.png')


# NEW DIAGRAMS (veneto & trento)
YLABEL = 'new death'
trento = rdf.get_region('P.A. Trento')
april = trento.get_previous('2020-03-19').get_deaths()[:DAYS]
september = trento.get_after('2020-08-22').get_deaths()[-DAYS:]
plot_multiple([april, september], xlabel=XLABEL, save='aprilseptembertr.png',
              ylabel=YLABEL, xlabels=[a_xlabels, s_xlabels], style=dark, ylim=max(april+september))

veneto = rdf.get_region('Veneto')
april = veneto.get_previous('2020-03-19').get_deaths()[:DAYS]
september = veneto.get_after('2020-08-22').get_deaths()[-DAYS:]
plot_multiple([april, september], xlabel=XLABEL, save='aprilseptemberve.png',
              ylabel=YLABEL, xlabels=[a_xlabels, s_xlabels], style=dark, ylim=max(april+september))

april = veneto.get_previous('2020-03-19').get_intensive()[:DAYS]
september = veneto.get_after('2020-08-22').get_intensive()[-DAYS:]
plot_multiple([april, september], xlabel=XLABEL, save='aprilseptemberveintensive.png',
              ylabel=YLABEL, xlabels=[a_xlabels, s_xlabels], style=dark, ylim=max(april+september))

lazio = rdf.get_region('Lazio')
april = lazio.get_previous('2020-03-19').get_intensive()[:DAYS]
september = lazio.get_after('2020-08-22').get_intensive()[-DAYS:]
plot_multiple([april, september], xlabel=XLABEL, save='aprilseptemberveintensila.png',
              ylabel=YLABEL, xlabels=[a_xlabels, s_xlabels], style=dark, ylim=max(april+september))

# Terapia intensiva prevista
y = ndf.get_after('2020-08-31').get_intensive()
labels = ndf.get_after('2020-08-31').get_dates()
plot_prediction(y, xlabels=labels, ylabel='intensive care',
                save='predictionint.png')

# Storico infezioni
intensive, dates = ndf.get_new_cases(), ndf.get_dates()
plot(intensive, dates, xlabel='days', ylabel='new infected',
     style=dark, save='infections.png')


# nations comparison DEATHS global
BASE_DATE = '2020-02-24'
y = [
    ndf.get_after(BASE_DATE).get_deaths()[2:],
    ukdf.get_after(BASE_DATE).get_deaths()[2:],
    frdf.get_after(BASE_DATE).get_deaths()[2:]
]
x = [
    ndf.get_after(BASE_DATE).get_dates_as_int(BASE_DATE)[1:],
    ukdf.get_after(BASE_DATE).get_dates_as_int(BASE_DATE)[1:],
    frdf.get_after(BASE_DATE).get_dates_as_int(BASE_DATE)[1:]
]

ylabels = [
    'italia',
    'UK',
    'francia'
]
dates = ndf.get_after(BASE_DATE).get_dates()[1:]
plot_comparison(x, y, dates, ylabels, style=dark,
                title='andamento morti', save='gdeaths.png')


# nations comparison new infected latest
BASE_DATE = '2020-08-01'
y = [
    ndf.get_after(BASE_DATE).get_new_cases(),
    ukdf.get_after(BASE_DATE).get_new_cases(),
    frdf.get_after(BASE_DATE).get_new_cases()
]
x = [
    ndf.get_after(BASE_DATE).get_dates_as_int(BASE_DATE),
    ukdf.get_after(BASE_DATE).get_dates_as_int(BASE_DATE),
    frdf.get_after(BASE_DATE).get_dates_as_int(BASE_DATE)
]

ylabels = [
    'italia',
    'UK',
    'francia'
]
dates = ndf.get_after(BASE_DATE).get_dates()
plot_comparison(x, y, dates, ylabels, style=dark,
                title='nuovi casi di covid', save='ginfections.png')


# ita vs france
y = [
    ndf.get_after(BASE_DATE).get_intensive(),
    frdf.get_after(BASE_DATE).get_intensive()
]
x = [
    ndf.get_after(BASE_DATE).get_dates_as_int(BASE_DATE),
    frdf.get_after(BASE_DATE).get_dates_as_int(BASE_DATE)
]

ylabels = [
    'italia',
    'francia'
]
dates = ndf.get_after(BASE_DATE).get_dates()
plot_comparison(x, y, dates, ylabels, style=dark,
                title='terapia intensiva FR vs IT', save='gintensive.png')


# WRITE
# NEW
# README
write_rd()


print('DONE')
