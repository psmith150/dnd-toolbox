from __future__ import absolute_import
from enum import Enum, auto

class Ability(Enum):
    STRENGTH = auto()
    DEXTERITY = auto()
    CONSTITUTION = auto()
    INTELLIGENCE = auto()
    WISDOM = auto()
    CHARISMA = auto()

    @classmethod
    def get_values(cls):
        values = []
        for name, _ in Ability.__members__.items():
            values.append(name.title())
        return values

    @classmethod
    def get_display_name(cls, value):
        try:
            display = Ability(value).name.title()
        except ValueError:
            display = 'Unknown'
        return display
    
    @classmethod
    def convert_display_name(cls, name):
        try:
            converted_name = name.upper()
            value = Ability[converted_name]
        except KeyError:
            value = Ability.STRENGTH
        return value

class Skill(Enum):
    ACROBATICS = auto()
    ANIMAL_HANDLING = auto()
    ARCANA = auto()
    ATHLETICS = auto()
    DECEPTION = auto()
    HISTORY = auto()
    INSIGHT = auto()
    INTIMIDATION = auto()
    INVESTIGATION = auto()
    MEDICINE = auto()
    NATURE = auto()
    PERCEPTION = auto()
    PERFORMANCE = auto()
    PERSUASION = auto()
    RELIGION = auto()
    SLEIGHT_OF_HAND = auto()
    STEALTH = auto()
    SURVIVAL = auto()

    def ability(self) -> Ability:
        mapping = {
            self.ACROBATICS: Ability.DEXTERITY,
            self.ANIMAL_HANDLING: Ability.WISDOM,
            self.ARCANA: Ability.INTELLIGENCE,
            self.ATHLETICS: Ability.STRENGTH,
            self.DECEPTION: Ability.CHARISMA,
            self.HISTORY: Ability.INTELLIGENCE,
            self.INSIGHT: Ability.WISDOM,
            self.INTIMIDATION: Ability.CHARISMA,
            self.INVESTIGATION: Ability.INTELLIGENCE,
            self.MEDICINE: Ability.WISDOM,
            self.NATURE: Ability.INTELLIGENCE,
            self.PERCEPTION: Ability.WISDOM,
            self.PERFORMANCE: Ability.CHARISMA,
            self.PERSUASION: Ability.CHARISMA,
            self.RELIGION: Ability.INTELLIGENCE,
            self.SLEIGHT_OF_HAND: Ability.DEXTERITY,
            self.STEALTH: Ability.DEXTERITY,
            self.SURVIVAL: Ability.WISDOM
        }
        return mapping[self]
    
    @classmethod
    def get_values(cls):
        values = []
        for name, _ in Skill.__members__.items():
            values.append(name.title().replace('_', ' '))
        return values

    @classmethod
    def get_display_name(cls, value):
        try:
            display = Skill(value).name.title().replace('_', ' ')
        except ValueError:
            display = 'Unknown'
        return display
    
    @classmethod
    def convert_display_name(cls, name):
        try:
            converted_name = name.upper().replace(' ', '_')
            value = Skill[converted_name]
        except KeyError:
            value = Skill.ACROBATICS
        return value

