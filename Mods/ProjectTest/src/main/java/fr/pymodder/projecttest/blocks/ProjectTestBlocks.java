
package fr.pymodder.projecttest.blocks;

import fr.pymodder.projecttest.ProjectTest;
import net.minecraft.block.Block;
import net.minecraft.item.BlockItem;
import net.minecraft.item.Item;
import net.minecraft.item.ItemGroup;
import net.minecraftforge.event.RegistryEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.ObjectHolder;

@Mod.EventBusSubscriber(modid = ProjectTest.MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD)
public class ProjectTestBlocks
{
    @ObjectHolder(ProjectTest.MOD_ID + ":bloc")
    public static final Block PROJECTBLOC = null;


    @SubscribeEvent
    public static void registerBlock(final RegistryEvent.Register<Block> event)
    {
        event.getRegistry().register(new Projectbloc());

    }

    @SubscribeEvent
    public static void registerItem(final RegistryEvent.Register<Item> event)
    {
        event.getRegistry().register(new BlockItem(PROJECTBLOC, new Item.Properties().group(ProjectTest.PROJECTTAB_GROUP)).setRegistryName(PROJECTBLOC.getRegistryName()));

    }
}
