#!/usr/bin/env python2

"""
Name: Joshua Brockschmidt
UW NetID: 1629722
Section: AA
CSE 160
Final Project

Calculates correlation between Bitcoin and mainstream currencies, and market indexes (namely the
S&P 500 and Dow 30). Normalized graphs of these exchange rates and adjusted close values are
plotted against each other and saved as PNGs. Finally, a CSV file containing the correlation
coefficient and the corresponding p-value between indexes and currencies is produced.
"""

import csv
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as md
from scipy.stats import pearsonr

class Rates:
    """
    Represents a series of rates versus dates.
    """

    def __init__(self, rates=None, dates=None,
                 fn=None, rate_col=None, date_col=None, date_format=None,
                 label=""):
        """
        Creates a new rates object.

        Args:
            rates: Collection of rates. Must be passed with a corresponding collection of dates.
            dates: Collection of dates. Must be the same length as 'rates'.
            fn: File path of CSV file containing rates data. Must be passed alongside 'rate_col',
                'date_col', and 'date_format'.
            rate_col: Name of column for rates. Accompanies 'fn'.
            date_col: Name of column for dates. Accompanies 'fn'.
            date_format: Format of date strings in CSV file. See datetime.datetime.strptime(...)
                or datetime.date.strftime(...) for details.
            label: Label to associate with rates.
        """
        if not ((fn is None) or (date_col is None) or (rate_col is None) or (date_format is None)):
            # Load data from a CSV file.
            self.load_csv(fn, date_col, rate_col, date_format)
        elif not ((dates is None) or (rates is None)):
            # Use dates and rates passed as arguments.
            end = min(len(dates), len(rates))
            self.dates = dates[:end]
            self._md_dates = md.datestr2num(dates)
            self.rates = rates[:end]
            self.date_to_rate = {}
            for i, date in enumerate(dates):
                self.date_to_rate[date] = rates[i]
        self.label = label

    def load_csv(self, fn, date_col, rate_col, date_format):
        """
        Load rates data from a CSV file.

        Args:
            fn: File path of CSV file.
            date_col: Column in CSV file that contains dates to associate with
                each rate.
            rate_col: Column in CSV file that contains the desired rates.
            date_format: Format of date strings. See datetime.datetime.strptime(...)
                or datetime.date.strftime(...) for details.
        """
        dates = []
        rates = []
        date_to_rate = {}
        with open(fn, 'r') as f:
            data = csv.DictReader(f, delimiter=',')
            i = 0
            for row in data:
                try:
                    # Use a common date format.
                    date = dt.datetime.strptime(row[date_col], date_format)
                    date = dt.date.strftime(date, "%Y-%m-%d")
                    rate = float(row[rate_col])
                    dates.append(date)
                    rates.append(rate)
                    date_to_rate[date] = rate
                except ValueError:
                    pass
        self.dates = dates
        self._md_dates = md.datestr2num(dates)
        self.rates = rates
        self.date_to_rate = date_to_rate

    def normalize(self):
        """
        Creates a Rates object whose rates are normalized, such that the maximum
        magnitude of any given rate is no greater than 1.

        Returns:
            Normalized version of this Rates object.
        """
        max_rate = max(max(self.rates), abs(min(self.rates)))
        norm_rates = [r / max_rate for r in self.rates]
        new_rates = Rates(dates=self.dates, rates=norm_rates, label=self.label)
        return new_rates

    def calc_derivatives(self):
        """
        Calculates the rates of change (rate per day) between each point.

        NOTE: This function was used for an analysis that I decided to omit. I kept this code
        in because there's no real reason to delete it.

        Returns:
            Rates object containing rates of change.
        """
        derivRates = []
        derivDates = []
        for i in range(len(self.rates) - 1):
            date1 = dt.datetime.strptime(self.dates[i], "%Y-%m-%d")
            date2 = dt.datetime.strptime(self.dates[i+1], "%Y-%m-%d")
            deltaTime = (date2 - date1).days
            if deltaTime != 0:
                delta = self.rates[i+1] - self.rates[i]
                derivRates.append(delta / deltaTime)
                derivDates.append(self.dates[i])

        return Rates(derivRates, derivDates)

    def add_to_plot(self):
        """
        Add rate data to the current plot.
        """
        plt.plot_date(self._md_dates, self.rates,
                      linestyle='solid', marker='None', label=self.label)

    def correlate(self, other):
        """
        Find the correlation between this set of rates and another.

        Returns:
            Pearson correlation coefficient and p-value for testing non-correlation.
        """
        rates1 = []
        rates2 = []

        # Only use rates that overlap.
        dates = set(self.dates).intersection(other.dates)
        for d in dates:
            rates1.append(self.date_to_rate[d])
            rates2.append(other.date_to_rate[d])

        corr, p = pearsonr(rates1, rates2)

        return corr, p

def calc_correlation(rates1, rates2):
    """
    Calculates the Pearson correlation coefficient of two rates objects.

    Args:
        rates1: First rates object.
        rates2: Second rates object.
    Returns:
        A dictionay containing the label of the first rates object, the label of the second rates object,
        the correlation coefficient, and the p confidence value that the correlation is incorrect.
    """
    # Calculate correlation and build row data.
    r, p = rates1.correlate(rates2)
    row = {
        'label1' : rates1.label,
        'label2' : rates2.label,
        'correlation' : r,
        'p' : p
    }

    # Display results.
    print "{} and {}:  {:.4f},  p = {:.4g}".format(rates1.label, rates2.label, r, p)

    return row

