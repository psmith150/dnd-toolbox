"""Implements a GUI that provides an interface to use the toolbox calculation methods.
"""
from __future__ import division, absolute_import
from math import ceil, floor
import sys
from pathlib import Path
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from numpy import size
from toolbox.common import Skill, Tool, Ability, Dice
from toolbox.currency import Currency, CurrencyOptions
from toolbox.combat import WeaponType, DamageType, Weapon, Damage, WeaponAttack
from toolbox.dice import DiceTarget, SpecialRoll, DiceRoll, DiceCollection
from toolbox.magic_items import MagicItem, MagicItemDbInterface, MagicItemDistribution, MagicItemDistributionRow
from toolbox import version

#region GUI Constants
#region Color Constants
BASE_THEME = 'DarkBlue3'
BACKGROUND_COLOR = '#64778D'
BUTTON_FOREGROUND_COLOR = 'white'
BUTTON_BACKGROUND_COLOR = '#416D9F'
TAB_NOT_SELECTED_FOREGROUND_COLOR = 'lightgray'
TAB_NOT_SELECTED_BACKGROUND_COLOR = '#6D8199'
TAB_SELECTED_FOREGROUND_COLOR = 'white'
TAB_SELECTED_BACKGROUND_COLOR = '#64778D'
#endregion

COMBAT_SCREEN_KEY = '-screen-0-'
CURRENCY_SCREEN_KEY = '-screen-1-'
DOWNTIME_SCREEN_KEY = '-screen-2-'
DICE_SCREEN_KEY = '-screen-3-'
MAGIC_ITEM_SCREEN_KEY = '-screen-4-'
WEAPON_TYPE_KEY = '-weapon-type-'
WEAPON_BONUS_KEY = '-weapon-bonus-'
EXIT_BUTTON_KEY = '-exit-'
NAV_COMBO_KEY = '-nav-'
CHARACTER_LEVEL_KEY = '-character-level-'
CHARACTER_ATTACK_STAT_KEY = '-character-attack-stat-'
CHARACTER_DAMAGE_MOD_KEY = '-character-damage-mod-'
TARGET_AC_KEY = '-target-ac-'
WEAPON_PANEL_KEY = '-weapon-panel-'
ADD_WEAPON_DAMAGE_BUTTON_KEY = '-add-weapon-damage-'
REMOVE_WEAPON_DAMAGE_BUTTON_KEY = '-remove-weapon-damage-'
WEAPON_DAMAGE_PANEL_KEY = '-weapon-damage-panel-'
DICE_NUMBER_KEY = '-dice-number-'
DAMAGE_DIE_KEY = '-damage-die-'
DAMAGE_TYPE_KEY = '-damage-type-'
PROFICIENCY_KEY = '-proficient-'
HIT_BONUS_KEY = '-hit-bonus-'
AVG_HIT_DAMAGE_KEY = '-avg-hit-damage-'
AVG_DAMAGE_KEY = '-avg-damage-'
WEAPON_DAMAGE_FRAME_KEY = '-weapon-damage-frame-'
WEAPON_SUMMARY_KEY = '-weapon-damage-summary-'
SPLIT_PLATINUM_INPUT_KEY = '-split-platinum-input-'
SPLIT_GOLD_INPUT_KEY = '-split-gold-input-'
SPLIT_ELECTRUM_INPUT_KEY = '-split-electrum-input-'
SPLIT_SILVER_INPUT_KEY = '-split-silver-input-'
SPLIT_COPPER_INPUT_KEY = '-split-copper-input-'
SPLIT_CONSOLIDATE_CURRENCY_KEY = '-split-consolidate-currency-'
PARTY_SIZE_KEY = '-party-size-'
SPLIT_PLATINUM_USED_KEY = '-split-platinum-used-'
SPLIT_GOLD_USED_KEY = '-split-gold-used-'
SPLIT_ELECTRUM_USED_KEY = '-split-electrum-used-'
SPLIT_SILVER_USED_KEY = '-split-silver-used-'
SPLIT_COPPER_USED_KEY = '-split-copper-used-'
SPLIT_CURRENCIES_USED_PANEL = 'split-currencies-col-'
SPLIT_CURRENCY_RESULTS_KEY = '-split-currency-results-'
MATH_PLATINUM_INPUT_1_KEY = '-math-platinum-input-1-'
MATH_GOLD_INPUT_1_KEY = '-math-gold-input-1-'
MATH_ELECTRUM_INPUT_1_KEY = '-math-electrum-input-1-'
MATH_SILVER_INPUT_1_KEY = '-math-silver-input-1-'
MATH_COPPER_INPUT_1_KEY = '-math-copper-input-1-'
MATH_PLATINUM_INPUT_2_KEY = '-math-platinum-input-2-'
MATH_GOLD_INPUT_2_KEY = '-math-gold-input-2-'
MATH_ELECTRUM_INPUT_2_KEY = '-math-electrum-input-2-'
MATH_SILVER_INPUT_2_KEY = '-math-silver-input-2-'
MATH_COPPER_INPUT_2_KEY = '-math-copper-input-2-'
MATH_CONSOLIDATE_CURRENCY_KEY = '-math-consolidate-currency-'
MATH_PLATINUM_USED_KEY = '-math-platinum-used-'
MATH_GOLD_USED_KEY = '-math-gold-used-'
MATH_ELECTRUM_USED_KEY = '-math-electrum-used-'
MATH_SILVER_USED_KEY = '-math-silver-used-'
MATH_COPPER_USED_KEY = '-math-copper-used-'
MATH_CURRENCIES_USED_PANEL = 'math-currencies-col-'
MATH_CURRENCY_RESULTS_KEY = '-math-currency-results-'
MATH_OPERATION_KEY = '-math-operation-'
DOWNTIME_TABS_KEY = '-downtime-tabs-'
DOWNTIME_LANGUAGE_TAB_KEY = '-downtime-language-tab-'
DOWNTIME_SKILL_TAB_KEY = '-downtime-skill-tab-'
DOWNTIME_TOOL_TAB_KEY = '-downtime-tool-tab-'
DOWNTIME_WEAPON_TAB_KEY = '-downtime-weapon-tab-'
DOWNTIME_ARMOR_TAB_KEY = '-downtime-armor-tab-'
DOWNTIME_STRENGTH_INPUT_KEY = '-downtime-strength-'
DOWNTIME_DEXTERITY_INPUT_KEY = '-downtime-dexterity-'
DOWNTIME_CONSTITUTION_INPUT_KEY = '-downtime-constitution-'
DOWNTIME_INTELLIGENCE_INPUT_KEY = '-downtime-intelligence-'
DOWNTIME_PROFICIENCY_BONUS_INPUT_KEY = '-downtime-prof-bonus-'
DOWNTIME_WISDOM_INPUT_KEY = '-downtime-wisdom-'
DOWNTIME_CHARISMA_INPUT_KEY = '-downtime-charisma-'
DOWNTIME_CATEGORY_INPUT_KEY = '-downtime-category-'
DOWNTIME_SKILL_INPUT_KEY = '-downtime-skill-'
DOWNTIME_TOOL_INPUT_KEY = '-downtime-tool-'
DOWNTIME_TOOL_SKILL_PANEL_KEYS = [f'-downtime-tool-skill-col-{x}' for x in range(0, len(Skill))]
DOWNTIME_TOOL_SKILL_PROFICIENCY_KEYS = [f'-downtime-tool-skill-prof-{x}' for x in range(0, len(Skill))]
DOWNTIME_TOOL_SKILL_BONUS_KEYS = [f'-downtime-tool-skill-bonus-{x}' for x in range(0, len(Skill))]
DOWNTIME_WEAPON_STRENGTH_KEY = '-downtime-weapon-strength-'
DOWNTIME_WEAPON_DEXTERITY_KEY = '-downtime-weapon-dexterity-'
DOWNTIME_ARMOR_LIGHT_KEY = '-downtime-armor-light-'
DOWNTIME_ARMOR_MEDIUM_KEY = '-downtime-armor-medium-'
DOWNTIME_ARMOR_HEAVY_KEY = '-downtime-armor-heavy-'
DOWNTIME_RESULT_KEY = '-downtime-result-'
DICE_PANEL_KEY = '-dice-panel-'
DICE_NUMBER_OF_DICE_KEY = '-dice-number'
DICE_DIE_TYPE_KEY = '-dice-type'
DICE_MODIFIER_KEY = '-dice-modifier'
DICE_SPECIAL_ROLL_KEY = '-dice-special'
DICE_SPECIAL_VALUE_KEY = '-dice-special-value'
DICE_COLLECTION_SPECIAL_ROLL_KEY = '-dice-collection-special-'
DICE_COLLECTION_SPECIAL_VALUE_KEY = '-dice-collection-special-value-'
DICE_ADD_DICE_KEY = '-dice-add-'
DICE_REMOVE_DICE_KEY = '-dice-remove-'
DICE_TARGET_KEY = '-dice-target-'
DICE_TARGET_VALUE1_KEY = '-dice-target-value-1-'
DICE_TARGET_VALUE2_KEY = '-dice-target-value-2-'
DICE_CALCULATION_KEY = '-dice-calculate-'
DICE_PROBABILITY_RESULT_KEY = '-dice-probability-result-'
DICE_PROBABILITY_GRAPH_KEY = '-dice-probability-graph-'
MAGIC_ITEMS_DISTRIBUTION_COMPARISON_TABLE_KEY = '-magic-item-distribution-comparison-'
MAGIC_ITEMS_DISTRIBUTION_ITEM_LIST_KEY = '-magic-item-distribution-item-list-'
MAGIC_ITEMS_DISTRIBUTION_ADD_ITEM_KEY = '-magic-item-distribution-add-item-'
MAGIC_ITEMS_DISTRIBUTION_REMOVE_ITEM_KEY = '-magic-item-distribution-remove-item-'
MAGIC_ITEMS_DISTRIBUTION_MOVE_UP_KEY = '-magic-item-distribution-move-item-up-'
MAGIC_ITEMS_DISTRIBUTION_MOVE_DOWN_KEY = '-magic-item-distribution-move-item-down-'
MAGIC_ITEM_SELECT_LIST_KEY = '-magic-item-select-combo-'
MAGIC_ITEM_SELECT_DESCRIPTION_KEY = '-magic-item-select-description-'
MAGIC_ITEM_SELECT_OK_BUTTON = '-magic-item-select-ok-'
MAGIC_ITEM_SELECT_CANCEL_BUTTON = '-magic-item-select-cancel-'
SCREEN_NAMES = ['Combat', 'Currency', 'Downtime Training', 'Dice Calculator', 'Magic Items']
#endregion

