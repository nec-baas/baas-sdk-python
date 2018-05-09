import os
import yaml

import necbaas as baas


def load_config():
    """
    Load test config from ~/.baas/python_test_config.yaml

    :return dict: config in dict
    """
    f = open(os.path.expanduser("~/.baas/python_test_config.yaml"), 'r')
    config = yaml.load(f)
    f.close()
    return config


def create_service(master=False):
    """
    Create service from config file.

    Args:
        master (bool): use master key
    Returns:
        Service: service
    """
    c = load_config()
    param = c["service"]
    if master:
        param["appKey"] = param["masterKey"]
    return baas.Service(param)


def remove_all_users():
    s = create_service(True)

    users = baas.User.query(s)
    for u in users:
        print(u)
        baas.User.remove(s, u["_id"])
