# Correlation of Bitcoin with Stock Market Performance Versus Mainstream Currencies

**Author**: Joshua Brockschmidt

# Summary of Research Questions

 * What is the correlation between the exchange rate of Bitcoin (BTC) to the U.S. dollar (USD) and stock market indexes, such as the S&P 500 and Dow 30, over the last year?
 * What is the correlation between the performance of mainstream currencies—such as the USD, the Canadian dollar (CAN), the Chinese Yuan (CNY), and the Japanese Yen (JPY)—and the same aforementioned stock market indexes over the last year?
 * Is the sign of the correlation coefficient of BTC to USD the same as or different from that of the other currency exchange rates? What does this imply?
 * Is the magnitude of the correlation coefficient of BTC to USD similar to that of the other currency exchange rates or does it differ considerably? What does this imply?
What final conclusion can we draw from the previous two comparisons?

# Motivation and Background:

In the last couple years, there’s been a lot of talk about what role Bitcoin plays in the market. Namely, is it a viable alternative to mainstream currencies? While this questions are complex and impossible to fully address in a single paper, we can at least begin to scratch the surface. In this paper, we will investigate the correlation between the exchange rate of BTC to USD and that of stock market indexes suck as the S&P 500 and Dow 300 over the last year, and compare that to the correlation of mainstream currencies, such as USD, CAN, CNY, and JPY.

# Dataset

For historical daily exchange rates from BTC to USD and the daily adjusted close rates of the S&P 500 and the Dow 30, we gathered data from Yahoo! Financei. For daily historical exchange rates for CAN to USD, CNY to USD, and JPY to USD as well as the trade weight U.S. dollar index, we gathered data from the Federal Reserve Bank of St. Louis’s websiteii. The trade weighted U.S. dollar index takes into account the exchange rates of USD to that of numerous currencies. It serves to represent the overall performance of USD in the foreign exchange (Forex) market. Since we are using the exchange rates of currencies to USD, we had to include an index like this in order to compare Bitcoin’s market correlation to that of the U.S. dollar (since the exchange rate from USD to USD is entirely useless and meaningless). For specific links to datasets, see the “Reproducing our results” section.

# Methodology

To measure correlation, we used the Pearson correlation coefficient (PCC). First, we computed the correlation between the daily exchange rates of BTC to USD and the stock market indexes of the S&P 500 and the Dow 30, spanning from 5/1/2017 to 4/30/2018. Then, we computed the correlation between the daily exchange rates of CAN to USD, CNY to USD, and JPY to USD and the S&P 500 and Dow 300 over the same time period. Finally, we calculated the correlation between a trade weighted U.S. dollar index and the S&P 500 and Dow 300 over the same period of a year.

# Results

*Figure 1. Correlations of stock market indexes and currencies*

Index | Currency | Correlation Coefficient | p-value
--- | --- | --- | ---
Dow 30 | BTC to USD | 0.8609 | 5.043e-75
Dow 30 | CAN to USD | -0.4534 | 4.452e-14
Dow 30 | CNY to USD | -0.8385 | 2.461e-67
Dow 30 | JPY to USD | -0.3523 | 1.023e-8
Dow 30 | U.S. dollar index | -0.6955 | 1.838e-37
S&P 500 | BTC to USD | 0.8363 | 6.323e-67
S&P 500 | CAN to USD | -0.4338 | 6.765e-13
S&P 500 | CNY to USD | -0.8309 | 4.459e-65
S&P 500 | JPY to USD | -0.3749 | 9.150e-10
S&P 500 | U.S. dollar index | -0.6936 | 3.462e-37

Figure 1 displays a table of the calculated correlation coefficients between indexes and currencies / currency indexes. The p-values are the probability that the calculated Pearson correlation for a given index and currency are not actually as extreme as they appear.iii We can immediately see that the correlations calculated against the S&P 500 and Dow 30 are relatively similar, withinof each other, or a difference no greater than 0.1%. With such a small difference and the absence of significant outliers, it is reasonable to say the correlation of each currency exchange rate and currency index against the stock market indexes are roughly representative of their correlation to the stock market as a whole. Given that no p-value reaches above, we state that the calculated correlation coefficients are accurate with more than 99.9999% confidence.

