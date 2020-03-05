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
    volume: float = 0.0
    averageAcquiredPrice: float = 0.0
    profit: float = 0.0
    profitPercent: float = 0.0

class Main:
    def __init__(self):
        self.avanza = avanza.Avanza()

    def make_item(self, stock):
        return asdict(from_dict(data_class=Stock, data=stock))
    
    def merge_dicts(self, x, y):
        z = x.copy()
        z.update(y)
        return z

    def main(self):
        tabulate_list = []
        watchlists = self.avanza.watchlists()
        positions = self.avanza.positions()['instrumentPositions'][0]['positions']
        for watchlist in watchlists:
            if watchlist['name'] == 'Min bevakningslista':
                for stock in watchlist['orderbooks']:
                    for position in positions:
                        if stock == position['orderbookId']:
                            merged = self.merge_dicts(self.avanza.stock(stock), position)
                            tabulate_list.append(self.make_item(merged))
                            break
                    else:        
                        tabulate_list.append(self.make_item(self.avanza.stock(stock)))
        table = tabulate(tabulate_list, headers='keys', floatfmt='.2f', tablefmt='fancy_grid')
        print(table)

if __name__ == "__main__":
    logging.basicConfig(filename='avanza.log', level=logging.DEBUG)
    Main().main()
