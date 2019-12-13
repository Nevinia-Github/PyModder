
package fr.pymodder.projecttest.items;

import fr.pymodder.projecttest.ProjectTest;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.Item;

public class Projectitem extends Item
{
    protected Projectitem()
    {
        super(new Item.Properties().group(ProjectTest.PROJECTTAB_GROUP).maxStackSize(25));
        setRegistryName("projectitem");
    }

    
    
}
