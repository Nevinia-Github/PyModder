import os


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
            "REGISTRY_NAME": self.bloc.registry_name
        }
        file = """
package PACKAGE.blocks;

import net.minecraft.block.Block;
import net.minecraft.block.material.Material;

public class NAMECLASS extends Block
{
    protected NAMECLASS()
    {
        super(Block.Properties.create(Material.MATERIAL).hardnessAndResistance(HARDNESS, RESISTANCE));
        setRegistryName("REGISTRY_NAME");
    }
}
"""
        for k, v in replaces.items():
            file = file.replace(k, v)
        with open(os.path.join(self.project.paths["Main"], "blocks", self.bloc.name.title().replace(" ", "_")+".java"),
                  "w") as f:
            f.write(file)


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
                "NAME": self.project.name
            }
            declare_blocks += '    @ObjectHolder(NAME.MOD_ID + ":REGISTRY_NAME")\n'\
                .replace("REGISTRY_NAME", i.registry_name).replace("NAME", self.project.name)
            declare_blocks += '    public static final Block NAMEVAR = null;\n'
            register_blocks += "        event.getRegistry().register(new NAMECLASS());\n"
            register_items += "        event.getRegistry().register(new BlockItem(NAMEVAR, new Item.Properties()" \
                              ".group(ItemGroup.BUILDING_BLOCKS)).setRegistryName(NAMEVAR.getRegistryName()));\n"
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
        file = """
package PACKAGE.blocks;

import PACKAGE.NAME;
import net.minecraft.block.Block;
import net.minecraft.item.BlockItem;
import net.minecraft.item.Item;
import net.minecraft.item.ItemGroup;
import net.minecraftforge.event.RegistryEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.ObjectHolder;

@Mod.EventBusSubscriber(modid = NAME.MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD)
public class NAMEBlocks
{
DECLAREBLOCKS

    @SubscribeEvent
    public static void registerBlock(final RegistryEvent.Register<Block> event)
    {
REGISTERBLOCKS
    }

    @SubscribeEvent
    public static void registerItem(final RegistryEvent.Register<Item> event)
    {
REGISTERITEMS
    }
}
"""
        for k, v in replaces.items():
            file = file.replace(k, v)
        os.makedirs(os.path.join(self.project.paths["Main"], "blocks"), exist_ok=True)
        with open(os.path.join(self.project.paths["Main"], "blocks", self.project.name+"Blocks.java"), "w") as f:
            f.write(file)
