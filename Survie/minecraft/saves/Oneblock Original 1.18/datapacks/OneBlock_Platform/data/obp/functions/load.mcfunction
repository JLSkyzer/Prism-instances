execute unless entity @e[tag=obp_stand] run setblock 0 80 0 minecraft:grass_block
execute unless entity @e[tag=obp_stand] run tp @a 0 80 0
execute unless entity @e[tag=obp_stand] run summon marker 0 0 0 {Tags:["obp_stand"]}

scoreboard objectives add math_input1 dummy
scoreboard objectives add math_input2 dummy
scoreboard objectives add math_output dummy