
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

class Pokemon:
    def __init__(self, pokemon_data, pokemon_names):
        self.pokemon_data = pokemon_data
        self.stamina = 0
        self.pokemon_id = 0
        self.cp = 0
        self.stamina_max = 0
        self.is_egg = False
        self.origin = -1
        self.height_m = 0.0
        self.weight_kg = 0.0
        self.individual_attack = 0
        self.individual_defense = 0
        self.individual_stamina = 0
        self.cp_multiplier = 0.0
        self.nickname = ""
        self.additional_cp_multiplier = 0.0
        self.id = 0
        self.pokemon_id = 0
        self.favorite = -1
        self.is_favorite = False
        self.iv = 0.0
        self.parse_values()
        self.pokemon_type = pokemon_names.get(str(self.pokemon_id), "NA").encode('ascii', 'ignore')

    def parse_values(self):
        self.stamina = self.pokemon_data.get('stamina', 0)
        self.favorite = self.pokemon_data.get('favorite', -1)
        self.is_favorite = self.favorite != -1
        self.pokemon_id = self.pokemon_data.get('pokemon_id', 0)
        self.id = self.pokemon_data.get('id', 0)
        self.cp = self.pokemon_data.get('cp', 0)
        self.stamina_max = self.pokemon_data.get('stamina_max', 0)
        self.is_egg = self.pokemon_data.get('is_egg', False)
        self.origin = self.pokemon_data.get('origin', 0)
        self.height_m = self.pokemon_data.get('height', 0.0)
        self.weight_kg = self.pokemon_data.get('weight_kg', 0.0)
        self.individual_attack = self.pokemon_data.get('individual_attack', 0)
        self.individual_defense = self.pokemon_data.get('individual_defense', 0)
        self.individual_stamina = self.pokemon_data.get('individual_stamina', 0)
        self.cp_multiplier = self.pokemon_data.get('cp_multiplier', 0.0)
        self.additional_cp_multiplier = self.pokemon_data.get('additional_cp_multiplier', 0.0)
        self.nickname = self.pokemon_data.get('nickname', "")
        self.iv = self.get_iv_percentage()

    def __str__(self):
        return (cgray + "Type: " + cwhite + "{1:<16}" + cgray + " CP: " + cwhite + "{2:<4}" + cgray + " IV: " + cwhite + "{3:>.0f}" + cdefault).format(self.nickname, self.pokemon_type, self.cp, self.iv)

    def __repr__(self):
        return self.__str__()

    def get_iv_percentage(self):
        return ((self.individual_attack + self.individual_stamina + self.individual_defense + 0.0) / 45.0) * 100.0

    def is_valid_pokemon(self):
        return self.pokemon_id > 0
