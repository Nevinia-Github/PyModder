import os
import json
import requests
import io
import zipfile
import shutil
import subprocess

from tkinter.messagebox import showinfo, showerror

from Core.Project.JavaClass import MainClass, BlocksClass, ItemsClass
from Core.Project.Jsons import BlockJson, BlockStatesJson, LangJson, ItemJson, BlockLootJson
from Core.Project.Objects import Blocks, ItemGroup, Items


class Project:
    def __init__(self, main, name):
        self.main = main
        self.paths = {
            "Folder": os.path.join(os.path.dirname(__file__), "..", "..", "Mods", name)
        }
        self.paths["Java"] = os.path.join(self.paths["Folder"], "src", "main", "java")
        self.paths["Ressources"] = os.path.join(self.paths["Folder"], "src", "main", "resources")
        self.name = name
        self.old_name = name

        self.objects = {
            "blocks": [],
            "itemgroups": [],
            "items": []
        }

        if not os.path.exists(self.paths["Folder"]):
            self.version = "1.0.0"
            self.modid = name.strip().lower()
            self.paths["Assets"] = os.path.join(self.paths["Ressources"], "assets", self.modid)
            self.url = ""
            self.credits = "PyModder, MFF anf Forge guys"
            self.authors = "Author"
            self.description = "Coming Soon"
            self.main.logger.info("Creating Project folder.")
            self.create_folder()
        else:
            with open(os.path.join(self.paths["Folder"], "project.json"), "r") as f:
                datas = json.load(f)
            self.version = datas["version"]
            self.modid = datas["modid"]
            self.url = datas["url"]
            self.credits = datas["credits"]
            self.authors = datas["authors"]
            self.description = datas["description"]
            self.objects["blocks"] += \
                [Blocks.SimpleBlock.from_json(i) for i in datas["objects"]["blocks"] if i["type"] == "SimpleBlock"]
            self.objects["itemgroups"] += \
                [ItemGroup.ItemGroup.from_json(i) for i in datas["objects"]["itemgroups"] if i["type"] == "ItemGroup"]
            self.objects["items"] += \
                [Items.SimpleItem.from_json(i) for i in datas["objects"]["items"] if i["type"] == "SimpleItem"]
            self.paths["Main"] = os.path.join(self.paths["Java"], "fr", "pymodder", self.modid)
            self.paths["Assets"] = os.path.join(self.paths["Ressources"], "assets", self.modid)

        self.main.logger.info("Project loaded.")

        for i in self.objects["blocks"] + self.objects["itemgroups"] + self.objects["items"]:
            self.main.elements.add_object(i)

        self.old_modid = self.modid

    def build(self):
        showinfo(self.main.lang.get_translate("compilation_title", "Compilation"),
                 self.main.lang.get_translate("compilation_begin", "The compilation of your mod will start.\nIt may "
                                                                   "take up to several minutes."))
        sub = subprocess.Popen(["cd", self.paths["Folder"], "&&", r".\gradlew.bat", "build"],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        error = False
        for line in sub.stdout:
            line = line.decode("utf8").replace("\n", "")
            if "FAILED" in line:
                error = True
            self.main.logger.debug(line)
        if not error:
            path = os.path.join(self.paths["Folder"], "build", "libs",
                                self.name + "-" + self.version + ".jar")
            shutil.copy(path, os.path.join(self.paths["Folder"], self.name + "-" + self.version + ".jar"))
            showinfo(self.main.lang.get_translate("compilation_title", "Compilation"),
                     self.main.lang.get_translate("compilation_success",
                                                  "The compilation was successful.\nYour file is available in the mods"
                                                  " folder.\nIts name is {}", self.name + "-" + self.version + ".jar"))
        else:
            showerror(self.main.lang.get_translate("compilation_title", "Compilation"),
                      self.main.lang.get_translate("compilation_failed", "The compilation failed.\nLook at the logs."))

    def save(self):
        shutil.rmtree(os.path.join(self.paths["Folder"], "src"))
        os.makedirs(os.path.join(self.paths["Java"], "fr", "pymodder", self.modid), exist_ok=True)
        self.paths["Main"] = os.path.join(self.paths["Java"], "fr", "pymodder", self.modid)
        self.paths["Assets"] = os.path.join(self.paths["Ressources"], "assets", self.modid)
        os.makedirs(self.paths["Assets"], exist_ok=True)
        os.makedirs(os.path.join(self.paths["Ressources"], "META-INF"))
        with open(os.path.join(self.paths["Ressources"], "pack.mcmeta"), "w") as f:
            f.write(json.dumps({
                "pack": {
                    "description": "examplemod resources",
                    "pack_format": 4,
                    "_comment": "A pack_format of 4 requires json lang files. Note: we require v4 pack meta for all mo"
                                "ds."
                }
            }, indent=4))

        datas = {
            "modid": self.modid,
            "version": self.version,
            "url": self.url,
            "credits": self.credits,
            "authors": self.authors,
            "description": self.description,
            "objects": {
                "blocks": [i.to_json() for i in self.objects["blocks"]],
                "itemgroups": [i.to_json() for i in self.objects["itemgroups"]],
                "items": [i.to_json() for i in self.objects["items"]]
            }
        }
        with open(os.path.join(self.paths["Folder"], "project.json"), "w") as f:
            json.dump(datas, f, indent=4)

        if self.old_name != self.name:
            path = os.path.join(os.path.dirname(__file__), "..", "..", "Mods", self.name)
            os.rename(self.paths["Folder"], path)
            self.paths["Folder"] = path
            self.paths["Java"] = os.path.join(self.paths["Folder"], "src", "main", "java")
            self.paths["Ressources"] = os.path.join(self.paths["Folder"], "src", "main", "resources")
            self.paths["Main"] = os.path.join(self.paths["Java"], "fr", "pymodder", self.modid)
            self.paths["Assets"] = os.path.join(self.paths["Ressources"], "assets", self.modid)
            os.rename(os.path.join(self.paths["Main"], self.old_name+".java"),
                      os.path.join(self.paths["Main"], self.name+".java"))
            self.old_name = self.name

        if self.old_modid != self.modid:
            path = os.path.join(self.paths["Java"], "fr", "pymodder", self.modid)
            old_path = os.path.join(self.paths["Java"], "fr", "pymodder", self.old_modid)
            os.rename(old_path, path)
            self.paths["Main"] = path
            self.old_modid = self.modid

        self.edit_toml()
        self.edit_build()
        self.edit_main()
        self.edit_objects()

        self.main.logger.info("Project saved.")

    def add_object(self, type_, name):
        if type_ == "SimpleBlock":
            object_ = Blocks.SimpleBlock(name)
            type_ = "blocks"
        elif type_ == "ItemGroup":
            object_ = ItemGroup.ItemGroup(name)
            type_ = "itemgroups"
        elif type_ == "SimpleItem":
            object_ = Items.SimpleItem(name)
            type_ = "items"
        else:
            raise ValueError("Wrong Type : "+type_)
        self.objects[type_].append(object_)
        self.edit_objects()
        return object_

    def edit_objects(self):
        LangJson.EnJson(self).save()
        if len(self.objects["blocks"]):
            BlocksClass.BlocksClass(self).save()
            os.makedirs(os.path.join(self.paths["Assets"], "textures", "block"), exist_ok=True)
            for i in self.objects["blocks"]:
                if i.type_ == "SimpleBlock":
                    BlocksClass.SimpleBlocksClass(self, i).save()
                    BlockStatesJson.BlockStatesJson(self, i).save()
                    BlockJson.SimpleBlockJson(self, i).save()
                    BlockJson.BlockItemJson(self, i).save()
                    if i.loot:
                        BlockLootJson.SimpleBlockLootJson(self, i).save()
                    if i.texture != "":
                        shutil.copyfile(os.path.join(self.paths["Folder"], "textures", i.texture+".png"),
                                        os.path.join(self.paths["Assets"], "textures", "block", i.texture+".png"))
        if len(self.objects["items"]):
            ItemsClass.ItemsClass(self).save()
            os.makedirs(os.path.join(self.paths["Assets"], "textures", "item"), exist_ok=True)
            for i in self.objects["items"]:
                if i.type_ == "SimpleItem":
                    ItemsClass.SimpleItemClass(self, i).save()
                    ItemJson.SimpleItemJson(self, i).save()
                    if i.texture != "":
                        shutil.copyfile(os.path.join(self.paths["Folder"], "textures", i.texture+".png"),
                                        os.path.join(self.paths["Assets"], "textures", "item", i.texture+".png"))

    def edit_main(self):
        main = MainClass.MainClass(self)
        main.save()

    def create_folder(self):
        os.makedirs(os.path.join(self.paths["Folder"], "textures"))
        datas = {
            "version": self.version,
            "modid": self.modid,
            "url": self.url,
            "credits": self.credits,
            "authors": self.authors,
            "description": self.description
        }
        with open(os.path.join(self.paths["Folder"], "project.json"), "w") as f:
            json.dump(datas, f, indent=4)
        forge = "https://files.minecraftforge.net/maven/net/minecraftforge/forge/1.14.4-28.1.0/" \
                "forge-1.14.4-28.1.0-mdk.zip"
        r = requests.get(forge)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(self.paths["Folder"])
        shutil.rmtree(os.path.join(self.paths["Java"], "com"))
        os.makedirs(os.path.join(self.paths["Java"], "fr", "pymodder", self.modid), exist_ok=True)
        self.paths["Main"] = os.path.join(self.paths["Java"], "fr", "pymodder", self.modid)
        self.paths["Assets"] = os.path.join(self.paths["Ressources"], "assets", self.modid)
        os.makedirs(self.paths["Assets"])
        self.main.logger.info("Forge downloaded.")
        self.create_mc()
        self.edit_toml()
        self.edit_build()
        self.edit_main()
        self.main.logger.info("Project folder created.")

    def create_mc(self):
        os.makedirs(os.path.join(self.paths["Folder"], "mc"))
        os.makedirs(os.path.join(self.paths["Folder"], "mc", "assets"))
        os.makedirs(os.path.join(self.paths["Folder"], "mc", "assets", "objects"))
        os.makedirs(os.path.join(self.paths["Folder"], "mc", "assets", "indexes"))
        os.makedirs(os.path.join(self.paths["Folder"], "mc", "assets", "virtual"))
        os.makedirs(os.path.join(self.paths["Folder"], "mc", "assets", "virtual", "legacy"))
        os.makedirs(os.path.join(self.paths["Folder"], "mc", "libraries"))
        os.makedirs(os.path.join(self.paths["Folder"], "mc", "natives"))
        os.makedirs(os.path.join(self.paths["Folder"], "mc", "resources"))
        os.makedirs(os.path.join(self.paths["Folder"], "mc", "versions"))
        r = requests.get("http://163.172.232.196/versions-1.14.4.zip")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(os.path.join(self.paths["Folder"], "mc", "versions"))
        self.main.logger.info("Minecraft downloaded.")

    def edit_toml(self):
        toml = """
modLoader="javafml"
loaderVersion="[28,)"

[[mods]]
modId="{0}"
version="{1}"
displayName="{2}"
displayURL="{3}"
credits="{4}"
authors="{5}"
description="{6}"

[[dependencies.{0}]]
modId="forge"
mandatory=true
versionRange="[28,)"
ordering="NONE"
side="BOTH"

[[dependencies.{0}]]
modId="minecraft"
mandatory=true
versionRange="[1.14.4]"
ordering="NONE"
side="BOTH"
""".format(self.modid, self.version, self.name, self.url, self.credits, self.authors, self.description)
        with open(os.path.join(self.paths["Ressources"], "META-INF", "mods.toml"), "w") as f:
            f.write(toml)

    def edit_build(self):
        build = """
buildscript {
    repositories {
        maven { url = 'https://files.minecraftforge.net/maven' }
        jcenter()
        mavenCentral()
    }
    dependencies {
        classpath group: 'net.minecraftforge.gradle', name: 'ForgeGradle', version: '3.+', changing: true
    }
}
apply plugin: 'net.minecraftforge.gradle'
// Only edit below this line, the above code adds and enables the necessary things for Forge to be setup.
apply plugin: 'eclipse'
apply plugin: 'maven-publish'

version = 'VERSION'
group = 'fr.pymodder.MODID' // http://maven.apache.org/guides/mini/guide-naming-conventions.html
archivesBaseName = 'NOM'

sourceCompatibility = targetCompatibility = compileJava.sourceCompatibility = compileJava.targetCompatibility = '1.8' // Need this here so eclipse task generates correctly.

minecraft {
    // The mappings can be changed at any time, and must be in the following format.
    // snapshot_YYYYMMDD   Snapshot are built nightly.
    // stable_#            Stables are built at the discretion of the MCP team.
    // Use non-default mappings at your own risk. they may not always work.
    // Simply re-run your setup task after changing the mappings to update your workspace.
    mappings channel: 'snapshot', version: '20190719-1.14.3'
    // makeObfSourceJar = false // an Srg named sources jar is made by default. uncomment this to disable.
    
    // accessTransformer = file('src/main/resources/META-INF/accesstransformer.cfg')

    // Default run configurations.
    // These can be tweaked, removed, or duplicated as needed.
    runs {
        client {
            workingDirectory project.file('run')

            // Recommended logging data for a userdev environment
            property 'forge.logging.markers', 'SCAN,REGISTRIES,REGISTRYDUMP'

            // Recommended logging level for the console
            property 'forge.logging.console.level', 'debug'

            mods {
                examplemod {
                    source sourceSets.main
                }
            }
        }

        server {
            workingDirectory project.file('run')

            // Recommended logging data for a userdev environment
            property 'forge.logging.markers', 'SCAN,REGISTRIES,REGISTRYDUMP'

            // Recommended logging level for the console
            property 'forge.logging.console.level', 'debug'

            mods {
                examplemod {
                    source sourceSets.main
                }
            }
        }

        data {
            workingDirectory project.file('run')

            // Recommended logging data for a userdev environment
            property 'forge.logging.markers', 'SCAN,REGISTRIES,REGISTRYDUMP'

            // Recommended logging level for the console
            property 'forge.logging.console.level', 'debug'

            args '--mod', 'examplemod', '--all', '--output', file('src/generated/resources/')

            mods {
                examplemod {
                    source sourceSets.main
                }
            }
        }
    }
}

dependencies {
    // Specify the version of Minecraft to use, If this is any group other then 'net.minecraft' it is assumed
    // that the dep is a ForgeGradle 'patcher' dependency. And it's patches will be applied.
    // The userdev artifact is a special name and will get all sorts of transformations applied to it.
    minecraft 'net.minecraftforge:forge:1.14.4-28.1.0'

    // You may put jars on which you depend on in ./libs or you may define them like so..
    // compile "some.group:artifact:version:classifier"
    // compile "some.group:artifact:version"

    // Real examples
    // compile 'com.mod-buildcraft:buildcraft:6.0.8:dev'  // adds buildcraft to the dev env
    // compile 'com.googlecode.efficient-java-matrix-library:ejml:0.24' // adds ejml to the dev env

    // The 'provided' configuration is for optional dependencies that exist at compile-time but might not at runtime.
    // provided 'com.mod-buildcraft:buildcraft:6.0.8:dev'

    // These dependencies get remapped to your current MCP mappings
    // deobf 'com.mod-buildcraft:buildcraft:6.0.8:dev'

    // For more info...
    // http://www.gradle.org/docs/current/userguide/artifact_dependencies_tutorial.html
    // http://www.gradle.org/docs/current/userguide/dependency_management.html

}

// Example for how to get properties into the manifest for reading by the runtime..
jar {
    manifest {
        attributes([
            "Specification-Title": "examplemod",
            "Specification-Vendor": "examplemodsareus",
            "Specification-Version": "1", // We are version 1 of ourselves
            "Implementation-Title": project.name,
            "Implementation-Version": "${version}",
            "Implementation-Vendor" :"examplemodsareus",
            "Implementation-Timestamp": new Date().format("yyyy-MM-dd'T'HH:mm:ssZ")
        ])
    }
}

// Example configuration to allow publishing using the maven-publish task
// we define a custom artifact that is sourced from the reobfJar output task
// and then declare that to be published
// Note you'll need to add a repository here
def reobfFile = file("$buildDir/reobfJar/output.jar")
def reobfArtifact = artifacts.add('default', reobfFile) {
    type 'jar'
    builtBy 'reobfJar'
}
publishing {
    publications {
        mavenJava(MavenPublication) {
            artifact reobfArtifact
        }
    }
    repositories {
        maven {
            url "file:///${project.projectDir}/mcmodsrepo"
        }
    }
}""".replace("VERSION", self.version).replace("MODID", self.modid).replace("NOM", self.name)
        with open(os.path.join(self.paths["Folder"], "build.gradle"), "w") as f:
            f.write(build)

    @classmethod
    def new(cls, main):
        name = "Untitled"
        while name in os.listdir(os.path.join(os.path.dirname(__file__), "..", "..", "Mods")):
            if name == "Untitled":
                name = name + "-1"
            else:
                name = name.split("-")[0] + "-" + str(int(name.split("-")[1])+1)
        return Project(main, name)