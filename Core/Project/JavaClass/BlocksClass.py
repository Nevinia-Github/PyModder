import os
from Core.Utils.Constants import ITEMGROUP
from Core.Utils.Utils import save_template


class SimpleBlocksClass:
    def __init__(self, project, bloc):
        self.bloc = bloc
        self.project = project

    def save(self):
        replaces = {
            "PACKAGE": "fr.pymodder.MODID",
            "MODID": self.project.modid,
            "NAMECLASS": self.bloc.name.title().replace(" ", "_"),
            "MATERIAL": self.bloc.material,
            "HARDNESS": self.bloc.hardness,
            "RESISTANCE": self.bloc.resistance,
            "REGISTRY_NAME": self.bloc.registry_name,
            "SCRIPT": "\n".join("    " + i for i in self.bloc.script.split("\n") if not i.startswith("import")),
            "EXTRAIMPORTS": "\n".join(i for i in self.bloc.script.split("\n") if i.startswith("import"))
        }
        file = os.path.join(self.project.paths["Main"], "blocks", self.bloc.name.title().replace(" ", "_")+".java")
        save_template(file, "SimpleBlockClass.txt", replaces)


class BlocksClass:
    def __init__(self, project):
        self.project = project

    def save(self):
        declare_blocks = ""
        register_blocks = ""
        register_items = ""
        for i in self.project.objects["blocks"]:
            replaces = {
                "REGISTRY_NAME": i.registry_name,
                "NAMEVAR": i.name.upper().replace(" ", "_"),
                "NAMECLASS": i.name.title().replace(" ", "_"),
                "ITEMGROUP": "ItemGroup." + i.itemgroup if i.itemgroup in ITEMGROUP else "NAME." + i.itemgroup,
                "NAME": self.project.name
            }
            declare_blocks += '    @ObjectHolder(NAME.MOD_ID + ":REGISTRY_NAME")\n'\
                .replace("REGISTRY_NAME", i.registry_name).replace("NAME", self.project.name)
            declare_blocks += '    public static final Block NAMEVAR = null;\n'
            register_blocks += "        event.getRegistry().register(new NAMECLASS());\n"
            register_items += "        event.getRegistry().register(new BlockItem(NAMEVAR, new Item.Properties()" \
                              ".group(ITEMGROUP)).setRegistryName(NAMEVAR.getRegistryName()));\n"
            for k, v in replaces.items():
                declare_blocks = declare_blocks.replace(k, v)
                register_blocks = register_blocks.replace(k, v)
                register_items = register_items.replace(k, v)
        replaces = {
            "PACKAGE": "fr.pymodder.MODID",
            "MODID": self.project.modid,
            "NAME": self.project.name,
            "DECLAREBLOCKS": declare_blocks,
            "REGISTERBLOCKS": register_blocks,
            "REGISTERITEMS": register_items
        }
        file = os.path.join(self.project.paths["Main"], "blocks", self.project.name+"Blocks.java")
        save_template(file, "BlocksClass.txt", replaces)
