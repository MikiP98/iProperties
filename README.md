# iProperties

<br/>

## Description

### Iris Properties

An alternative preprocessing app to [PoTater](https://github.com/Null-MC/PoTater)

<br/>

## Features

### Auto `.glsl` definition file generation <sup>(similar to [PoTater](https://github.com/Null-MC/PoTater))</sup>

```properties
#= BLOCK_WATER
block.8=minecraft:water minecraft:flowing_water
#= BLOCK_BAMBOO
block.11=bamboo bamboo_sapling
```
Will generate
```glsl
#define BLOCK_WATER 8
#define BLOCK_BAMBOO 11
```

You can also provide multiple definition entries separated by `,`
```properties
#= BLOCK_WALL_POST, BLOCK_WALL_MIN
block.64=cobblestone_wall:north=none:east=none:south=none:west=none:up=true
```
Will generate
```glsl
#define BLOCK_WALL_POST 64
#define BLOCK_WALL_MIN 64
```

<br/>

### Auto numering

`*` can be used as a wildcard for the number <sup>(similar to [PoTater](https://github.com/Null-MC/PoTater))</sup>

```properties
block.8=minecraft:water minecraft:flowing_water
block.*=minecraft:short_grass minecraft:grass
block.*=minecraft:tall_grass:half=lower
block.16=bamboo bamboo_sapling
block.*=minecraft:tall_grass:half=upper
```
Will generate
```properties
block.8=minecraft:water minecraft:flowing_water
block.9=minecraft:short_grass minecraft:grass
block.10=minecraft:tall_grass:half=lower
block.16=bamboo bamboo_sapling
block.17=minecraft:tall_grass:half=upper
```

Additionaly if you want to repeat an entry multiple times, e.g. inside an `#ifdef`, you can use the `**` operator

```properties
block.8=minecraft:water minecraft:flowing_water
block.11=bamboo bamboo_sapling
block.*=minecraft:tall_grass:half=lower
block.*=minecraft:tall_grass:half=upper

#ifdef BOES_EARTH_BLOCKSTATES
block.*=vine:is_on_leaves=false
#else
block.**=vine
#endif

block.*=minecraft:hanging_roots minecraft:weeping_vines minecraft:cave_vines:berries=false
```
Will generate
```properties
block.8=minecraft:water minecraft:flowing_water
block.11=bamboo bamboo_sapling
block.12=minecraft:tall_grass:half=lower
block.13=minecraft:tall_grass:half=upper

#= BLOCK_VINE
#ifdef BOES_EARTH_BLOCKSTATES
block.14=vine:is_on_leaves=false
#else
block.14=vine
#endif

block.15=minecraft:hanging_roots minecraft:weeping_vines minecraft:cave_vines:berries=false
```
The `glsl` file also won't repeat the same entry multiple times, a.k.a. `#define BLOCK_VINE 14` will be generated only once

<br/>

### Dynamic variable groups for automation

```properties
$colors = black blue brown cyan gray green light_blue light_gray lime magenta orange pink purple red white yellow
$vanilla_wood_types = acacia bamboo birch cherry crimson dark_oak jungle mangrove oak pale_oak spruce warped

block.8=minecraft:water minecraft:flowing_water

$tall_plants = minecraft:small_dripleaf minecraft:pitcher_plant minecraft:tall_grass minecraft:sunflower minecraft:large_fern minecraft:peony minecraft:rose_bush minecraft:lilac minecraft:tall_seagrass \
 biomesoplenty:tall_lavender biomesoplenty:eyebulb biomesoplenty:blue_hydrangea

block.*=[tall_plants]:half=lower
block.*=[tall_plants]:half=upper
block.*=[vanilla_wood_types]_sapling

#$
$humility-afm_candlestick_metals = copper exposed_copper gold oxidized_copper waxed_copper waxed_exposed_copper waxed_oxidized_copper waxed_weathered_copper weathered_copper
#$
$candles = candle [colors]_candle
$humility-afm_candlesticks = humility-afm:candlestick_[humility-afm_candlestick_metals]_candle humility-afm:candlestick_[humility-afm_candlestick_metals]_candle_[colors]
$supplementaries_candles = supplementaries:candle_holder supplementaries:candle_holder_[colors]
#$

# Blocks for FloodFill to ignore
block.50=chain ladder lever lightning_rod scaffolding tripwire tripwire_hook [candles]:lit=false [vanilla_wood_types]_button \
 gravestones:gravestone gravestones:gravestone_chipped gravestones:gravestone_damaged \
 [humility-afm_candlesticks]:lit=false \
 [supplementaries_candles]:lit=false
```
Will generate
```properties
block.8=minecraft:water minecraft:flowing_water

block.9=minecraft:small_dripleaf:half=lower minecraft:pitcher_plant:half=lower minecraft:tall_grass:half=lower minecraft:sunflower:half=lower minecraft:large_fern:half=lower minecraft:peony:half=lower minecraft:rose_bush:half=lower minecraft:lilac:half=lower minecraft:tall_seagrass:half=lower \
 biomesoplenty:tall_lavender:half=lower biomesoplenty:eyebulb:half=lower biomesoplenty:blue_hydrangea:half=lower

block.10=minecraft:small_dripleaf:half=upper minecraft:pitcher_plant:half=upper minecraft:tall_grass:half=upper minecraft:sunflower:half=upper minecraft:large_fern:half=upper minecraft:peony:half=upper minecraft:rose_bush:half=upper minecraft:lilac:half=upper minecraft:tall_seagrass:half=upper \
 biomesoplenty:tall_lavender:half=upper biomesoplenty:eyebulb:half=upper biomesoplenty:blue_hydrangea:half=upper

block.11=acacia_sapling bamboo_sapling birch_sapling cherry_sapling crimson_sapling dark_oak_sapling jungle_sapling mangrove_sapling oak_sapling pale_oak_sapling spruce_sapling warped_sapling

# Blocks for FloodFill to ignore
block.50=chain ladder lever lightning_rod scaffolding tripwire tripwire_hook candle:lit=false black_candle:lit=false blue_candle:lit=false brown_candle:lit=false cyan_candle:lit=false gray_candle:lit=false green_candle:lit=false light_blue_candle:lit=false light_gray_candle:lit=false lime_candle:lit=false magenta_candle:lit=false orange_candle:lit=false pink_candle:lit=false purple_candle:lit=false red_candle:lit=false white_candle:lit=false yellow_candle:lit=false acacia_button bamboo_button birch_button cherry_button crimson_button dark_oak_button jungle_button mangrove_button oak_button pale_oak_button spruce_button warped_button polished_blackstone_button stone_button rail activator_rail detector_rail powered_rail:powered=false redstone_wire:power=0 repeater:powered=false comparator:powered=false \
 gravestones:gravestone gravestones:gravestone_chipped gravestones:gravestone_damaged \
 humility-afm:candlestick_copper_candle:lit=false humility-afm:candlestick_exposed_copper_candle:lit=false humility-afm:candlestick_gold_candle:lit=false humility-afm:candlestick_oxidized_copper_candle:lit=false humility-afm:candlestick_waxed_copper_candle:lit=false humility-afm:candlestick_waxed_exposed_copper_candle:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle:lit=false humility-afm:candlestick_waxed_weathered_copper_candle:lit=false humility-afm:candlestick_weathered_copper_candle:lit=false humility-afm:candlestick_copper_candle_black:lit=false humility-afm:candlestick_copper_candle_blue:lit=false humility-afm:candlestick_copper_candle_brown:lit=false humility-afm:candlestick_copper_candle_cyan:lit=false humility-afm:candlestick_copper_candle_gray:lit=false humility-afm:candlestick_copper_candle_green:lit=false humility-afm:candlestick_copper_candle_light_blue:lit=false humility-afm:candlestick_copper_candle_light_gray:lit=false humility-afm:candlestick_copper_candle_lime:lit=false humility-afm:candlestick_copper_candle_magenta:lit=false humility-afm:candlestick_copper_candle_orange:lit=false humility-afm:candlestick_copper_candle_pink:lit=false humility-afm:candlestick_copper_candle_purple:lit=false humility-afm:candlestick_copper_candle_red:lit=false humility-afm:candlestick_copper_candle_white:lit=false humility-afm:candlestick_copper_candle_yellow:lit=false humility-afm:candlestick_exposed_copper_candle_black:lit=false humility-afm:candlestick_exposed_copper_candle_blue:lit=false humility-afm:candlestick_exposed_copper_candle_brown:lit=false humility-afm:candlestick_exposed_copper_candle_cyan:lit=false humility-afm:candlestick_exposed_copper_candle_gray:lit=false humility-afm:candlestick_exposed_copper_candle_green:lit=false humility-afm:candlestick_exposed_copper_candle_light_blue:lit=false humility-afm:candlestick_exposed_copper_candle_light_gray:lit=false humility-afm:candlestick_exposed_copper_candle_lime:lit=false humility-afm:candlestick_exposed_copper_candle_magenta:lit=false humility-afm:candlestick_exposed_copper_candle_orange:lit=false humility-afm:candlestick_exposed_copper_candle_pink:lit=false humility-afm:candlestick_exposed_copper_candle_purple:lit=false humility-afm:candlestick_exposed_copper_candle_red:lit=false humility-afm:candlestick_exposed_copper_candle_white:lit=false humility-afm:candlestick_exposed_copper_candle_yellow:lit=false humility-afm:candlestick_gold_candle_black:lit=false humility-afm:candlestick_gold_candle_blue:lit=false humility-afm:candlestick_gold_candle_brown:lit=false humility-afm:candlestick_gold_candle_cyan:lit=false humility-afm:candlestick_gold_candle_gray:lit=false humility-afm:candlestick_gold_candle_green:lit=false humility-afm:candlestick_gold_candle_light_blue:lit=false humility-afm:candlestick_gold_candle_light_gray:lit=false humility-afm:candlestick_gold_candle_lime:lit=false humility-afm:candlestick_gold_candle_magenta:lit=false humility-afm:candlestick_gold_candle_orange:lit=false humility-afm:candlestick_gold_candle_pink:lit=false humility-afm:candlestick_gold_candle_purple:lit=false humility-afm:candlestick_gold_candle_red:lit=false humility-afm:candlestick_gold_candle_white:lit=false humility-afm:candlestick_gold_candle_yellow:lit=false humility-afm:candlestick_oxidized_copper_candle_black:lit=false humility-afm:candlestick_oxidized_copper_candle_blue:lit=false humility-afm:candlestick_oxidized_copper_candle_brown:lit=false humility-afm:candlestick_oxidized_copper_candle_cyan:lit=false humility-afm:candlestick_oxidized_copper_candle_gray:lit=false humility-afm:candlestick_oxidized_copper_candle_green:lit=false humility-afm:candlestick_oxidized_copper_candle_light_blue:lit=false humility-afm:candlestick_oxidized_copper_candle_light_gray:lit=false humility-afm:candlestick_oxidized_copper_candle_lime:lit=false humility-afm:candlestick_oxidized_copper_candle_magenta:lit=false humility-afm:candlestick_oxidized_copper_candle_orange:lit=false humility-afm:candlestick_oxidized_copper_candle_pink:lit=false humility-afm:candlestick_oxidized_copper_candle_purple:lit=false humility-afm:candlestick_oxidized_copper_candle_red:lit=false humility-afm:candlestick_oxidized_copper_candle_white:lit=false humility-afm:candlestick_oxidized_copper_candle_yellow:lit=false humility-afm:candlestick_waxed_copper_candle_black:lit=false humility-afm:candlestick_waxed_copper_candle_blue:lit=false humility-afm:candlestick_waxed_copper_candle_brown:lit=false humility-afm:candlestick_waxed_copper_candle_cyan:lit=false humility-afm:candlestick_waxed_copper_candle_gray:lit=false humility-afm:candlestick_waxed_copper_candle_green:lit=false humility-afm:candlestick_waxed_copper_candle_light_blue:lit=false humility-afm:candlestick_waxed_copper_candle_light_gray:lit=false humility-afm:candlestick_waxed_copper_candle_lime:lit=false humility-afm:candlestick_waxed_copper_candle_magenta:lit=false humility-afm:candlestick_waxed_copper_candle_orange:lit=false humility-afm:candlestick_waxed_copper_candle_pink:lit=false humility-afm:candlestick_waxed_copper_candle_purple:lit=false humility-afm:candlestick_waxed_copper_candle_red:lit=false humility-afm:candlestick_waxed_copper_candle_white:lit=false humility-afm:candlestick_waxed_copper_candle_yellow:lit=false humility-afm:candlestick_waxed_exposed_copper_candle_black:lit=false humility-afm:candlestick_waxed_exposed_copper_candle_blue:lit=false humility-afm:candlestick_waxed_exposed_copper_candle_brown:lit=false humility-afm:candlestick_waxed_exposed_copper_candle_cyan:lit=false humility-afm:candlestick_waxed_exposed_copper_candle_gray:lit=false humility-afm:candlestick_waxed_exposed_copper_candle_green:lit=false humility-afm:candlestick_waxed_exposed_copper_candle_light_blue:lit=false humility-afm:candlestick_waxed_exposed_copper_candle_light_gray:lit=false humility-afm:candlestick_waxed_exposed_copper_candle_lime:lit=false humility-afm:candlestick_waxed_exposed_copper_candle_magenta:lit=false humility-afm:candlestick_waxed_exposed_copper_candle_orange:lit=false humility-afm:candlestick_waxed_exposed_copper_candle_pink:lit=false humility-afm:candlestick_waxed_exposed_copper_candle_purple:lit=false humility-afm:candlestick_waxed_exposed_copper_candle_red:lit=false humility-afm:candlestick_waxed_exposed_copper_candle_white:lit=false humility-afm:candlestick_waxed_exposed_copper_candle_yellow:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle_black:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle_blue:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle_brown:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle_cyan:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle_gray:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle_green:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle_light_blue:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle_light_gray:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle_lime:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle_magenta:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle_orange:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle_pink:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle_purple:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle_red:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle_white:lit=false humility-afm:candlestick_waxed_oxidized_copper_candle_yellow:lit=false humility-afm:candlestick_waxed_weathered_copper_candle_black:lit=false humility-afm:candlestick_waxed_weathered_copper_candle_blue:lit=false humility-afm:candlestick_waxed_weathered_copper_candle_brown:lit=false humility-afm:candlestick_waxed_weathered_copper_candle_cyan:lit=false humility-afm:candlestick_waxed_weathered_copper_candle_gray:lit=false humility-afm:candlestick_waxed_weathered_copper_candle_green:lit=false humility-afm:candlestick_waxed_weathered_copper_candle_light_blue:lit=false humility-afm:candlestick_waxed_weathered_copper_candle_light_gray:lit=false humility-afm:candlestick_waxed_weathered_copper_candle_lime:lit=false humility-afm:candlestick_waxed_weathered_copper_candle_magenta:lit=false humility-afm:candlestick_waxed_weathered_copper_candle_orange:lit=false humility-afm:candlestick_waxed_weathered_copper_candle_pink:lit=false humility-afm:candlestick_waxed_weathered_copper_candle_purple:lit=false humility-afm:candlestick_waxed_weathered_copper_candle_red:lit=false humility-afm:candlestick_waxed_weathered_copper_candle_white:lit=false humility-afm:candlestick_waxed_weathered_copper_candle_yellow:lit=false humility-afm:candlestick_weathered_copper_candle_black:lit=false humility-afm:candlestick_weathered_copper_candle_blue:lit=false humility-afm:candlestick_weathered_copper_candle_brown:lit=false humility-afm:candlestick_weathered_copper_candle_cyan:lit=false humility-afm:candlestick_weathered_copper_candle_gray:lit=false humility-afm:candlestick_weathered_copper_candle_green:lit=false humility-afm:candlestick_weathered_copper_candle_light_blue:lit=false humility-afm:candlestick_weathered_copper_candle_light_gray:lit=false humility-afm:candlestick_weathered_copper_candle_lime:lit=false humility-afm:candlestick_weathered_copper_candle_magenta:lit=false humility-afm:candlestick_weathered_copper_candle_orange:lit=false humility-afm:candlestick_weathered_copper_candle_pink:lit=false humility-afm:candlestick_weathered_copper_candle_purple:lit=false humility-afm:candlestick_weathered_copper_candle_red:lit=false humility-afm:candlestick_weathered_copper_candle_white:lit=false humility-afm:candlestick_weathered_copper_candle_yellow:lit=false \
 supplementaries:candle_holder:lit=false supplementaries:candle_holder_black:lit=false supplementaries:candle_holder_blue:lit=false supplementaries:candle_holder_brown:lit=false supplementaries:candle_holder_cyan:lit=false supplementaries:candle_holder_gray:lit=false supplementaries:candle_holder_green:lit=false supplementaries:candle_holder_light_blue:lit=false supplementaries:candle_holder_light_gray:lit=false supplementaries:candle_holder_lime:lit=false supplementaries:candle_holder_magenta:lit=false supplementaries:candle_holder_orange:lit=false supplementaries:candle_holder_pink:lit=false supplementaries:candle_holder_purple:lit=false supplementaries:candle_holder_red:lit=false supplementaries:candle_holder_white:lit=false supplementaries:candle_holder_yellow:lit=false
```

You can also use `\n` between the entries in the variable or make a multiline variable, so that the later generated properties file will have a new line in those places
```properties
$vanilla_stairs = acacia_stairs andesite_stairs
$createdeco_stairs = createdeco:andesite_sheet_stairs createdeco:brass_sheet_stairs
$create_stairs = create:copper_shingle_stairs create:copper_tile_stairs

$stairs = [vanilla_stairs] \n [createdeco_stairs] \n [create_stairs]

block.128=[stairs]:shape=straight:half=bottom:facing=north
```
As well as
```properties
$stairs = acacia_stairs andesite_stairs \
 createdeco:andesite_sheet_stairs createdeco:brass_sheet_stairs \
 create:copper_shingle_stairs create:copper_tile_stairs

block.128=[stairs]:shape=straight:half=bottom:facing=north
```
Will generate
```properties
block.128=acacia_stairs:shape=straight:half=bottom:facing=north andesite_stairs:shape=straight:half=bottom:facing=north \
 reatedeco:andesite_sheet_stairs:shape=straight:half=bottom:facing=north createdeco:brass_sheet_stairs:shape=straight:half=bottom:facing=north \
 create:copper_shingle_stairs:shape=straight:half=bottom:facing=north create:copper_tile_stairs:shape=straight:half=bottom:facing=north
```

<br/>

### Custom ignored comments

You can create ignored comments using `#$`, such comment won't be transfered to the resulting processed files, the line will be skipped

<br/>

## How to use

### First install the package:

- Make sure you have [Python](https://www.python.org/downloads/) installed  
  The app was tested using Python 3.12
- Open console and run `pip install git+https://github.com/MikiP98/iProperties.git`

### Create template files for processing

IProperties will try to find a file named `block.iProperties.properties` to process  
If such a file won't be found it will try to find file named `block.template.properties`

These files will then be processed into 3 files:
- `block.properties` - ready to use by Iris or Optifine properties file
- `block.glsl` - ready to use by Iris or Optifine glsl mapping file
- `block.PoTater.properties` - template in PoTater format if you would need it

### How to run the app

- Open the console in the target directory or use the `cd` command to go there
- Run command `iProperties` or `Iris`

`block.iProperties.properties` or `block.template.properties` will be processed to `block.properties`, `block.glsl` and `block.PoTater.properties`