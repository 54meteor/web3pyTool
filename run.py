import sys
from app.util.cfgReady import Cfg
from app.contracts import Contracts

def main(argv):
    if(len(argv) == 0):
        print("plaese choose net")
        exit(0)
    cfg = Cfg()
    cfg.getNet(argv[0])
    token = Contracts("ArmorsToken","ArmorsToken.sol",cfg,"0.5.0")
    token.deploy_contract_t(cfg.address)
    mdx = Contracts("MdxToken","mdx.sol",cfg,"0.6.12")
    mdx.deploy_contract_t()

if __name__ == "__main__":
   main(sys.argv[1:])