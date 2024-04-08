import gc
import os
import re
import sys
import yaml
import warnings

from deoplete.source.base import Base
from operator import itemgetter
from typing import Optional

warnings.filterwarnings('ignore')


# GitHub: use config repo.
class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name: Optional[str] = 'pressure'
        self.filetypes = ['ruby']
        mark_synbol: Optional[str] = '[virtual_environment]'
        self.mark = str(mark_synbol)
        ruby_match = [r'\.[a-zA-Z0-9_?!]*|[a-zA-Z]\w*::\w*']
        slash_no_match = [r'[;/[^¥/]\*/]']
        self.input_pattern = '|'.join(ruby_match + slash_no_match)
        self.rank = 500

    def get_complete_position(self, context):
        m = re.search('[a-zA-Z0-9_?!]*$', context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):
        try:
            # It doesn't support python4 yet.
            py_mj: Optional[int] = sys.version_info[0]
            py_mi: Optional[int] = sys.version_info[1]

            # 3.5 and higher, 4.x or less,python version is required.
            if (py_mj == 3 and py_mi > 4) or (py_mj < 4):

                # Settings, Config path is true/false change.
                config_load: Optional[str] = '~/config/load.yml'
                neo_config: Optional[str] = '~/.neovim/plugged/config/load.yml'

                # Settings, Loading File PATH.
                file_load: Optional[str] = 'Home_File'
                neo_load: Optional[str] = 'VimPlug_Neovim'

                # Home Folder, Set the dictionary.
                if os.path.exists(os.path.expanduser(config_load)):
                    with open(os.path.expanduser(config_load)) as yml:
                        config = yaml.safe_load(yml)

                    # Get Receiver/go_straight behavior.
                    with open(os.path.expanduser(config[file_load])) as r_meth:
                        # real clone
                        index_rb: Optional[list] = list(r_meth.readlines())
                        vir_c: Optional[list] = [s.rstrip() for s in index_rb]
                        vir_c.sort(key=itemgetter(0))
                        return vir_c

                # Neovim Folder, Set the dictionary.
                elif os.path.exists(os.path.expanduser(neo_config)):
                    with open(os.path.expanduser(neo_config)) as yml:
                        config = yaml.safe_load(yml)

                    # Get Receiver/go_straight behavior.
                    with open(os.path.expanduser(config[neo_load])) as r_meth:
                        # real clone
                        neo_ruby: Optional[list] = list(r_meth.readlines())
                        neo_c: Optional[list] = [s.rstrip() for s in neo_ruby]
                        neo_c.sort(key=itemgetter(0))
                        return neo_c

                # Config Folder not found.
                else:
                    raise ValueError("None, Please Check the Config Folder")

            # Python_VERSION: 3.5 or higher and 4.x or less.
            else:
                raise ValueError("VERSION: 3.5 and higher, 4.x or less")

        # Custom Exception.
        except ValueError as ext:
            print(ext)
            raise RuntimeError from None

        # Once Exec.
        finally:
            # GC collection.
            gc.collect()