Looking at Figure 1, we can see that the correlation of BTC against each stock market index is positive, while the correlation for all other currency exchange rates/indexes are negative. It’s positive correlation with stock market performance means a rise in the stock market is generally associated with a rise in the BTC to USD exchange rate, and a dip in the stock market is generally associated with a dip in the latter exchange rate. For the other currency exchange rates, their negative correlation essentially just means that the exchange rate in the opposite direction (i.e. from USD to CAN, CNY, or JPY) is positively correlated with stock market performance in the same way. The sign of BTC to USD appears to be more in line with that of stocks than currency exchange rates to USD.

Another thing to notice about the correlation is how much stronger the correlation for BTC’s exchange rate is versus the other currencies. The disparity in the magnitudes (i.e. absolute value) of these correlations is as great as 0.5 (specifically between BTC and JPY). Even the magnitude of CNY’s correlation, which is the highest of the mainstream currencies, is consistently about 0.02 below BTC’s exchange rate. What this implies is that the exchange rate BTC is significantly more tied to the stock market than the exchange rates for other currencies.

Our results seem to imply that the behavior of BTC is not entirely in-line with that of mainstream currencies. As mentioned, the sign of BTC to USD implies that BTC is treated more like a stock than a Forex. The higher magnitude of the correlation of BTC versus other currencies implies the same. Essentially, it appears BTC is treated more as a investment than a means of exchanging goods. In other words, those who use BTC are typically treating it more like a tradable asset than a mainstream currency. It’s usage is relegated more to the world of market speculation and investing than it is to that of the exchange of goods and services—at least relative to other currencies. This is an indicator that BTC has not yet been fully adopted as a viable alternative to other currencies.

# Reproducing our Results:

Before running our code, the datasets we are interacting with will need to be retrieved. These datasets will be saved as CSV files within the directory entitled “data” which shares the same root as main.py. The time period for each dataset should be adjusted to 2017-05-01 to 2018-04-30 on each site. You are free to pick a different time frame. But this is the time frame used in this study, and will be necessary for the accurate replication of our results. The datasets, their file name, and their download links are as follows:

 * [S&P 500 (^DJI.csv)](https://finance.yahoo.com/quote/%5EGSPC/history)
 * [Dow 30 (^GSPC.csv)](https://finance.yahoo.com/quote/%5EDJI/history)
 * [BTC to USD (BTC-USD.csv)](https://finance.yahoo.com/quote/BTC-USD/history)
 * [CAN to USD (DEXCAUS.csv)](https://fred.stlouisfed.org/series/DEXCAUS)
 * [CNY to USD (DEXCHUS.csv)](https://fred.stlouisfed.org/series/DEXCHUS)
 * [JPY to USD  (DEXJPUS.csv)](https://fred.stlouisfed.org/series/DEXJPUS)
 * [Trade weighted U.S dollar index (DTWEXB.csv)](https://fred.stlouisfed.org/series/DTWEXB/)

The data cleaning for these files is handled at runtime.

To perform the analysis, you will first need to install the dependencies matplotlib and SciPy for Python 2. After verifying these are installed, simply execute main.py from it’s root directory (so “data” is visible to the script). This will save the calculated correlation data to a CSV titled correlation.csv, as well as print the results to the terminal. It will also produce PNGs of the various normalized plots seen earlier in this paper’s “Results” section (btc-indexes-fig.png for Figure 2, currencies-indexes-fig.png for Figure 3, and sp-dow-dtwexb-fig.png for Figure 4).

# Testing

For testing, I created test.py. This script tests the functionality of the Rates class created in main.py, which handles data cleanup and calculations. To test the loading of CSV files, I created a small test file in the “data” directory entitled test-small.csv, which is loaded by the test script. I also tested that the Rates object stored data in the proper sequential order, that normalizing a series of rates worked properly, that calculating the rates of change of a series of rates worked properly (a function that I did not end up using in my final script/analysis), and whether the correlation coefficient of two series of rates was calculated properly. These tests serve to help verify the validity of my final calculations, as their accurate hinges on the accuracy of the aforementioned tested functionality. For all aforementioned tests, I utilized asserts to test the produced results against precomputed, expected results. To reproduce my tests, simply run test.py from it’s root directory (such that the “data” directory containing the test CSV file is visible).
