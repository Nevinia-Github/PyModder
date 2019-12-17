import os
from Core.Utils.Constants import ITEMGROUP
from Core.Utils.Utils import save_template


class SimpleItemClass:
    def __init__(self, project, item):
        self.item = item
        self.project = project

    def save(self):
        replaces = {
            "PACKAGE": "fr.pymodder.MODID",
            "MODID": self.project.modid,
            "NAMECLASS": self.item.name.title().replace(" ", "_"),
            "REGISTRY_NAME": self.item.registry_name,
            "SCRIPT": "\n".join("    " + i for i in self.item.script.split("\n") if not i.startswith("import")),
            "EXTRAIMPORTS": "\n".join(i for i in self.item.script.split("\n") if i.startswith("import")),
            "ITEMGROUP": "ItemGroup." + self.item.itemgroup if self.item.itemgroup in ITEMGROUP else
            "NAME." + self.item.itemgroup,
            "NAME": self.project.name,
            "STACKSIZE": self.item.stacksize
        }
        file = os.path.join(self.project.paths["Main"], "items", self.item.name.title().replace(" ", "_") + ".java")
        save_template(file, "SimpleItemClass.txt", replaces)


class ItemsClass:
    def __init__(self, project):
        self.project = project

    def save(self):
        declare_item = ""
        register_items = ""
        for i in self.project.objects["items"]:
            replaces = {
                "REGISTRY_NAME": i.registry_name,
                "NAMEVAR": i.name.upper().replace(" ", "_"),
                "NAMECLASS": i.name.title().replace(" ", "_"),
                "NAME": self.project.name
            }
            declare_item += '    @ObjectHolder(NAME.MOD_ID + ":REGISTRY_NAME")\n' \
                .replace("REGISTRY_NAME", i.registry_name).replace("NAME", self.project.name)
            declare_item += '    public static final Item NAMEVAR = null;\n'
            register_items += "        event.getRegistry().register(new NAMECLASS());\n"
            for k, v in replaces.items():
                declare_item = declare_item.replace(k, v)
                register_items = register_items.replace(k, v)
        replaces = {
            "PACKAGE": "fr.pymodder.MODID",
            "MODID": self.project.modid,
            "NAME": self.project.name,
            "DECLAREITEMS": declare_item,
            "REGISTERITEMS": register_items
        }
        file = os.path.join(self.project.paths["Main"], "items", self.project.name + "Items.java")
        save_template(file, "ItemsClass.txt", replaces)
