from functions.dataset import *
from functions.plot import plot_linear, plot, plot_multiple
import pandas as pd

FNAME_REGIONAL = "./data/regional_data.json"
FNAME_NATIONAL = "./data/national_data.json"

# load datasets
ndf = load_national(FNAME_NATIONAL)
rdf = load_regional(FNAME_REGIONAL)

# plot hospitalized people in april vs september
DAYS, YLIM = 23, 20000
XLABEL, YLABEL = '{} days'.format(DAYS), 'people in hospital'
september = ndf.get_after('2020-08-22').get_hospitalized()[-DAYS:]

plot_linear(september, xlabel=XLABEL, ylabel=YLABEL)


# plot intensive care for the whole dataset
intensive, dates = ndf.get_intensive(), ndf.get_dates()
plot(intensive, dates, xlabel='giorni', ylabel='terapia intensiva')

# comparison: april vs september
april = ndf.get_previous('2020-03-19').get_hospitalized()[:DAYS]
plot_multiple([april, september], ylim=YLIM, xlabel=XLABEL, ylabel=YLABEL)
