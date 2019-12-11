import os
from Core.Utils.Constants import ICON_BLOCKS


class MainClass:
    def __init__(self, project):
        self.project = project

    def save(self):
        groups = ""
        extra_imports = ""
        if len(self.project.objects["itemgroups"]):
            extra_imports += "import net.minecraft.item.ItemGroup;\nimport net.minecraft.item.ItemStack;\nimport " \
                             "net.minecraftforge.api.distmarker.Dist;\nimport net.minecraftforge.api.distmarker.OnlyIn;"
            for i in self.project.objects["itemgroups"]:
                replaces = {
                    'NAMEVAR': i.name.upper().replace(" ", "_") + "_GROUP",
                    "REGISTRY_NAME": i.registry_name,
                    "SEARCH": "true" if i.search else "false",
                    "ICON": "Blocks." + i.icon if i.icon in ICON_BLOCKS else "NAMEBlocks." + i.icon,
                    "NAME": self.project.name,
                    "PACKAGE": "fr.pymodder.MODID",
                    "MODID": self.project.modid,
                    "SCRIPT": "\n".join("        " + l for l in i.script.split("\n"))
                }
                if i.icon not in ICON_BLOCKS and not extra_imports.endswith("Blocks;"):
                    extra_imports += "\nimport PACKAGE.blocks.NAMEBlocks;"
                groups += "\n".join([
                    '    public static final ItemGroup NAMEVAR = new ItemGroup("REGISTRY_NAME")',
                    '    {',
                    '        @OnlyIn(Dist.CLIENT)',
                    '        @Override',
                    '        public ItemStack createIcon()',
                    '        {',
                    '            return new ItemStack(ICON);',
                    '        }', ''
                    '        @Override'
                    '        public boolean hasSearchBar()',
                    '        {',
                    '            return SEARCH;'
                    '        }',
                    '        SCRIPT'
                    '    };'
                ])
                groups += "\n"
                for k, v in replaces.items():
                    extra_imports = extra_imports.replace(k, v)
                    groups = groups.replace(k, v)

        replaces = {
            "NAME": self.project.name,
            "PACKAGE": "fr.pymodder.MODID",
            "MODID": self.project.modid,
            'EXTRA_IMPORTS': extra_imports,
            "GROUPS": groups
        }
        file = """
package PACKAGE;

import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.*;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
EXTRA_IMPORTS

import java.util.stream.Collectors;

@Mod(NAME.MOD_ID)
public class NAME
{
    public static final String MOD_ID = "MODID";
    public static final Logger LOGGER = LogManager.getLogger(MOD_ID);

GROUPS
    
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
