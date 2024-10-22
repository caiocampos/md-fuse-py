"""
Módulo para processamento dos arquivos de entrada e saída
"""

import os
from .configuration import TemplateFileParametersConf


def parse_folder(folder: str) -> str:
    """
    Função para corrigir possíveis problemas com formato de nome de pasta
    """
    if folder.endswith(os.path.sep):
        return folder

    return folder + os.path.sep


def generate_text(folder: str, inputs: list[str]) -> str:
    """
    Função para ler os arquivos de entrada e gerar o texto que será gravado no arquivo de saída
    """
    res = ""

    for path in inputs:
        full_path = parse_folder(folder) + path
        try:
            with open(full_path, "r", encoding="utf-8") as file:
                res += file.read()

        except (OSError, EOFError) as ex:
            print(f"Could not load the file {full_path} for read \nError: {ex}")
            continue

    return res


def generate_from_template(
    folder: str, path: str, parameters: list[TemplateFileParametersConf]
) -> str:
    """
    Função para ler os arquivos de entrada e montar o texto a partir do template
    """
    res = ""

    full_path = parse_folder(folder) + path
    try:
        with open(full_path, "r", encoding="utf-8") as file:
            res = file.read()

    except (OSError, EOFError) as ex:
        print(f"Could not load the file {full_path} for read \nError: {ex}")

    for parameter in parameters:
        template = f"{{{{{parameter.name}}}}}"
        prefix = "ENV_VAR:"
        if parameter.value.startswith(prefix):
            env_key = parameter.value[len(prefix) :]
            env_value = os.getenv(env_key, "")
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

    full_path = parse_folder(folder) + path

    try:
        with open(full_path, "w", encoding="utf-8") as file:
            file.write(text)

            return full_path

    except OSError as ex:
        print(f"Could not write the file {full_path} \nError: {ex}")
        return ""
