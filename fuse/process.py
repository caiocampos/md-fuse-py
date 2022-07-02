"""
Módulo para processar os dados e gerar o arquivo final
"""

from .configuration import load as config_load
from .file import generate_text, write_text


def process(conf_file_path: str):
    """
    Função para processar os dados e gerar o arquivo final
    """
    conf = config_load(conf_file_path)

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
