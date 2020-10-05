import pandas as pd
import numpy
from datetime import date

_cache = {}

# wraps a dataframe to make it easier / more readible


class MyDF(object):
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.functs = {
            'region': self.get_region,
            'prevous': self.get_previous,
            'after': self.get_after,
            'new': self.get_new_cases,
            'hospital': self.get_hospitalized,
            'intensive': self.get_intensive,
            'deaths': self.get_deaths,
            'dates': self.get_dates,
            'datesint': self.get_dates_as_int,
        }

    def get_region(self, region_name='Veneto'):
        return MyDF(self.df[self.df['denominazione_regione'] == region_name])

    def get_previous(self, date: str) -> '(aaaa-mm-gg) => [...]':
        return MyDF(self.df[self.df['data'] < date])

    def get_after(self, date: str) -> '(aaaa-mm-gg) => [...]':
        return MyDF(self.df[self.df['data'] > date])

    def get_new_cases(self):
        return self.df['nuovi_positivi'].values.tolist()

    def get_hospitalized(self):
        return self.df['totale_ospedalizzati'].values.tolist()

    def get_intensive(self):
        return self.df['terapia_intensiva'].values.tolist()

    def get_deaths(self):
        a = self.df['deceduti'].values.tolist()
        res = [0]
        for i in range(len(a)):
            res.append(max(a[i]-a[i-1], 0))
        return res

    def get_dates(self):
        tmp = self.df['data'].values.tolist()
        tmp = [x[:10] for x in tmp]
        return tmp

    # returns a list of integers represinting the distance of each date from the zero_date
    def get_dates_as_int(self, zero_date):
        tmp = self.df['data'].values.tolist()
        tmp = [x[:10] for x in tmp]

        bd = date(*[int(x) for x in zero_date.split('-')])
        tmp2 = []
        for dd in tmp:
            d = date(*[int(x) for x in dd.split('-')])
            tmp2.append((d-bd).days)

        return tmp2

    def __getattribute__(self, f_name):
        if isinstance(f_name[0], str):
            res = self.functs[f_name[0]](f_name[1])
        elif isinstance(f_name[0], (tuple, list)):
            res = None
            for fn, fv in f_name:
                res = self.functs[fn](fv)

        return res


# load file into memory
def load_file(fpath):
    global _cache
    if fpath not in _cache:
        _cache[fpath] = pd.read_json(fpath)
    return MyDF(_cache[fpath])
