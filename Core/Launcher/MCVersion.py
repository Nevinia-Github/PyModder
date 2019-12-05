import os
import json
from Core.Utils.Utils import notnone
from Core.Launcher.Library import Library
from Core.Launcher.Rules import check_os
import shutil


def arg_parse(arr):
    strlist = list()
    for item in arr:
        if type(item) == dict:
            allow = True

            rule = item.get("rules")
            if rule:
                allow = check_os(rule)

            value = item.get("value")

            if allow and value:
                if type(value) == list:
                    strlist.extend(value)
                else:
                    strlist.append(value)
        else:
            strlist.append(item)

    return strlist


class MCVersion(object):
    def __init__(self, launcher, d):
        self.d = d
        self.id = d.get('id')

        self.asset_id = None
        self.asset_url = None
        self.asset_hash = None

        asset_index = d.get("assetIndex")
        if asset_index:
            self.asset_id = notnone(asset_index.get("id"))
            self.asset_url = notnone(asset_index.get("url"))
            self.asset_hash = notnone(asset_index.get("sha1"))

        self.client_dl_url = None
        self.client_hash = None

        downloads = d.get("downloads")
        if downloads:
            client = downloads.get("client")
            if client:
                self.client_dl_url = client.get("url")
                self.client_hash = client.get("sha1")

        self.libraries = []
        for x in d.get("libraries"):
            temp = Library.parse_from_json(launcher, x)
            if temp is not None:
                if isinstance(temp, tuple):
                    self.libraries += temp
                else:
                    self.libraries.append(temp)
        self.main_class = notnone(d.get("mainClass"))

        self.game_arguments = []
        self.jvm_arguments = []

        self.minecraft_arguments = d.get("minecraftArguments")
        arg = d.get("arguments")
        if arg:
            if arg.get("game"):
                self.game_arguments = arg_parse(arg.get("game"))
            if arg.get("jvm"):
                self.jvm_arguments = arg_parse(arg.get("jvm"))

        self.release_time = notnone(d.get("releaseTime"))
        self.type_ = notnone(d.get("type"))

        self.inherits = d.get('inheritsFrom')
        self.jar = self.id

        self.path = os.path.join(launcher.mc_dir, "versions", self.id)

    def inherit(self, parent):
        if not self.asset_id:
            self.asset_id = parent.asset_id
        if not self.asset_url:
            self.asset_url = parent.asset_url
        if not self.asset_hash:
            self.asset_hash = parent.asset_hash
        if not self.client_dl_url:
            self.client_dl_url = parent.client_dl_url
        if not self.client_hash:
            self.client_hash = parent.client_hash
        if not self.main_class:
            self.main_class = parent.main_class
        if not self.minecraft_arguments:
            self.minecraft_arguments = parent.minecraft_arguments

        if parent.libraries:
            self.libraries += parent.libraries
        if parent.game_arguments:
            self.game_arguments += parent.game_arguments
        if parent.jvm_arguments:
            self.jvm_arguments += parent.jvm_arguments


class MCVersionsList(object):
    def __init__(self, launcher):
        self._dict = {}
        os.chdir(os.path.join(launcher.mc_dir, 'versions'))
        for version in os.listdir("."):
            if os.path.isdir(version):
                json_file = os.path.join(version, version + '.json')
                if os.path.exists(json_file):
                    with open(json_file) as fp:
                        self._dict[version] = MCVersion(launcher, json.load(fp))
        os.chdir('..')

        self.list = sorted(self._dict)

    def get(self, version_id):
        this = self._dict.get(version_id)
        if this is None:
            raise ValueError('Invalid version id {0}. Please check if {0}.json exists.'.format(version_id))
        parent_id = this.inherits
        if parent_id:
            parent = self.get(parent_id)
            this.inherit(parent)
        return this

    def __str__(self):
        return str(self._dict)
