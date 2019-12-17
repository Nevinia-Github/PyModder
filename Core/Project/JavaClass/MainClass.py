import os
from Core.Utils.Constants import ICON_BLOCKS
from Core.Utils.Utils import save_template


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
                    "SCRIPT": "\n".join("    " + j for j in i.script.split("\n") if not j.startswith("import"))
                }
                if i.icon not in ICON_BLOCKS and not extra_imports.endswith("Blocks;"):
                    extra_imports += "\nimport PACKAGE.blocks.NAMEBlocks;"
                extra_imports += "\n" + "\n".join(j for j in i.script.split("\n") if j.startswith("import"))
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
        file = os.path.join(self.project.paths["Main"], self.project.name+".java")
        save_template(file, "MainClass.txt", replaces)
