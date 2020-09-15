import pandas as pd
import numpy as np
from functions.dataset import *
from functions.plot import plot_linear, plot, plot_multiple, plot_prediction
from functions.craft_readme import write_rd
from functions import scraper

FNAME_REGIONAL = "./data/regional_data.json"
FNAME_NATIONAL = "./data/national_data.json"

# load datasets
ndf = load_national(FNAME_NATIONAL)
rdf = load_regional(FNAME_REGIONAL)
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


# WRITE
# NEW
# README
write_rd()


print('DONE')
