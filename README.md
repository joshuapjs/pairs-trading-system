# pairs-trading

Please first have a look at the [Disclaimer](#Disclaimer)

This is an implementation of a Pairs Trading System written in Python. The Trading System interacts directly with the Trader-Workstation (TWS) from Interactive Brokers. The Project focuses on the technical side and serves an educational purpose only.

I intentionally kept certain parts of the System very rudimentary, e.g. the Execution Model. On the one hand I aspire to implement other Systems using other languages soon (I am happy to receive your Pull request if you want to add something). On the other hand I don't want anyone to come up with the idea to plug his fortune into this System and the further I develop it the more tempting this idea might become I suppose.

This appears to be an ideal time to make the repository public, allowing others with a shared interest in the applications of technology and mathematics in financial markets to discover and leverage this project to inspire their own initiatives.

# Features

The Trading System will create its own SQLite file, and respective Tables to store its trades and signals that were generated. It will remember which signals were used for its positions if the the bot is switch off.

First of all the Model will generate Signals. In the second step those Signals will be analyzed and if possible executed. You can change the Variables in `constant.py` to influence how much capital is allocated on how many different trades. In the last step the Portfolio will try to optimize itself by looking into the opportunity costs of Signals that could not be followed because all capital was allocated and comparing them with the potential of its current positions.

The Trading System is build out of different parts, including an Alpha Model, Execution Model, a Portfolio Model and more. Each Instance will print to the Terminal to inform the user about its most recent actions.

# What is Pairs Trading ? 

Pairs Trading is theoretically a market independed trading strategy. Market independened means, even if stocks in general loose value because e.g. the Economic Situation is unfortunate, the strategy will still be able to generate positive returns. Such returns are called $\alpha$-Returns because in the CAPM (Capital Asset Pricing Model) The returns are captured in the constant of the Regression.

$$
R_{s} = \alpha + \beta \cdot (R_{m} - R_{f})
$$

According to the CAPM, the returns of the stocks we are interest in ($R_{s}$), can be traced back on the the market returns ($R_{m}$) minus the Risk-Free-Rate ($R_{f}$). While there is some cotroversy around it, the CAPM was actually very successful by explaining stock returns in the past. The name of $\alpha$ returns is still widely used to discribe those "risk free" returns.

Pairs trading involves recognizing pairs, i.e. a collection of different stocks whose prices are related to each other so that a deviation from their equilibrium can be exploited. This can be achieved by selling $\text{stock}_{a}$ when its price is overvalued in terms of $\text{stock}_{b}$, while buying $\text{stock}_{b}$ at the same time to profit from the reversion to their equilibrium. One such measure, suitable as a starting point to find Pairs, would be Cointegration. As the internet provides an abundance of further information around this topic (for free) I would encourage the curious reader to continue with one of the other resources.

# Prerequisites

One major requirement is an Account at interactive Brokers that is sufficiently funded to be eligible to receive Market Data. Besides that there are a couple of dependencies.

A `.txt` file is included in the folder `env`, enabling the reproduction of my environment explained [here](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#building-identical-conda-environments).

Beyond that, it is required to create a file named `personal_constants.py`, including the `ACCOUNT_NUMBER` of your Paper Trading Account.

The Pairs in the file have no durable relationship at all, they are only in there for demostration purposes.

# Usage

Python 3.11.5 or higher is recommended as I used this version for development. The Program will only run if TWS is set up correctly to allow interactions with a Program. Please disable `API > Setting > Read-Only API`.

If all requirements above are fullfilled you can log into your Paper Trading Account and run the Program from the Terminal. Please make sure to `cd` to the directory where the clone of this Repository is stored and run it through `python pairs-trading`.

To end the Program it is safe to end the program manually via `ctrl + c` from your Terminal.

# License

This project is licensed by the GNU Licence. Please visit [LICENSE](docs/LICENSE.md) for further information.

# Disclaimer

This trading bot is provided solely for educational and informational purposes and is not intended as financial or investment advice. All decisions made by the bot are automated and provided "as is" without any warranty. Users should not rely on the bot's outputs for making real-world trading or investment decisions. Consultation with a qualified financial advisor is recommended for any trading or investment activities. The creators of this bot assume no responsibility for any losses or damages resulting from its use. The Bot must not be used in a live Trading Environment of interactive Broker. Usage is only allowed in Paper Trading Accounts.
