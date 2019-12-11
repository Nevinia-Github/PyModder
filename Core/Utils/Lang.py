import os


class Lang:
    def __init__(self, file):
        self.dic = {}
        if os.path.exists(file):
            with open(file, "r", encoding="utf8") as f:
                for i in f.readlines():
                    if len(i.split(": ")) >= 2:
                        self.dic[i.split(": ")[0]] = i.split(": ", 1)[1].replace("\n", "")

    def get_translate(self, key, default, *args):
        return self.dic.get(key, default).format(*args).replace("\\n", "\n")
