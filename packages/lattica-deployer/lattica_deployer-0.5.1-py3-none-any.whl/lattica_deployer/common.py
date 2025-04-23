import os
import yaml

from typing import Union


def read_params_config(config_path: Union[str, os.PathLike]) -> dict:
    with open(config_path, 'rb') as f:
        params_config = yaml.safe_load(f)
        params_config['full_q_list'] = [
            [str(x) for x in row]
            for row in params_config['full_q_list']
        ]
        return params_config
    