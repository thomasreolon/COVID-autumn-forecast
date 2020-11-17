import pandas as pd
import numpy
from datetime import date

_cache = {}

# wraps a dataframe to make it easier / more readible


class MyDF(object):
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def _call(self, fname, *args, **kw):
        res = None
        if fname == 'region':
            res = self.get_region(*args, **kw)
        elif fname == 'previous':
            res = self.get_previous(*args, **kw)
        elif fname == 'after':
            res = self.get_after(*args, **kw)
        elif fname == 'new_cases':
            res = self.get_new_cases(*args, **kw)
        elif fname == 'hospitalized':
            res = self.get_hospitalized(*args, **kw)
        elif fname == 'intensive':
            res = self.get_intensive(*args, **kw)
        elif fname == 'deaths':
            res = self.get_deaths(*args, **kw)
        elif fname == 'dates':
            res = self.get_dates(*args, **kw)
        elif fname == 'dates_as_int':
            res = self.get_dates_as_int(*args, **kw)

        if not res:
            raise(Exception(f'{fname} not found'))
        return res

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
            # solve bug: dataset dates have _ instead of -
            dd = '-'.join(dd.split('_'))

            d = date(*[int(x) for x in dd.split('-')])
            tmp2.append((d-bd).days)

        return tmp2

    def compose(self, todos):
        res = self
        if isinstance(todos, str):
            res = res._call(todos)
        elif isinstance(todos, (tuple, list)):
            for todo in todos:
                if isinstance(todo, str):
                    res = res._call(todo)
                else:
                    res = res._call(*todo)

        return res


# load file into memory
def load_file(fpath):
    global _cache
    if fpath not in _cache:
        _cache[fpath] = pd.read_json(fpath)
    return MyDF(_cache[fpath])
