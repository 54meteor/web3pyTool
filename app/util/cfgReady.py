import configparser

class Cfg():

    config = configparser.ConfigParser()
    path = "cfg.ini"
    config.read(path)
    url = ''
    chainid = ''
    address = ''
    account = ''

    def getNet(self,tag='mainnet'):
        value = self.config.items(tag)
        self.url = value[0][1]
        self.chainid = value[1][1]
        self.address = value[2][1]
        self.account = value[3][1]
        self.time = value[4][1]

