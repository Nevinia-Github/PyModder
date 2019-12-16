
package fr.pymodder.projecttest.items;

import fr.pymodder.projecttest.ProjectTest;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.Item;
import net.minecraft.client.util.ITooltipFlag;
import net.minecraft.item.ItemStack;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.StringTextComponent;
import net.minecraft.world.World;
import java.util.List;

public class Projectitem extends Item
{
    protected Projectitem()
    {
        super(new Item.Properties().group(ProjectTest.PROJECTTAB_GROUP).maxStackSize(25));
        setRegistryName("projectitem");
    }

    
    @Override
    public void addInformation(ItemStack stack, World worldIn, List<ITextComponent> tooltip, ITooltipFlag flag) {
        tooltip.add(new StringTextComponent("ProjectItem by PyModder"));
    }
    
    
}