DAMAGE_CALCULATION_EVENTS = [CHARACTER_LEVEL_KEY, CHARACTER_ATTACK_STAT_KEY,
                             CHARACTER_DAMAGE_MOD_KEY, TARGET_AC_KEY, WEAPON_TYPE_KEY,
                             WEAPON_BONUS_KEY, DICE_NUMBER_KEY, DAMAGE_DIE_KEY, DAMAGE_TYPE_KEY,
                             PROFICIENCY_KEY, REMOVE_WEAPON_DAMAGE_BUTTON_KEY,
                             ADD_WEAPON_DAMAGE_BUTTON_KEY]

NUM_DAMAGE_PANELS = 3

BASE_DOWNTIME_DAYS = 250

NUM_DICE_PANELS = 3

DICE_CALCULATION_EVENTS = [DICE_NUMBER_OF_DICE_KEY, DICE_DIE_TYPE_KEY, DICE_MODIFIER_KEY,
                            DICE_SPECIAL_ROLL_KEY, DICE_SPECIAL_VALUE_KEY, DICE_COLLECTION_SPECIAL_ROLL_KEY,
                            DICE_COLLECTION_SPECIAL_VALUE_KEY, DICE_ADD_DICE_KEY, DICE_REMOVE_DICE_KEY,
                            DICE_TARGET_KEY, DICE_TARGET_VALUE1_KEY, DICE_TARGET_VALUE2_KEY]
dice_canvas = None

magic_items_target_distribution = MagicItemDistribution()

def main():
    """The main calling program that displays the GUI and handles events.

    The primary purpose of this program is the repeated loop that listens for events and calls
    the appropriate function.
    """
    set_theme()
    window = main_window()
    active_layout = 0
    first_read = False

    while True:
        if not first_read:
            event, values = window.read(timeout=10)
        else:
            event, values = window.read()
        print(event, values)
        if not first_read:
            first_read = True
            init_combat_panel(window, values)
            init_currency_panel(window, values)
            init_downtime_panel(window, values)
            init_dice_panel(window, values)
            init_magic_items_panel(window, values)
        if event == sg.WINDOW_CLOSED or event == EXIT_BUTTON_KEY:
            break

        if event == NAV_COMBO_KEY:
            try:
                new_layout = SCREEN_NAMES.index(values[NAV_COMBO_KEY])
                active_layout = change_screen(window, active_layout, new_layout)
            except ValueError:
                window[NAV_COMBO_KEY].update(value=SCREEN_NAMES[active_layout])

        #region Combat screen events
        if ADD_WEAPON_DAMAGE_BUTTON_KEY in event:
            add_index = int(event.replace(ADD_WEAPON_DAMAGE_BUTTON_KEY, '')[1:])
            add_weapon_damage(window, add_index)

        if REMOVE_WEAPON_DAMAGE_BUTTON_KEY in event:
            remove_index = int(event.replace(REMOVE_WEAPON_DAMAGE_BUTTON_KEY, '')[1:])
            remove_weapon_damage(window, remove_index)

        if any(key in event for key in DAMAGE_CALCULATION_EVENTS):
            global_events = [CHARACTER_LEVEL_KEY, CHARACTER_ATTACK_STAT_KEY,
                             CHARACTER_DAMAGE_MOD_KEY, TARGET_AC_KEY]
            if event in global_events:
                for update_index in range(1, 3):
                    update_weapon_attack(window, values, update_index)
            else:
                damage_panel_events = [DICE_NUMBER_KEY, DAMAGE_TYPE_KEY, DAMAGE_TYPE_KEY]
                splits = event.split('-')
                if any(key in event for key in damage_panel_events):
                    update_index = int(splits[len(splits)-2])
                else:
                    update_index = int(splits[len(splits)-1])
                update_weapon_attack(window, values, update_index)
        #endregion

        #region Currency screen events
        if event in [SPLIT_PLATINUM_INPUT_KEY, SPLIT_GOLD_INPUT_KEY, SPLIT_ELECTRUM_INPUT_KEY,
                     SPLIT_SILVER_INPUT_KEY, SPLIT_COPPER_INPUT_KEY]:
            # Input validation
            if not values[event]:
                continue
            if values[event][-1] not in '0123456789':
                window[event].update(values[event][:-1])
                continue
            if int(values[event]) >= int(1e9):
                window[event].update(str(int(1e9)-1))
            if int(values[event]) < 0:
                window[event].update(str(0))
            split_currency(window, values)

        if event in [SPLIT_PLATINUM_USED_KEY, SPLIT_GOLD_USED_KEY, SPLIT_ELECTRUM_USED_KEY,
                     SPLIT_SILVER_USED_KEY, SPLIT_COPPER_USED_KEY, SPLIT_CONSOLIDATE_CURRENCY_KEY]:
            split_currency(window, values)
            if event == SPLIT_CONSOLIDATE_CURRENCY_KEY:
                window[SPLIT_CURRENCIES_USED_PANEL].update(visible=values[event])

        if event == PARTY_SIZE_KEY:
            if not values[event]:
                continue
            if values[event][-1] not in '0123456789':
                window[event].update(values[event][:-1])
                continue
            if int(values[event]) > 20:
                window[event].update(str(20))
            if int(values[event]) < 1:
                window[event].update(str(1))
            split_currency(window, values)

        if event in [MATH_PLATINUM_INPUT_1_KEY, MATH_GOLD_INPUT_1_KEY, MATH_ELECTRUM_INPUT_1_KEY,
                     MATH_SILVER_INPUT_1_KEY, MATH_COPPER_INPUT_1_KEY, MATH_PLATINUM_INPUT_2_KEY,
                     MATH_GOLD_INPUT_2_KEY, MATH_ELECTRUM_INPUT_2_KEY, MATH_SILVER_INPUT_2_KEY, 
                     MATH_COPPER_INPUT_2_KEY]:
            # Input validation
            if not values[event]:
                continue
            if values[event][-1] not in '0123456789':
                window[event].update(values[event][:-1])
                continue
            if int(values[event]) >= int(1e9):
                window[event].update(str(int(1e9)-1))
            if int(values[event]) < 0:
                window[event].update(str(0))
            calculate_currency(window, values)

        if event in [MATH_PLATINUM_USED_KEY, MATH_GOLD_USED_KEY, MATH_ELECTRUM_USED_KEY,
                     MATH_SILVER_USED_KEY, MATH_COPPER_USED_KEY, MATH_CONSOLIDATE_CURRENCY_KEY,
                     MATH_OPERATION_KEY]:
            calculate_currency(window, values)
            if event == MATH_CONSOLIDATE_CURRENCY_KEY:
                window[MATH_CURRENCIES_USED_PANEL].update(visible=values[event])
        #endregion

        #region Downtime screen events
        if event == DOWNTIME_TABS_KEY:
            init_active_downtime_panel(window, values)

        if event in [DOWNTIME_STRENGTH_INPUT_KEY, DOWNTIME_DEXTERITY_INPUT_KEY,
                     DOWNTIME_CONSTITUTION_INPUT_KEY, DOWNTIME_INTELLIGENCE_INPUT_KEY,
                     DOWNTIME_WISDOM_INPUT_KEY, DOWNTIME_CHARISMA_INPUT_KEY]:
            # Input validation
            if not values[event]:
                continue
            if values[event][-1] not in '0123456789':
                window[event].update(values[event][:-1])
                continue
            if int(values[event]) > 30:
                window[event].update(str(int(30)))
            if int(values[event]) < 1:
                window[event].update(str(1))
            init_active_downtime_panel(window, values)

        if event == DOWNTIME_PROFICIENCY_BONUS_INPUT_KEY:
            # Input validation
            if not values[event]:
                continue
            if values[event][-1] not in '0123456789':
                window[event].update(values[event][:-1])
                continue
            if int(values[event]) > 6:
                window[event].update(str(6))
            if int(values[event]) < 2:
                window[event].update(str(2))
            calculate_tool_training(window, values)

        if event == DOWNTIME_SKILL_INPUT_KEY:
            calculate_skill_training(window, values)

        if event == DOWNTIME_TOOL_INPUT_KEY:
            show_tool_skills(window, values)
            calculate_tool_training(window, values)

        if event in DOWNTIME_TOOL_SKILL_PROFICIENCY_KEYS:
            calculate_tool_training(window, values)

        if event in DOWNTIME_TOOL_SKILL_BONUS_KEYS:
            # Input validation
            if not values[event]:
                continue
            if values[event][-1] not in '0123456789':
                window[event].update(values[event][:-1])
                continue
            if int(values[event]) > 20:
                window[event].update(str(20))
            if int(values[event]) < 0:
                window[event].update(0)
            calculate_tool_training(window, values)

        if event in [DOWNTIME_WEAPON_STRENGTH_KEY, DOWNTIME_WEAPON_DEXTERITY_KEY]:
            calculate_weapon_training(window, values)

        if event in [DOWNTIME_ARMOR_LIGHT_KEY, DOWNTIME_ARMOR_MEDIUM_KEY,
                     DOWNTIME_ARMOR_HEAVY_KEY]:
            calculate_armor_training(window, values)
        #endregion

        #region Dice screen events
        if event == DICE_ADD_DICE_KEY:
            add_dice_roll(window)

        if event == DICE_REMOVE_DICE_KEY:
            remove_dice_roll(window)
        
        if DICE_NUMBER_OF_DICE_KEY in event:
            # Input validation
            if not values[event]:
                continue
            if values[event][-1] not in '0123456789':
                window[event].update(values[event][:-1])
                continue
            if int(values[event]) >= 100:
                window[event].update(str(99))
            if int(values[event]) <= 0:
                window[event].update(str(1))

        if DICE_MODIFIER_KEY in event:
            # Input validation
            if not values[event]:
                continue
            if values[event][-1] not in '0123456789':
                window[event].update(values[event][:-1])
                continue
            if int(values[event]) >= 100:
                window[event].update(str(99))
            if int(values[event]) <= -100:
                window[event].update(str(-99))
        
        if DICE_SPECIAL_VALUE_KEY in event:
            # Input validation
            if not values[event]:
                continue
            if values[event][-1] not in '0123456789':
                window[event].update(values[event][:-1])
                continue
            num_dice = int(values[event.replace(DICE_SPECIAL_VALUE_KEY, DICE_NUMBER_OF_DICE_KEY)])
            if int(values[event]) >= num_dice:
                window[event].update(str(num_dice-1))
            if int(values[event]) < 0:
                window[event].update(str(0))
        
        if event in [DICE_TARGET_VALUE1_KEY, DICE_TARGET_VALUE2_KEY]:
            # Input validation
            if not values[event]:
                continue
            if values[event][-1] not in '0123456789':
                window[event].update(values[event][:-1])
                continue

        if any(key in event for key in DICE_CALCULATION_EVENTS):
            global_events = [DICE_COLLECTION_SPECIAL_ROLL_KEY, DICE_COLLECTION_SPECIAL_VALUE_KEY,
                             DICE_TARGET_KEY, DICE_TARGET_VALUE1_KEY, DICE_TARGET_VALUE2_KEY,
                             DICE_CALCULATION_KEY, DICE_ADD_DICE_KEY, DICE_REMOVE_DICE_KEY]
            if event in global_events:
                update_dice_collection(window, values)
            else:
                splits = event.split('-')
                update_index = int(splits[-2])
                update_dice_roll(window, values, update_index)
        
        if event == DICE_CALCULATION_KEY:
            update_dice_results(window, values)
        #endregion

        #region Magic Item screen events
        if event == MAGIC_ITEMS_DISTRIBUTION_ADD_ITEM_KEY:
            add_magic_item(window, values)

    window.close()


