from data_connector import Pair
from tws_connection import ib, build_connection
import execution_model
import alpha_model
from portfolio_model import Portfolio

# TODO BUG es ist a) nicht geklärt wie geshortet werden kann bzw. verkauft. Das kann das Execution Model noch gar nicht. b) das Portfolio adjustment gibt lediglich die Position an, auf die Korrigiert werden soll. Gerade wird nicht überprüft wie die Position gerade überhaupt aussieht.
# TODO Die Log Funktion muss auch genutzt werden. Das Programm muss sich erinnern können welchen Signalen es am Ende gefolgt ist und welche nicht.bzw. auch prüfen wie das Portfolio aktuell aussieht und sie entsprechend updaten -> Initialisierungsfunktion
# TODO Wie komme ich an Lvl 1 (Live) data. Gerade funktioniert das noch nicht.
# TODO Was ist wenn kein Signal erzeugt wird? Was ist wenn kein Adjustment erzeugt wird? - Randfälle werden gerade noch nicht abgefangen.


# Check if a connection exists already
if not ib.isConnected():
    build_connection()


def connect_pairs(pairs):
    for pair in pairs:
        pair.connect_data()

if __name__ == "__main__":
    # Create a new Portfolio TODO Log the last Portfolio and load if the existet one in the past.
    portfolio = Portfolio()
    # Test data TODO Equation muss eingefügt werder sobald Test Daten verfügbar sind. (Siehe Alpha Model)
    test_pairs = [Pair(("AAPL", "MSFT"), "USD", (1,1,1)),
                  Pair(("GM", "TSLA"), "USD", (1,1,1)),
                  Pair(("AMZN", "CPNG"), "USD", (1,1,1))]

    connect_pairs(test_pairs)
    ib.sleep(3)
    
    # Generiere die initialen Signale TODO Sollte nur gemacht werden wenn es kein Portfolio log zum laden gibt.
    signals = alpha_model.generate_signals(test_pairs)

    # Erstelle das Initale Portfolio
    initial_execution = portfolio.analyze_signals(signals)  # TODO Wenn das eine Klasse ist warum return diese Methode ? Ist das gut so ?
    print(initial_execution)
    execution_model.execute_portfolio_adjustments(portfolio, initial_execution)
    # TODO implement controls through terminal
    while True:
        ib.sleep(10)
        new_adjustments = portfolio.optimize()
        execution_model.execute_portfolio_adjustments(portfolio, new_adjustments)

else:
    raise ImportError("This module is not for external use")

