import yaml

with open("resources/config.yaml", "r") as f:
    CONFIG_DICT = yaml.load(f, Loader=yaml.Loader)