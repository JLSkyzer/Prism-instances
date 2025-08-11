function obp:random

execute positioned 0 80 0 as @e[type=item,distance=..0.5] run tp @s ~ ~1 ~

execute if entity @s[scores={math_output=1}] run setblock 0 80 0 minecraft:grass_block
execute if entity @s[scores={math_output=2}] run setblock 0 80 0 minecraft:oak_leaves[persistent=true]
execute if entity @s[scores={math_output=3}] run setblock 0 80 0 minecraft:oak_log
execute if entity @s[scores={math_output=4}] run setblock 0 80 0 minecraft:podzol
execute if entity @s[scores={math_output=5}] run setblock 0 80 0 minecraft:coarse_dirt
execute if entity @s[scores={math_output=6}] run setblock 0 80 0 minecraft:dirt
execute if entity @s[scores={math_output=7}] run setblock 0 80 0 minecraft:mycelium
execute if entity @s[scores={math_output=8}] run setblock 0 80 0 minecraft:clay
execute if entity @s[scores={math_output=9}] run setblock 0 80 0 minecraft:moss_block
execute if entity @s[scores={math_output=10}] run setblock 0 80 0 minecraft:crimson_stem
execute if entity @s[scores={math_output=11}] run setblock 0 80 0 minecraft:warped_stem
execute if entity @s[scores={math_output=12}] run setblock 0 80 0 minecraft:azalea_leaves[persistent=true]
execute if entity @s[scores={math_output=12}] run setblock 0 80 0 minecraft:rooted_dirt