# Stratestic+  📈📊🛠️

[![codecov](https://codecov.io/gh/diogomatoschaves/stratestic/graph/badge.svg?token=4E2B0ZOH1K)](https://codecov.io/gh/diogomatoschaves/stratestic)
![tests_badge](https://github.com/diogomatoschaves/stratestic/actions/workflows/run-tests.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/stratestic.svg)](https://badge.fury.io/py/stratestic)

`stratestic` est une bibliothèque Python pour le backtesting, l'analyse et l'optimisation des stratégies de trading. 
Elle inclut un certain nombre de stratégies pré-implémentées, mais il est également possible de créer de nouvelles stratégies, ainsi que
de les combiner. Elle fournit une stratégie générale de Machine Learning, qui peut être adaptée à vos besoins spécifiques.

## Nouvelle fonctionnalité ajoutée

J'ai contribué à ce projet en ajoutant la stratégie Ichimoku, offrant ainsi un nouvel outil d'analyse technique à la bibliothèque. Le reste du code et des fonctionnalités sont l'œuvre de l'auteur original.

## Installation

    $ pip install stratestic

## Usage

1. [ Vectorized Backtesting ](#vectorized-backtesting)
2. [ Iterative Backtesting ](#iterative-backtesting)
3. [ Backtesting with leverage and margin ](#leverage) <br>
    3.1. [ Calculating the maximum allowed leverage ](#maximum-leverage)
4. [ Optimization ](#optimization) <br>
    4.1 [ Brute Force ](#brute-force) <br>
    4.2 [ Genetic Algorithm ](#genetic-algorithm)
5. [ Strategies ](#strategies) <br>
    5.1. [ Combined strategies](#combined-strategies) <br>
    5.2. [ Create new strategies](#new-strategies) <br>
    5.3. [ Machine Learning strategy ](#machine-learning)

<a name="vectorized-backtesting"></a>
### Vectorized Backtesting

The `VectorizedBacktester` is a backtesting class that allows you to test trading strategies
on historical price data. It has the advantage of being faster than the iterative backtesting, but at
a cost of flexibility, as it will be hard or outright not possible to accomplish this for some more 
complex strategies. For all the strategies provided by this library, vectorized backtesting is supported.

Below is an example of how to use it for the `MovingAverageCrossover` strategy:

```python
from stratestic.backtesting import VectorizedBacktester
from stratestic.strategies import MovingAverageCrossover

symbol = "BTCUSDT"
trading_costs = 0.1 # This should be in percentage, i.e. 0.1% 

mov_avg = MovingAverageCrossover(50, 200)

vect = VectorizedBacktester(  # Initializes the VectorizedBacktester class with the strategy.
    mov_avg,
    symbol,
    amount=1000,
    trading_costs=trading_costs
)
vect.load_data()  # Load the default sample data. You can pass your own DataFrame to 'load_data'
vect.run()  # Runs the backtest and shows the results
```

This will output the results in textual and graphical form.

```
************************************************************
                    BACKTESTING RESULTS                     
************************************************************
                          Overview                          
------------------------------------------------------------
Total Duration                          4 years and 38 weeks
Start Date                               2018-05-23 13:00:00
End Date                                 2023-02-13 01:00:00
Trading Costs [%]                                        0.1
Exposure Time [%]                                      100.0
Leverage [x]                                               1
Equity - Initial [USDT]                                 1000
Equity - Final [USDT]                                3215.96
Equity - Peak [USDT]                                 5356.87
------------------------------------------------------------
                          Returns                           
------------------------------------------------------------
Total Return [%]                                       221.6
Annualized Return [%]                                  21.49
Annualized Volatility [%]                              73.95
Buy & Hold Return [%]                                 175.98
------------------------------------------------------------
                         Drawdowns                          
------------------------------------------------------------
Max Drawdown [%]                                      -61.18
Avg Drawdown [%]                                        -8.2
Max Drawdown Duration                    1 year and 38 weeks
Avg Drawdown Duration                     3 weeks and 2 days
------------------------------------------------------------
                           Trades                           
------------------------------------------------------------
Total Trades                                             267
Win Rate [%]                                           32.21
Best Trade [%]                                         87.77
Worst Trade [%]                                       -21.11
Avg Trade [%]                                           0.44
Max Trade Duration                        5 weeks and 3 days
Avg Trade Duration                       6 days and 11 hours
Expectancy [%]                                           5.9
------------------------------------------------------------
                           Ratios                           
------------------------------------------------------------
Sharpe Ratio                                            0.33
Sortino Ratio                                           0.28
Calmar Ratio                                            0.35
Profit Factor                                            1.0
System Quality Number                                  -0.02
------------------------------------------------------------
************************************************************
```

<a name="iterative-backtesting"></a>
### Iterative Backtesting

The `IterativeBacktester` is a backtesting class that allows you to test trading strategies
on historical price data. It works by iterating through each historical data point and simulating
trades based on your strategy. This feature allows for a greater degree of flexibility, 
allowing you to add more complex logic to the strategies. Below is an example of how you would use this 
class to backtest the `MovingAverageConvergenceDivergence` strategy. 

```python
from stratestic.backtesting import IterativeBacktester
from stratestic.strategies import MovingAverageConvergenceDivergence

symbol = "BTCUSDT"

macd = MovingAverageConvergenceDivergence(26, 12, 9)

ite = IterativeBacktester(macd, symbol=symbol) # Initializes the IterativeBacktester class with the strategy
ite.load_data() # Load the default sample data. You can pass your own DataFrame to load_data
ite.run() # Runs the backtest and shows the results
```

<a name="strategies"></a>
### Strategies

#### Ichimoku Cloud Strategy

Vous pouvez utiliser la stratégie Ichimoku Cloud que j'ai implémentée :

```python
from stratestic.backtesting import VectorizedBacktester
from stratestic.strategies import IchimokuCloud

symbol = "BTCUSDT"
trading_costs = 0.1

# Initialiser la stratégie Ichimoku avec les paramètres par défaut
ichimoku = IchimokuCloud()

# Ou avec des paramètres personnalisés
# ichimoku = IchimokuCloud(tenkan_period=9, kijun_period=26, senkou_span_b_period=52, displacement=26)

vect = VectorizedBacktester(ichimoku, symbol, amount=1000, trading_costs=trading_costs)
vect.load_data()
vect.run()
```

<a name="combined-strategies"></a>
#### Combined strategies

It is possible to combine 2 or more strategies into one, by means of the `StrategyCombiner` class. The options
for combining the strategies are `Unanimous` or `Majority`. The `Unaninmous` option signals a buy or a sell
if all the individual strategy signals agree (unanimous), whereas the `Majority` method provides a buy a 
or sell signal if the majority of the individual strategy signals points in one direction. 

Here's an example of how that could be achieved:

```python
from stratestic.backtesting import VectorizedBacktester
from stratestic.strategies import MovingAverageCrossover, Momentum, BollingerBands, IchimokuCloud
from stratestic.backtesting.combining import StrategyCombiner

symbol = "BTCUSDT"
trading_costs = 0.1

mov_avg = MovingAverageCrossover(30, 200)
momentum = Momentum(70)
boll_bands = BollingerBands(20, 2)
ichimoku = IchimokuCloud()

# The strategies are passed on to StrategyCombiner as list.
combined = StrategyCombiner([mov_avg, momentum, boll_bands, ichimoku], method='Unanimous')

vect = VectorizedBacktester(combined, symbol, amount=1000, trading_costs=trading_costs)
vect.load_data() # Load the default sample data. You can pass your own DataFrame to 'load_data'

vect.run()
```

<a name="new-strategies"></a>
#### Create new strategies

This module comes with some default strategies ready to be used, but chances are you will want
to expand this and create your own strategies. This can be easily achieved by using the template class below, 
which inherits the `StrategyMixin` class:

```python
from collections import OrderedDict
from stratestic.strategies._mixin import StrategyMixin


class MyStrategy(StrategyMixin):
    """
    Description of my strategy

    Parameters
    ----------
    parameter1 : type
        Description of parameter1.
    parameter2 : type, optional
        Description of parameter2, by default default_value.

    Attributes
    ----------
    params : OrderedDict
        Parameters for the strategy, by default {"parameter1": lambda x: x}

    Methods
    -------
    __init__(self, parameter1, parameter2=default_value, **kwargs)
        Initializes the strategy object.
    update_data(self)
        Retrieves and prepares the data.
    calculate_positions(self, data)
        Calculates positions based on strategy rules.
    get_signal(self, row=None)
        Returns signal based on current data.
    """

    def __init__(
        self, 
        parameter1: <type>,
        parameter2: <type> = <some_default_value>,
        data=None,
        **kwargs
    ):
        """
        Initializes the strategy object.

        Parameters
        ----------
        parameter1 : type
            Description of parameter1.
        parameter2 : type, optional
            Description of parameter2, by default default_value.
        data : pd.DataFrame, optional
            Dataframe of OHLCV data, by default None.
        **kwargs : dict, optional
            Additional keyword arguments to be passed to parent class, by default None.
        """
        self._parameter1 = parameter1  # Each specific parameter that you want to add to the strategy
                                       # must be initalized in this manner, with a _ followed by the name 
                                       # of the parameter
        self._parameter2 = parameter2

        self.params = OrderedDict(
            parameter1=lambda x: <type>(x),
            parameter2=lambda x: <type>(x)
        ) 

        StrategyMixin.__init__(self, data, **kwargs)

    def update_data(self, data):
        """
        Updates the input data with additional columns required for the strategy.

        Parameters
        ----------
        data : pd.DataFrame
            OHLCV data to be updated.

        Returns
        -------
        pd.DataFrame
            Updated OHLCV data containing additional columns.
        """
        super().update_data(data)

        # Code to update data goes here. Check the given strategies for an example.
        
        return data

    def calculate_positions(self, data):
        """
        Calculates positions based on strategy rules.

        Parameters
        ----------
        data : pd.DataFrame
            OHLCV data.

        Returns
        -------
        pd.DataFrame
            OHLCV data with additional 'position' column containing -1 for short, 1 for long.
        """
        data["side"] =  # Code to calculate side goes here

        return data

    def get_signal(self, row=None):
        """
        Returns signal based on current data.

        Parameters
        ----------
        row : pd.Series, optional
            Row of OHLCV data to generate signal for, by default None.

        Returns
        -------
        int
            Signal (-1 for short, 1 for long, 0 for neutral).
        """
        # Code to generate signal goes here

        return signal

```

## Credit

Le projet original a été développé par [diogomatoschaves](https://github.com/diogomatoschaves/stratestic). J'ai simplement contribué en ajoutant la stratégie Ichimoku à l'ensemble des stratégies existantes.

Si vous êtes intéressé par un bot de trading qui s'intègre parfaitement à cette bibliothèque, consultez [MyCryptoBot](https://github.com/diogomatoschaves/MyCryptoBot).