def main_window() -> sg.Window:
    """Create the main window used by the GUI.

    The Window consists of a navigation dropdown, the subscreen actively displayed, a button to
    close the application, and a bottom status bar.

    Returns:
        sg.Window: The created Window object.
    """
    bottom_bar_color = '#3F4B59'
    bottom_bar_layout = [
        [
            sg.Text(version.__version__, background_color=bottom_bar_color)
        ]
    ]
    bottom_bar = sg.Column(bottom_bar_layout, background_color=bottom_bar_color,
                           element_justification='left', vertical_alignment='bottom', pad=((0, 0), (5, 0)),
                           expand_x=True, expand_y=True)
    layout = [
        [sg.Combo(SCREEN_NAMES, key=NAV_COMBO_KEY, enable_events=True, default_value='Combat',
                  size=(20, 1), pad=(0, 8))],
        [combat_panel(True), currency_panel(False), downtime_panel(False), dice_panel(False), magic_items_panel(False)],
        [sg.Exit(key=EXIT_BUTTON_KEY, size=(12, 1))],
        [bottom_bar]
    ]
    base_path = getattr(sys, '_MEIPASS', str(Path(__file__).parent))+'/'
    icon_path = Path(base_path).absolute() / 'images' / 'icon.ico'
    return sg.Window("D&D Toolbox", layout=layout, element_justification='center', margins=(0, 0),
                     icon=icon_path)

def set_theme():
    """Set the active theme of the GUI.
    """
    sg.theme(BASE_THEME)
    sg.theme_background_color(BACKGROUND_COLOR)
    sg.theme_button_color((BUTTON_FOREGROUND_COLOR, BUTTON_BACKGROUND_COLOR))
    sg.theme_border_width()
    sg.theme_element_background_color()
    sg.theme_element_text_color()
    sg.theme_input_background_color()
    sg.theme_input_text_color()
    sg.theme_progress_bar_border_width()
    sg.theme_progress_bar_color()
    sg.theme_slider_border_width()
    sg.theme_slider_color()
    sg.theme_text_color()
    sg.theme_text_element_background_color()

#region GUI Elements
#region Combat Screen
def combat_panel(visible: bool = False) -> sg.Column:
    """Create the combat screen shown in the GUI.

    The screen consists of a section for defining character attributes, 2 sections for defining
    the weapons to be compared, and a section for the result of the comparison.

    Args:
        visible (bool, optional): If True, the screen will start as visible. Defaults to False.

    Returns:
        sg.Column: The created Column object.
    """
    layout = [
        [combat_character_panel()],
        [combat_weapon_panel(1), combat_weapon_panel(2)],
        [sg.HorizontalSeparator()],
        [sg.Frame('Results', layout=[
            [combat_weapon_result_panel(1), sg.VerticalSeparator(), combat_weapon_result_panel(2)],
            [sg.Text('Weapon 2 deals equal damage to Weapon 1', key=WEAPON_SUMMARY_KEY,
                     size=(40, 1), justification='center')]])]
    ]

    return sg.Column(layout, key=COMBAT_SCREEN_KEY, visible=visible)

def combat_character_panel() -> sg.Column:
    """Create the character definition section of the combat screen.

    The character definition section consists of inputs for the character's level, attack stat,
    a flat damage modifier, and the AC of the target to attack.

    Returns:
        sg.Column: The created Column object.
    """
    layout = [
        [sg.Text('Character Level:', size=(30, 1), justification='right'),
         sg.Spin(list(range(1, 20)), key=CHARACTER_LEVEL_KEY,
                 enable_events=True, size=(5, 1), auto_size_text=False),
         sg.Text('', size=(22, 1))],
        [sg.Text('Attack Stat:', size=(30, 1), justification='right'),
         sg.Spin(list(range(1, 30)), initial_value=10,
                 key=CHARACTER_ATTACK_STAT_KEY, enable_events=True, size=(5, 1),
                 auto_size_text=False),
         sg.Text('', size=(22, 1))],
        [sg.Text('Additional Damage Modifier:', size=(30, 1), justification='right'),
         sg.Spin(list(range(0, 100)), key=CHARACTER_DAMAGE_MOD_KEY,
                 enable_events=True, size=(5, 1), auto_size_text=False),
         sg.Text('', size=(22, 1))],
        [sg.Text('Target AC:', size=(30, 1), justification='right'),
         sg.Spin(list(range(1, 30)), initial_value=16, key=TARGET_AC_KEY,
                 enable_events=True, size=(5, 1), auto_size_text=False),
         sg.Text('', size=(22, 1))],
    ]

    return sg.Column(layout, expand_x=True, element_justification='center')

def combat_weapon_panel(index: int) -> sg.Column:
    """Create a section for defining a weapon in the combat screen.

    The weapon definition area consists of inputs for the weapon type, the weapon's bonus,
    a selection for if the character is proficient, and a configurable number of sections for
    defining bonus damage.

    Args:
        index (int): The index of the panel. Must be unique.

    Returns:
        sg.Column: The created Column object.
    """
    weapon_values = WeaponType.get_values()
    weapon_values.sort()
    layout = [[sg.Frame(f'Weapon {index}', layout=[
        [sg.Text('Weapon type:', size=(15, 1), justification='left'),
         sg.Combo(weapon_values,
                  default_value=WeaponType.get_display_name(WeaponType.BATTLEAXE),
                  key=f'{WEAPON_TYPE_KEY}-{index}', enable_events=True,
                  readonly=True, size=(20, 1))],
        [sg.Text('Bonus:', size=(15, 1), justification='left'),
         sg.Spin([i for i in range(0, 10)], initial_value=0,
                 key=f'{WEAPON_BONUS_KEY}-{index}', enable_events=True,
                 size=(5, 1), auto_size_text=False)],
        [sg.Text('Proficient?', size=(15, 1), justification='left'),
         sg.Checkbox('', key=f'{PROFICIENCY_KEY}-{index}',
                     enable_events=True, default=True)]
        ])],
              [sg.Column(layout=[[sg.Button('Add Damage',
                                            key=f'{ADD_WEAPON_DAMAGE_BUTTON_KEY}-{index}',
                                            size=(12, 1))]]),
               sg.Column(layout=[[sg.Button('Remove Damage',
                                            key=f'{REMOVE_WEAPON_DAMAGE_BUTTON_KEY}-{index}',
                                            visible=False, size=(12, 1))]])],
             ]
    damage_panels = []
    for panel in range(NUM_DAMAGE_PANELS):
        damage_panels.append([combat_weapon_damage_panel(index, panel + 1, False)])
    
    layout += [
        [sg.Frame('Additional Damage', damage_panels, key=f'{WEAPON_DAMAGE_FRAME_KEY}-{index}',
                  visible=False)],
    ]

    return sg.Column(layout, key=WEAPON_PANEL_KEY + f'-{index}', expand_y=True)

def combat_weapon_damage_panel(parent_index: int, index: int, visible: bool = False) -> sg.Column:
    """Create a section used to define bonus damage of a weapon on the combat screen.

    The weapon damage section has inputs for the number of dice, the type of dice, and the damage
    type.

    Args:
        parent_index (int): The index of the parent weapon section.
        index (int): The index of the weapon damage panel. Must be unique within the parent.
        visible (bool, optional): If True, start as visible. Defaults to False.

    Returns:
        sg.Column: The created Column object.
    """
    layout = [
        [sg.Text('Number of dice:', size=(15, 1), justification='left'),
         sg.Spin([i for i in range(0, 20)], initial_value=0,
                 key=f'{DICE_NUMBER_KEY}-{parent_index}-{index}',
                 enable_events=True, size=(5, 1), auto_size_text=False)],
        [sg.Text('Damage die:', size=(15, 1), justification='left'),
         sg.Combo(Dice.get_values(), default_value=Dice.get_display_name(Dice.D6),
                  key=f'{DAMAGE_DIE_KEY}-{parent_index}-{index}', enable_events=True,
                  readonly=True, size=(5, 1))],
        [sg.Text('Damage type:', size=(15, 1), justification='left'),
         sg.Combo(DamageType.get_values(),
                  default_value=DamageType.get_display_name(DamageType.ACID),
                  key=f'{DAMAGE_TYPE_KEY}-{parent_index}-{index}',
                  enable_events=True, readonly=True, size=(12, 1))]
    ]

    return sg.Column(layout, key=WEAPON_DAMAGE_PANEL_KEY + f"-{parent_index}-{index}",
                     visible=visible, size=(291, 78))

def combat_weapon_result_panel(parent_index: int) -> sg.Column:
    """Create a section used to display the results of the weapon comparison.

    The result section contains outputs for the weapon's hit bonus, the average damage on
    a hit, and the average damage against a target AC.

    Args:
        parent_index (int): The index of the corresponding weapon panel. Must be unique.

    Returns:
        sg.Column: The created Column object.
    """
    layout = [
        [sg.Text('Hit Bonus:', size=(20, 1)),
         sg.Text('0', key=f'{HIT_BONUS_KEY}-{parent_index}', size=(10, 1))],
        [sg.Text('Average Damage on Hit:', size=(20, 1)),
         sg.Text('0', key=f'{AVG_HIT_DAMAGE_KEY}-{parent_index}', size=(10, 1))],
        [sg.Text('Average Damage to Target:', size=(20, 1)),
         sg.Text('0', key=f'{AVG_DAMAGE_KEY}-{parent_index}', size=(10, 1))]
    ]

    return sg.Column(layout, size=(291, 78), pad=((5, 18), (5, 5)))
