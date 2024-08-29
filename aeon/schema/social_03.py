import json
import pandas as pd
import aeon.io.reader as _reader
from aeon.schema.streams import Stream


class Pose(Stream):

    def __init__(self, path):
        super().__init__(_reader.Pose(f"{path}_202_*"))


class EnvActiveConfigReader(_reader.JsonList):
    def __init__(self, pattern):
        super().__init__(pattern)

    def read(self, file):
        data = super().read(file)
        data["name"] = data["value"].apply(lambda x: x["name"])
        return data


class ActiveConfiguration(Stream):

    def __init__(self, path):
        super().__init__(EnvActiveConfigReader(f"{path}_ActiveConfiguration_*"))
