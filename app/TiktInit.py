import sys

from contracts import Contracts
from TkitInitialOffering import TiktInital
from util.cfgReady import Cfg


def main(argv):
    if (len(argv) == 0):
        print("plaese choose net")
        exit(0)
    cfg = Cfg()
    cfg.getNet(argv[0])

    cts = Contracts("TiktToken","./tikt/tiktToken.sol",cfg,"0.6.12")
    cts.initAccounts()
    cts.deploy_contract_t()

    tikt = TiktInital("TiktInitialOffering","./tikt/tikt_ieo.sol",cfg,"0.6.12")
    tikt.deploy_contract_t(cts.contractAddr)
    tikt.initAccounts()

    tikt.testInit(cts)



    # tstMin(tikt,cts)
    tstMin_Max(tikt,cts)
    # tstWithdraw(tikt,cts)

def tstMin(tikt,cts):
    tikt.testRW(1, cts.accountList[1])
    tikt.testClaim(cts, cts.accountList[1])

def tstMin_Max(tikt,cts):
    tikt.testRW(1, cts.accountList[1])
    tikt.testRW(2, cts.accountList[1])
    tikt.testRW(2, cts.accountList[2])
    tikt.testRW(3, cts.accountList[3])
    tikt.testRW(4, cts.accountList[4])
    tikt.testRW(5, cts.accountList[5])
    # tikt.testClaim(cts, cts.accountList[1])
    # tikt.testClaim(cts, cts.accountList[2])
    # tikt.testClaim(cts, cts.accountList[3])
    # tikt.testClaim(cts, cts.accountList[4])
    # tikt.testClaim(cts, cts.accountList[5])

def tstWithdraw(tikt,cts):
    tikt.testWithdrawProvidedHT()
    tikt.testWithdrawUnclaimedSWF(cts)


if __name__ == "__main__":
   main(sys.argv[1:])