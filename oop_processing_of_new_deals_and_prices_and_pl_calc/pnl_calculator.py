class PnLCalculator:
    def __init__(self, 
                 file: str):
        self.file = file
        self.trades = {} # dict of trades with instruments as keys and dict of trade_ids as values
        self.prices = {} # dict of prices with instruments as keys and prices as values


    def process_all_events(self) -> None:
        # process all events line by line from self.file
        with open(self.file, "r") as f:
            lines = f.readlines()

        for line in lines:
            line = line.split()
            if line[0] == "TRADE":
                tradeId = int(line[1])
                instrumentId = line[2]
                buySell = line[3]
                price = int(line[4])
                self.process_trade(tradeId, instrumentId, buySell, price)
            elif line[0] == "PRICE_UPDATE":
                instrumentId = line[1]
                price = int(line[2])
                self.process_price_update(instrumentId, price)
            elif line[0] == "WORST_TRADE":
                instrumentId = line[1]
                print(instrumentId, 'worst trade id is', self.output_worst_trade(instrumentId))
            else:
                raise Exception("Malformed input!")


    def process_trade(self, 
                      trade_id: int, 
                      instrument_id: str, 
                      buy_sell: str, 
                      price: int) -> None:
        # add the trade to the trade dictionary
        if buy_sell == 'BUY':
            buy_sell = 1
        else:
            buy_sell = -1
        if instrument_id not in self.trades:
            self.trades[instrument_id] = {trade_id: [buy_sell, price]}
        else:
            self.trades[instrument_id][trade_id] = [buy_sell, price]
        

    def process_price_update(self, instrument_id: str, price: int) -> None:
        # update the price of the instrument in price dictionary
        self.prices[instrument_id] = price


    def output_worst_trade(self, instrument_id: str) -> str:
        # return id of the worst trade for given instrument_id
        worst_pl_per_vol = 1 # because looking for only negative trades
        if instrument_id in self.trades:
            for tr_id, values in self.trades[instrument_id].items():
                pl_per_vol = values[0] * (self.prices[instrument_id] - values[1])
                if pl_per_vol <= worst_pl_per_vol:
                    worst_pl_per_vol = pl_per_vol
                    worst_trade_id = tr_id
        if worst_pl_per_vol >= 0:
            return 'NO BAD TRADES'
        else:
            return worst_trade_id


if __name__ == "__main__()":
    # example of using PnLCalculator class
    calculator = PnLCalculator('events.txt')
    calculator.process_all_events()