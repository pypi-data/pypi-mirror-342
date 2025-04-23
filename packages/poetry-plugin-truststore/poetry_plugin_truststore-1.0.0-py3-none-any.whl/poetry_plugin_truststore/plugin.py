from importlib.metadata import version

import truststore
from cleo.io.io import IO
from poetry.plugins import Plugin
from poetry.poetry import Poetry


class PoetryPluginTruststore(Plugin):

    def activate(self, poetry: Poetry, io: IO):
        if io.is_verbose():
            ts_version = version("truststore")
            io.write_line(f'Using system cert store via Truststore {ts_version}')

        truststore.inject_into_ssl()