class Tool(Enum):
    ALCHEMIST = auto()
    BREWER = auto()
    CALLIGRAPHER = auto()
    CARPENTER = auto()
    CARTOGRAPHER = auto()
    COBBLER = auto()
    COOK = auto()
    DISGUISE = auto()
    FORGERY = auto()
    GAMING = auto()
    GLASSBLOWER = auto()
    HERBALISM = auto()
    JEWELER = auto()
    VEHICLES = auto()
    LEATHERWORKER = auto()
    MASON = auto()
    MUSICAL = auto()
    NAVIGATOR = auto()
    PAINTER = auto()
    POISONER = auto()
    POTTER = auto()
    SMITH = auto()
    THIEVES = auto()
    TINKER = auto()
    WEAVER = auto()
    WOODCARVER = auto()

    def skills(self) -> Skill:
        mapping = {
            self.ALCHEMIST: [Skill.ARCANA, Skill.INVESTIGATION],
            self.BREWER: [Skill.HISTORY, Skill.MEDICINE, Skill.PERSUASION],
            self.CALLIGRAPHER: [Skill.ARCANA, Skill.HISTORY],
            self.CARPENTER: [Skill.HISTORY, Skill.INVESTIGATION, Skill.PERCEPTION, Skill.STEALTH],
            self.CARTOGRAPHER: [Skill.ARCANA, Skill.HISTORY, Skill.RELIGION, Skill.NATURE, Skill.SURVIVAL],
            self.COBBLER: [Skill.ARCANA, Skill.HISTORY, Skill.INVESTIGATION],
            self.COOK: [Skill.HISTORY, Skill.MEDICINE, Skill.SURVIVAL],
            self.DISGUISE: [Skill.DECEPTION, Skill.INTIMIDATION, Skill.PERFORMANCE, Skill.PERSUASION],
            self.FORGERY: [Skill.ARCANA, Skill.DECEPTION, Skill.HISTORY, Skill.INVESTIGATION],
            self.GAMING: [Skill.HISTORY, Skill.INSIGHT, Skill.SLEIGHT_OF_HAND],
            self.GLASSBLOWER: [Skill.ARCANA, Skill.HISTORY, Skill.INVESTIGATION],
            self.HERBALISM: [Skill.ARCANA, Skill.INVESTIGATION, Skill.MEDICINE, Skill.NATURE, Skill.SURVIVAL],
            self.JEWELER: [Skill.ARCANA, Skill.INVESTIGATION],
            self.VEHICLES: [Skill.ARCANA, Skill.INVESTIGATION, Skill.PERCEPTION],
            self.LEATHERWORKER: [Skill.ARCANA, Skill.INVESTIGATION],
            self.MASON: [Skill.HISTORY, Skill.INVESTIGATION, Skill.PERCEPTION],
            self.MUSICAL: [Skill.HISTORY, Skill.PERFORMANCE],
            self.NAVIGATOR: [Skill.SURVIVAL],
            self.PAINTER: [Skill.ARCANA, Skill.HISTORY, Skill.RELIGION, Skill.INVESTIGATION, Skill.PERCEPTION],
            self.POISONER: [Skill.HISTORY, Skill.INVESTIGATION, Skill.PERCEPTION, Skill.MEDICINE, Skill.NATURE, Skill.SURVIVAL],
            self.POTTER: [Skill.HISTORY, Skill.INVESTIGATION, Skill.PERCEPTION],
            self.SMITH: [Skill.ARCANA, Skill.HISTORY, Skill.INVESTIGATION],
            self.THIEVES: [Skill.HISTORY, Skill.INVESTIGATION, Skill.PERCEPTION, Skill.SLEIGHT_OF_HAND],
            self.TINKER: [Skill.HISTORY, Skill.INVESTIGATION],
            self.WEAVER: [Skill.ARCANA, Skill.HISTORY, Skill.INVESTIGATION],
            self.WOODCARVER: [Skill.ARCANA, Skill.HISTORY, Skill.NATURE]
        }
        return mapping[self]
    
    @classmethod
    def get_values(cls):
        values = []
        for name, _ in Tool.__members__.items():
            values.append(name.title().replace('_', ' '))
        return values

    @classmethod
    def get_display_name(cls, value):
        try:
            display = Tool(value).name.title().replace('_', ' ')
        except ValueError:
            display = 'Unknown'
        return display
    
    @classmethod
    def convert_display_name(cls, name):
        try:
            converted_name = name.upper().replace(' ', '_')
            value = Tool[converted_name]
        except KeyError:
            value = Tool.ALCHEMIST
        return value

class AbilitySet():
    def __init__(self, strength:int=10, dexterity:int=10, constitution:int=10, intelligence:int=10,
                    wisdom:int=10, charisma:int=10) -> None:
        self.strength = int(strength)
        self.dexterity = int(dexterity)
        self.constitution = int(constitution)
        self.intelligence = int(intelligence)
        self.wisdom = int(wisdom)
        self.charisma = int(charisma)
    
    def __delitem__(self, key):
        pass

    def __getitem__(self, key):
        if not isinstance(key, Ability):
            raise TypeError('Key is not a valid Ability object.')
        mapping = {
            Ability.STRENGTH: self.strength,
            Ability.DEXTERITY: self.dexterity,
            Ability.CONSTITUTION: self.constitution,
            Ability.INTELLIGENCE: self.intelligence,
            Ability.WISDOM: self.wisdom,
            Ability.CHARISMA: self.charisma
        }
        return mapping[key]
    
    def __setitem__(self, key, value):
        if not isinstance(key, Ability):
            raise TypeError('Key is not a valid Ability object.')
        if key == Ability.STRENGTH:
            self.strength = int(value)
        elif key == Ability.DEXTERITY:
            self.dexterity = int(value)
        elif key == Ability.CONSTITUTION:
            self.constitution = int(value)
        elif key == Ability.INTELLIGENCE:
            self.intelligence = int(value)
        elif key == Ability.WISDOM:
            self.wisdom = int(value)
        elif key == Ability.CHARISMA:
            self.charisma = int(value)
        