def plot_rates(rates_list, title, y_lim=None, fn="", display=False):
    """
    Plots a collection of rates.

    Args:
        rates_list: Collection of rates to plot.
        title: Title of plot.
        y_lim: Limits of the Y axis.
        fn: Name of file to save figure to.
        display: Boolean, whether to display graph or not.
    """
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Exchange rates / close rates")
    if not y_lim is None:
        axes = plt.gca()
        axes.set_ylim(y_lim)
    for rates in rates_list:
        rates.add_to_plot()
    plt.legend(loc='lower right')
    plt.xticks(rotation='vertical')
    plt.tight_layout()
    if len(fn) > 0:
        plt.savefig(fn)
    if display:
        plt.show()
    else:
        plt.clf()

def plot_rates_normalized(rates_list, title, y_lim=(-1, 1), fn="", display=False):
    """
    Normalizes and plots a collection of rates.

    Args:
        rates_list: Collection of rates to normalize and plot.
        title: Title of plot.
        y_lim: Limits of the Y axis.
        fn: Name of file to save figure to.
        display: Boolean, whether to display graph or not.
    """
    norm_rates = [rates.normalize() for rates in rates_list]
    plot_rates(norm_rates, title, y_lim, fn=fn, display=display)

def main():
    """
    Initializes rates for market indexes and currency exchange rates. Then creates and saves plots
    of these rates against each other. Finally, correlation between these rates are calculated and
    saved to a CSV file.
    """
    # Load S&P 500 and Dow 30 adjusted close rates.
    sp_rates = Rates(
        fn="data/^GSPC.csv",
        date_col="Date", rate_col="Adj Close", date_format="%Y-%m-%d",
        label="S&P 500"
    )
    dow_rates = Rates(
        fn="data/^DJI.csv",
        date_col="Date", rate_col="Adj Close", date_format="%Y-%m-%d",
        label="Dow 30"
    )

    # Load BTC-to-USD exchange rates.
    btc_rates = Rates(
        fn="data/BTC-USD.csv",
        date_col="Date", rate_col="Adj Close", date_format="%Y-%m-%d",
        label="BTC to USD"
    )

    # Load exchange rates for CAN, CNY, and JPY to USD.
    can_to_usd = Rates(
        fn="data/DEXCAUS.csv",
        date_col="DATE", rate_col="DEXCAUS", date_format="%Y-%m-%d",
        label="CAN to USD"
    )
    cny_to_usd = Rates(
        fn="data/DEXCHUS.csv",
        date_col="DATE", rate_col="DEXCHUS", date_format="%Y-%m-%d",
        label="CNY to USD"
    )
    jpy_to_usd = Rates(
        fn="data/DEXJPUS.csv",
        date_col="DATE", rate_col="DEXJPUS", date_format="%Y-%m-%d",
        label="JPY to USD"
    )

    # Load trade weighted U.S. dollar index.
    dtwexb_rates = Rates(
        fn="data/DTWEXB.csv",
        date_col="DATE", rate_col="DTWEXB", date_format="%Y-%m-%d",
        label="U.S. Dollar Index"
    )

    # Plot normalized BTC-to-USD exchange rates against S&P 500 and Dow 30 adjusted close rates.
    list_rates1 = (sp_rates, dow_rates, btc_rates)
    plot_rates_normalized(
        list_rates1,
        "BTC to USD against S&P 500 and Dow 30",
        y_lim=(0, 1),
        fn="btc-indexes-fig.png",
        display=False
    )

    # Plot normalized currency exchange rates against S&P 500 and Dow 30 adjusted close rates.
    list_rates2 = (sp_rates, dow_rates, can_to_usd, cny_to_usd, jpy_to_usd)
    plot_rates_normalized(
        list_rates2,
        "Currencies against S&P 500 and Dow 30",
        y_lim=(0.7, 1),
        fn="currencies-indexes-fig.png",
        display=False
    )

    # Plot normalized BTC-to-USD exchange rates against U.S. dollar index.
    list_rates3 = (dtwexb_rates, btc_rates)
    plot_rates_normalized(
        list_rates3,
        "BTC to USD against U.S. Dollar Index",
        y_lim=(0, 1),
        fn="btc-dtwexb-fig.png",
        display=False
    )

    # Plot normalized U.S. dollar index rates against the S&P 500 and Dow 30 adjusted close rates.
    list_rates4 = (sp_rates, dow_rates, dtwexb_rates)
    plot_rates_normalized(
        list_rates4,
        "U.S dollar against S&P 500 and Dow 30",
        y_lim=(0.7, 1),
        fn="sp-dow-dtwexb-fig.png",
        display=False
    )

    # Calculate correlation between stock indexes and currencies and the U.S. dollar index.
    currencies = (btc_rates, can_to_usd, cny_to_usd, jpy_to_usd, dtwexb_rates)
    indexes = (sp_rates, dow_rates)
    rows = []
    for index in indexes:
        for currency in currencies:
            row = calc_correlation(index, currency)
            rows.append(row)

    # Write rows of correlation data to a CSV file.
    with open('correlations.csv', 'w') as f:
        writer = csv.DictWriter(f, ('label1', 'label2', 'correlation', 'p'))
        writer.writerow({
            'label1' : 'label1',
            'label2' : 'label2',
            'correlation' : 'correlation',
            'p' : 'p'
        })
        for row in rows:
            writer.writerow(row)

if __name__ == "__main__":
    main()
