import dataclasses
import os

import simplejson


# E5
@dataclasses.dataclass
class E5File:

    # ---------- JSON -----------
    @classmethod
    def load_json(cls, fullpath: str) -> (bool, str, any):
        success = False
        message = ""
        data = None
        try:
            with open(file=fullpath, mode="r", encoding="utf-8") as reader:
                data = simplejson.load(reader)
            success = True
        except Exception as ex:
            message = ex
        return success, message, data

    # ---------- CHECK -----------
    @classmethod
    def is_valid_path(cls, isdir: bool, path: str) -> bool:
        return bool((isdir and os.path.isdir(path)) or (not isdir and os.path.isfile(path)))
