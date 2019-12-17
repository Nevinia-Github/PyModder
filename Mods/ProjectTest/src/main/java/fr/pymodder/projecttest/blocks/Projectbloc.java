package fr.pymodder.projecttest.blocks;

import net.minecraft.block.Block;
import net.minecraft.block.material.Material;

public class Projectbloc extends Block
{
    protected Projectbloc()
    {
        super(Block.Properties.create(Material.ROCK).hardnessAndResistance(2F, 6F));
        setRegistryName("bloc");
    }

    
    
}