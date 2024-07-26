# Installation:

## Linux/WSL:
1) git clone https://github.com/camfulton/dotloot2.git
1.1) install make if you don't have it, google it for your distribution
1.2) install python3 if you don't have it, google it for your distribution
2) make install

Requires espeak for text to speech, which is installed by the makefile.

# Windows

No idea, install WSL and follow the instructions above

# Usage:

## Flags:
Blocks tagged with `leveling:` will be skipped unless you pass this flag:
--leveling

Blocks with lookups will be skipped if you pass this flag, useful for league start:
--skip-lookups

1) Set up your output path in config.py to whatever your POE filter folder is
2) Write a filter in the filters folder
3) Add any custom sounds to the sounds folder
4) `poetry run python3 dotloot.py filters/example.yaml`
5) replace `example.yaml` above with whatever you named your filter if you didn't catch that
6) load up your filter in poe

# Syntax Reference
## Read the filter in filters/example.yaml -- it has some comments that guide you through how things work.

## https://www.poewiki.net/wiki/Guide:Item_filter
^ This is an important reference for GGG's filter syntax.

## https://www.poewiki.net/wiki/Guide:Item_filter_guide
^ This one also helpful, but more verbose.

## These are all of the keys you can use in your filter yaml file:
| yaml key | corresponding ggg filter syntax key |
| -------- | --------------------- |
| ilvl | ItemLevel |
| alvl | AreaLevel |
| droplvl | DropLevel |
| quality | Quality |
| rarity | Rarity |
| classes | Class |
| bases | BaseType |
| sockets | Sockets |
| links | LinkedSockets |
| colors | SocketGroup |
| height | Height |
| width | Width |
| explicit | HasExplicitMod |
| enchanted | AnyEnchantment |
| enchantments | HasEnchantment |
| stacksize | StackSize |
| gemlvl | GemLevel |
| identified | Identified |
| corrupted | Corrupted |
| influence | HasInfluence |
| elder | ElderItem |
| shaper | ShaperItem |
| fractured | FracturedItem |
| synthesized | SynthesisedItem |
| synthesised | SynthesisedItem |
| shapedmap | ShapedMap |
| eldermap | ElderMap |
| blighted | BlightedMap |
| uberblighted | UberBlightedMap |
| maptier | MapTier |
| border | SetBorderColor |
| fg | SetTextColor |
| bg | SetBackgroundColor |
| fontsize | SetFontSize |
| sound | PlayAlertSound |
| positionalsound | PlayAlertSoundPositional |
| customsound | CustomAlertSound |
| icon | MinimapIcon |
| beam | PlayEffect |
| altquality | AlternateQuality |
| replica | Replica |
| defencepercentile | BaseDefencePercentile |
| scourged | Scourged |
| exarch | HasSearingExarchImplicit |
| eater | HasEaterOfWorldsImplicit |
