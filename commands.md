# List of all commands
All examples are with `prefix -`


## Screeer 
This class includes a set of functions to screen the market.

### price
This command gets multiple tickers _separated by space_ and returns their price changes. Example: `-price msft aapl tsla`

### wl
This command returns the price changes of a watchlist. There are multiple names associated to any watchlist. Example: `-wl ev`

`-wl weed` and `-wl weeds`, and `-wl pots` all return the same watchlist. 

List of available watchlists:
- EV
- Weed
- NFT
- 3D printing
- Crypto
- Battery
- Oiler
- Shippers
- Precious metals
- Space
- WSB
- Sustainability

## Statistics
This class includes a list of functions for statistical analysis. 

### mean_return_1d
This command copmputes the number of times in the past that a ticker experienced `c%` daily change and shows the average return in the following `d` days. Example: in `mean_return_1d TSLA 30 -1.5`, ticker is TSLA, `c=-1.5%` and `d=30`. 




### mean_return_kd
This command returns the price changes of a watchlist. There are multiple names associated to any watchlist. Example: `-wl ev`

