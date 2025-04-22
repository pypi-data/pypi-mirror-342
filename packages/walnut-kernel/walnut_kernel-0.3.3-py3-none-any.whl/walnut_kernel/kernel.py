from .magic import MyMagic
from . import config
from ._version import __version__
from metakernel.process_metakernel import ProcessMetaKernel
from metakernel.replwrap import REPLWrapper
from pexpect import spawn


class WalnutKernel(ProcessMetaKernel):
    # Identifiers:
    implementation = "Walnut"
    implementation_version = __version__
    language = "walnut"
    language_info = {
        "mimetype": "text/x-walnut",
        "name": "walnut",
        "codemirror_mode": "null",
        "language": "walnut",
        "file_extension": ".walnut",
        "version": __version__,
    }

    _banner = "Walnut Jupyter kernel"

    def __init__(self, *args, **kwargs):
        ProcessMetaKernel.__init__(self, *args, **kwargs)
        self.register_magics(MyMagic)

    def makeWrapper(self):
        child = spawn(
            f"{config.JAVA} -Xmx{config.WALNUT_MEM} -jar {config.WALNUT_JAR}",
            cwd=str(config.WALNUT_HOME),
            echo=True,
            encoding="utf-8",
        )
        child.expect(r"\n")
        return REPLWrapper(child, r"\[Walnut\]\$ ", None, echo=True)
