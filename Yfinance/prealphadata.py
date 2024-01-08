import yfinance as yf
import datetime
import pandas as pd
from time import sleep

class Data:
    
    def __init__(self, symbol):
        """
        Constructeur de la classe Data.
        :param symbol: Symbole de l'action.
        """
        self.symbol = symbol
        self.currentprice = self.get_current_price()
        self.previousClose = yf.Ticker(self.symbol).info['previousClose'] # Permmant d'avoir accès au prix de clôture le plus récent
        self.change = self.calculate_change()

    def get_current_price(self):
        """
        Récupère le prix de clôture le plus récent pour un symbole donné.
        
        :param symbol: Symbole de l'action (par exemple, 'META' pour Meta Platforms Inc.).
        :return: Prix de clôture le plus récent de l'action.
        """
        # Récupère les données historiques pour le symbole spécifié sur une journée
        data = yf.Ticker(self.symbol).history(period='1d')
        
        # Récupère le prix de clôture le plus récent et le retourne
        return float('%.2f'%(data.iloc[-1]['Close']))
        pass

    def get_current_volume(self):
        """
        Récupère le volume de trading actuel pour un symbole donné.
        
        :param symbol: Symbole de l'action.
        :return: Volume de trading actuel formaté avec des séparateurs de milliers.
        """
        # Récupère les informations sur le volume pour le symbole spécifié
        volume = yf.Ticker(self.symbol).info['volume']
        
        # Formate le volume avec des séparateurs de milliers et le retourne
        return "{:,.0f}".format(volume)
        pass

    def calculate_change(self):
        """
        Calcule le changement absolu et en pourcentage par rapport à un prix de référence donné.
        
        :param current_price: Prix actuel.
        :param reference_price: Prix de référence.
        :return: Tuple contenant le changement absolu et le changement en pourcentage.
        """
        # Calcul du changement absolu
        
        current_price = self.get_current_price()
        absolute_change = current_price - self.previousClose
        
        # Calcul du changement en pourcentage
        percentage_change = (absolute_change / self.previousClose) * 100
        
        if self.previousClose > current_price:
            self.change = "%.2f (%.2f%%)" % (absolute_change, percentage_change)
        else:
            self.change = "+%.2f (+%.2f%%)" % (absolute_change, percentage_change)
        return self.change

    def get_info(self, mode = 0):
        """
        Récupère les informations importantes pour un symbole d'action donné.
        
        :param symbol: Symbole de l'action.
        :param new_current_price: Prix de clôture le plus récent.
        :return: Tuple contenant le prix actuel, le changement, le volume et l'objectif sur un an.
        """
        pass
def data_main(symbole):
    """
    Fonction principal pour récupérer et stocker les informations.
    """
    pass

        
        
        

# Boucle principale pour récupérer et stocker les informations

if __name__ == '__main__':
    symbole = 'meta'
    data_main(symbole)
