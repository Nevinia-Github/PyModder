import os
import shutil
from Core.Launcher.MCVersion import MCVersionsList
from Core.Launcher.Download import Download
import string
import re
import zipfile
import subprocess
import sys

pre_compiled = re.compile(r"\\$\\{(.*?)}")


def m(p):
    p = os.path.normpath(p)
    if not os.path.isdir(p):
        os.makedirs(p)
    return p


def e(t):
    if " " in t:
        return '"' + t + '"'
    else:
        return t


def ea(t):
    if " " in t and "=" in t:
        s = t.split("=")
        return s[0] + '="' + s[1] + '"'
    else:
        return t


def arg_in(arg, dicts):
    args = list()
    for item in arg:
        if type(item) is str:
            m_ = pre_compiled.search(item)
            if m_:
                arg_key = m_.group()
                arg_value = dicts.get(arg_key[2:-1])

                if arg_value:
                    args.append(pre_compiled.sub(arg_value.replace("\\", "\\\\"), item))
                else:
                    args.append(item)
            else:
                args.append(ea(item))

    for k, v in dicts.items():
        for i in range(len(args)):
            args[i] = args[i].replace("${"+k+"}", v)

    return args


def arg_str(arg, dicts):
    for k, v in dicts.items():
        arg = arg.replace("${"+k+"}", v)


class Launcher:
    def __init__(self, main):
        self.main = main
        self.mc_dir = m(os.path.join(main.project.paths["Folder"], "mc"))
        self.libs_dir = m(os.path.join(self.mc_dir, "libraries"))
        self.version_dir = m(os.path.join(self.mc_dir, "versions"))
        self.resources_dir = m(os.path.join(self.mc_dir, "resources"))
        self.natives_dir = m(os.path.join(self.mc_dir, "natives"))
        self.assets_dir = m(os.path.join(self.mc_dir, "assets"))
        self.indexes_dir = m(os.path.join(self.assets_dir, "indexes"))
        self.objects_dir = m(os.path.join(self.assets_dir, "objects"))
        self.legacy_dir = m(os.path.join(self.assets_dir, "virtual", "legacy"))

        print("Initialize dirs in", self.mc_dir)

        self.java_dir = shutil.which("javaw")
        self.mem = 2048
        self.user = "Dev"
        self.uuid = "uuid"
        self.access_token = "token"

        self.version = MCVersionsList(self).get("1.14.4-forge-28.1.0")

        download = Download(self, self.version, self.download_event)
        download.download_all(True)

        self.start_profile = self.version
        self.launcher_name = "PyModder"

    @staticmethod
    def download_event(kind, name, max_, current):
        print(kind, name, max_, current)

    def launch(self):
        self.clean_natives()
        self.extract_natives()
        args = self.create_args()
        print(args)
        os.system("subst H: "+self.mc_dir)
        mc = subprocess.Popen("javaw "+args, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, cwd=self.mc_dir, shell=True)
        print("LAUNCHED !")
        # write output
        with mc.stdout as gameLog:
            while True:
                try:
                    line = gameLog.readline()
                    if not line:
                        break
                    print(line.decode(sys.getdefaultencoding()), end="")
                except:
                    pass

        if mc.returncode:
            print(f"Client returned {mc.returncode}!")

    def extract_natives(self):
        for item in self.version.libraries:
            if item.native:
                try:
                    lib = zipfile.ZipFile(item.path)
                    lib.extractall(self.natives_dir)
                except Exception as e_:
                    print(e_)

    def clean_natives(self):
        for item in os.listdir(self.natives_dir):
            path = os.path.join(self.natives_dir, item)

            if os.path.isfile(path):
                try:
                    os.remove(path)
                except Exception as e_:
                    print(e_)

    def create_args(self):
        args = ["-XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 "
                "-XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=16M", "-Xmx"+str(self.mem)+"m"]

        lib_args = []

        for i in self.version.libraries:
            if not i.native:
                lib_args.append(e(i.path))

        lib_args.append(e(os.path.join(self.version_dir, self.version.jar, self.version.jar+".jar")))
        libs = os.pathsep.join(lib_args)

        jvmdict = {
            "natives_directory": e(self.natives_dir),
            "launcher_name": self.launcher_name,
            "launcher_version": "1",
            "classpath": libs
        }

        if self.version.jvm_arguments:
            args += arg_in(self.version.jvm_arguments, jvmdict)
        else:
            args.append("-Djava.library.path=" + e(self.natives_dir))
            args.append("-cp "+libs)

        args.append(self.version.main_class)

        gamedict = {
            "auth_player_name": self.user,
            "version_name": self.version.id,
            "game_directory": e(self.mc_dir),
            "assets_root": e(self.assets_dir),
            "assets_index_name": self.version.asset_id,
            "auth_uuid": self.uuid,
            "auth_access_token": self.access_token,
            "user_properties": "{}",
            "user_type": "Mojang",
            "game_assets": e(self.legacy_dir),
            "auth_session": self.access_token
        }

        if self.launcher_name:
            gamedict["version_type"] = self.launcher_name
        else:
            gamedict["version_type"] = self.version.type

        if self.version.game_arguments:  # 1.3
            args += arg_in(self.version.game_arguments, gamedict)
        elif self.version.minecraftArguments:
            args.append(arg_str(self.version.minecraftArguments, gamedict))

        for i in range(len(args)):
            args[i] = str(args[i]).replace(self.mc_dir, "H:")

        return " ".join(args)


