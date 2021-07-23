from collections import namedtuple
from exceptions import handle
import itertools
import json
import re

import constants
import requests
from utils import items


OverviewAndType = namedtuple('OverviewAndType', ['overview', 'type'])
LookupData = namedtuple('LookupData', ['overview', 'type', 'min_chaos', 'max_chaos'])

class PoeNinjaClient():
    def __init__(self, league):
        self.base_url = 'https://poe.ninja/api/data/'
        self.league = league
        # POE Ninja requires this for urls
        self.CURRENCY_OVERVIEW = 'currency'
        self.ITEM_OVERVIEW = 'item'
        # Convert the friendly filter syntax to POE Ninja syntax.
        self.ITEM_TYPES = {
            'currency': OverviewAndType(self.CURRENCY_OVERVIEW, 'Currency'),
            'fragments': OverviewAndType(self.CURRENCY_OVERVIEW, 'Fragment'),
            'bases': OverviewAndType(self.ITEM_OVERVIEW, 'BaseType'),
            'oils': OverviewAndType(self.ITEM_OVERVIEW, 'Oil'),
            'incubators': OverviewAndType(self.ITEM_OVERVIEW, 'Incubator'),
            'scarabs': OverviewAndType(self.ITEM_OVERVIEW, 'Scarab'),
            'fossils': OverviewAndType(self.ITEM_OVERVIEW, 'Fossil'),
            'resonators': OverviewAndType(self.ITEM_OVERVIEW, 'Resonator'),
            'essences': OverviewAndType(self.ITEM_OVERVIEW, 'Essence'),
            'divination cards': OverviewAndType(self.ITEM_OVERVIEW, 'DivinationCard'),
            'prophecies': OverviewAndType(self.ITEM_OVERVIEW, 'Prophecy'),
            'gems': OverviewAndType(self.ITEM_OVERVIEW, 'SkillGem'),
            'helmet enchants': OverviewAndType(self.ITEM_OVERVIEW, 'HelmetEnchant'),
            'unique maps': OverviewAndType(self.ITEM_OVERVIEW, 'UniqueMap'),
            'maps': OverviewAndType(self.ITEM_OVERVIEW, 'Map'),
            'unique jewels': OverviewAndType(self.ITEM_OVERVIEW, 'UniqueJewel'),
            'unique flasks': OverviewAndType(self.ITEM_OVERVIEW, 'UniqueFlask'),
            'unique weapons': OverviewAndType(self.ITEM_OVERVIEW, 'UniqueWeapon'),
            'unique armours': OverviewAndType(self.ITEM_OVERVIEW, 'UniqueArmour'),
            'unique accessories': OverviewAndType(self.ITEM_OVERVIEW, 'UniqueAccessory'),
            'uniques': OverviewAndType(self.ITEM_OVERVIEW, 'ALL_UNIQUES'),
            'exclusive uniques': OverviewAndType(self.ITEM_OVERVIEW, 'EXCLUSIVE_UNIQUES')
        }
        self.GROUP_BY_TYPES = {
            'STR_GROUPS': {
                'variant',
            },
            'INT_GROUPS': {
                'levelRequired',
            }
        }
        self.QUALIFIER_SYNTAX = {
            'corrupted': 'corrupted',
            'gemlvl': 'gemLevel',
            'quality': 'gemQuality',
            'ilvl': 'levelRequired',
            'links': 'links',
            'maptier': 'mapTier',
            'variant': 'variant',
        }
        self.PROPERTY_SYNTAX = {
            'frame_type': 'itemClass',
            'name': 'name',
            'base_type': 'baseType',
        }
        self.ALL_UNIQUE_TYPES = [
            v for k, v in self.ITEM_TYPES.items()
            if 'unique' in k and
            k not in ['uniques', 'exclusive uniques']
        ]
        self.qualifiers = None

    def get_item_groups_for_block(self, block):
        print(f'  $ Looking up price data for: {block.lines[0].block_name} on poe.ninja')
        # We store things like links, quality, etc. as "qualifiers" for each block.
        # This way we know what to loop over when considering if an item from a POE Ninja
        # lookup meets the requirements specified in the filter.
        self.clear_then_set_qualifiers(block)
        # Parse the lookup line and get back a LookupData object.
        lookup_data = self.parse_lookup(block)
        # Perform and process request(s) to the POE Ninja API to build item data info.
        item_data, low_value_bases = self.fetch_item_data_and_low_value_bases(lookup_data)
        # Group up all the items so they can be written into actual filter blocks.
        item_groups = self.group_items(item_data, low_value_bases, lookup_data.type)

        return item_groups

    def group_items(self, item_data, low_value_bases, lookup_type):
        '''Sometimes we end up w/ a base type lookup (or whatever) where, for example,
        a Shaper OR Hunter item of the same base is worth more than 100c, but other
        variants are not.

        In order to write these in the filter, the function returns different groups
        for the variants since the filter logic needs to write them separately.
        '''
        group_by = [self.QUALIFIER_SYNTAX['variant'], self.QUALIFIER_SYNTAX['ilvl']]

        items = [item_data]

        for key in group_by:
            items = self.group_by(items, key)

        if lookup_type == self.ITEM_TYPES['exclusive uniques']:
            items = self.trim_groups_for_exclusive_bases(groups_of_items, low_value_bases)

        return items

    def trim_groups_for_exclusive_bases(self, item_groups):
        new_groups = []

        for group in item_groups:
            new_group = []

            for item in group:
                if item['baseType'] not in self.low_value_bases:
                    new_group.append(item)

            new_groups.append(new_group)

        return new_groups

    def group_by(self, item_groups, group_by):
        '''This function is a little wobbly but basically what is happening here is this:

        We initially ingest item_groups = [[item_data]]

        So we have one item group, which is just all of the item data.

        We then go through that one big group and sort it all by whatever key we are grouping by,
        let's say variant.

        Then we use itertools.groupby on our sorted group to make new lists of only items that
        match whatever we are grouping by, again variant.

        Then we return something like:
        [
            [shaper items],
            [elder items],
            [redeemer items],
            ...
        ]

        Then this function is called again w/ the data we just returned, but with a new thing to
        group on -- let's say ilvl.

        Repeat the process and we end up with a bunch of things like low level shaper items,
        shaper items above 82, 83, 84, 86, whatever.
        '''
        def get_group_by(item):
            if group_by in self.GROUP_BY_TYPES['STR_GROUPS']:
                return item.get(group_by, '')
            elif group_by in self.GROUP_BY_TYPES['INT_GROUPS']:
                return item.get(group_by, 0)
            else:
                msg = f'You need to add the type of {group_by} to the GROUP_BY_TYPES in the PoeNinjaClient class.'

                handle(msg)

        new_item_groups = []

        for group in item_groups:
            # self.scrub_garbage_variants(item_groups)

            sorted_group = sorted(group, key=get_group_by)

            for _, group in itertools.groupby(sorted_group, key=get_group_by):
                new_item_groups.append(list(group))

        return new_item_groups

    def scrub_garbage_variants(self, item_groups):
        for item_group in item_groups:
            for item in item_group:
                variant = item.get('variant')
                if variant and variant.upper() not in constants.VARIANTS_THAT_MATTER_FOR_FILTERS:
                    item['variant'] = 'SCRUBBED'


    def fetch_item_data_and_low_value_bases(self, lookup_data):
        item_data = []
        low_value_bases = set()

        # Sometimes a block has more than one type of item data it needs to request.
        # Most commonly this is for uniques.
        overviews_and_types = self.get_overviews_and_types_for_lookup(lookup_data)

        for overview_and_type in overviews_and_types:
            url = self.generate_url(overview_and_type)
            data = self.get_item_data_from_api(url)
            items = self.get_matching_items(data, lookup_data)

            low_value_bases.update(self.get_low_value_bases(item_data, lookup_data))
            item_data.extend(items)

        return (item_data, low_value_bases)

    
    def get_matching_items(self, data, lookup_data):
        matching_items = [
            item for item in data if
            not self.low_confidence(item) and
            self.in_price_range(item, lookup_data.min_chaos, lookup_data.max_chaos) and
            self.item_passes_block_qualifiers(item) and
            not items.nodrop(item) and
            not self.is_type(item, ['RELIC']) and
            not self.linked(item)
        ]

        return matching_items

    def is_type(self, item, item_types):
        for item_type in item_types:
            if item.get(self.PROPERTY_SYNTAX['frame_type']) == constants.FRAME_TYPES[item_type]:
                return True

        return False
    
    def get_low_value_bases(self, data, lookup_data):
        low_value_bases = [
            item.get('baseType', 'ITEM_HAS_NO_BASE') for item in data if
            not self.low_confidence(item) and
            not self.in_price_range(item, lookup_data.min_chaos, lookup_data.max_chaos) and
            self.item_passes_block_qualifiers(item) and
            not items.nodrop(item) and
            not self.is_type(item, ['RELIC']) and
            not self.linked(item)
        ]

        return low_value_bases

    def in_price_range(self, item, min_chaos=None, max_chaos=None):
        chaos_value = item.get('chaosValue')

        if not chaos_value:
            print(f'''
                    poe.ninja didn\'t have a buy price for {item['name']}
                    You will probably want to figure out if it should be in your filter.
                ''')

            return False

        if not min_chaos and not max_chaos:
            return True
        if min_chaos and chaos_value < min_chaos:
            return False
        if max_chaos and chaos_value >= max_chaos:
            return False

        return True
    
    def low_confidence(self, item):
        # The poe.ninja guy on the POE Discord claimed that 5 is the cutoff for low confidence.
        if item.get('count', 0) < 5:
            return True

    def linked(self, item):
        if 'links' in self.qualifiers:
            return False
        if item.get('links', 0) > 0 and item.get('name', '').lower() not in constants.ONLY_LINKED:
            return True

    def item_passes_block_qualifiers(self, item):
        '''This function parses things like:

        quality: ">= 10"

        Performing a lookup on the returned JSON from PoeNinja against the value of the
        qualifier.
        '''
        for qual_key, qual_value in self.qualifiers.items():
            item_value = item[qual_key]

            if isinstance(qual_value, bool):
                if item_value != qual_value:
                    return False

            elif qual_key in ['gemLevel', 'gemQuality', 'levelRequired', 'links', 'mapTier']:
                # we accept "gemLevel: 20" to mean gems of exactly level 20 here
                if isinstance(qual_value, int):
                    if item[qual_key] != qual_value:
                        return False
                else:
                    operator, qual_value = qual_value.split(' ')
                    qual_value = int(qual_value)

                    if operator == '>=':
                        if not item_value >= qual_value:
                            return False
                    elif operator == '>':
                        if not item_value > qual_value:
                            return False
                    elif operator == '<=':
                        if not item_value <= qual_value:
                            return False
                    elif operator == '<':
                        if not item_value < qual_value:
                            return False
                    elif operator in ['=', '==']:
                        if item_value != qual_value:
                            return False

        return True
    
    def generate_url(self, lookup_data):
        return f'{self.base_url}{lookup_data.overview}Overview?league={self.league}&type={lookup_data.type}'
    
    def get_item_data_from_api(self, url):
        try:
            return json.loads(requests.get(url).content)['lines']
        except json.decoder.JSONDecodeError:
            print(self.ALL_UNIQUE_TYPES)
            msg = f'Failed to get a response from url: {url}'

            handle(msg)

    def get_overviews_and_types_for_lookup(self, lookup_data):
        global_unique_lookup_types = [
            self.ITEM_TYPES['uniques'].type,
            self.ITEM_TYPES['exclusive uniques'].type,
        ]
        
        if lookup_data.type in global_unique_lookup_types:
            return self.ALL_UNIQUE_TYPES
        
        return [OverviewAndType(lookup_data.overview, lookup_data.type)]

    def parse_lookup(self, block):
        pattern = re.compile('^(\D+)\s(\d+)\s*(\d*)')
        item_type, min_chaos, max_chaos = pattern.match(block.lookup).groups()

        if item_type not in self.ITEM_TYPES.keys():
            msg = (
                f'The `{type(self).__name__}` does not know how to handle: '
                f'`{item_type}`\nPlease choose from the following options:\n\n'
            )

            for item_type in self.ITEM_TYPES.keys():
                msg += (f'- {item_type}\n')
            
            handle(msg)

        overview = self.ITEM_TYPES[item_type].overview
        item_type = self.ITEM_TYPES[item_type].type
        min_chaos = float(min_chaos)
        max_chaos = float(max_chaos) if max_chaos else None

        return LookupData(overview, item_type, min_chaos, max_chaos)
    
    def clear_then_set_qualifiers(self, block):
        qualifiers = {}

        for line in block.lines:
            qualifier = self.QUALIFIER_SYNTAX.get(line.parameter)
            if qualifier:
                qualifiers[qualifier] = value
        
        self.qualifiers = qualifiers
