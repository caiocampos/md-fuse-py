import json


class FileConf:
    def __init__(self, name: str, inputs: list[str], output: str):
        self.name = name
        self.inputs = inputs
        self.output = output


class Conf:
    def __init__(self, input_folder: str, output_folder: str, files: list[FileConf]):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.files = files


def default_conf():
    return Conf("", "", [])


def parse(config_json: dict) -> Conf:
    if not config_json:
        return default_conf()

    conf = Conf(config_json.get("input_folder") or "",
                config_json.get("output_folder") or "", [])

    for file in config_json.get("files") or []:
        conf.files.append(
            FileConf(file.get("name") or "",
                     file.get("inputs") or [],
                     file.get("output") or "")
        )

    return conf


def load(conf_file_path: str) -> Conf:
    try:
        conf_file = open(conf_file_path)
    except:
        print("Could not load the file {}".format(conf_file_path))
        return default_conf()

    try:
        config_json: dict = json.load(conf_file)

        return parse(config_json)
    except:
        print("Could not read the file {}".format(conf_file_path))
        return default_conf()
    finally:
        conf_file.close()
