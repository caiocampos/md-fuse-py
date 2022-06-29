import configuration
import file


def process(conf_file_path: str):
    conf = configuration.load(conf_file_path)

    for file_conf in conf.files:
        print("Processando {}".format(file_conf.name))
        text = file.generate_text(conf.input_folder, file_conf.inputs)
        if text:
            print("Arquivos lidos com sucesso!")
        else:
            continue

        res = file.write_text(conf.output_folder, file_conf.output, text)
        if res:
            print("Arquivo {} gravado com sucesso!".format(res))
