import os


class MainClass:
    def __init__(self, project):
        self.project = project

    def save(self):
        replaces = {
            "NAME": self.project.name,
            "PACKAGE": "fr.pymodder.MODID",
            "MODID": self.project.modid,
        }
        file = """
package PACKAGE;

import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.*;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.stream.Collectors;

@Mod(NAME.MOD_ID)
public class NAME
{
    public static final String MOD_ID = "MODID";
    public static final Logger LOGGER = LogManager.getLogger(MOD_ID);
    
    public NAME()
    {
        FMLJavaModLoadingContext.get().getModEventBus().addListener(this::setup);
        FMLJavaModLoadingContext.get().getModEventBus().addListener(this::clientSetup);
        FMLJavaModLoadingContext.get().getModEventBus().addListener(this::serverSetup);
    }
    
    private void setup(final FMLCommonSetupEvent event) {
        LOGGER.info("NAME setup completed.");
    }

    private void clientSetup(final FMLClientSetupEvent event) {
        LOGGER.info("NAME client setup completed.");
    }

    private void serverSetup(final FMLDedicatedServerSetupEvent event) {
        LOGGER.info("NAME server setup completed.");
    }
}"""
        for k, v in replaces.items():
            file = file.replace(k, v)
        with open(os.path.join(self.project.paths["Main"], self.project.name+".java"), "w") as f:
            f.write(file)