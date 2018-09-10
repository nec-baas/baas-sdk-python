# -*- coding: utf-8 -*-
import os
import yaml

import necbaas as baas


def load_config():
    """
    Load test config from ~/.baas/python_test_config.yaml

    Returns:
        dict: Loaded config
    """
    f = open(os.path.expanduser("~/.baas/python_test_config.yaml"), 'r')
    config = yaml.load(f)
    f.close()
    return config


def create_service(master=False, key="service"):
    """
    Create service from config file.

    Args:
        master (bool): use master key
        key (str): service key in config
    Returns:
        Service: service"
    """
    c = load_config()
    param = c[key]
    if master:
        param["appKey"] = param["masterKey"]
    return baas.Service(param)


def remove_all_users(key="service"):
    s = create_service(True, key=key)

    users = baas.User.query(s)
    for u in users:
        print(u)
        baas.User.remove(s, u["_id"])


def remove_all_groups():
    s = create_service(True)

    groups = baas.Group.query(s)
    for g in groups:
        print(g)
        group = baas.Group(s, g["name"])
        group.remove()


def setup_user(service):
    remove_all_users()

    # Register user
    user = baas.User(service)
    user.username = "user1"
    user.email = "user1@example.com"
    user.password = "Passw0rD"
    user.register()

    # Login
    baas.User.login(service, username=user.username, password=user.password)
    return user
