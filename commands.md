# List of all commands
All examples are with `prefix -`

## Main comments 
### help
To get the list of all commands and classes. Use `-help`.

### load
This command activates a certain class (called Cog in Discord terminology) and its commands. You can get the list of cogs from `-help`. Example: `-load Screener` activates all commands of Screener class.

### unload
This command deactivates a certain class (called Cog in Discord terminology) and its commands. You can get the list of cogs from `-help`. Example: `-unload Screener` deactivates all commands of Screener class.

### reload
This command reloads (deactivate and then activate) a certain class (called Cog in Discord terminology). You can get the list of cogs from `-help`. Example: `-reload Screener` loads the most updated version of the Screener class.


## Initialization

### alive 
Checks if the bot is alive. Example: `-alive`

## Screener 
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

### sympathy
This commands returns sympathys plays of a ticker. Use `-sympathy mara`


## Statistics
This class includes a list of functions for statistical analysis. 

### mean_return_1d
This command computes the number of times in the past (last 20 years) that a ticker experienced `c%` daily change and shows the average return in the following `d` days. Example: in `mean_return_1d TSLA 30 -1.5`, ticker is TSLA, `c=-1.5%` and `d=30`. 


### mean_return_kd
This command checks the price changes of a ticker in the past `d%` days, computes the number of times in the past that similar changes happened in past (last 20 years), and shows the average return in the following `f` days. Example: in `-mean_return_kd tsla 30 5`, ticker is TSLA, `d=5` and `f=30`. 

## Announcements 

## roi 
This returns the return-of-investment in a specified Discord channel. To activate, type `-roi` and then you will see `Write "stop" to stop, otherwise enter a new ROI entry as <ticker> / <buy> / <sell>`. To enter entry, follow the instrudction. Example: you had two trades one one TSLA with buy price 616.55 and sell at 636.12 and another one on NIO with buy at 38.9 and sell at 40.2. Enter `-roi` and then enter `TSLA/616.55/636.12`, then enter `NIO/38.9/40.2`, and finally enter `stop` to see your time-stampped return-of-investment report with your name and avatar.

## mywl
This prints your watchlist with your name and avatar in a specified Discord channel. To activate, type `-mywl <name>` where <name> is your watchlist name, like daily or weekely or any other name. By this command, you will see `Write "stop" to stop, otherwise enter a new WL entry as <ticker> / <message>`. To enter entry, follow the instrudction. Example: you have a weekly watchlist with TSLA and XOM. TSLA because it is a good buy point now, and XOM because the oil price is expected to increase. Enter `-mywl weekly` and then enter `TSLA/it is a good buy point now.`, then enter `XOM/the oil price is expected to increase.`, and finally enter `stop` to see your watchlist. 