#endregion

#region Currency Screen
def currency_panel(visible: bool = False) -> sg.Column:
    """Create the currency screen shown in the GUI.

    The currency screen consists of a group of tabs, which includes a tab for splitting
    currency between multiple party members, and a tab for adding/subtracting currencies.

    Args:
        visible (bool, optional): If True, starts as visible. Defaults to False.

    Returns:
        sg.Column: The created Column object.
    """
    tabs = [[currency_split_panel(), currency_math_panel()]]
    layout = [[sg.TabGroup(layout=tabs, tab_location='top', border_width=0,
                           tab_background_color=TAB_NOT_SELECTED_BACKGROUND_COLOR,
                           title_color=TAB_NOT_SELECTED_FOREGROUND_COLOR,
                           selected_background_color=TAB_SELECTED_BACKGROUND_COLOR,
                           selected_title_color=TAB_SELECTED_FOREGROUND_COLOR)]]
    return sg.Column(layout, key=CURRENCY_SCREEN_KEY, visible=visible,
                     element_justification='center')

def currency_split_panel() -> sg.Tab:
    """Create the tab on the currency screen for splitting currency.

    The currency split tab consists of inputs for the number of platinum, gold, electrum, silver,
    and copper coins, the number of people to split, an option to consolidate the result, options
    for which coins to consolidate to, and an output for the result.

    Returns:
        sg.Tab: The created Tab object.
    """
    layout = [
        [
            sg.Text('Platinum'),
            sg.Input(key=SPLIT_PLATINUM_INPUT_KEY, default_text=0, enable_events=True,
                     size=(10, 1)),
            sg.Text('Gold'),
            sg.Input(key=SPLIT_GOLD_INPUT_KEY, default_text=0, enable_events=True, size=(10, 1)),
            sg.Text('Electrum'),
            sg.Input(key=SPLIT_ELECTRUM_INPUT_KEY, default_text=0, enable_events=True,
                     size=(10, 1)),
            sg.Text('Silver'),
            sg.Input(key=SPLIT_SILVER_INPUT_KEY, default_text=0, enable_events=True, size=(10, 1)),
            sg.Text('Copper'),
            sg.Input(key=SPLIT_COPPER_INPUT_KEY, default_text=0, enable_events=True, size=(10, 1)),
        ],
        [
            sg.Text('Party size:'),
            sg.Input(default_text='1', size=(5, 1), key=PARTY_SIZE_KEY, enable_events=True)
        ],
        [
            sg.Text('Consolidate currency?'),
            sg.Checkbox('', default=True, key=SPLIT_CONSOLIDATE_CURRENCY_KEY, enable_events=True)
        ],
        [
            sg.pin(sg.Column(layout=[
                [
                    sg.Text('Platinum'),
                    sg.Checkbox('', default=False, key=SPLIT_PLATINUM_USED_KEY,
                                enable_events=True),
                    sg.Text('Gold'),
                    sg.Checkbox('', default=True, key=SPLIT_GOLD_USED_KEY, enable_events=True),
                    sg.Text('Electrum'),
                    sg.Checkbox('', default=False, key=SPLIT_ELECTRUM_USED_KEY,
                                enable_events=True),
                    sg.Text('Silver'),
                    sg.Checkbox('', default=True, key=SPLIT_SILVER_USED_KEY, enable_events=True),
                    sg.Text('Copper'),
                    sg.Checkbox('', default=True, key=SPLIT_COPPER_USED_KEY, enable_events=True,
                                disabled=True)
                ],
            ], key=SPLIT_CURRENCIES_USED_PANEL)),
        ],
        [
            sg.HorizontalSeparator()
        ],
        [
            sg.Text('Results', font='any 10 bold'),
        ],
        [
            sg.Text('', key=SPLIT_CURRENCY_RESULTS_KEY, size=(20, 1), justification='center')
        ]
    ]

    return sg.Tab('Split', layout=layout, element_justification='center')

def currency_math_panel() -> sg.Tab:
    """Create the tab on the currency screen for adding/subtracting currency values.

    The currency math panel consists of two sets of inputs for number of platinum, gold, electrum,
    silver, and copper coins, an option to add the coins, an option to consolidate the result,
    options for which coins to consolidate to, and an output for the result of the operation.

    Returns:
        sg.Tab: The created Tab object.
    """
    layout = [
        [
            sg.Text('Platinum'),
            sg.Input(key=MATH_PLATINUM_INPUT_1_KEY, default_text=0, enable_events=True,
                     size=(10, 1)),
            sg.Text('Gold'),
            sg.Input(key=MATH_GOLD_INPUT_1_KEY, default_text=0, enable_events=True,
                     size=(10, 1)),
            sg.Text('Electrum'),
            sg.Input(key=MATH_ELECTRUM_INPUT_1_KEY, default_text=0, enable_events=True,
                     size=(10, 1)),
            sg.Text('Silver'),
            sg.Input(key=MATH_SILVER_INPUT_1_KEY, default_text=0, enable_events=True,
                     size=(10, 1)),
            sg.Text('Copper'),
            sg.Input(key=MATH_COPPER_INPUT_1_KEY, default_text=0, enable_events=True,
                     size=(10, 1)),
        ],
        [
            sg.Text('Platinum'),
            sg.Input(key=MATH_PLATINUM_INPUT_2_KEY, default_text=0, enable_events=True,
                     size=(10, 1)),
            sg.Text('Gold'),
            sg.Input(key=MATH_GOLD_INPUT_2_KEY, default_text=0, enable_events=True, size=(10, 1)),
            sg.Text('Electrum'),
            sg.Input(key=MATH_ELECTRUM_INPUT_2_KEY, default_text=0, enable_events=True,
                     size=(10, 1)),
            sg.Text('Silver'),
            sg.Input(key=MATH_SILVER_INPUT_2_KEY, default_text=0, enable_events=True,
                     size=(10, 1)),
            sg.Text('Copper'),
            sg.Input(key=MATH_COPPER_INPUT_2_KEY, default_text=0, enable_events=True,
                     size=(10, 1)),
        ],
        [
            sg.Text('Add values?'),
            sg.Checkbox('', default=True, key=MATH_OPERATION_KEY, enable_events=True)
        ],
        [
            sg.Text('Consolidate currency?'),
            sg.Checkbox('', default=False, key=MATH_CONSOLIDATE_CURRENCY_KEY, enable_events=True)
        ],
        [
            sg.pin(sg.Column(layout=[
                [
                    sg.Text('Platinum'),
                    sg.Checkbox('', default=False, key=MATH_PLATINUM_USED_KEY, enable_events=True),
                    sg.Text('Gold'),
                    sg.Checkbox('', default=True, key=MATH_GOLD_USED_KEY, enable_events=True),
                    sg.Text('Electrum'),
                    sg.Checkbox('', default=False, key=MATH_ELECTRUM_USED_KEY, enable_events=True),
                    sg.Text('Silver'),
                    sg.Checkbox('', default=True, key=MATH_SILVER_USED_KEY, enable_events=True),
                    sg.Text('Copper'),
                    sg.Checkbox('', default=True, key=MATH_COPPER_USED_KEY, enable_events=True,
                                disabled=True)
                ],
            ], key=MATH_CURRENCIES_USED_PANEL, visible=False)),
        ],
        [
            sg.HorizontalSeparator()
        ],
        [
            sg.Text('Results', font='any 10 bold'),
        ],
        [
            sg.Text('', key=MATH_CURRENCY_RESULTS_KEY, size=(20, 1), justification='center')
        ]
    ]

    return sg.Tab('Math', layout=layout, element_justification='center')

#endregion

#region Downtime Training Screen
def downtime_panel(visible: bool = False) -> sg.Column:
    """Create the downtime training screen shown on the GUI.
    
    The downtime training screen consists of a group of tabs containing the downtime language
    section, the downtime skill section, the downtime tool section, the downtime weapon section,
    the downtime armor section, inputs for the character's strength, dexterity, constitution,
    intelligence, wisdom, and charisma, an input for the character's proficiency bonus, and an
    output for the result of the active tab.
    """
    tabs = [
        [
            downtime_language_panel(),
            downtime_skill_panel(),
            downtime_tool_panel(),
            downtime_weapon_panel(),
            downtime_armor_panel(),
        ]
    ]
    layout = [
        [sg.Text('Ability Scores')],
        [
            sg.Text('Strength'),
            sg.Input(key=DOWNTIME_STRENGTH_INPUT_KEY, default_text=10, enable_events=True,
                     size=(5, 1)),
            sg.Text('Dexterity'),
            sg.Input(key=DOWNTIME_DEXTERITY_INPUT_KEY, default_text=10, enable_events=True,
                     size=(5, 1)),
            sg.Text('Constitution'),
            sg.Input(key=DOWNTIME_CONSTITUTION_INPUT_KEY, default_text=10, enable_events=True,
                     size=(5, 1)),
            sg.Text('Intelligence'),
            sg.Input(key=DOWNTIME_INTELLIGENCE_INPUT_KEY, default_text=10, enable_events=True,
                     size=(5, 1)),
            sg.Text('Wisdom'),
            sg.Input(key=DOWNTIME_WISDOM_INPUT_KEY, default_text=10, enable_events=True,
                     size=(5, 1)),
            sg.Text('Charisma'),
            sg.Input(key=DOWNTIME_CHARISMA_INPUT_KEY, default_text=10, enable_events=True,
                     size=(5, 1)),
        ],
        [
            sg.Text('Proficiency Bonus'),
            sg.Input(key=DOWNTIME_PROFICIENCY_BONUS_INPUT_KEY, default_text=2, enable_events=True,
                     size=(5, 1)),
        ],
        [sg.TabGroup(layout=tabs, tab_location='top', border_width=0, key=DOWNTIME_TABS_KEY,
                     enable_events=True, tab_background_color=TAB_NOT_SELECTED_BACKGROUND_COLOR,
                     title_color=TAB_NOT_SELECTED_FOREGROUND_COLOR,
                     selected_background_color=TAB_SELECTED_BACKGROUND_COLOR,
                     selected_title_color=TAB_SELECTED_FOREGROUND_COLOR)],
        [
            sg.HorizontalSeparator()
        ],
        [
            sg.Text('Results', font='any 10 bold'),
        ],
        [
            sg.Text('', key=DOWNTIME_RESULT_KEY, size=(40, 1), justification='center')
        ]
    ]
    return sg.Column(layout, key=DOWNTIME_SCREEN_KEY, visible=visible,
                     element_justification='center')

