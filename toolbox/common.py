"""A collection of classes that are commonly used across multiple aspects of Dungeons & Dragons
5th edition.

Classes:
    Ability: Enumeration of the basic abilities.
    Skill: Enumeration of ability based skills.
    Tool: Enumeration of skill based tools.
    AbilitySet: A collection of ability scores used by a player character.
"""
from __future__ import absolute_import
from enum import Enum, auto

class Ability(Enum):
    """Defines annumeration of basic abilities.

    Members:
        STRENGTH
        DEXTERITY
        CONSTITUTION
        INTELLIGENCE
        WISDOM
        CHARISMA
    
    Methods:
        get_values: Return a list of string representations of the members.
        get_display_name: Get a formatted string representation of a member.
        convert_display_name: Convert a string representation of a member into the member object.
    """
    STRENGTH = auto()
    DEXTERITY = auto()
    CONSTITUTION = auto()
    INTELLIGENCE = auto()
    WISDOM = auto()
    CHARISMA = auto()

    @classmethod
    def get_values(cls):
        """Return a list of string representations of the class' members.
        
        Returns:
            A list of string representations of the class' members.
        """
        values = []
        for name, _ in Ability.__members__.items():
            values.append(name.title())
        return values

    @classmethod
    def get_display_name(cls, value):
        """Return a string representation of a member.

        Members are represented by the member name in titlecase.
        
        Args:
            value:
                A member of the class.
        
        Returns:
            A string representing the member.
        """
        try:
            display = Ability(value).name.title()
        except ValueError:
            display = 'Unknown'
        return display
    
    @classmethod
    def convert_display_name(cls, name):
        """Convert a string name into the corresponding class name.

        Strings are converted by transforming the string into uppercase
        and matching the result against all members.
        
        Args:
            name:
                The name to convert.
        
        Returns:
            The matching member.
        """
        try:
            converted_name = name.upper()
            value = Ability[converted_name]
        except KeyError:
            value = Ability.STRENGTH
        return value

class Skill(Enum):
    """Defines an enumeration of skills.
    
    Members:
        ACROBATICS
        ANIMAL_HANDLING
        ARCANA
        ATHLETICS
        DECEPTION
        HISTORY
        INSIGHT
        INTIMIDATION
        INVESTIGATION
        MEDICINE
        NATURE
        PERCEPTION
        PERFORMANCE
        PERSUASION
        RELIGION
        SLEIGHT_OF_HAND
        STEALTH
        SURVIVAL
    
    Methods:
        ability: Return the Ability associated with a skill.
        get_values: Return a list of string representations of the members.
        get_display_name: Get a formatted string representation of a member.
        convert_display_name: Convert a string representation of a member into the member object.
    """
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
        """Retrn the Ability associated with the Skill.

        Returns:
            The associated Ability.
        """
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
        """Return a list of string representations of the class' members.
        
        Returns:
            A list of string representations of the class' members.
        """
        values = []
        for name, _ in Skill.__members__.items():
            values.append(name.title().replace('_', ' '))
        return values

    @classmethod
    def get_display_name(cls, value):
        """Return a string representation of a member.

        Members are represented by the member name in titlecase and with underscores
        replaced by spaces.
        
        Args:
            value:
                A member of the class.
        
        Returns:
            A string representing the member.
        """
        try:
            display = Skill(value).name.title().replace('_', ' ')
        except ValueError:
            display = 'Unknown'
        return display
    
    @classmethod
    def convert_display_name(cls, name):
        """Convert a string name into the corresponding class name.

        Strings are converted by transforming the string into uppercase
        and matching the result against all members.
        
        Args:
            name:
                The name to convert.
        
        Returns:
            The matching member.
        """
        try:
            converted_name = name.upper().replace(' ', '_')
            value = Skill[converted_name]
        except KeyError:
            value = Skill.ACROBATICS
        return value

