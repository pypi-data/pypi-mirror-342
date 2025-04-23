import os
import yaml
from layered_py.decorators import register

DEFAULTS = {
    'service_destination': 'services',
    'domain_destination': 'domain',
    'repository_destination': 'repository',
    'presentation_destination': 'presentation'
}


def _load_config(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found at {path}")

    with open(path, 'r') as file:
        return yaml.safe_load(file)


@register('Config')
class Config:
    def __init__(self):
        self.config = DEFAULTS.copy()

        if os.path.exists('layeredpy_config.yml'):
            self.config.update(_load_config('layeredpy_config.yml'))

    def get(self, key):
        return self.config.get(key)

    def get_folder_array(self):
        return {
            self.get('service_destination'),
            self.get('domain_destination'),
            self.get('repository_destination'),
            self.get('presentation_destination')
        }