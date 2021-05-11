from contracts import Contracts

class TiktInital(Contracts):

    def getContractName(self):
        self.printO("Contract Name is " + self.function.name().call())

    def testInit(self,cts):
        self.printN("transfer token to iso contract")
        amount = 250000000 * self.DECIMAL
        cts.function.transfer(self.contractAddr,amount).transact()
        balance = cts.function.balanceOf(self.contractAddr).call()
        self.printO(self.contractAddr + " iso Balance has : " + str(balance) + "SWF")


    def testRW(self,amount,sender):
        self.printN(sender + " buy ")
        self.function.buy().transact({'from':sender,'value': amount * self.DECIMAL})
        balance = self.function.provided(sender).call()
        self.printO(sender + " iso buy Balance has : " + str(balance) + "HT")
        eBalance = self.w3.eth.getBalance(self.contractAddr)
        self.printO(self.contractAddr + " iso contract HT Balance has : " + str(eBalance) + "HT")


    def testClaim(self,cts,sender):
        self.printN(sender + " claim " )
        self.function.claim().transact({'from':sender})
        balance = cts.function.balanceOf(sender).call()
        self.printO(sender + " token Balance has : " + str(balance) + "swf")
        balance1 = self.function.provided(sender).call()
        self.printO(sender + " iso Balance has : " + str(balance1) + "HT")


    def testWithdrawProvidedHT(self):
        self.function.withdrawProvidedHT().transact()
        eBalance = self.w3.eth.getBalance(self.contractAddr)
        self.printO(self.contractAddr + " HT Balance has : " + str(eBalance))



    def testWithdrawUnclaimedSWF(self,cts):
        balance = cts.function.balanceOf(self.contractAddr).call()
        self.printO(self.contractAddr + " Balance has : " + str(balance))
        balance = cts.function.balanceOf(self.getDefaultAccount()).call()
        self.printO(self.contractAddr + " Balance has : " + str(balance))
        self.function.withdrawUnclaimedSWF().transact()
        balance = cts.function.balanceOf(self.contractAddr).call()
        self.printO(self.contractAddr + " Balance has : " + str(balance))
        balance = cts.function.balanceOf(self.getDefaultAccount()).call()
        self.printO(self.contractAddr + " Balance has : " + str(balance))


