
package fr.pymodder.projecttest;

import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.*;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemStack;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.api.distmarker.OnlyIn;
import fr.pymodder.projecttest.blocks.ProjectTestBlocks;

import java.util.stream.Collectors;

@Mod(ProjectTest.MOD_ID)
public class ProjectTest
{
    public static final String MOD_ID = "projecttest";
    public static final Logger LOGGER = LogManager.getLogger(MOD_ID);

    public static final ItemGroup PROJECTTAB_GROUP = new ItemGroup("projecttab")
    {
        @OnlyIn(Dist.CLIENT)
        @Override
        public ItemStack createIcon()
        {
            return new ItemStack(ProjectTestBlocks.PROJECTBLOC);
        }
        @Override        public boolean hasSearchBar()
        {
            return true;        }
    };

    
    public ProjectTest()
    {
        FMLJavaModLoadingContext.get().getModEventBus().addListener(this::setup);
        FMLJavaModLoadingContext.get().getModEventBus().addListener(this::clientSetup);
        FMLJavaModLoadingContext.get().getModEventBus().addListener(this::serverSetup);
    }
    
    private void setup(final FMLCommonSetupEvent event) {
        LOGGER.info("ProjectTest setup completed.");
    }

    private void clientSetup(final FMLClientSetupEvent event) {
        LOGGER.info("ProjectTest client setup completed.");
    }

    private void serverSetup(final FMLDedicatedServerSetupEvent event) {
        LOGGER.info("ProjectTest server setup completed.");
    }
}