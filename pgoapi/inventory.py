from __future__ import absolute_import

from collections import defaultdict

from pgoapi.protos.POGOProtos.Inventory import Item_pb2 as Inventory_Enum

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
        self.lucky_eggs = 0
        self.pokemon_candy = defaultdict()
        self.eggs_available = []
        self.incubators_available = []
        self.incubators_busy = []
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
            elif item_id == Inventory_Enum.ITEM_LUCKY_EGG:
                self.lucky_eggs = item_count
            pokemon_family = inventory_item['inventory_item_data'].get('pokemon_family', {})
            self.pokemon_candy[pokemon_family.get('family_id', -1)] = pokemon_family.get('candy', -1)
            pokemon_data = inventory_item['inventory_item_data'].get('pokemon_data', {})
            if pokemon_data.get('is_egg', False) and not pokemon_data.get('egg_incubator_id', False):
                self.eggs_available.append(pokemon_data)
            egg_incubators = inventory_item['inventory_item_data'].get('egg_incubators', {}).get('egg_incubator', {})
            for incubator in egg_incubators:
                if "pokemon_id" in incubator:
                    self.incubators_busy.append(incubator)
                else:
                    self.incubators_available.append(incubator)

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

    def take_next_ball(self, capture_priority=None):
        if not capture_priority:
            capture_priority = {1: 35.0, 2: 45.0, 3: 55.0}
        priority = Inventory.__get_ball_priority(capture_priority)
        if self.can_attempt_catch() and priority <= Inventory_Enum.ITEM_MASTER_BALL:
            if priority <= Inventory_Enum.ITEM_POKE_BALL and self.poke_balls > 0:
                self.take_pokeball()
                return Inventory_Enum.ITEM_POKE_BALL
            if priority <= Inventory_Enum.ITEM_GREAT_BALL and self.great_balls > 0:
                self.take_greatball()
                return Inventory_Enum.ITEM_GREAT_BALL
            if priority <= Inventory_Enum.ITEM_ULTRA_BALL and self.ultra_balls > 0:
                self.take_ultraball()
                return Inventory_Enum.ITEM_ULTRA_BALL
            if priority <= Inventory_Enum.ITEM_MASTER_BALL and self.master_balls > 0:
                self.take_masterball()
                return Inventory_Enum.ITEM_MASTER_BALL
            else:
                return self.take_next_ball()
        else:
            return -1

    @staticmethod
    def __get_ball_priority(capture_priority):
        if capture_priority.get(Inventory_Enum.ITEM_POKE_BALL, 0.0) > 0.30:
            return Inventory_Enum.ITEM_POKE_BALL
        if capture_priority.get(Inventory_Enum.ITEM_GREAT_BALL, 0.0) > 0.30:
            return Inventory_Enum.ITEM_GREAT_BALL
        if capture_priority.get(Inventory_Enum.ITEM_ULTRA_BALL, 0.0) > 0.30:
            return Inventory_Enum.ITEM_ULTRA_BALL
        else:
            return Inventory_Enum.ITEM_MASTER_BALL

    def has_lucky_egg(self):
        for inventory_item in self.inventory_items:
            item = inventory_item['inventory_item_data'].get('item', {})
            item_id = item.get('item_id', -1)
            if item_id == Inventory_Enum.ITEM_LUCKY_EGG:
                return True
        return False

    def take_lucky_egg(self):
        self.lucky_eggs -= 1
        return Inventory_Enum.ITEM_LUCKY_EGG

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
        return (cwhite + "{0}" + ccyan + " x " + cdarkcyan + "Poke Balls"  + cmagenta + " / " + \
                cwhite + "{1}" + ccyan + " x " + cdarkcyan + "Great Balls" + cmagenta + " / " + \
                cwhite + "{3}" + ccyan + " x " + cdarkcyan + "Ultra Balls" + cmagenta + " / " + \
                cwhite + "{2}" + ccyan + " x " + cdarkcyan + "Master Balls" + cdefault \
                ).format(self.poke_balls,
                #cdefault + "{0}" + cmagenta + "x" + cdarkcyan +  + cmagenta + " /" + cdarkcyan + " Ultra Balls: " + cdefault + "{3:>3}" + cmagenta + " /" + cdarkcyan + " Master Balls: " + cdefault + "{2:>3}" + cdefault).format(self.poke_balls,
                #cmagenta + "\nINVENTORY --> " + cdarkcyan + "Poke Balls: " + cdefault + "{0:>3}" + cmagenta + " |" + cdarkcyan + " Great Balls:  " + cdefault + "{1:>3}" + cmagenta + " |" + cdarkcyan + " Ultra Balls:  " + cdefault + "{3:>3}" + cmagenta + " |" + cdarkcyan + " Master Balls: " + cdefault + "{2:>3}" + cmagenta + "|" + \
                #cmagenta + "\nINVENTORY --> " + cred   + "Potion:     " + cdefault + "{4:>3}" + cmagenta + " |" + cred   + " Super Potion: " + cdefault + "{5:>3}" + cmagenta + " |" + cred   + " Hyper Potion: " + cdefault + "{7:>3}" + cmagenta + " |" + cred   + " Max Potion:   " + cdefault + "{6:>3}" + cmagenta + "|" + cdefault).format(self.poke_balls,
                                                                                        self.great_balls,
                                                                                        self.master_balls,
                                                                                        self.ultra_balls,
                                                                                        self.potion,
                                                                                        self.super_potion,
                                                                                        self.max_potion,
                                                                                        self.hyper_potion,
                                                                                        self.lucky_eggs)

    def __repr__(self):
        return self.__str__()
