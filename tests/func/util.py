import os
import yaml


def load_config():
    """
    Load test config from ~/.baas/python_test_config.yaml

    :return dict: config in dict
    """
    f = open(os.path.expanduser("~/.baas/python_test_config.yaml"), 'r')
    config = yaml.load(f)
    f.close()
    return config
