import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import pytz
from stratesticPlus.backtesting import VectorizedBacktester
import logging
import threading
import sys
from dateutil import parser
from tabulate import tabulate

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("forward_test.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

class ForwardTester:
    def __init__(
        self,
        symbol,
        strategy,
        initial_amount=1000,
        interval='1h',
        trading_costs=0.1,
        leverage=1
    ):
        self.symbol = symbol
        self.strategy = strategy
        self.initial_amount = initial_amount
        self.interval = interval
        self.trading_costs = trading_costs
        self.leverage = leverage
        self.all_data = pd.DataFrame()
        self.processed_data = pd.DataFrame()
        self.trade_ids = set()
        self.utc = pytz.UTC
        self.is_running = False
        self.current_balance = initial_amount
        self.backtester = None
        self.start_time = None
        self.end_time = None
        self.current_time = None
        self.running_thread = None
        self.trades_log = []
        self._determine_min_data_points()
        self._init_backtester()

    def _determine_min_data_points(self):
        params = []
        for param in ['slow_period', 'fast_period', 'sma_l', 'sma_s', 'window', 'n_long', 'n_short']:
            if hasattr(self.strategy, f'_{param}'):
                params.append(getattr(self.strategy, f'_{param}'))
        self.min_data_points = max(params) * 2 if params else 100
        logging.info(f"Minimum data points required: {self.min_data_points}")

    def _init_backtester(self):
        self.backtester = VectorizedBacktester(
            strategy=self.strategy,
            symbol=self.symbol,
            amount=self.initial_amount,
            trading_costs=self.trading_costs,
            leverage=int(self.leverage),
            margin_threshold=0.8
        )

    def _fetch_data(self, start_date, end_date):
        try:
            ticker = yf.Ticker(self.symbol)
            data = ticker.history(
                start=start_date,
                end=end_date,
                interval=self.interval,
                auto_adjust=False
            )
            if data.empty:
                return None
            data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
            data.columns = ['open', 'high', 'low', 'close', 'volume']
            data.index = data.index.tz_localize(self.utc) if data.index.tzinfo is None else data.index.tz_convert(self.utc)
            data = data[~data.index.duplicated(keep='last')].sort_index()
            return data
        except Exception as e:
            logging.error(f"Error fetching data: {e}")
            return None

    def _process_trades(self, current_trades):
        new_trades = []
        for trade in current_trades:
            trade_id = (str(trade.entry_date), trade.entry_price, trade.side)
            if trade_id not in self.trade_ids:
                new_trades.append(trade)
                self.trade_ids.add(trade_id)
                self.trades_log.append(trade)
                trade_info = (
                    f"TRADE - {self.symbol} - {'ACHAT' if trade.side == 1 else 'VENTE'} - "
                    f"Entrée: {trade.entry_price:.5f} à {trade.entry_date}, "
                    f"Unités: {trade.units:.2f}"
                )
                if hasattr(trade, 'exit_price') and trade.exit_price is not None:
                    profit_loss = "PROFIT" if trade.pnl > 0 else "PERTE"
                    trade_info += (
                        f" | Sortie: {trade.exit_price:.5f} à {trade.exit_date}, "
                        f"{profit_loss}: {trade.pnl:.2f}€"
                    )
                logging.info(trade_info)
        return new_trades
    
    def _fetch_all_historical_data(self, start_date, end_date):
        """
        Fetch all historical data between start and end dates.
        
        Args:
            start_date (datetime): Start date for historical data
            end_date (datetime): End date for historical data
            
        Returns:
            pd.DataFrame: Historical price data
        """
        try:
            # Add a buffer period before the start date to have enough data for indicators
            buffer_start = start_date - timedelta(days=30)  # 30 days buffer should be enough for most strategies
            
            logging.info(f"Fetching historical data from {buffer_start} to {end_date}")
            
            # Use yf.Ticker for reliability
            ticker = yf.Ticker(self.symbol)
            data = ticker.history(
                start=buffer_start,
                end=end_date,
                interval=self.interval,
                auto_adjust=False
            )
            
            if data.empty:
                logging.error(f"No data fetched for {self.symbol} between {buffer_start} and {end_date}")
                return None
                
            # Standardize columns
            data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
            data.columns = ['open', 'high', 'low', 'close', 'volume']
            data.index.name = 'date'
            
            # Ensure UTC timezone
            if data.index.tzinfo is None:
                data.index = data.index.tz_localize(self.utc)
            else:
                data.index = data.index.tz_convert(self.utc)
                
            # Remove duplicates and sort
            data = data[~data.index.duplicated(keep='last')]
            data = data.sort_index()
            
            logging.info(f"Successfully fetched {len(data)} data points")
            return data
            
        except Exception as e:
            logging.error(f"Error fetching historical data: {e}")
            return None

    def _run_forward_test(self):
        if self.all_data.empty:
            self.all_data = self._fetch_data(self.start_time - timedelta(days=30), self.end_time)
        if self.all_data.empty:
            logging.error("No data available")
            self.is_running = False
            return

        historical_data = self.all_data[self.all_data.index <= datetime.now(self.utc)]
        time_indices = historical_data.index[
            (historical_data.index >= self.start_time) &
            (historical_data.index <= self.end_time)
        ]
        for idx in time_indices:
            if not self.is_running:
                break
            self.current_time = idx
            current_data = self.all_data[self.all_data.index <= self.current_time]
            if len(current_data) < self.min_data_points:
                continue
            try:
                self.backtester.load_data(current_data.copy())
                result = self.backtester.run(print_results=False, plot_results=False)
                if result:
                    perf, _, _ = result
                    self.current_balance = self.initial_amount * (1 + perf/100)
                self._process_trades(getattr(self.backtester, 'trades', []))
                self._log_progress(idx, time_indices)
            except Exception as e:
                logging.error(f"Error processing {idx}: {e}")

        if datetime.now(self.utc) < self.end_time:
            self._live_trading_loop()

        self._final_run()

    def _log_progress(self, current_idx, time_indices):
        progress = (time_indices.get_loc(current_idx) + 1) / len(time_indices) * 100
        elapsed = current_idx - self.start_time
        remaining = self.end_time - current_idx
        logging.info(
            f"PROGRESSION [{progress:.1f}%] - Date: {current_idx}, "
            f"Balance: {self.current_balance:.2f}€, "
            f"P&L: {(self.current_balance - self.initial_amount):.2f}€"
        )

    def _live_trading_loop(self):
        interval_td = self._get_interval_timedelta()
        next_time = self.all_data.index[-1] + interval_td
        while next_time <= self.end_time and self.is_running:
            now = datetime.now(self.utc)
            if next_time > now:
                time.sleep((next_time - now).total_seconds())
            new_data = self._fetch_data(next_time - interval_td, next_time)
            if new_data is not None and not new_data.empty:
                self.all_data = pd.concat([self.all_data, new_data])
                self.backtester.load_data(self.all_data.copy())
                self.backtester.run(print_results=False, plot_results=False)
                self.current_time = next_time
                self._process_trades(getattr(self.backtester, 'trades', []))
                self.current_balance = self.backtester.amount  # Assuming backtester updates amount
                logging.info(f"Live update at {next_time}: Balance {self.current_balance:.2f}€")
            next_time += interval_td

    def _get_interval_timedelta(self):
        interval_map = {
            '1m': timedelta(minutes=1),
            '1h': timedelta(hours=1),
            '1d': timedelta(days=1),
        }
        return interval_map.get(self.interval, timedelta(hours=1))


    def _final_run(self):
        """Final run and display complete results."""
        if not self.is_running:
            return

        logging.info("=" * 50)
        logging.info("RÉSULTATS FINAUX DU FORWARD TEST")
        logging.info("=" * 50)
        
        try:
            if not self.all_data.empty:
                # Get only the data in the specified time range
                test_data = self.all_data[(self.all_data.index >= self.start_time) & 
                                          (self.all_data.index <= self.end_time)]
                
                # Run backtest on the full period
                self.backtester.load_data(data=test_data.copy())
                result = self.backtester.run(print_results=False, plot_results=False)

                metrics = {
                    'Symbole': self.symbol,
                    'Période de Test': f"{self.start_time.strftime('%Y-%m-%d %H:%M')} à {self.end_time.strftime('%Y-%m-%d %H:%M')}",
                    'Durée': str(self.end_time - self.start_time).split('.')[0],
                    'Capital Initial': f"{self.initial_amount:.2f}€",
                    'Balance Finale': f"{self.current_balance:.2f}€",
                    'Profit/Perte': f"{(self.current_balance - self.initial_amount):.2f}€",
                    'Rendement Total': "N/A",
                    'Surperformance': "N/A",
                    'Nombre de Trades': len(self.trades_log),
                    'Taux de Réussite': "N/A",
                    'Drawdown Maximum': "N/A"
                }

                if result is not None:
                    perf, outperf, results = result
                    
                    # Add calculated metrics if available
                    if perf is not None:
                        metrics['Rendement Total'] = f"{perf:.2f}%"
                    if outperf is not None:
                        metrics['Surperformance'] = f"{outperf:.2f}%"
                    if results:
                        if 'win_rate' in results:
                            metrics['Taux de Réussite'] = f"{results['win_rate']:.2f}%"
                        if 'max_drawdown' in results:
                            metrics['Drawdown Maximum'] = f"{results['max_drawdown']:.2f}%"

                # Display metrics as a nice table
                table_data = [[k, v] for k, v in metrics.items()]
                print(tabulate(table_data, tablefmt="grid"))
                
                # Log the trades summary
                if self.trades_log:
                    logging.info("=" * 50)
                    logging.info(f"RÉSUMÉ DES TRADES ({len(self.trades_log)} total):")
                    logging.info("=" * 50)
                    
                    winning_trades = [t for t in self.trades_log if hasattr(t, 'pnl') and t.pnl > 0]
                    losing_trades = [t for t in self.trades_log if hasattr(t, 'pnl') and t.pnl <= 0]
                    
                    logging.info(f"Trades gagnants: {len(winning_trades)} ({len(winning_trades)/len(self.trades_log)*100:.1f}%)")
                    logging.info(f"Trades perdants: {len(losing_trades)} ({len(losing_trades)/len(self.trades_log)*100:.1f}%)")
                    
                    if winning_trades:
                        avg_win = sum(t.pnl for t in winning_trades) / len(winning_trades)
                        logging.info(f"Gain moyen par trade gagnant: {avg_win:.2f}€")
                    
                    if losing_trades:
                        avg_loss = sum(t.pnl for t in losing_trades) / len(losing_trades)
                        logging.info(f"Perte moyenne par trade perdant: {avg_loss:.2f}€")
                
                # Generate visual output with the backtester
                try:
                    self.backtester.run(print_results=True, plot_results=True)
                except Exception as e:
                    logging.warning(f"Could not display visual results: {e}")
                
            else:
                logging.warning("No data collected during test. No results to display.")

        except Exception as e:
            logging.error(f"Error during finalization: {e}")

        self.is_running = False
        logging.info("Forward test terminé")

    def _validate_dates(self, start_date, end_date):
        """Validate that dates are in the correct format and make sense."""
        if start_date >= end_date:
            raise ValueError("La date de début doit être antérieure à la date de fin")
            
        # Check if dates are in the future
        now = datetime.now(self.utc)
        if end_date > now:
            logging.warning("La date de fin est dans le futur. Le test s'arrêtera à la dernière donnée disponible.")

    def start(self, start_date, end_date, strategy_info=None):
        """
        Start the forward test between specified dates.

        Args:
            start_date (datetime): Start datetime for the test.
            end_date (datetime): End datetime for the test.
            strategy_info (dict, optional): Information about the strategy for logging.
        """
        if self.is_running:
            logging.warning("Un test forward est déjà en cours.")
            return
            
        # Ensure dates are in UTC timezone
        if start_date.tzinfo is None:
            start_date = start_date.replace(tzinfo=self.utc)
        else:
            start_date = start_date.astimezone(self.utc)
            
        if end_date.tzinfo is None:
            end_date = end_date.replace(tzinfo=self.utc)
        else:
            end_date = end_date.astimezone(self.utc)
            
        try:
            self._validate_dates(start_date, end_date)
        except ValueError as e:
            logging.error(f"Erreur de validation des dates: {e}")
            return
            
        self.start_time = start_date
        self.end_time = end_date
        self.all_data = pd.DataFrame()
        self.processed_data = pd.DataFrame()
        self.trade_ids = set()
        self.trades_log = []
        self.current_balance = self.initial_amount
        self._init_backtester()
        
        # Fetch all historical data for the period
        self.all_data = self._fetch_all_historical_data(start_date, end_date)
        if self.all_data is None or self.all_data.empty:
            logging.error("Impossible de récupérer les données historiques. Le test ne peut pas démarrer.")
            return
            
        # Display starting information
        logging.info("=" * 50)
        logging.info("DÉMARRAGE DU FORWARD TEST")
        logging.info("=" * 50)
        logging.info(f"Symbole: {self.symbol}")
        logging.info(f"Début: {self.start_time}")
        logging.info(f"Fin: {self.end_time}")
        logging.info(f"Durée: {self.end_time - self.start_time}")
        logging.info(f"Intervalle de données: {self.interval}")
        logging.info(f"Capital initial: {self.initial_amount}€")
        
        # Display strategy information if provided
        if strategy_info:
            logging.info("=" * 50)
            logging.info("PARAMÈTRES DE LA STRATÉGIE")
            logging.info("=" * 50)
            for key, value in strategy_info.items():
                logging.info(f"{key}: {value}")
        
        logging.info("=" * 50)
        
        self.is_running = True
        self.running_thread = threading.Thread(target=self._run_forward_test)
        self.running_thread.daemon = True
        self.running_thread.start()

    def stop(self):
        """Stop the running forward test."""
        if not self.is_running:
            logging.warning("Aucun test forward n'est en cours.")
            return

        logging.info("Arrêt du test forward...")
        self.is_running = False

        if self.running_thread and self.running_thread.is_alive():
            self.running_thread.join(timeout=10)

        self._final_run()
        
    def get_results_dataframe(self):
        """Return a dataframe with the processed results."""
        return self.processed_data
        
    def save_results(self, filename=None):
        """Save the results to a CSV file."""
        if self.processed_data.empty:
            logging.warning("Pas de données à sauvegarder.")
            return
            
        if filename is None:
            filename = f"forward_test_{self.symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
        self.processed_data.to_csv(filename)
        logging.info(f"Résultats sauvegardés dans {filename}")


def get_user_input():
    """Get user input for the forward test."""
    print("\n=== CONFIGURATION DU TEST FORWARD ===\n")
    
    # Get symbol
    symbol = input("Entrez le symbole à trader (ex: EURUSD=X, AAPL): ").strip()
    
    # Get interval
    valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
    print(f"\nIntervalles disponibles: {', '.join(valid_intervals)}")
    interval = input("Choisissez l'intervalle de données (défaut: 1h): ").strip() or '1h'
    
    while interval not in valid_intervals:
        print(f"Intervalle invalide. Veuillez choisir parmi: {', '.join(valid_intervals)}")
        interval = input("Choisissez l'intervalle de données (défaut: 1h): ").strip() or '1h'
    
    # Get dates
    print("\nFormat de date: YYYY-MM-DD HH:MM ou YYYY-MM-DD (pour minuit)")
    start_date_str = input("Date de début: ").strip()
    end_date_str = input("Date de fin: ").strip()
    
    try:
        start_date = parser.parse(start_date_str)
        end_date = parser.parse(end_date_str)
    except Exception as e:
        print(f"Erreur de format de date: {e}")
        print("Utilisation des dates par défaut: derniers 30 jours")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
    
    # Get initial capital
    try:
        initial_amount = float(input("\nCapital initial (défaut: 1000€): ").strip() or 1000)
    except ValueError:
        print("Montant invalide. Utilisation du montant par défaut: 1000€")
        initial_amount = 1000
    
    # Get trading costs
    try:
        trading_costs = float(input("Coûts de trading en % (défaut: 0.1): ").strip() or 0.1)
    except ValueError:
        print("Valeur invalide. Utilisation de la valeur par défaut: 0.1%")
        trading_costs = 0.1
    
    # Get leverage
    try:
        leverage = float(input("Levier financier (défaut: 1): ").strip() or 1)
    except ValueError:
        print("Valeur invalide. Utilisation de la valeur par défaut: 1")
        leverage = 1
    
    # Get strategy
    print("\n=== CHOIX DE LA STRATÉGIE ===")
    print("1. MovingAverageCrossover")
    print("2. BollingerBands")
    print("3. MACD (Moving Average Convergence Divergence)")
    
    strategy_choice = input("\nChoisissez une stratégie (1-5): ").strip()
    
    strategy = None
    strategy_info = {}
    
    from stratesticPlus.strategies import (
        MovingAverageCrossover, BollingerBands,
         MovingAverageConvergenceDivergence
    )
    
    if strategy_choice == "1":
        try:
            sma_s = int(input("Période courte SMA (défaut: 20): ").strip() or 20)
            sma_l = int(input("Période longue SMA (défaut: 50): ").strip() or 50)
            strategy = MovingAverageCrossover(sma_s, sma_l)
            strategy_info = {"Nom": "Moving Average Crossover", "SMA Court": sma_s, "SMA Long": sma_l}
        except ValueError:
            print("Valeurs invalides. Utilisation des valeurs par défaut: 20, 50")
            strategy = MovingAverageCrossover(20, 50)
            strategy_info = {"Nom": "Moving Average Crossover", "SMA Court": 20, "SMA Long": 50}
    
    elif strategy_choice == "2":
        try:
            window = int(input("Période (défaut: 20): ").strip() or 20)
            num_std = float(input("Nombre d'écarts types (défaut: 2.0): ").strip() or 2.0)
            strategy = BollingerBands(window, num_std)
            strategy_info = {"Nom": "Bollinger Bands", "Période": window, "Écarts types": num_std}
        except ValueError:
            print("Valeurs invalides. Utilisation des valeurs par défaut: 20, 2.0")
            strategy = BollingerBands(20, 2.0)
            strategy_info = {"Nom": "Bollinger Bands", "Période": 20, "Écarts types": 2.0}
    
    elif strategy_choice == "3":
        try:
            window = int(input("Période RSI (défaut: 14): ").strip() or 14)
            oversold = float(input("Niveau de survente (défaut: 30): ").strip() or 30)
            overbought = float(input("Niveau de surachat (défaut: 70): ").strip() or 70)
            strategy_info = {"Nom": "RSI", "Période": window, "Survente": oversold, "Surachat": overbought}
        except ValueError:
            print("Valeurs invalides. Utilisation des valeurs par défaut: 14, 30, 70")
            strategy_info = {"Nom": "RSI", "Période": 14, "Survente": 30, "Surachat": 70}
    
    elif strategy_choice == "4":
        try:
            slow = int(input("Période lente (défaut: 26): ").strip() or 26)
            fast = int(input("Période rapide (défaut: 12): ").strip() or 12)
            signal = int(input("Période signal (défaut: 9): ").strip() or 9)
            strategy = MovingAverageConvergenceDivergence(slow, fast, signal)
            strategy_info = {"Nom": "MACD", "Période lente": slow, "Période rapide": fast, "Signal": signal}
        except ValueError:
            print("Valeurs invalides. Utilisation des valeurs par défaut: 26, 12, 9")
            strategy = MovingAverageConvergenceDivergence(26, 12, 9)
            strategy_info = {"Nom": "MACD", "Période lente": 26, "Période rapide": 12, "Signal": 9}
    
    
    else:
        print("Choix invalide. Utilisation de MovingAverageCrossover par défaut")
        strategy = MovingAverageCrossover(20, 50)
        strategy_info = {"Nom": "Moving Average Crossover", "SMA Court": 20, "SMA Long": 50}
    
    return {
        'symbol': symbol,
        'interval': interval,
        'start_date': start_date,
        'end_date': end_date,
        'initial_amount': initial_amount,
        'trading_costs': trading_costs,
        'leverage': leverage,
        'strategy': strategy,
        'strategy_info': strategy_info
    }


if __name__ == "__main__":
    print("\n============================================")
    print("  STRATESTIC FORWARD TESTER")
    print("============================================\n")
    
    try:
        # Get user configuration
        config = get_user_input()
        
        # Initialize tester with user config
        tester = ForwardTester(
            symbol=config['symbol'],
            strategy=config['strategy'],
            initial_amount=config['initial_amount'],
            interval=config['interval'],
            trading_costs=config['trading_costs'],
            leverage=int(config['leverage'])
        )
        
        print("\nDémarrage du test forward...\n")
        
        # Start the test
        tester.start(
            start_date=config['start_date'],
            end_date=config['end_date'],
            strategy_info=config['strategy_info']
        )
        
        # Wait for test to complete
        try:
            while tester.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nTest interrompu par l'utilisateur. Arrêt en cours...")
            tester.stop()
            
        # Save results if the test ran
        if hasattr(tester, 'processed_data') and not tester.processed_data.empty:
            save_choice = input("\nSouhaitez-vous sauvegarder les résultats? (o/n): ").lower().strip()
            if save_choice.startswith('o'):
                filename = input("Nom du fichier (laissez vide pour nom par défaut): ").strip()
                tester.save_results(filename if filename else None)
        
    except Exception as e:
        logging.error(f"Erreur pendant l'exécution: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nTest terminé. Consultez le fichier 'forward_test.log' pour plus de détails.")