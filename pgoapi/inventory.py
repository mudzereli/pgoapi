from __future__ import absolute_import

from collections import defaultdict

from pgoapi.protos.POGOProtos import Inventory_pb2 as Inventory_Enum

cdarkgray = '\033[1;30m'
cblack = '\033[0;30m'
cred = '\033[1;31m'
cdarkred = '\033[0;31m'
cgreen = '\033[1;32m'
cdarkgreen = '\033[0;32m'
cyellow = '\033[1;33m'
cdarkyellow = '\033[0;33m'
cblue = '\033[1;34m'
cdarkblue = '\033[0;34m'
cmagenta = '\033[1;35m'
cdarkmagenta = '\033[0;35m'
ccyan = '\033[1;36m'
cdarkcyan = '\033[0;36m'
cgray = '\033[0;37m'
cwhite = '\033[1;37m'
cdefault = '\033[0;39m'

class Inventory:
    def __init__(self, inventory_items):
        self.inventory_items = inventory_items
        self.ultra_balls = 0
        self.great_balls = 0
        self.poke_balls = 0
        self.master_balls = 0
        self.potion = 0
        self.hyper_potion = 0
        self.super_potion = 0
        self.max_potion = 0
        self.pokemon_candy = defaultdict()
        self.setup_inventory()

    def setup_inventory(self):
        for inventory_item in self.inventory_items:
            item = inventory_item['inventory_item_data'].get('item', {})
            item_id = item.get('item_id', -1)
            item_count = item.get('count', 0)
            if item_id == Inventory_Enum.ITEM_POTION:
                self.potion = item_count
            elif item_id == Inventory_Enum.ITEM_SUPER_POTION:
                self.super_potion = item_count
            elif item_id == Inventory_Enum.ITEM_MAX_POTION:
                self.max_potion = item_count
            elif item_id == Inventory_Enum.ITEM_HYPER_POTION:
                self.hyper_potion = item_count
            elif item_id == Inventory_Enum.ITEM_POKE_BALL:
                self.poke_balls = item_count
            elif item_id == Inventory_Enum.ITEM_GREAT_BALL:
                self.great_balls = item_count
            elif item_id == Inventory_Enum.ITEM_MASTER_BALL:
                self.master_balls = item_count
            elif item_id == Inventory_Enum.ITEM_ULTRA_BALL:
                self.ultra_balls = item_count
            pokemon_family = inventory_item['inventory_item_data'].get('pokemon_family', {})
            self.pokemon_candy[pokemon_family.get('family_id', -1)] = pokemon_family.get('candy', -1)


    def can_attempt_catch(self):
        return self.poke_balls + self.great_balls + self.ultra_balls + self.master_balls > 0

    def take_pokeball(self):
        self.poke_balls -= 1

    def take_greatball(self):
        self.poke_balls -= 1

    def take_masterball(self):
        self.master_balls -= 1

    def take_ultraball(self):
        self.ultra_balls -= 1

    def take_next_ball(self):
        if self.poke_balls > 0:
            self.take_pokeball()
            return Inventory_Enum.ITEM_POKE_BALL
        elif self.great_balls > 0:
            self.take_greatball()
            return Inventory_Enum.ITEM_GREAT_BALL
        elif self.ultra_balls > 0:
            self.take_ultraball()
            return Inventory_Enum.ITEM_ULTRA_BALL
        elif self.master_balls > 0:
            self.take_masterball()
            return Inventory_Enum.ITEM_MASTER_BALL
        else:
            return -1

    def take_ball(self, ball_id):
        if ball_id == Inventory_Enum.ITEM_POKE_BALL:
            self.poke_balls -= 1
        elif ball_id == Inventory_Enum.ITEM_GREAT_BALL:
            self.great_balls -= 1
        elif ball_id == Inventory_Enum.ITEM_ULTRA_BALL:
            self.ultra_balls -= 1
        elif ball_id == Inventory_Enum.ITEM_MASTER_BALL:
            self.master_balls -= 1

    def __str__(self):
        return (cdarkgray + "\nINVENTORY --> " + cdarkcyan + "Poke Balls: " + cdefault + "{0:>3}" + cdarkgray + " |" + cdarkcyan + " Great Balls:  " + cdefault + "{1:>3}" + cdarkgray + " |" + cdarkcyan + " Ultra Balls:  " + cdefault + "{3:>3}" + cdarkgray + " |" + cdarkcyan + " Master Balls: " + cdefault + "{2:>3}" + \
                cdarkgray + "\nINVENTORY --> " + cred   + "Potion:     " + cdefault + "{4:>3}" + cdarkgray + " |" + cred   + " Super Potion: " + cdefault + "{5:>3}" + cdarkgray + " |" + cred   + " Hyper Potion: " + cdefault + "{7:>3}" + cdarkgray + " |" + cred   + " Max Potion:   " + cdefault + "{6:>3}" + cred + "").format(self.poke_balls,
                                                                                        self.great_balls if self.great_balls > 0 else "-",
                                                                                        self.master_balls if self.master_balls > 0 else "-",
                                                                                        self.ultra_balls if self.ultra_balls > 0 else "-",
                                                                                        self.potion if self.potion > 0 else "-",
                                                                                        self.super_potion if self.super_potion > 0 else "-",
                                                                                        self.max_potion if self.max_potion > 0 else "-",
                                                                                        self.hyper_potion if self.hyper_potion > 0 else "-")

    def __repr__(self):
        return self.__str__()
