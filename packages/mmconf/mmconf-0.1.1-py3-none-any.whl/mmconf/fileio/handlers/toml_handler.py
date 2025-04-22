import rtoml

from .base import BaseFileHandler


class TomlHandler(BaseFileHandler):

    def load_from_fileobj(self, file):
        return rtoml.load(file)

    def dump_to_fileobj(self, obj, file, **kwargs):
        rtoml.dump(obj, file, **kwargs)

    def dump_to_str(self, obj, **kwargs):
        return rtoml.dumps(obj, **kwargs)
