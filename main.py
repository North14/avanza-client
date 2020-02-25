import constants
import logging
from avanza import avanza
from dacite import from_dict
from dataclasses import dataclass, asdict
from tabulate import tabulate

@dataclass
class Stock:
    name: str = '-'
    tickerSymbol: str = '-'
    currency: str = '-'
    buyPrice: float = 0.0
    sellPrice: float = 0.0
    highestPrice: float = 0.0
    lowestPrice: float = 0.0
    change: float = 0.0

def make_item(stock):
    return asdict(from_dict(data_class=Stock, data=stock))
    


def main(avanza_run):
    tabulate_list = []
    for cert in constants.certificates:
        tabulate_list.append(make_item(avanza_run.certificate_path(cert)))
    for stock in constants.stocks:
        tabulate_list.append(make_item(avanza_run.stock_path(stock)))
    table = tabulate(tabulate_list, headers='keys', floatfmt='.2f', tablefmt='fancy_grid')
    print(table)


if __name__ == "__main__":
    logging.basicConfig(filename='avanza.log', level=logging.DEBUG)
    avanza_run = avanza.Avanza({
            'username': '',
            'password': '',
            'totp_secret': ''
            })
    main(avanza_run)
