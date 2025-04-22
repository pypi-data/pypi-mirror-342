import os

def rm(path, missing_ok=True):
    try:
        os.remove(path)
    except FileNotFoundError:
        if not missing_ok:
            raise
