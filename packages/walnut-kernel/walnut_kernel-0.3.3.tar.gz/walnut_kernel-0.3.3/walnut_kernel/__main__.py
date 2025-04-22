from .kernel import WalnutKernel
from . import config

if __name__ == "__main__":
    config.setup_path()
    WalnutKernel.run_as_main()
