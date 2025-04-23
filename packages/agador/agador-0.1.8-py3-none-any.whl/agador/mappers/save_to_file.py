import os
import re
from datetime import timedelta
from typing import Union

from nornir.core.inventory import Host


class SaveResult:
    """
    Generic "take nornir getter result and save it to a file" class
    """

    def __init__(self, host: Host, base_dir: str, result: list[dict]):
        self._host = host
        self._base_dir = base_dir
        self._result = result

        self._output_file = self._set_output_file()
        self.write_to_file()

    def _get_hostname(self, netbox_name: str) -> str:
        """
        Removes stack member prefix from netbox hostnames
        """
        return re.sub(r"_\d$", "", netbox_name)

    def _set_output_file(self) -> str:
        """
        Uses nornir host role data to determine sub-folder
        and ensures its created at the right path
        """
        role = self._host.data["device_role"]["slug"]
        if not os.path.exists(f"{self._base_dir}/{role}"):
            os.makedirs(f"{self._base_dir}/{role}")

        return f"{self._base_dir}/{role}/{self._get_hostname(self._host.name)}"

    def write_to_file(self):
        """
        Saves data to file. Override in child classes if a
        different type of transformation needs to happen
        """
        result = self._result
        if isinstance(result, dict):
            result = [result]
        with open(self._output_file, "w", encoding="utf-8") as fh:
            fh.write(",".join(result[0].keys()) + "\n")

            for row in result:
                values = [str(r) for r in row]
                fh.writelines(",".join(values) + "\n" for r in result)


class SaveConfig(SaveResult):
    """
    Saves running config from "get_config" to a file, redacting
    out passwords
    """

    def write_to_file(self):

        with open(self._output_file, "w", encoding="utf-8") as fh:

            for line in self._result["running"].split("\n"):

                # cisco type 7 password redaction
                if re.search(r"(password|key) 7", line):
                    line = "!!!" + re.sub(
                        r"(password|key) 7 \S+", r"\g<1> [redacted]", line
                    )

                # juniper type 9 password redaction
                if re.search(r"(secret|password) \"$9$", line):
                    line = "#" + re.sub(
                        r"(secret|password) \S+", r"\g<1> [redacted]", line
                    )

                fh.write(f"{line}\n")
