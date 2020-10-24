import pandas as pd
import numpy as np
from functions.dataset import *
from functions.plot import plot_linear, plot, plot_multiple, plot_prediction, plot_comparison
from functions.craft_readme import write_rd2 as write_rd
from functions import scraper
from functions.plot_maker import PlotsMaker

FOLDER = "./data/"

# load datasets
ndf = load_file(FOLDER+'national_data.json')
rdf = load_file(FOLDER+'regional_data.json')
ukdf = load_file(FOLDER+'uk.json')
frdf = load_file(FOLDER+'france.json')
dark = 'dark_background'

# loads plotMaker
pltmk = PlotsMaker(ndf, rdf, ukdf, frdf)


#########################################################
# CAMPI CHIAMABILI NEL CAMPO kind
#
#  intensive --> terapia_intensiva
#  hospitalized --> totale_ospedalizzati
#  deaths --> deceduti
#  new_cases --> nuovi_positivi
#########################################################


# april vs september (natioanal & regional level)
pltmk.make_april_september(region="Veneto")
pltmk.make_april_september(region="Lombardia")
pltmk.make_april_september(region="P.A. Trento")
pltmk.make_april_september(region="Campania", kind="intensive")

pltmk.make_april_september(region="Veneto", kind="new_cases")
pltmk.make_april_september(region="Campania", kind="new_cases")

# nations comparisons
pltmk.make_states_comparison(kind='intensive')
pltmk.make_states_comparison(kind='new_cases')
pltmk.make_states_comparison(kind='hospitalized')

# prediction for the future
pltmk.make_prediction(base_date='2020-09-21')
pltmk.make_prediction(base_date='2020-09-15', kind='hospitalized')

# plot all history
pltmk.make_history()
pltmk.make_history(kind='hospitalized')
pltmk.make_history(kind='new_cases')
pltmk.make_history(kind='deaths')


# WRITE
# NEW
# README
write_rd(ndf.df.iloc[-1], ndf.df.iloc[-4])


print('DONE')
