import os
import requests
import json
from shutil import copyfile
import shutil
import hashlib


def mkd(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def download(url, path):
    dirpath = os.path.dirname(path)
    mkd(dirpath)

    response = requests.get(url, stream=True)
    if int(response.status_code / 100) is not 2:
        return

    with open(path, 'wb') as f:
        shutil.copyfileobj(response.raw, f)


class Download:
    def __init__(self, launcher, _profile, callback):
        self.launcher = launcher
        self.checkHash = True
        self.profile = _profile
        self.doFireEvents = True
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

    def download_all(self, download_assets):
        self.download_libraries()
        self.download_minecraft()
        if download_assets:
            self.download_index()
            self.download_resources()

    def download_libraries(self):
        count = len(self.profile.libraries)
        for i in range(0, count):
            lib = self.profile.libraries[i]
            if lib.required and lib.path and lib.url and not self.check_valide(lib.path, lib.hash):
                download(lib.url, lib.path)

            self.fire_event("library", lib.name, count, i + 1)

    def download_index(self):
        path = os.path.normpath(self.launcher.indexes_dir + "/" + self.profile.asset_id + ".json")
        if self.profile.asset_url and not self.check_valide(path, self.profile.asset_hash):
            download(self.profile.asset_url, path)

        self.fire_event("index", self.profile.asset_id, 1, 1)

    def download_resources(self):
        index_path = os.path.normpath(self.launcher.indexes_dir + "/" + self.profile.asset_id + ".json")
        if not os.path.isfile(index_path):
            return

        f = open(index_path, "r")
        content = f.read()
        f.close()

        index = json.loads(content)

        is_virtual = False
        v = index.get("virtual")
        if v and v is True:
            is_virtual = True

        is_map_resource = False
        m = index.get("map_to_resources")
        if m and m is True:
            is_map_resource = True

        items = list(index.get("objects").items())
        count = len(items)
        for i in range(0, count):
            key = items[i][0]
            value = items[i][1]

            hash_ = value.get("hash")
            hash_name = hash_[:2] + "/" + hash_
            hash_path = os.path.normpath(self.launcher.objects_dir + "/" + hash_name)
            hash_url = "http://resources.download.minecraft.net/" + hash_name

            if not os.path.isfile(hash_path):
                download(hash_url, hash_path)

            if is_virtual:
                res_path = os.path.normpath(self.launcher.legacy_dir + "/" + key)

                if not os.path.isfile(res_path):
                    mkd(os.path.dirname(res_path))
                    copyfile(hash_path, res_path)

            if is_map_resource:
                res_path = os.path.normpath(self.launcher.resources_dir + "/" + key)

                if not os.path.isfile(res_path):
                    mkd(os.path.dirname(res_path))
                    copyfile(hash_path, res_path)

            self.fire_event("resource", "", count, i + 1)

    def download_minecraft(self):
        if not self.profile.client_dl_url:
            return

        id_ = self.profile.jar
        path = os.path.normpath(self.launcher.version_dir + "/" + id_ + "/" + id_ + ".jar")
        if not self.check_valide(path, self.profile.client_hash):
            download(self.profile.client_dl_url, path)

        self.fire_event("minecraft", id_, 1, 1)