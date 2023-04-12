from datetime import datetime

now_log = f"0_geral_{datetime.now().isoformat()}"


def log(msg="", tipo="NORMAL"):
    now = datetime.now().isoformat()
    with open(f"log/{now_log}_{tipo}.log", "a") as fd:
        fd.write(f"{now}: {msg}\n")


