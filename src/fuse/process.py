"""
Módulo para processar os dados e gerar o arquivo final
"""

from .configuration import load as config_load
from .file import (
    generate_text,
    generate_from_template,
    write_text,
    read_dictionary_inputs,
)


def process(conf_file_path: str):
    """
    Função para processar os dados e gerar o arquivo final
    """
    dict_vars: dict[str, str] = {}
    conf = config_load(conf_file_path)

    for dict_conf in conf.dictionary_inputs:
        print(f"Processando {dict_conf}")
        res = read_dictionary_inputs(
            conf.input_folder, conf.dictionary_subfolder, dict_conf
        )
        if res is not None:
            print("Arquivo lido com sucesso!")
        else:
            continue

        dict_vars.update(res)

    for file_conf in conf.template_files:
        print(f"Processando {file_conf.name}")
        text = generate_from_template(
            conf.input_folder, file_conf.input, file_conf.parameters, dict_vars
        )
        if text:
            print("Arquivo lido com sucesso!")
        else:
            continue

        res = write_text(conf.input_folder, file_conf.output, text)
        if res:
            print(f"Arquivo {res} gravado com sucesso!")

    for file_conf in conf.files:
        print(f"Processando {file_conf.name}")
        text = generate_text(conf.input_folder, file_conf.inputs)
        if text:
            print("Arquivos lidos com sucesso!")
        else:
            continue

        res = write_text(conf.output_folder, file_conf.output, text)
        if res:
            print(f"Arquivo {res} gravado com sucesso!")
