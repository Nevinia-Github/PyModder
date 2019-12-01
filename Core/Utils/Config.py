import json


class Config:
    def __init__(self, file):
        self.file = file
        with open(self.file, "r", encoding="utf8") as f:
            self.dic = json.load(f)

    def get(self, key, default):
        keys = key.split(".")
        if len(keys) == 1:
            return self.dic.get(key, default)
        else:
            value = self.dic
            for i in keys:
                if i != keys[-1]:
                    value = value[i]
                else:
                    value = value.get(i, default)
            return value

    def set(self, key, val):
        keys = key.split(".")
        if len(keys) == 0:
            self.dic[key] = val
        else:
            value = self.dic
            for i in keys:
                if i != keys[-1]:
                    value = value[i]
                else:
                    value[i] = val

    def save(self):
        with open(self.file, "w", encoding="utf8") as f:
            f.write(json.dumps(self.dic, indent=4))
