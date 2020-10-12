from functions.dataset import MyDF
from functions.plot import plot_multiple, plot_comparison, plot_prediction, plot


def remove_spaces(string):
    return "".join(string.split(" "))


class PlotsMaker():
    def __init__(self, national, regional, ukdf, frdf, AS_settings=None):
        self.national = national
        self.regional = regional
        self.YLABELS = {
            'deaths': 'morti giornalieri',
            'new_cases': 'nuovi casi giornalieri',
            'hospitalized': 'persone in ospedale',
            'intensive': 'persone in terapia intensiva',
        }

        # nations settings
        self.states = [
            (national, 'Italia'),
            (frdf, 'Francia'),
            (ukdf, 'Regno Unito'),
        ]

        # AS settings
        self.AS_settings = AS_settings or {
            'comp_days': 23,
            'style': 'dark_background',
            'april': '2020-03-19',
            'sept': '2020-08-22',
        }
        comp_days = self.AS_settings['comp_days']
        ap, st = self.AS_settings['april'], self.AS_settings['sept']
        self.AS_labels = [
            national.get_previous(ap).get_dates()[:comp_days],
            national.get_after(st).get_dates()[-comp_days:]
        ]

    def make_april_september(self, region=None, kind='intensive'):
        # infos
        st = self.AS_settings
        f_output = remove_spaces(f"AS_{region or 'national'}_{kind}.png")
        XLABEL = f"{st['comp_days']} giorni"

        # get dataset
        df = self.national
        if region:
            try:
                df = self.regional.get_region(region)
            except Exception as e:
                print(f"FAILED GETTING REGION {region} --> {e}")

        # get dates
        april = df.compose([('previous', st['april']), kind])[:st['comp_days']]
        sept = df.compose([('after', st['april']), kind])[-st['comp_days']:]

        # plot
        plot_multiple(
            [april, sept],
            save=f_output,
            xlabel=XLABEL,
            ylabel=self.YLABELS[kind],
            xlabels=self.AS_labels,
            style=st['style'],
            ylim=max(april+sept)
        )

    def make_states_comparison(self, kind='intensive', base_date='2020-08-01'):
        key_names = {
            'intensive': 'terapia_intensiva',
            'hospitalized': 'totale_ospedalizzati',
            'deaths': 'deceduti',
            'new_cases': 'nuovi_positivi'
        }
        x, y, labels = [], [], []
        for df, name in self.states:
            if key_names[kind] in df.df:
                y.append(df.compose([('after', base_date), kind]))
                x.append(df.compose(
                    [('after', base_date), ('dates_as_int', base_date)]
                ))
                labels.append(name)

        f_output = remove_spaces(f"ST_{'_'.join(labels)}_{kind}.png")
        title = f"{self.YLABELS[kind]} in {' & '.join(labels)}"
        dates = df.get_after(base_date).get_dates()

        plot_comparison(x, y, dates, labels, style='dark_background',
                        title=title, save=f_output)

    def make_prediction(self, region=None, kind='intensive', base_date='2020-08-31'):
        # get region
        df = self.national
        if region:
            try:
                df = self.regional.get_region(region)
            except Exception as e:
                print(f"FAILED GETTING REGION {region} --> {e}")

        # prediction: exponential fit
        y = df.compose([('after', base_date), kind])
        labels = df.compose([('after', base_date), 'dates'])
        f_output = remove_spaces(f"PR_{region or 'national'}_{kind}.png")

        plot_prediction(y, xlabels=labels,
                        ylabel=self.YLABELS[kind], save=f_output)

    def make_history(self, region=None, kind='intensive'):
        # get region
        df = self.national
        if region:
            try:
                df = self.regional.get_region(region)
            except Exception as e:
                print(f"FAILED GETTING REGION {region} --> {e}")
        f_output = remove_spaces(f"HS_{region or 'national'}_{kind}.png")
        intensive, dates = df.compose([kind]), df.get_dates()

        plot(intensive, dates, xlabel='giorni', ylabel=self.YLABELS[kind],
             style='dark_background', save=f_output)
