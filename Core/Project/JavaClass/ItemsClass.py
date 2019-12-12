import os
from Core.Utils.Constants import ITEMGROUP


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
            "SCRIPT": "\n".join("    " + i for i in self.item.script.split("\n")),
            "ITEMGROUP": "ItemGroup." + self.item.itemgroup if self.item.itemgroup in ITEMGROUP else
            "NAME." + self.item.itemgroup,
            "NAME": self.project.name
        }
        file = """
package PACKAGE.items;

import PACKAGE.NAME;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.Item;

public class NAMECLASS extends Item
{
    protected NAMECLASS()
    {
        super(new Item.Properties().group(ITEMGROUP));
        setRegistryName("REGISTRY_NAME");
    }

SCRIPT
}
"""
        for k, v in replaces.items():
            file = file.replace(k, v)
        with open(
                os.path.join(self.project.paths["Main"], "items", self.item.name.title().replace(" ", "_") + ".java"),
                "w") as f:
            f.write(file)


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
        file = """
package PACKAGE.items;

import PACKAGE.NAME;
import net.minecraft.item.Item;
import net.minecraft.item.ItemGroup;
import net.minecraftforge.event.RegistryEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.ObjectHolder;

@Mod.EventBusSubscriber(modid = NAME.MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD)
public class NAMEItems
{
DECLAREITEMS

    @SubscribeEvent
    public static void registerItem(RegistryEvent.Register<Item> event)
    {
REGISTERITEMS
    }
}
"""
        for k, v in replaces.items():
            file = file.replace(k, v)
        os.makedirs(os.path.join(self.project.paths["Main"], "items"), exist_ok=True)
        with open(os.path.join(self.project.paths["Main"], "items", self.project.name + "Items.java"), "w") as f:
            f.write(file)