def downtime_language_panel() -> sg.Tab:
    """Create the downtime language section of the downtime training screen.

    The downtime language section is empty.

    Returns:
        sg.Tab: The created Tab object.
    """
    layout = [[]]
    return sg.Tab('Languages', layout=layout, element_justification='center',
                  key=DOWNTIME_LANGUAGE_TAB_KEY)

def downtime_skill_panel() -> sg.Tab:
    """Create the downtime skill section of the downtime training screen.

    The downtime skill section consists of an input for selecting a Skill object.

    Returns:
        sg.Tab: The created Tab object.
    """
    layout = [
        [
            sg.Combo(Skill.get_values(), default_value=Skill.get_display_name(Skill.ACROBATICS),
                     key=DOWNTIME_SKILL_INPUT_KEY, enable_events=True, size=(20, 1))
        ]
    ]
    return sg.Tab('Skills', layout=layout, element_justification='center',
                  key=DOWNTIME_SKILL_TAB_KEY)

def downtime_tool_panel() -> sg.Tab:
    """Create the downtime tool section of the downtime training screen.

    The downtime tool section consists of an input for selecting a Tool object, and a skill
    display for the tool's associated skills. The skill displays consist of an input option for if
    the character is proficient in the skill and any additional bonus to the skill. The skill
    displays are selectively shown/hidden based on the active Tool.

    Returns:
        sg.Tab: The created Tab object.
    """
    skill_columns = []
    for index, (_, member) in enumerate(Skill.__members__.items()):
        column_layout = [
            [
                sg.Text(Skill.get_display_name(member), size=(20, 1), justification='right'),
                sg.Text('Proficient?'),
                sg.Checkbox('', default=False, key=DOWNTIME_TOOL_SKILL_PROFICIENCY_KEYS[index],
                            enable_events=True),
                sg.Text('Bonus'),
                sg.Input('0', key=DOWNTIME_TOOL_SKILL_BONUS_KEYS[index], enable_events=True,
                         size=(5, 1))
            ]
        ]
        skill_columns.append([sg.pin(sg.Column(layout=column_layout,
                                               key=DOWNTIME_TOOL_SKILL_PANEL_KEYS[index],
                                               visible=False))])
    layout = [
        [
            sg.Combo(Tool.get_values(), default_value=Tool.get_display_name(Tool.ALCHEMIST),
                     key=DOWNTIME_TOOL_INPUT_KEY, enable_events=True, size=(30, 1))
        ],
        *skill_columns
    ]
    return sg.Tab('Tools', layout=layout, element_justification='center', key=DOWNTIME_TOOL_TAB_KEY)

def downtime_weapon_panel() -> sg.Tab:
    """Create the downtime weapon section of the downtime training screen.

    The downtime weapon section consists of options for selecting which Ability is used by the
    desired weapon.

    Returns:
        sg.Tab: The created Tab object.
    """
    layout = [
        [
            sg.Radio('Strength', 'Downtime-Weapon-Radio', default=True,
                     key=DOWNTIME_WEAPON_STRENGTH_KEY, enable_events=True),
            sg.Radio('Dexterity', 'Downtime-Weapon-Radio', key=DOWNTIME_WEAPON_DEXTERITY_KEY,
                     enable_events=True),
        ]
    ]
    return sg.Tab('Weapons', layout=layout, element_justification='center', key=DOWNTIME_WEAPON_TAB_KEY)

def downtime_armor_panel() -> sg.Tab:
    """Create the downtime armor section of the downtime training screen.

    The downtime armor section sists of options for selecting which type of armor is being trained.

    Returns:
        sg.Tab: The created Tab object.
    """
    layout = [
        [
            sg.Radio('Light', 'Downtime-Armor-Radio', default=True, key=DOWNTIME_ARMOR_LIGHT_KEY,
                     enable_events=True),
            sg.Radio('Medium', 'Downtime-Armor-Radio', key=DOWNTIME_ARMOR_MEDIUM_KEY,
                     enable_events=True),
            sg.Radio('Heavy', 'Downtime-Armor-Radio', key=DOWNTIME_ARMOR_HEAVY_KEY,
                     enable_events=True),
        ]
    ]
    return sg.Tab('Armor', layout=layout, element_justification='center', key=DOWNTIME_ARMOR_TAB_KEY)

#endregion

#region Dice Calculation Screen
def dice_panel(visible: bool = False) -> sg.Column:
    """Create the dice screen shown in the GUI.

    The screen consists of a section for defining individual groups of dice, and a
    section for displaying probability distributions.

    Args:
        visible (bool, optional): If True, the screen will start as visible. Defaults to False.

    Returns:
        sg.Column: The created Column object.
    """
    layout = [
        [dice_collection_panel()],
        [sg.HorizontalSeparator()],
        [sg.Button('Calculate', key=DICE_CALCULATION_KEY, enable_events=True, size=(20,1))],
        [dice_result_panel()]
    ]

    return sg.Column(layout, key=DICE_SCREEN_KEY, visible=visible, element_justification='center')

def dice_collection_panel() -> sg.Column:
    """Create a section for defining a collection of dice rolls in the dice screen.

    The dice collection section consists of a variable number of panels for configuring
    dice rolls, a selection of a special roll modifier, and a value associated with the
    selected special roll modifer.

    Returns:
        sg.Column: The created Column object.
    """
    weapon_values = WeaponType.get_values()
    weapon_values.sort()
    layout = [[]]
    dice_roll_panels = []
    for panel in range(NUM_DICE_PANELS):
        dice_roll_panels.append([dice_roll_panel(panel + 1, panel == 0)])
    
    layout += [
        [sg.Frame('Dice Rolls', dice_roll_panels)],
    ]

    layout += [[sg.Column(layout=[[sg.Button('Add Dice',
                                            key=DICE_ADD_DICE_KEY,
                                            size=(12, 1))]]),
               sg.Column(layout=[[sg.Button('Remove Dice',
                                            key=DICE_REMOVE_DICE_KEY,
                                            visible=False, size=(12, 1))]])]]
    
    layout += [
        [sg.HorizontalSeparator()],
        [sg.Text('Result is'),
         sg.Combo(DiceTarget.get_values(), default_value=DiceTarget.get_display_name(DiceTarget.EQUAL_TO),
                  key=DICE_TARGET_KEY, enable_events=True,
                  readonly=True, size=(12, 1)),
         sg.Input('0', size=(5,1), key=DICE_TARGET_VALUE1_KEY),
         sg.Input('0', size=(5,1), key=DICE_TARGET_VALUE2_KEY, visible=False),]
        ]

    return sg.Column(layout, expand_y=True, element_justification='center')

def dice_roll_panel(index: int, visible: bool = False) -> sg.Column:
    """Create a section for defining a dice roll in the dice screen.

    The weapon definition area consists of inputs for the dice type, the number of dice,
    a static modifier to the roll, a selection of special roll modifiers, and a value
    associated with the chosen special roll.

    Args:
        index (int): The index of the panel. Must be unique.

    Returns:
        sg.Column: The created Column object.
    """
    layout = [
        [sg.Input(default_text=1, key=f'{DICE_NUMBER_OF_DICE_KEY}-{index}-',
                 enable_events=True, size=(5, 1)),
         sg.Text('x'),
         sg.Combo(Dice.get_values(), default_value=Dice.get_display_name(Dice.D20),
                  key=f'{DICE_DIE_TYPE_KEY}-{index}-', enable_events=True,
                  readonly=True, size=(5, 1)),
         sg.Text('+'),
         sg.Input(default_text=0, key=f'{DICE_MODIFIER_KEY}-{index}-',
                  enable_events=True, size=(5, 1))],
        [sg.Text('Special:'),
         sg.Combo(SpecialRoll.get_values(),
                  default_value=SpecialRoll.get_display_name(SpecialRoll.NONE),
                  key=f'{DICE_SPECIAL_ROLL_KEY}-{index}-',
                  enable_events=True, readonly=True, size=(12, 1)),
         sg.Input(default_text=0, key=f'{DICE_SPECIAL_VALUE_KEY}-{index}-', enable_events=True,
                  size=(5,1))]
    ]

    return sg.Column(layout, key=f'{DICE_PANEL_KEY}-{index}-',
                     visible=visible)

def dice_result_panel() -> sg.Column:
    layout =[
        [sg.Text('0.00%', size=(6,1), key=DICE_PROBABILITY_RESULT_KEY, justification='center')],
        [sg.Canvas(key=DICE_PROBABILITY_GRAPH_KEY)]
    ]
    return sg.Column(layout, element_justification='center')
#endregion

#region Magic Items Screen
def magic_items_panel(visible: bool = False) -> sg.Column:
    layout = [
        [magic_item_distribution_comparison_panel()],
        [magic_item_items_panel()]
    ]
    return sg.Column(layout, key=MAGIC_ITEM_SCREEN_KEY, visible=visible, element_justification='center')

def magic_item_distribution_comparison_panel() -> sg.Column:
    row = MagicItemDistributionRow(1, 20)
    num_columns = 1 + len(row.values)
    headings = ['Level/CR'] + [heading.replace('_', ' ').title() for heading in row.values.keys()]
    default_values = [    
        ['Total'] + ['0/0'] * num_columns
    ]
    layout = [
        [sg.Table(default_values, headings=headings, num_rows=2, hide_vertical_scroll=True, key=MAGIC_ITEMS_DISTRIBUTION_COMPARISON_TABLE_KEY)]
    ]
    return sg.Column(layout, expand_x=True, expand_y=True)

def magic_item_items_panel() -> sg.Column:
    button_layout = [
        [sg.Button('Add', key=MAGIC_ITEMS_DISTRIBUTION_ADD_ITEM_KEY, size=(8,1))]
    ]
    layout = [
        [
            sg.Push(),
            sg.Column(layout=[[sg.Listbox([], key=MAGIC_ITEMS_DISTRIBUTION_ITEM_LIST_KEY,
                                            size=(50, 10))]], element_justification='center',
                                            expand_y=True),
            sg.Column(layout=button_layout, element_justification='left',
                        expand_y=True),
            sg.Push()
        ]
    ]
    return sg.Column(layout, expand_x=False, expand_y=True, pad=(0, 5))

