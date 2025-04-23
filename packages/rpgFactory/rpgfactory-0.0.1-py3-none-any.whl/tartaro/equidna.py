class Equidna:
    def __init__(self, especie, class_, level):
        self.name = ""
        self.level = int(level)
        self.especie = especie
        self.class_ = class_
        self.attribute = {"strength": 0, "inteligence": 0, "dexterity": 0, "speed": 0, "vitality": 0}
        self.hp = 0 
        self.mp = 0 
        self.attack = 0 
        self.defense = 0 
        self.skills = []
        self.items = []

    modifiers = { "Beast": [2, 1, 0, 3, 3], "Demon": [1, 2, 3, 2, 1], "Dragon": [8, 5, 4, 6, 8],
                  "Elemental": [1, 3, 2, 1, 2], "Fairy": [0, 3, 3, 2, 1], "Human": [2, 2, 2, 2, 2],
                    "Insect": [2, 1, 1, 4, 1], "Plant": [3, 1, 1, 1, 4], "Undead": [4, 0, 0, 1, 4] }
    
    grown_factor = { "Beast": 1.2, "Demon": 1.2, "Dragon": 1.4, "Elemental": 1.2, "Fairy": 1.1, 
                    "Human": 1.1,"Insect": 1.1, "Plant": 1.2, "Undead": 1 }
    
    skill_list = { "Beast": ["Bite", "Claw", "Roar"], "Demon": ["Fireball", "Darkness", "Curse"],
                    "Dragon": ["Fire Breath", "Tail Whip", "Wing Attack"], "Elemental": ["Fire", "Water", "Earth"],
                    "Fairy": ["Heal", "Protect", "Charm"], "Human": ["Sword", "Bow", "Magic"],
                    "Insect": ["Sting", "Web", "Acid"], "Plant": ["Roots", "Pollen", "Vine"], "Undead": ["Drain", "Fear", "Curse"] }

    items_list = { "Beast": ["Fur", "Claw", "Meat"], "Demon": ["Horn", "Fang", "Soul"],
                    "Dragon": ["Scale", "Claw", "Fire Stone"], "Elemental": ["Crystal", "Fire Stone", "Stone"],
                    "Fairy": ["Dust", "Wing", "Flower"], "Human": ["Coin", "Sword", "Bow"],
                    "Insect": ["Stinger", "Web", "Acid"], "Plant": ["Leaf", "Pollen", "Vine"], "Undead": ["Bone", "Cloth", "Curse"] }
    @classmethod
    def create_horde(cls, especie, class_, *levels):
        horde = [cls(i, especie, class_) for i in levels]
        for monster in horde:
            monster.apply_especie_modifiers(cls.modifiers, cls.grown_factor)
            monster.set_skills(cls.skill_list)
            monster.set_items(cls.items_list)
        return horde

    def apply_especie_modifiers(self, modifiers, grown_factor):
        for key, value in modifiers.items():
            if key == self.especie:
                self.attribute["strength"] += (value[0] + round(self.level * grown_factor[self.especie]))
                self.attribute["inteligence"] += (value[1] + round(self.level * grown_factor[self.especie]))
                self.attribute["dexterity"] += (value[2] + round(self.level * grown_factor[self.especie]))
                self.attribute["speed"] += (value[3] + round(self.level * grown_factor[self.especie]))
                self.attribute["vitality"] += (value[4] + round(self.level * grown_factor[self.especie]))
                break
                
        self.update_stats()

    def set_skills(self, skill_list):
        for key, value in skill_list.items():
            if key == self.especie:
                self.skills = value
                break
    
    def set_items(self, items_list):
        for key, value in items_list.items():
            if key == self.especie:
                self.items = value
                break

    def update_stats(self):
        self.hp = 10 * (self.attribute["vitality"] + self.level)
        self.mp = 10 * (self.attribute["inteligence"] + self.level)
        self.attack = (self.attribute["strength"] + self.attribute["dexterity"]) * 2 + self.level
        self.defense = (self.attribute["vitality"] + self.attribute["speed"]) * 2 + self.level

    def __str__(self):
        return f'{self.name} ({self.especie}), {self.level}\n HP: {self.hp}, MP: {self.mp}\n ATK: {self.attack}, DEF: {self.defense}\n Skills: {", ".join(self.skills)}'