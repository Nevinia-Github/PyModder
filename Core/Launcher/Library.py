import os
from Core.Launcher.Rules import check_os


default_libs_server = "https://libraries.minecraft.net/"


class Library:
    def __init__(self, name, path, url, native, hash_):
        self.name = name
        self.path = path
        self.url = url
        self.required = True
        self.hash = hash_
        self.native = native

    def __str__(self):
        return "Lib :\n- Name : "+self.name+"\nPath : "+self.path+"\nUrl : "+self.url+"\nRequired : "+\
               str(self.required)+"\nHash : "+self.hash

    @classmethod
    def parse_from_json(cls, launcher, json):
        name = json.get("name")
        if name is None:
            return None

        rules = json.get("rules")
        if rules:
            is_require = check_os(rules)
            if not is_require:
                return None

        downloads = json.get("downloads")
        if not downloads:
            natives = json.get("natives")
            native_id = None
            if natives is not None:
                native_id = natives.get('windows')

            path = os.path.join(launcher.libs_dir, name_to_path(json.get("path"), native_id))
            url = json.get("url")
            if not url:
                url = default_libs_server + path
            elif not url.split('/')[-1]:
                url += path
            return Library(name, path, url, True if native_id else False, json.get("sha1"))

        classif = downloads.get("classifiers")
        if classif:
            native_id = None
            native_obj = json.get("natives")
            if native_obj:
                native_id = native_obj.get("windows")

            if native_id and classif.get(native_id):
                native_id = native_id.replace("${arch}", "64")
                job = classif.get(native_id)

                path = os.path.join(launcher.libs_dir, name_to_path(job.get("path"), native_id))
                url = job.get("url")
                if not url:
                    url = default_libs_server + path
                elif not url.split('/')[-1]:
                    url += path

                temp = Library(name, path, url, True if native_id else False, job.get("sha1"))

                arti = downloads.get("artifact")
                if arti:
                    json = arti
                    path = os.path.join(launcher.libs_dir, name_to_path(json.get("path"), ""))
                    url = json.get("url")
                    if not url:
                        url = default_libs_server + path
                    elif not url.split('/')[-1]:
                        url += path

                    return Library(name, path, url, True if "" else False, json.get("sha1")), temp

                return temp

        arti = downloads.get("artifact")
        if arti:
            json = arti
            path = os.path.join(launcher.libs_dir, name_to_path(json.get("path"), ""))
            url = json.get("url")
            if not url:
                url = default_libs_server + path
            elif not url.split('/')[-1]:
                url += path

            return Library(name, path, url, True if "" else False, json.get("sha1"))

        return None


def name_to_path(name, native):
    try:
        temp = name.split(":")
        front = temp[0].replace(".", "/")
        back = ""

        for i in range(1, len(temp)):
            if i == len(temp) - 1:
                back += temp[i]
            else:
                back += temp[i] + ":"

        libpath = front + "/" + back.replace(":", "/") + "/" + (back.replace(":", "-"))
        if native:
            libpath += "-"+native+".jar"
        else:
            libpath += ".jar"
        return libpath
    except Exception as e:
        print(e)
        return ""