def add_magic_item_popup(items: 'list[MagicItem]') -> sg.Window:
    layout = [
        [sg.Listbox(items, key=MAGIC_ITEM_SELECT_LIST_KEY, size=(30, 10), enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, expand_x=True)],
        [sg.Text('', key=MAGIC_ITEM_SELECT_DESCRIPTION_KEY, expand_x=True, justification='center')],
        [sg.Button('Add', key=MAGIC_ITEM_SELECT_OK_BUTTON, size=(10, 1)), sg.Button('Cancel', key=MAGIC_ITEM_SELECT_CANCEL_BUTTON, size=(10,1))]
    ]
    return sg.Window('Add Item', layout, disable_close=True, keep_on_top=True,
                        element_justification='center', size=(600, 250))
#endregion

def change_screen(window: sg.Window, old_layout: int, new_layout: int) -> int:
    """Change the active screen being displayed in the window.

    Args:
        window (sg.Window): The Window that contains the screens
        old_layout (int): The number of the screen to change from.
        new_layout (int): The number of the screen to change to.

    Returns:
        int: The number of the active screen.
    """
    if ((0 <= old_layout < len(SCREEN_NAMES)) and (0 <= new_layout < len(SCREEN_NAMES)) and old_layout != new_layout):
        window[f'-screen-{old_layout}-'].update(visible=False)
        window[f'-screen-{new_layout}-'].update(visible=True)
        return new_layout
    return old_layout

#endregion

#region Combat Screen Functions
def add_weapon_damage(window: sg.Window, parent_index: int):
    """Adds a new weapon damage section to the combat screen

    Args:
        window (sg.Window): The Window containing the combat screen.
        parent_index (int): The index of the weapon section containing the damage section.
    """
    # Find first hidden panel
    window[f'{WEAPON_DAMAGE_FRAME_KEY}-{parent_index}'].update(visible=True)
    window[f'{WEAPON_DAMAGE_FRAME_KEY}-{parent_index}'].unhide_row()
    next_index = -1
    for index in range(NUM_DAMAGE_PANELS):
        col = window[f'{WEAPON_DAMAGE_PANEL_KEY}-{parent_index}-{index+1}']
        if not col.visible:
            next_index = index
            break
    if next_index < 0:
        window[f'{ADD_WEAPON_DAMAGE_BUTTON_KEY}-{parent_index}'].update(visible=False)
        return
    col = window[f'{WEAPON_DAMAGE_PANEL_KEY}-{parent_index}-{next_index+1}']
    col.unhide_row()
    col.update(visible=True)
    window[f'{DICE_NUMBER_KEY}-{parent_index}-{next_index+1}'].update(value=0)
    window[f'{DAMAGE_DIE_KEY}-{parent_index}-{next_index+1}'].update(value=Dice.get_display_name(Dice.D6))
    window[f'{DAMAGE_TYPE_KEY}-{parent_index}-{next_index+1}'].update(value=DamageType.get_display_name(DamageType.ACID))
    window[f'{REMOVE_WEAPON_DAMAGE_BUTTON_KEY}-{parent_index}'].update(visible=True)
    if next_index == NUM_DAMAGE_PANELS - 1:
        window[f'{ADD_WEAPON_DAMAGE_BUTTON_KEY}-{parent_index}'].update(visible=False)
    window.refresh()

def remove_weapon_damage(window: sg.Window, parent_index: int):
    """Removes a weapon damage section from the combat screen

    Args:
        window (sg.Window): The Window containing the combat screen.
        parent_index (int): The index of the weapon section containing the damage section.
    """
    # Find last visible panel
    next_index = -1
    for index in range(NUM_DAMAGE_PANELS, 0, -1):
        col = window[f'{WEAPON_DAMAGE_PANEL_KEY}-{parent_index}-{index}']
        if col.visible:
            next_index = index
            break
    if next_index < 0:
        window[f'{REMOVE_WEAPON_DAMAGE_BUTTON_KEY}-{parent_index}'].update(visible=False)
        return
    col = window[f'{WEAPON_DAMAGE_PANEL_KEY}-{parent_index}-{next_index}']
    col.hide_row()
    col.update(visible=False)
    window[f'{ADD_WEAPON_DAMAGE_BUTTON_KEY}-{parent_index}'].update(visible=True)
    if next_index == 1:
        window[f'{REMOVE_WEAPON_DAMAGE_BUTTON_KEY}-{parent_index}'].update(visible=False)
        window[f'{WEAPON_DAMAGE_FRAME_KEY}-{parent_index}'].hide_row()
        window[f'{WEAPON_DAMAGE_FRAME_KEY}-{parent_index}'].update(visible=False)
    window.refresh()

def update_weapon_attack(window: sg.Window, values: dict, index: int):
    """Calculate the properties of a WeaponAttack and display them on the combat screen.

    Args:
        window (sg.Window): The Window containing the combat screen.
        values (dict): The values of the last window read.
        index (int): The index of the weapon section to calculate for.
    """
    weapon_type = WeaponType.convert_display_name(values[f'{WEAPON_TYPE_KEY}-{index}'])
    bonus = int(values[f'{WEAPON_BONUS_KEY}-{index}'])
    extra_damage = []
    for damage_index in range(NUM_DAMAGE_PANELS):
        col = window[f'{WEAPON_DAMAGE_PANEL_KEY}-{index}-{damage_index+1}']
        if col.visible:
            num_dice = int(values[f'{DICE_NUMBER_KEY}-{index}-{damage_index+1}'])
            damage_die = Dice.convert_display_name(values[f'{DAMAGE_DIE_KEY}-{index}-{damage_index+1}'])
            damage_type = DamageType.convert_display_name(values[f'{DAMAGE_TYPE_KEY}-{index}-{damage_index+1}'])
            extra_damage.append(Damage(num_dice, damage_die, damage_type))
    weapon = Weapon(weapon_type, bonus, extra_damage)
    level = int(values[CHARACTER_LEVEL_KEY])
    attack_stat = int(values[CHARACTER_ATTACK_STAT_KEY])
    proficient = bool(values[f'{PROFICIENCY_KEY}-{index}'])
    damage_mod = int(values[CHARACTER_DAMAGE_MOD_KEY])
    target_ac = int(values[TARGET_AC_KEY])
    attack = WeaponAttack(weapon, level, attack_stat, proficient, damage_mod)
    hit_bonus = attack.hit_bonus
    avg_hit_damage = attack.average_hit_damage()
    avg_damage = attack.average_damage(target_ac)
    
    window[f'{HIT_BONUS_KEY}-{index}'].update(value=hit_bonus)
    window[f'{AVG_HIT_DAMAGE_KEY}-{index}'].update(value='{:.2f}'.format(avg_hit_damage))
    window[f'{AVG_DAMAGE_KEY}-{index}'].update(value='{:.2f}'.format(avg_damage))
    _, values = window.read(timeout=0)
    update_weapon_summary(window)

def update_weapon_summary(window: sg.Window):
    """Update the result of the weapon comparison on the combat screen.

    Args:
        window (sg.Window): The Window containing the combat screen.
    """
    weapon_damages = []
    for weapon_index in range(1, 3):
        weapon_damages.append(float(window[f'{AVG_DAMAGE_KEY}-{weapon_index}'].get()))
    if abs(weapon_damages[1]) < 0.00001:
        difference = 0.0
    else:
        if weapon_damages[0] >= weapon_damages[1]:
            difference = (weapon_damages[0] - weapon_damages[1]) / weapon_damages[1]
        else:
            difference = (weapon_damages[1] - weapon_damages[0]) / weapon_damages[0]
    if abs(difference) < 0.00001:
        summary = 'Weapon 1 deals the same damage as weapon 2'
    elif weapon_damages[0] >= weapon_damages[1]:
        summary = f'Weapon 1 deals {"{:0.2%}".format(difference)} more damage than weapon 2'
    else:
        summary = f'Weapon 2 deals {"{:0.2%}".format(difference)} more damage than weapon 1'
    window[WEAPON_SUMMARY_KEY].update(value=summary)
    window[WEAPON_SUMMARY_KEY].expand(expand_x=True)

def init_combat_panel(window: sg.Window, values: dict):
    """Initialize the combat screen by evaluating the current data.

    Args:
        window (sg.Window): The Window containing the combat screen.
        values (dict): The values of the last window read.
    """
    for update_index in range(1, 3):
        update_weapon_attack(window, values, update_index)

#endregion

#region Currency Screen Functions
def split_currency(window: sg.Window, values: dict):
    """Split the Currency entered on the currency split tab and display the result.

    Args:
        window (sg.Window): The Window containing the currency split tab.
        values (dict): The values of the last window read.
    """
    currency = Currency(
        int(values[SPLIT_PLATINUM_INPUT_KEY]),
        int(values[SPLIT_GOLD_INPUT_KEY]),
        int(values[SPLIT_ELECTRUM_INPUT_KEY]),
        int(values[SPLIT_SILVER_INPUT_KEY]),
        int(values[SPLIT_COPPER_INPUT_KEY]))
    party_size = int(values[PARTY_SIZE_KEY])
    consolidate = values[SPLIT_CONSOLIDATE_CURRENCY_KEY]
    currencies_used = CurrencyOptions.COPPER
    currencies_used |= CurrencyOptions.SILVER if values[SPLIT_SILVER_USED_KEY] else CurrencyOptions.COPPER
    currencies_used |= CurrencyOptions.ELECTRUM if values[SPLIT_ELECTRUM_USED_KEY] else CurrencyOptions.COPPER
    currencies_used |= CurrencyOptions.GOLD if values[SPLIT_GOLD_USED_KEY] else CurrencyOptions.COPPER
    currencies_used |= CurrencyOptions.PLATINUM if values[SPLIT_PLATINUM_USED_KEY] else CurrencyOptions.COPPER
    results = currency.split(party_size, consolidate, currencies_used)
    if len(results) <= 1:
        output = str(results[0])
        num_rows = 1
    else:
        counts = {}
        for result in results:
            result_str = str(result)
            if result_str in counts:
                counts[result_str] += 1
            else:
                counts[result_str] = 1
        output = ''
        for curr, count in counts.items():
            output += f'{count}x {curr}\n'
        output.strip()
        num_rows = len(counts)
    window[SPLIT_CURRENCY_RESULTS_KEY].update(output)
    window[SPLIT_CURRENCY_RESULTS_KEY].set_size((None, num_rows))

