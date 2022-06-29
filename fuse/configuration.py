"""
Módulo para processamento do arquivo de configuração
"""

from dataclasses import dataclass
import json


@dataclass
class FileConf:
    """
    Classe que representa a configuração do arquivo que será gerado
    """

    def __init__(self, name: str, inputs: list[str], output: str):
        self.name = name
        self.inputs = inputs
        self.output = output

    @staticmethod
    def default():
        """
        Método para criar a instancia padrão de FileConf
        """
        return FileConf("", [], "")


@dataclass
class Conf:
    """
    Classe que representa os dados de configuração
    """

    def __init__(self, input_folder: str, output_folder: str, files: list[FileConf]):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.files = files

    @staticmethod
    def default():
        """
        Método para criar a instancia padrão de Conf
        """
        return Conf("", "", [])


def parse(config_json: dict) -> Conf:
    """
    Função para processar os dados recebidos no JSON
    """
    if not config_json:
        return Conf.default()

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
    """
    Função para carregar os dados armazenados no JSON de configuração
    """
    try:
        with open(conf_file_path, "r", encoding="utf-8") as conf_file:
            config_json: dict = json.load(conf_file)

            return parse(config_json)
    except (OSError, EOFError) as ex:
        print(f"Could not read the file {conf_file_path} \nError: {ex}")
        return Conf.default()
