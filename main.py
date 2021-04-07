import pandas as pd
import datetime
from dateutil.parser import *
import matplotlib.pyplot as plt

gold_data = pd.read_csv("gold_usd_eur.csv")
# removing commas from the thousands separator
gold_data = gold_data.replace(',','', regex=True)
gold_data['Date'] = [parse(x) for x in gold_data["Date"]]

# extracts all the 18th of the month gold values in EUR from Jan 2020 to present
gold_reduced = []
for x in range(len(gold_data)):
    if (gold_data["Date"][x].day == 18):
        gold_reduced.append(((gold_data["Date"][x]),gold_data["EUR"][x],gold_data["USD"][x]))
    if ((gold_data["Date"][x].day == 17 or gold_data["Date"][x].day == 16) and (gold_data["Date"][x+1].day > 18)):
        gold_reduced.append((gold_data["Date"][x+1],gold_data["EUR"][x],gold_data["USD"][x]))

gold_dataframe = pd.DataFrame(data = gold_reduced, columns = ["Date","EUR","USD"])
gold_dataframe["EURUSD"] = gold_dataframe["EUR"].astype(float)/gold_dataframe["USD"].astype(float)
gold_dataframe["Nakup_zlata"] = 50/gold_dataframe["EUR"].astype(float)
kolicina = 0
kumulativa = []
for x in range(len(gold_dataframe["Date"])):
    kolicina += gold_dataframe["Nakup_zlata"][x]
    if (x==0):
        kumulativa.append(gold_dataframe["Nakup_zlata"][x])
    else:
        kumulativa.append(kolicina)

gold_dataframe["Kolicina_zlata"] = kumulativa
gold_dataframe["Vrednost_zlata"] = gold_dataframe["Kolicina_zlata"].astype(float)*gold_dataframe["EUR"].astype(float)

bitcoin_data = pd.read_csv("Binance_BTCUSDT_d.csv")
bitcoin_data["date"] = [parse(x) for x in bitcoin_data["date"]]

# extracting only the dates we need
bitcoin_reduced = []
for goldDate in gold_dataframe["Date"]:
    for i in range(len(bitcoin_data)):
        bitDate = bitcoin_data["date"][i]
        if (goldDate == bitDate):
            bitcoin_reduced.append(bitcoin_data["close"][i])

gold_dataframe["BTC"] = bitcoin_reduced
gold_dataframe["BTC_in_EUR"] = gold_dataframe["BTC"]*gold_dataframe["EURUSD"]
gold_dataframe["Nakup_BTC"] = (50)/gold_dataframe["BTC_in_EUR"].astype(float)

kolicina_btc = 0
kumulativa_btc = []
for x in range(len(gold_dataframe["Date"])):
    kolicina_btc += gold_dataframe["Nakup_BTC"][x]
    if (x==0):
        kumulativa_btc.append(gold_dataframe["Nakup_BTC"][x])
    else:
        kumulativa_btc.append(kolicina_btc)

gold_dataframe["Kolicina_BTC"] = kumulativa_btc

gold_dataframe["Vrednost_BTC"] = gold_dataframe["Kolicina_BTC"].astype(float)*gold_dataframe["BTC_in_EUR"].astype(float)
gold_dataframe["Vrednost_EUR"] = [(x+1)*50 for x in range(len(gold_dataframe["Date"]))]

plt.plot(gold_dataframe["Date"],gold_dataframe["Vrednost_zlata"], color ="orange", label="Vrednost zlata")
plt.plot(gold_dataframe["Date"],gold_dataframe["Vrednost_BTC"], label = "Vrednost Bitcoina")
plt.plot(gold_dataframe["Date"], gold_dataframe["Vrednost_EUR"], color ="green", label="Vrednost denarja na bančnem računu")

plt.xlabel('Datum (vplačilo 18ga v mesecu)')
plt.ylabel('Vrednost v EUR')
plt.title('Primerjava investicijskih instrumentov v obdobju Jan 2020 - Mar 2021')

plt.grid()

plt.legend()

#plt.savefig("pathname", dpi=260)
