import constants

def nodrop(item):
    if item.get('name').lower() in constants.UNDROPPABLE:
        return True