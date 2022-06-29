import os


def parse_folder(folder: str) -> str:
    if folder.endswith(os.path.sep):
        return folder

    return folder + os.path.sep


def generate_text(folder: str, inputs: list[str]) -> str:
    res = ""

    for path in inputs:
        full_path = parse_folder(folder) + path
        try:
            file = open(full_path, "r")
        except:
            print("Could not open the file {} for read".format(full_path))
            continue

        try:
            res += file.read()
        except:
            print("Could not load the file {}".format(full_path))
        finally:
            file.close()

    return res


def write_text(folder: str, path: str, text: str) -> str:
    if not os.path.isdir(folder):
        try:
            os.makedirs(folder)
        except:
            print("Could not create the folder {}".format(folder))
            return ""

    full_path = parse_folder(folder) + path

    try:
        file = open(full_path, "w")
    except:
        print("Could not open the file {} for write".format(full_path))
        return ""

    try:
        file.write(text)
        return full_path
    except:
        print("Could not write the file {}".format(full_path))
        return ""
    finally:
        file.close()
