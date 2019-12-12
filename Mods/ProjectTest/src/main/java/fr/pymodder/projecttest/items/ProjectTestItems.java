
package fr.pymodder.projecttest.items;

import fr.pymodder.projecttest.ProjectTest;
import net.minecraft.item.Item;
import net.minecraft.item.ItemGroup;
import net.minecraftforge.event.RegistryEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.ObjectHolder;

@Mod.EventBusSubscriber(modid = ProjectTest.MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD)
public class ProjectTestItems
{
    @ObjectHolder(ProjectTest.MOD_ID + ":projectitem")
    public static final Item PROJECTITEM = null;


    @SubscribeEvent
    public static void registerItem(RegistryEvent.Register<Item> event)
    {
        event.getRegistry().register(new Projectitem());

    }
}
