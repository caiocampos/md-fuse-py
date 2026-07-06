"""
Módulo para processamento dos arquivos de entrada e saída
"""

import os
import json
from pathlib import Path
from .configuration import TemplateFileParametersConf


def merge_path(*parts: str) -> str:
    """
    Função para mesclar partes de um caminho
    """
    return str(Path(*(part for part in parts if part)))


def read_dictionary_inputs(
    folder: str, subfolder: str, path: str
) -> dict[str, str] | None:
    """
    Função para ler os arquivos json que vão alimentar o dicionário
    """
    full_path = merge_path(folder, subfolder, path)
    try:
        with open(full_path, "r", encoding="utf-8") as dict_file:
            map: dict = json.load(dict_file)
            return map

    except (OSError, EOFError) as ex:
        print(f"Could not load the file {full_path} for read \nError: {ex}")
        return None


def generate_text(folder: str, inputs: list[str]) -> str:
    """
    Função para ler os arquivos de entrada e gerar o texto que será gravado no arquivo de saída
    """
    res = ""

    for path in inputs:
        full_path = merge_path(folder, path)
        try:
            with open(full_path, "r", encoding="utf-8") as file:
                res += file.read()

        except (OSError, EOFError) as ex:
            print(f"Could not load the file {full_path} for read \nError: {ex}")
            continue

    return res


def generate_from_template(
    folder: str,
    path: str,
    parameters: list[TemplateFileParametersConf],
    dictionary: dict[str, str],
) -> str:
    """
    Função para ler os arquivos de entrada e montar o texto a partir do template
    """
    res = ""

    full_path = merge_path(folder, path)
    try:
        with open(full_path, "r", encoding="utf-8") as file:
            res = file.read()

    except (OSError, EOFError) as ex:
        print(f"Could not load the file {full_path} for read \nError: {ex}")

    for parameter in parameters:
        template = f"{{{{{parameter.name}}}}}"
        dict_prefix = "DICT_VAR:"
        env_prefix = "ENV_VAR:"
        if parameter.value.startswith(dict_prefix):
            dict_key = parameter.value[len(dict_prefix) :]
            dict_value = dictionary.get(dict_key)
            if dict_value is None:
                print(f'Could not find the variable "{dict_key}"')
                dict_value = ""

            res = res.replace(template, dict_value)
        elif parameter.value.startswith(env_prefix):
            env_key = parameter.value[len(env_prefix) :]
            env_value = os.getenv(env_key)
            if env_value is None:
                print(f'Could not find the environment variable "{env_key}"')
                env_value = ""

            res = res.replace(template, env_value)
        else:
            res = res.replace(template, parameter.value)

    return res


def write_text(folder: str, path: str, text: str) -> str:
    """
    Função para gravar o arquivo de saída com o texto desejado
    """
    if not os.path.isdir(folder):
        try:
            os.makedirs(folder)
        except OSError as ex:
            print(f"Could not create the folder {folder} \nError: {ex}")
            return ""

    full_path = merge_path(folder, path)

    try:
        with open(full_path, "w", encoding="utf-8") as file:
            file.write(text)

            return full_path

    except OSError as ex:
        print(f"Could not write the file {full_path} \nError: {ex}")
        return ""
