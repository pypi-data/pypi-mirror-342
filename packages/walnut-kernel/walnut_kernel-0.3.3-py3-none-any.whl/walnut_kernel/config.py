import os
from pathlib import Path as P

WALNUT_JAR = None
WALNUT_HOME = None
WALNUT_MEM = "16g"
JAVA = None

def setup_path():
    global WALNUT_HOME, WALNUT_JAR, WALNUT_MEM, JAVA
    if "JAVA" in os.environ:
        JAVA = P(os.environ["JAVA"])
    elif "JAVA_HOME" in os.environ:
        JAVA = P(os.environ["JAVA_HOME"])/"bin"/"java"
    if JAVA is None or not JAVA.is_file():
        JAVA = "java"
    if "WALNUT_MEM" in os.environ:
        WALNUT_MEM = os.environ["WALNUT_MEM"]
    if "WALNUT_HOME" in os.environ:
        WALNUT_HOME = P(os.environ["WALNUT_HOME"])
    else:
        WALNUT_HOME = P(os.environ["HOME"])
    if not WALNUT_HOME.is_dir() or not (WALNUT_HOME / "Result").is_dir():
        raise RuntimeError(
            "Please define WALNUT_HOME and make it point to a writable directory containing Walnut runtime files"
        )
    if "WALNUT_JAR" in os.environ:
        WALNUT_JAR = P(os.environ["WALNUT_JAR"])
    else:
        WALNUT_JAR = WALNUT_HOME / "walnut.jar"
    if not WALNUT_JAR.is_file():
        raise RuntimeError(
            "Please define WALNUT_JAR and make it point to a Walnut main jar"
        )
