import dataclasses

from e5toolbox.base.E5File import E5File


# E5
@dataclasses.dataclass
class E5AppConf:
    confjson: dict = dataclasses.field(default_factory=dict)

    get_countries_url: str = ""
    get_upcoming_matchs_url: str = ""

    # E5
    def load(self, pathfile: str) -> (bool, str):
        success: bool
        message: str

        try:
            if E5File.is_valid_path(isdir=False, path=pathfile):
                success, message, self.confjson = E5File.load_json(pathfile)
                if success:
                    success, message = self.parse_json()
            else:
                success = False
                message = f"Invalid json file : {pathfile}"
        except Exception as ex:
            success = False
            message = str(ex)

        return success, message

    # E5
    def parse_json(self) -> (bool, str):
        success: bool = True
        message: str = ""

        try:
            # Get Countries Url Section
            if "get_countries_url" in self.confjson and isinstance(self.confjson["get_countries_url"], str):
                self.get_countries_url = self.confjson["get_countries_url"]
            else:
                success = False
                message = "get_countries_url must be present and type or string"

            # Get Upcoming Matchs Url Section
            if success:
                if "get_upcoming_matchs_url" in self.confjson and isinstance(self.confjson["get_upcoming_matchs_url"], str):
                    self.get_upcoming_matchs_url = self.confjson["get_upcoming_matchs_url"]
                else:
                    success = False
                    message = "get_upcoming_matchs_url must be present and type or string"

        except Exception as ex:
            success = False
            message = str(ex)

        return success, message