def calculate_currency(window: sg.Window, values: dict):
    """Add or subtract the Currencies entered on the currency math tab and display the result.

    Args:
        window (sg.Window): The Window containing the currency math tab.
        values (dict): The values of the last window read.
    """
    currency1 = Currency(
        int(values[MATH_PLATINUM_INPUT_1_KEY]),
        int(values[MATH_GOLD_INPUT_1_KEY]),
        int(values[MATH_ELECTRUM_INPUT_1_KEY]),
        int(values[MATH_SILVER_INPUT_1_KEY]),
        int(values[MATH_COPPER_INPUT_1_KEY]))
    currency2 = Currency(
        int(values[MATH_PLATINUM_INPUT_2_KEY]),
        int(values[MATH_GOLD_INPUT_2_KEY]),
        int(values[MATH_ELECTRUM_INPUT_2_KEY]),
        int(values[MATH_SILVER_INPUT_2_KEY]),
        int(values[MATH_COPPER_INPUT_2_KEY]))
    addition = values[MATH_OPERATION_KEY]
    consolidate = values[MATH_CONSOLIDATE_CURRENCY_KEY]
    currencies_used = CurrencyOptions.COPPER
    currencies_used |= CurrencyOptions.SILVER if values[MATH_SILVER_USED_KEY] else CurrencyOptions.COPPER
    currencies_used |= CurrencyOptions.ELECTRUM if values[MATH_ELECTRUM_USED_KEY] else CurrencyOptions.COPPER
    currencies_used |= CurrencyOptions.GOLD if values[MATH_GOLD_USED_KEY] else CurrencyOptions.COPPER
    currencies_used |= CurrencyOptions.PLATINUM if values[MATH_PLATINUM_USED_KEY] else CurrencyOptions.COPPER

    if addition:
        result = currency1 + currency2
    else:
        result = currency1 - currency2
    if consolidate:
        result = result.consolidate(currencies_used)
    window[MATH_CURRENCY_RESULTS_KEY].update(str(result))

def init_currency_panel(window: sg.Window, values: dict):
    """Initialize the currency screen by calculating with the current values.

    Args:
        window (sg.Window): The Window containing the currency screen.
        values (dict): The values of the last window read.
    """
    split_currency(window, values)
    calculate_currency(window, values)

#endregion

#region Downtime Training Screen Functions
def calculate_language_training(window: sg.Window, values: dict):
    """Calculate the time required for training a language on the downtime languages tab.

    Args:
        window (sg.Window): The Window containing the downtime languages tab.
        values (dict): The values of the last window read.
    """
    intelligence = int(values[DOWNTIME_INTELLIGENCE_INPUT_KEY])
    wisdom = int(values[DOWNTIME_WISDOM_INPUT_KEY])
    charisma = int(values[DOWNTIME_CHARISMA_INPUT_KEY])
    int_mod = intelligence - 10 if intelligence >= 10 else 0
    wis_mod = wisdom - 10 if wisdom >= 10 else 0
    cha_mod = charisma - 10 if charisma >= 10 else 0
    score = max(int_mod + wis_mod + cha_mod, 1)
    days = ceil(BASE_DOWNTIME_DAYS / score)
    window[DOWNTIME_RESULT_KEY].update(f'{days} days.')
    window[DOWNTIME_RESULT_KEY].set_size((None, 1))

def calculate_skill_training(window: sg.Window, values: dict):
    """Calculate the time required for training a skill on the downtime skill tab.

    Args:
        window (sg.Window): The Window containing the downtime skill tab.
        values (dict): The values of the last window read.
    """
    skill = Skill.convert_display_name(values[DOWNTIME_SKILL_INPUT_KEY])
    ability = skill.ability()
    ability_score = get_ability_score(values, ability)
    ability_score = max(ability_score, 1)
    base_days = ceil(BASE_DOWNTIME_DAYS / ability_score)
    expert_days = ceil(2 * BASE_DOWNTIME_DAYS / ability_score)
    window[DOWNTIME_RESULT_KEY].update(f'Proficient in {base_days} days.\nExpertise in an'
                                       + f' additional {expert_days} days.')
    window[DOWNTIME_RESULT_KEY].set_size((None, 2))

def calculate_tool_training(window: sg.Window, values: dict):
    """Calculate the time required for training a tool on the downtime tool tab.

    Args:
        window (sg.Window): The Window containing the downtime tool tab.
        values (dict): The values of the last window read.
    """
    tool = Tool.convert_display_name(values[DOWNTIME_TOOL_INPUT_KEY])
    total = 0
    related_skills = tool.skills()
    for index, (_, member) in enumerate(Skill.__members__.items()):
        if member in related_skills:
            ability_mod = floor((get_ability_score(values, member.ability()) - 10) / 2)
            proficiency_bonus = int(values[DOWNTIME_PROFICIENCY_BONUS_INPUT_KEY]) if values[DOWNTIME_TOOL_SKILL_PROFICIENCY_KEYS[index]] else 0
            bonus = int(values[DOWNTIME_TOOL_SKILL_BONUS_KEYS[index]])
            total += ability_mod + proficiency_bonus + bonus
    score = total / len(tool.skills()) + 10
    base_days = ceil(BASE_DOWNTIME_DAYS / score)
    expert_days = ceil(2 * BASE_DOWNTIME_DAYS / score)
    window[DOWNTIME_RESULT_KEY].update(f'Proficient in {base_days} days.\nExpertise in an'
                                       + f' additional {expert_days} days.')
    window[DOWNTIME_RESULT_KEY].set_size((None, 2))

def calculate_weapon_training(window: sg.Window, values: dict):
    """Calculate the time required for training a weapon on the downtime weapon tab.

    Args:
        window (sg.Window): The Window containing the downtime weapon tab.
        values (dict): The values of the last window read.
    """
    if bool(values[DOWNTIME_WEAPON_STRENGTH_KEY]):
        ability_score = get_ability_score(values, Ability.STRENGTH)
    elif bool(values[DOWNTIME_WEAPON_DEXTERITY_KEY]):
        ability_score = get_ability_score(values, Ability.DEXTERITY)
    else:
        window[DOWNTIME_RESULT_KEY].update('Invalid selection.')
        return
    ability_score = max(ability_score, 1)
    days = ceil(BASE_DOWNTIME_DAYS / ability_score)
    window[DOWNTIME_RESULT_KEY].update(f'{days} days.')
    window[DOWNTIME_RESULT_KEY].set_size((None, 1))

def calculate_armor_training(window: sg.Window, values: dict):
    """Calculate the time required for training an armor on the downtime armor tab.

    Args:
        window (sg.Window): The Window containing the downtime armor tab.
        values (dict): The values of the last window read.
    """
    if bool(values[DOWNTIME_ARMOR_LIGHT_KEY]):
        ability_score = get_ability_score(values, Ability.DEXTERITY)
    elif bool(values[DOWNTIME_ARMOR_MEDIUM_KEY]):
        ability_score = get_ability_score(values, Ability.STRENGTH)
    elif bool(values[DOWNTIME_ARMOR_HEAVY_KEY]):
        ability_score = get_ability_score(values, Ability.STRENGTH)
    else:
        window[DOWNTIME_RESULT_KEY].update('Invalid selection.')
        return
    ability_score = max(ability_score, 1)
    days = ceil(BASE_DOWNTIME_DAYS / ability_score)
    window[DOWNTIME_RESULT_KEY].update(f'{days} days.')
    window[DOWNTIME_RESULT_KEY].set_size((None, 1))

def init_downtime_panel(window: sg.Window, values: dict):
    """Initialize the downtime screen by calculating with the current values.

    Args:
        window (sg.Window): The Window containing the downtime window.
        values (dict): The values of the last window read.
    """
    calculate_language_training(window, values)

def init_active_downtime_panel(window: sg.Window, values: dict):
    """Initialize the downtime screen by calculating with the current value of the active tab.

    Args:
        window (sg.Window): The Window containing the downtime window.
        values (dict): The values of the last window read.
    """
    downtime_tab = values[DOWNTIME_TABS_KEY]
    if downtime_tab == DOWNTIME_LANGUAGE_TAB_KEY:
        calculate_language_training(window, values)
    elif downtime_tab == DOWNTIME_SKILL_TAB_KEY:
        calculate_skill_training(window, values)
    elif downtime_tab == DOWNTIME_TOOL_TAB_KEY:
        calculate_tool_training(window, values)
    elif downtime_tab == DOWNTIME_WEAPON_TAB_KEY:
        calculate_weapon_training(window, values)
    elif downtime_tab == DOWNTIME_ARMOR_TAB_KEY:
        calculate_armor_training(window, values)
    show_tool_skills(window, values)

def get_ability_score(values: dict, ability: Ability) -> int:
    """Return the ability score on the downtime screen corresponding to an Ability.

    Args:
        values (dict): The Window containing the downtime screen.
        ability (Ability): The Ability to get the score for.

    Returns:
        int: The score of the specified Ability.
    """
    mapping = {
        Ability.STRENGTH: int(values[DOWNTIME_STRENGTH_INPUT_KEY]),
        Ability.DEXTERITY: int(values[DOWNTIME_DEXTERITY_INPUT_KEY]),
        Ability.CONSTITUTION: int(values[DOWNTIME_CONSTITUTION_INPUT_KEY]),
        Ability.INTELLIGENCE: int(values[DOWNTIME_INTELLIGENCE_INPUT_KEY]),
        Ability.WISDOM: int(values[DOWNTIME_WISDOM_INPUT_KEY]),
        Ability.CHARISMA: int(values[DOWNTIME_CHARISMA_INPUT_KEY]),
    }
    return mapping[ability]

def show_tool_skills(window: sg.Window, values: dict):
    """Show/hide the Skills related to the active Tool on the downtime tool tab.

    Args:
        window (sg.Window): The Window containing the downtime tool tab.
        values (dict): The values of the last window read.
    """
    if values[DOWNTIME_TABS_KEY] != DOWNTIME_TOOL_TAB_KEY:
        for index in range(len(Skill)):
            window[DOWNTIME_TOOL_SKILL_PANEL_KEYS[index]].update(visible=False)
        return
    tool = Tool.convert_display_name(values[DOWNTIME_TOOL_INPUT_KEY])
    related_skills = tool.skills()
    for index, (_, member) in enumerate(Skill.__members__.items()):
        if member in related_skills:
            window[DOWNTIME_TOOL_SKILL_PANEL_KEYS[index]].update(visible=True)
        else:
            window[DOWNTIME_TOOL_SKILL_PANEL_KEYS[index]].update(visible=False)


#endregion

