from functions.dataset import MyDF
from functions.plot import plot_multiple


class PlotsMaker():
    def __init__(self, national, regional):
        self.national = national
        self.regional = regional
        self.AS_labels = None

    def make_april_september(self, region=None, kind='intensive', comp_days=23, style='dark_background'):
        # infos
        f_output = f"AS_{region or 'national'}_{kind}.png"
        XLABEL = f"{comp_days} giorni"
        YLABEL = f"people in hospital"

        # get dataset
        df = self.national
        if region:
            try:
                df = self.regional.get_region(region)
            except Exception as e:
                print(f"FAILED GETTING REGION {region} --> {e}")

        # get dates
        april = df.get_previous('2020-03-19').get_intensive()[:comp_days]
        september = df.get_after(
            '2020-08-22').get_intensive()[-comp_days:]

        # load labels
        if not self.AS_labels:
            self.AS_labels = [df.get_previous(
                '2020-03-19').get_dates()[:comp_days], df.get_after('2020-08-22').get_dates()[-comp_days:]]

        # plot
        plot_multiple(
            [april, september],
            save=f_output,
            xlabel=XLABEL,
            ylabel=YLABEL,
            xlabels=self.AS_labels,
            style=style,
            ylim=max(april+september)
        )
