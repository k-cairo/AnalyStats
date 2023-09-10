import dataclasses


# E5
@dataclasses.dataclass
class E5MySQLConf:
    user: str = ""
    password: str = ""
    host: str = ""
    db_name: str = ""

    def parse_json(self, jsondict: dict) -> (bool, str):
        success: bool = True
        message: str = ""

        try:
            if "user" in jsondict and isinstance(jsondict["user"], str):
                self.user = jsondict["user"]
            else:
                success = False
                message = "user must be present and type of str"

            if success:
                if "password" in jsondict and isinstance(jsondict["password"], str):
                    self.password = jsondict["password"]
                else:
                    success = False
                    message = "password must be present and type of str"

            if success:
                if "host" in jsondict and isinstance(jsondict["host"], str):
                    self.host = jsondict["host"]
                else:
                    success = False
                    message = "host must be present and type of str"

            if success:
                if "db_name" in jsondict and isinstance(jsondict["db_name"], str):
                    self.db_name = jsondict["db_name"]
                else:
                    success = False
                    message = "db_name must be present and type of str"
        except Exception as ex:
            success = False
            message = str(ex)

        return success, message
