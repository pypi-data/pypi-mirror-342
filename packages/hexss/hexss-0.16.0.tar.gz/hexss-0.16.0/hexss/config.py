from hexss import json_load, hexss_dir


def get_config_list():
    return [p.stem for p in (hexss_dir / 'config').iterdir() if p.is_file() and p.suffix == '.json']


def get_config(file_name):
    config_ = json_load(hexss_dir / 'config' / f'{file_name}.json', {})
    if file_name in config_:
        config = config_[file_name]
    else:
        config = config_

    return config


print(get_config_list())
