import os
from web3 import Web3
import solcx
import time


class Contracts():

    RPC = ""
    prefix = "<stdin>:"
    ROOT_PATH = os.path.split(os.path.abspath(__name__))[0]
    ZERO = "0x0000000000000000000000000000000000000000"
    DECIMAL = 10 ** 18
    NOTICE = "[\033[32mNOTICE\033[0m]"
    ERROR = "[\033[31mERROR\033[0m]"
    WARNING = "[\033[33mWARNING\033[0m]"
    OPERATING = "[\033[36mOPERATING\033[0m]"
    SUCCESS = "[\033[35mSUCCESS\033[0m]"
    abi = ""
    bin = ""
    CFG = ""

    def __init__(self,
                 contractName,
                 contractFileName,
                 cfg,
                 version="0.5.16",
                 contractPath="/contracts/"):
        self.CFG = cfg
        self.RPC = cfg.url
        self.printN("Project Strat")
        self.contractName = contractName
        self.contractFileName = contractFileName
        self.w3 = Web3(Web3.HTTPProvider(self.RPC))
        self.version = version
        self.CONTRACTS_PATH = self.ROOT_PATH + contractPath
        solcx.install_solc(self.version)
        # self.initAccounts()

    def initAccounts(self):
        self.accountList = self.w3.eth.accounts
        self.w3.eth.defaultAccount = self.accountList[0]

    def setDefaultAccount(self,account):
        self.w3.eth.defaultAccount = account

    def getDefaultAccount(self):
        return self.w3.eth.defaultAccount

    def readContract(self):
        with open(self.CONTRACTS_PATH + self.contractFileName,'r') as fp:
            content = fp.read()
            return  content

    def compile_source_file(self):
        self.printN("Compiling Contract... " + self.contractFileName)
        return solcx.compile_source(
            self.readContract(),
            output_values=["abi", "bin"],
            solc_version=self.version,
            optimize = True
        )

    def getContract(self):
        return self.compile_source_file().get(self.prefix + self.contractName)

    def compile_source_file1(self,f):
        self.printN("Compiling Contract... " + self.contractFileName)
        return solcx.compile_files(
            f,
            output_values=["abi", "bin"],
            solc_version=self.version,
            optimize = True
        )

    def deploy_contract_t(self,*pm):
        self.printN("Ready to Contract... " + self.contractFileName)
        contract_info = self.getContract()
        self.abi = contract_info['abi']
        self.bin = contract_info['bin']
        self.printN("Deploying Contract start... " + self.contractFileName)
        contract = self.w3.eth.contract(
            abi=self.abi,
            bytecode=self.bin).constructor(*pm)
        self.printN("Configing Contract... " + self.contractFileName)
        wallet_address = self.w3.toChecksumAddress(self.CFG.address)
        nonce = self.w3.eth.getTransactionCount(wallet_address)
        txn_dict = contract.buildTransaction({
            'gas': 8000000,
            'nonce': nonce
        })
        self.printN("Signing transaction... " + self.contractFileName)
        signed_txn = self.w3.eth.account.sign_transaction(txn_dict, private_key=self.CFG.account)
        self.printN("Sending transaction ... " + self.contractFileName)
        tx_hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        self.printN("Penging... hash is: " + self.w3.toHex(tx_hash))
        pause = int(self.CFG.time)
        time.sleep(pause)
        self.contractAddr = self.w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        self.printN("Deployed Contract end... Address:" + self.contractAddr)
        self.initContract()

    def initContract(self):
        self.printN("Mission Compeleted ")
        checksum_address = self.w3.toChecksumAddress(self.contractAddr)
        self.contract = self.w3.eth.contract(address=checksum_address, abi=self.abi)
        self.function = self.contract.functions

    def transact(self,obj,account):
        try:
            return obj.transact({"from":account})
        except ValueError as e:
            self.printE("error catched : " + e.args[0])
            return

    def call(self,obj):
        try:
            return obj.call()
        except ValueError as e:
            self.printE("error catched : " + e.args[0])
            return

    def printRed(self,str):
        print("\033[31m" + str +  "\033[0m")

    def textG(self,str):
        return "\033[32m" + str +  "\033[0m"

    def textR(self,str):
        return "\033[31m" + str + "\033[0m"

    def printN(self,str):
        print(self.NOTICE + str)

    def printW(self,str):
        print(self.WARNING + str)

    def printE(self,str):
        print(self.ERROR + str)

    def printO(self,str):
        print(self.OPERATING + str)

    def printS(self,str):
        print(self.SUCCESS + str)