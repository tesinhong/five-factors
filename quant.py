import os
os.environ['API_KEY'] = "{b4f4f166-a8c0-4f13-ad54-ff967efd9fd3}"
import qnt.data as qndata
import qnt.ta as qnta

futures = qndata.futures.load_data(min_date="2006-01-01")

price_open = futures.sel(field="open")
price_open_one_day_ago = qnta.shift(price_open, periods=1)

strategy = price_open - price_open_one_day_ago

weights = strategy / abs(strategy).sum("asset")

import qnt.output as output

output.write(weights)

#qnt.output.write(weights)

weights = output.clean(weights, futures, "futures")


