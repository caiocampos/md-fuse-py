"""
Módulo para processar os dados e gerar o arquivo final
"""

from . import configuration
from . import file


def process(conf_file_path: str):
    """
    Função para processar os dados e gerar o arquivo final
    """
    conf = configuration.load(conf_file_path)

    for file_conf in conf.files:
        print(f"Processando {file_conf.name}")
        text = file.generate_text(conf.input_folder, file_conf.inputs)
        if text:
            print("Arquivos lidos com sucesso!")
        else:
            continue

        res = file.write_text(conf.output_folder, file_conf.output, text)
        if res:
            print(f"Arquivo {res} gravado com sucesso!")
