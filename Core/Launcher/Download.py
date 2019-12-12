import os
import requests
import json
import shutil
import hashlib
from multiprocessing.pool import ThreadPool


class Object:
    def __init__(self, path, url, kind, name=""):
        self.path = path
        self.url = url
        self.kind = kind
        self.name = name


def mkd(path):
    if not os.path.isdir(path):
        os.makedirs(path)


class Download:
    def __init__(self, launcher, _profile, callback):
        self.launcher = launcher
        self.checkHash = True
        self.profile = _profile
        self.doFireEvents = True
        self.current_nb = 0
        self.max_nb = 0
        self.downloadFileChangedEvent = callback

    def fire_event(self, kind, name, max, current):
        if not self.doFireEvents:
            return
        self.downloadFileChangedEvent(kind, name, max, current)

    def check_sha1(self, path, fhash):
        if not self.checkHash:
            return True
        if not fhash:
            return True

        f = open(path, "rb")
        data = f.read()
        f.close()

        return fhash == hashlib.sha1(data).hexdigest()

    def check_valide(self, path, fhash):
        return os.path.isfile(path) and self.check_sha1(path, fhash)

    def download(self, obj):
        self.current_nb += 1
        self.fire_event(obj.kind, obj.name, self.max_nb, self.current_nb)

        dirpath = os.path.dirname(obj.path)
        mkd(dirpath)

        response = requests.get(obj.url, stream=True)
        if int(response.status_code / 100) is not 2:
            return

        with open(obj.path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)

    def download_all(self, download_assets, toplevel):
        self.download_libraries()
        self.download_minecraft()
        if download_assets:
            self.download_index()
            self.download_resources()
        toplevel.destroy()

    def download_libraries(self):
        libs = [Object(i.path, i.url, "Library", i.name) for i in self.profile.libraries if i.required and i.path and
                i.url and not self.check_valide(i.path, i.hash)]
        self.max_nb = len(libs)
        self.current_nb = 0
        result = ThreadPool().imap(self.download, libs)
        for _ in result:
            pass

    def download_index(self):
        path = os.path.normpath(self.launcher.indexes_dir + "/" + self.profile.asset_id + ".json")
        self.current_nb = 0
        self.max_nb = 1
        if self.profile.asset_url and not self.check_valide(path, self.profile.asset_hash):
            obj = Object(path, self.profile.asset_url, "Index", self.profile.asset_id)
            self.download(obj)

    def download_resources(self):
        index_path = os.path.normpath(self.launcher.indexes_dir + "/" + self.profile.asset_id + ".json")
        if not os.path.isfile(index_path):
            return

        f = open(index_path, "r")
        content = f.read()
        f.close()

        index = json.loads(content)

        items = index.get("objects").values()
        objects = []
        for i in items:

            hash_ = i.get("hash")
            hash_name = hash_[:2] + "/" + hash_
            hash_path = os.path.normpath(self.launcher.objects_dir + "/" + hash_name)
            hash_url = "http://resources.download.minecraft.net/" + hash_name

            if not os.path.isfile(hash_path):
                objects.append(Object(hash_path, hash_url, "Resource"))
        self.max_nb = len(objects)
        self.current_nb = 0
        result = ThreadPool().imap(self.download, objects)
        for _ in result:
            pass

    def download_minecraft(self):
        if not self.profile.client_dl_url:
            return

        id_ = self.profile.jar
        path = os.path.normpath(self.launcher.version_dir + "/" + id_ + "/" + id_ + ".jar")
        self.current_nb = 0
        self.max_nb = 1
        if not self.check_valide(path, self.profile.client_hash):
            obj = Object(path, self.profile.client_dl_url, "Minecraft", id_)
            self.download(obj)
