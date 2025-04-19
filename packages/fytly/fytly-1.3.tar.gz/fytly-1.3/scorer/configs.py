from configparser import ConfigParser
import os

class GraderConfigs:
    props = {}

    # default constructor
    def __init__(self):
        self.props = self._load_configs()

    def _load_configs(self,keywords_file='app.properties'):
        dict = {}

        script_dir = os.path.dirname(__file__)
        base_dir = os.path.abspath(os.path.join(script_dir, '..', '..', '..'))
        config_dir = os.path.join(base_dir, 'fytly', 'configs')
        file_path = os.path.join(config_dir, keywords_file)

        config = ConfigParser()
        with open(file_path, 'r') as f:
            config.read_string('[config]\n' + f.read())

        for k, v in config['config'].items():
            dict[k] = v
        return dict

