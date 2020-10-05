from functions.dataset import MyDF
from functions.plot import plot_multiple


class PlotsMaker():
    def __init__(self, national, regional, AS_settings=None):
        self.national = national
        self.regional = regional

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
        f_output = f"AS_{region or 'national'}_{kind}.png"
        XLABEL = f"{st['comp_days']} giorni"
        YLABELS = {
            'deaths': 'morti giornalieri',
            'new_cases': 'nuovi casi giornalieri',
            'hospitalized': 'persone in ospedale',
            'intensive': 'persone in terapia intensiva',
        }

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
            ylabel=YLABELS[kind],
            xlabels=self.AS_labels,
            style=st['style'],
            ylim=max(april+sept)
        )