#region Dice Calculation Screen Functions
def add_dice_roll(window: sg.Window):
    """Adds a new dice roll section to the combat screen

    Args:
        window (sg.Window): The Window containing the dice screen.
    """
    # Find first hidden panel
    next_index = -1
    for index in range(NUM_DICE_PANELS):
        col = window[f'{DICE_PANEL_KEY}-{index+1}-']
        if not col.visible:
            next_index = index
            break
    if next_index < 0:
        window[DICE_ADD_DICE_KEY].update(visible=False)
        return
    col = window[f'{DICE_PANEL_KEY}-{next_index+1}-']
    col.unhide_row()
    col.update(visible=True)
    window[f'{DICE_NUMBER_OF_DICE_KEY}-{next_index+1}-'].update(value=1)
    window[f'{DICE_DIE_TYPE_KEY}-{next_index+1}-'].update(value=Dice.get_display_name(Dice.D6))
    window[f'{DICE_MODIFIER_KEY}-{next_index+1}-'].update(value=0)
    window[f'{DICE_SPECIAL_ROLL_KEY}-{next_index+1}-'].update(value=SpecialRoll.get_display_name(SpecialRoll.NONE))
    window[f'{DICE_SPECIAL_VALUE_KEY}-{next_index+1}-'].update(value=0)
    window[DICE_REMOVE_DICE_KEY].update(visible=True)
    if next_index == NUM_DAMAGE_PANELS - 1:
        window[DICE_ADD_DICE_KEY].update(visible=False)
    window.refresh()

def remove_dice_roll(window: sg.Window):
    """Removes a dice roll section from the combat screen

    Args:
        window (sg.Window): The Window containing the dice screen.
    """
    # Find last visible panel
    next_index = -1
    for index in range(NUM_DICE_PANELS, 0, -1):
        col = window[f'{DICE_PANEL_KEY}-{index}-']
        if col.visible:
            next_index = index
            break
    if next_index <= 1:
        window[DICE_REMOVE_DICE_KEY].update(visible=False)
        return
    col = window[f'{DICE_PANEL_KEY}-{next_index}-']
    col.hide_row()
    col.update(visible=False)
    window[DICE_ADD_DICE_KEY].update(visible=True)
    if next_index == 2:
        window[DICE_REMOVE_DICE_KEY].update(visible=False)
    window.refresh()

def update_dice_roll(window: sg.Window, values: dict, index: int):
    """Calculate the properties of a DiceRoll and display them on the dice screen.

    Args:
        window (sg.Window): The Window containing the combat screen.
        values (dict): The values of the last window read.
        index (int): The index of the weapon section to calculate for.
    """
    special_roll = SpecialRoll.convert_display_name(values[f'{DICE_SPECIAL_ROLL_KEY}-{index}-'])
    if special_roll == SpecialRoll.NONE:
        if window[f'{DICE_SPECIAL_VALUE_KEY}-{index}-'].visible:
            window[f'{DICE_SPECIAL_VALUE_KEY}-{index}-'].update(visible=False)
    else:
        if not window[f'{DICE_SPECIAL_VALUE_KEY}-{index}-'].visible:
            window[f'{DICE_SPECIAL_VALUE_KEY}-{index}-'].update(visible=True, value=0)
    _, values = window.read(timeout=0)

def update_dice_collection(window: sg.Window, values: dict):
    target_type = DiceTarget.convert_display_name(values[DICE_TARGET_KEY])
    if target_type == DiceTarget.BETWEEN:
        if not window[DICE_TARGET_VALUE2_KEY].visible:
            window[DICE_TARGET_VALUE2_KEY].update(visible=True, value = values[DICE_TARGET_VALUE1_KEY])
    else:
        if window[DICE_TARGET_VALUE2_KEY].visible:
            window[DICE_TARGET_VALUE2_KEY].update(visible=False)
    
    _, values = window.read(timeout=0)

def update_dice_results(window: sg.Window, values: dict):
    dice_rolls = []
    for dice_index in range(NUM_DICE_PANELS):
        col = window[f'{DICE_PANEL_KEY}-{dice_index+1}-']
        if col.visible:
            num_dice = int(values[f'{DICE_NUMBER_OF_DICE_KEY}-{dice_index+1}-'])
            die_type = Dice.convert_display_name(values[f'{DICE_DIE_TYPE_KEY}-{dice_index+1}-'])
            modifier = int(values[f'{DICE_MODIFIER_KEY}-{dice_index+1}-'])
            special_roll = SpecialRoll.convert_display_name(values[f'{DICE_SPECIAL_ROLL_KEY}-{dice_index+1}-'])
            special_value = int(values[f'{DICE_SPECIAL_VALUE_KEY}-{dice_index+1}-'])
            dice_rolls.append(DiceRoll(die_type, num_dice, modifier, special_roll, special_value))
    collection = DiceCollection(dice_rolls)
    
    probability = 0.0
    target_type = DiceTarget.convert_display_name(values[DICE_TARGET_KEY])
    if (target_type == DiceTarget.EQUAL_TO):
        probability = collection.get_probability_target(int(values[DICE_TARGET_VALUE1_KEY]))
    elif (target_type == DiceTarget.LESS_THAN):
        probability = collection.get_probability_range(collection.min_value(), int(values[DICE_TARGET_VALUE1_KEY])-1)
    elif (target_type == DiceTarget.GREATER_THAN):
        probability = collection.get_probability_range(int(values[DICE_TARGET_VALUE1_KEY])+1, collection.max_value())
    elif target_type == DiceTarget.BETWEEN:
        probability = collection.get_probability_range(int(values[DICE_TARGET_VALUE1_KEY]), int(values[DICE_TARGET_VALUE2_KEY]))
    elif target_type == DiceTarget.NOT_EQUAL_TO:
        probability = 1.0 - collection.get_probability_target(int(values[DICE_TARGET_VALUE1_KEY]))
    else:
        raise NotImplementedError()
    
    window[DICE_PROBABILITY_RESULT_KEY].update(value="{:0.2%}".format(probability))
    graph_dice_probability(window, collection)


def graph_dice_probability(window: sg.Window, dice: DiceCollection):
    global dice_canvas
    try:
        dice_canvas.get_tk_widget().pack_forget()
    except AttributeError:
        pass
    except UnboundLocalError:
        pass
    fig = Figure(figsize=(5,4), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_xlabel('Total Roll')
    ax.set_ylabel('Probability')
    probabilities = dice.get_all_probabilities()
    ax.bar(probabilities.keys(), probabilities.values())
    canvas = window[DICE_PROBABILITY_GRAPH_KEY].TKCanvas
    canvas.delete('all')
    dice_canvas = FigureCanvasTkAgg(fig, canvas)
    dice_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    dice_canvas.draw()

def init_dice_panel(window: sg.Window, values: dict):
    """Initialize the dice screen by evaluating the current data.

    Args:
        window (sg.Window): The Window containing the dice screen.
        values (dict): The values of the last window read.
    """
    for update_index in range(1, NUM_DICE_PANELS+1):
        update_dice_roll(window, values, update_index)
#endregion

#region Magic Items Screen Functions
def update_magic_items_comparison(window: sg.Window) -> None:
    # TODO: Populate item data
    current_items = window[MAGIC_ITEMS_DISTRIBUTION_ITEM_LIST_KEY].get_list_values()
    magic_items_target_distribution.clear_items()
    magic_items_target_distribution.add_items(current_items)
    actual_distribution = magic_items_target_distribution.process_items()
    table_values = []
    for (row_index, row) in enumerate(actual_distribution.rows):
        row_values = [f'{row.start}-{row.end}']
        for key in row.values.keys():
            row_values.append(f'{row.values[key]}/{magic_items_target_distribution.rows[row_index].values[key]}')
        table_values.append(row_values)
    target_total_row = magic_items_target_distribution.total_row()
    actual_total_row = actual_distribution.total_row()
    table_values.append(['Total'] + [f'{actual_total_row.values[key]}/{target_total_row.values[key]}' for key in target_total_row.values.keys()])
    
    window[MAGIC_ITEMS_DISTRIBUTION_COMPARISON_TABLE_KEY].update(table_values, num_rows = len(table_values))

def add_magic_item(window: sg.Window, values: list) -> None:
    db = MagicItemDbInterface()
    items = db.get_magic_items()
    items.sort(key=lambda x: x.name)
    popup_window = add_magic_item_popup(items)

    while True:
        popup_event, popup_values = popup_window.read()
        print(popup_event, popup_values)
        if popup_event == sg.WINDOW_CLOSED or popup_event == MAGIC_ITEM_SELECT_CANCEL_BUTTON:
            new_item = None
            break
        if popup_event == MAGIC_ITEM_SELECT_LIST_KEY:
            selected_item = popup_values[MAGIC_ITEM_SELECT_LIST_KEY][0]
            description = f'{selected_item.item_type}, {selected_item.rarity}, {selected_item.power_level} magic item'
            if selected_item.attunement:
                description += f' (requires attunement by a {selected_item.attunement_requirement})'
            popup_window[MAGIC_ITEM_SELECT_DESCRIPTION_KEY].update(description)
        if popup_event == MAGIC_ITEM_SELECT_OK_BUTTON:
            new_item = popup_values[MAGIC_ITEM_SELECT_LIST_KEY][0]
            break
    
    popup_window.close()
    if new_item:
        current_items = window[MAGIC_ITEMS_DISTRIBUTION_ITEM_LIST_KEY].get_list_values()
        current_items.append(new_item)
        window[MAGIC_ITEMS_DISTRIBUTION_ITEM_LIST_KEY].update(values=current_items)
        update_magic_items_comparison(window)

def remove_magic_item(window: sg.Window, values: list) -> None:
    pass

def move_magic_item_up(window: sg.Window, values: list) -> None:
    pass

def move_magic_item_down(window: sg.Window, values: list) -> None:
    pass

def init_magic_items_panel(window: sg.Window, values: list) -> None:
    magic_items_target_distribution.add_row(
        MagicItemDistributionRow(1, 4, 6, 2, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0)
    )
    magic_items_target_distribution.add_row(
        MagicItemDistributionRow(5, 10, 10, 12, 5, 1, 0, 0, 0, 5, 1, 0, 0, 0)
    )
    magic_items_target_distribution.add_row(
        MagicItemDistributionRow(11, 16, 3, 6, 9, 5, 1, 0, 0, 1, 2, 2, 1, 0)
    )
    magic_items_target_distribution.add_row(
        MagicItemDistributionRow(17, 20, 0, 0, 4, 9, 6, 0, 0, 0, 1, 2, 3, 0)
    )
    update_magic_items_comparison(window)
#endregion

if __name__ == "__main__":
    main()