class Tool(Enum):
    """Defines an enumeration of tool proficiency.
    
    Members:
        ALCHEMIST
        BREWER
        CALLIGRAPHER
        CARPENTER
        CARTOGRAPHER
        COBBLER
        COOK
        DISGUISE
        FORGERY
        GAMING
        GLASSBLOWER
        HERBALISM
        JEWELER
        VEHICLES
        LEATHERWORKER
        MASON
        MUSICAL
        NAVIGATOR
        PAINTER
        POISONER
        POTTER
        SMITH
        THIEVES
        TINKER
        WEAVER
        WOODCARVER
    
    Methods:
        skills: Return a list of Skills associated with the Tool.
        get_values: Return a list of string representations of the members.
        get_display_name: Get a formatted string representation of a member.
        convert_display_name: Convert a string representation of a member into the member object.
    """
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
        """Return a list of Skills associated with a Tool.

        Returns:
            A list containing all Skills associated with the Tool.
        """
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
        """Return a list of string representations of the class' members.
        
        Returns:
            A list of string representations of the class' members.
        """
        values = []
        for _, member in Tool.__members__.items():
            values.append(cls.get_display_name(member))
        return values

    @classmethod
    def get_display_name(cls, value):
        """Return a string representation of a member.
        
        Args:
            value:
                A member of the class.
        
        Returns:
            A string representing the member.
        """
        for key, val in _TOOL_NAME_MAP.items():
            if key == value:
                return val
        return 'Unknown'
    
    @classmethod
    def convert_display_name(cls, name):
        """Convert a string name into the corresponding class name.
        
        Args:
            name:
                The name to convert.
        
        Returns:
            The matching member.
        """
        for key, value in _TOOL_NAME_MAP.items():
            if value == name:
                return key
        return Tool.ALCHEMIST

_TOOL_NAME_MAP = {
    Tool.ALCHEMIST: "Alchemist's Supplies", 
    Tool.BREWER: "Brewer's Supplies",
    Tool.CALLIGRAPHER: "Calligrapher's Supplies",
    Tool.CARPENTER: "Carpenter's Tools",
    Tool.CARTOGRAPHER: "Cartographer's Tools",
    Tool.COBBLER: "Cobbler's Tools",
    Tool.COOK: "Cook's Utensils",
    Tool.DISGUISE: "Disguise Kit",
    Tool.FORGERY: "Forgery Kit",
    Tool.GAMING: "Gaming Sets",
    Tool.GLASSBLOWER: "Glassblower's Tools",
    Tool.HERBALISM: "Herbalism Kit",
    Tool.JEWELER: "Jeweler's Tools",
    Tool.VEHICLES: "Land, Water, and Air Vehicles",
    Tool.LEATHERWORKER: "Leatherworker's Tools",
    Tool.MASON: "Mason's Tools",
    Tool.MUSICAL: "Musical Instruments",
    Tool.NAVIGATOR: "Navigator's Tools",
    Tool.PAINTER: "Painter's Supplies",
    Tool.POISONER: "Poisoner's Kit",
    Tool.POTTER: "Potter's Tools",
    Tool.SMITH: "Smith's Tools",
    Tool.THIEVES: "Thieves' Tools",
    Tool.TINKER: "Tinker's Tools",
    Tool.WEAVER: "Weaver's Tools",
    Tool.WOODCARVER: "Woodcarver's Tools"
}
class AbilitySet():
    """Represents the 6 ability scores used for a player character.

    Can be accessed using index notion with the corresponding Ability value.
    """
    def __init__(self, strength: int = 10, dexterity: int = 10, constitution: int = 10,
                 intelligence: int = 10, wisdom: int = 10, charisma: int = 10) -> None:
        """Initializes the AbilitySet using the provided ability values.

        Args:
            strength (int, optional): The score of Ability.STRENGTH. Defaults to 10.
            dexterity (int, optional): The score of Ability.DEXTERITY. Defaults to 10.
            constitution (int, optional): The score of Ability.CONSTITUTION. Defaults to 10.
            intelligence (int, optional): The score of Ability.INTELLIGENCE. Defaults to 10.
            wisdom (int, optional): The score of Ability.WISDOM. Defaults to 10.
            charisma (int, optional): The score of Ability.CHARISMA. Defaults to 10.
        """
        self.strength = int(strength)
        self.dexterity = int(dexterity)
        self.constitution = int(constitution)
        self.intelligence = int(intelligence)
        self.wisdom = int(wisdom)
        self.charisma = int(charisma)
    
    def __delitem__(self, _):
        """Not implemented
        """
        pass

    def __getitem__(self, key):
        """Gets the specified item

        Args:
            key (Ability): The Ability score to retrieve.

        Raises:
            TypeError: key is not a valid Ability object.

        Returns:
            int: The score of the specified Ability.
        """
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
        """Sets the value of the specified Ability

        Args:
            key (Ability): The Ability score to set.
            value (int): The score to set the Ability to.

        Raises:
            TypeError: key is not a valid Ability object.
        """
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
        