
import requests

class Config:
    def __init__(self):
        self.symbols = {
            'oraichain-token': 'orai-orai12hzjxfh77wl572gdzct2fxv2arxcwh6gykc7qh',
            # 'oraichain': 'orai-orai12hzjxfh77wl572gdzct2fxv2arxcwh6gykc7qh',
            'airight': 'orai10ldgzued6zjp0mkqwsv2mux3ml50l97c74x8sg-orai',
            'oraidex': 'orai1lus0f0rhx8s03gdllx2n6vhkmf0536dv57wfge-orai',
            'atom':'orai-ibc%2FA2E2EEC9057A4A1C2C0A6A4C78B0239118DF5F278830F50B4A6BDD7A66506B78'
        }
    
    def get_symbol_price(self, symbol: str):
       pass

    def get_symbol_address(self, symbol: str):
        if symbol in self.symbols:
            return self.symbols.get(symbol)
    
if __name__ == '__main__':
    config = Config()
    print(config.get_symbol_address('airight'))  # Output: Airight
    print(config.get_symbol_address('atom'))  # Output: Binance Coin
