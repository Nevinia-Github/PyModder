
package fr.pymodder.projecttest.blocks;

import net.minecraft.block.Block;
import net.minecraft.block.material.Material;

public class Bloc extends Block
{
    protected Bloc()
    {
        super(Block.Properties.create(Material.ROCK).hardnessAndResistance(25F, 600F));
        setRegistryName("bloc");
    }
}
