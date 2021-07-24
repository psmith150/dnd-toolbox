from enum import auto
from currency import Currency, CurrencyOptions
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Checkbox, HorizontalSeparator, VerticalSeparator
from combat import WeaponType, Dice, DamageType, Weapon, Damage, WeaponAttack

#region GUI Constants
THEME = 'Dark Grey 13'
COMBAT_SCREEN_KEY = '-screen-0-'
CURRENCY_SCREEN_KEY = '-screen-1-'
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
SCREEN_NAMES = ['Combat', 'Currency']
#endregion

DAMAGE_CALCULATION_EVENTS = [CHARACTER_LEVEL_KEY, CHARACTER_ATTACK_STAT_KEY,
    CHARACTER_DAMAGE_MOD_KEY, TARGET_AC_KEY, WEAPON_TYPE_KEY, WEAPON_BONUS_KEY,
    DICE_NUMBER_KEY, DAMAGE_DIE_KEY, DAMAGE_TYPE_KEY, PROFICIENCY_KEY,
    REMOVE_WEAPON_DAMAGE_BUTTON_KEY, ADD_WEAPON_DAMAGE_BUTTON_KEY]

NUM_DAMAGE_PANELS = 3

def main():
    sg.theme(THEME)
    window = main_window()
    active_layout = 0
    first_read = False

    while True:
        if (not first_read):
            event, values = window.read(timeout=10)
        else:
            event, values = window.read()
        #print(event, values)
        if (not first_read):
            first_read = True
            init_combat_panel(window, values)
            init_currency_panel(window, values)
        if event == sg.WINDOW_CLOSED or event == EXIT_BUTTON_KEY:
            break
        if event == NAV_COMBO_KEY:
            try:
                new_layout = SCREEN_NAMES.index(values[NAV_COMBO_KEY])
                active_layout = change_screen(window, active_layout, new_layout)
            except ValueError:
                window[NAV_COMBO_KEY].update(value=SCREEN_NAMES[active_layout])
        if ADD_WEAPON_DAMAGE_BUTTON_KEY in event:
            add_index = int(event.replace(ADD_WEAPON_DAMAGE_BUTTON_KEY,'')[1:])
            add_weapon_damage(window, add_index)
        if REMOVE_WEAPON_DAMAGE_BUTTON_KEY in event:
            remove_index = int(event.replace(REMOVE_WEAPON_DAMAGE_BUTTON_KEY,'')[1:])
            remove_weapon_damage(window, remove_index)
        if any(key in event for key in DAMAGE_CALCULATION_EVENTS):
            global_events = [CHARACTER_LEVEL_KEY, CHARACTER_ATTACK_STAT_KEY,
                                CHARACTER_DAMAGE_MOD_KEY, TARGET_AC_KEY]
            if event in global_events:
                for update_index in range(1,3):
                    update_weapon_attack(window, values, update_index)
            else:
                damage_panel_events = [DICE_NUMBER_KEY, DAMAGE_TYPE_KEY, DAMAGE_TYPE_KEY]
                splits = event.split('-')
                if any(key in event for key in damage_panel_events):
                    update_index = int(splits[len(splits)-2])
                else:
                    update_index = int(splits[len(splits)-1])
                update_weapon_attack(window, values, update_index)
        if event in [SPLIT_PLATINUM_INPUT_KEY, SPLIT_GOLD_INPUT_KEY, SPLIT_ELECTRUM_INPUT_KEY, SPLIT_SILVER_INPUT_KEY, SPLIT_COPPER_INPUT_KEY]:
            # Input validation
            if len(values[event]) == 0:
                continue
            if values[event][-1] not in '0123456789':
                window[event].update(values[event][:-1])
            if int(values[event])>= int(1e9):
                window[event].update(str(int(1e9)-1))
            split_currency(window, values)
        if event in [SPLIT_PLATINUM_USED_KEY, SPLIT_GOLD_USED_KEY, SPLIT_ELECTRUM_USED_KEY, SPLIT_SILVER_USED_KEY, SPLIT_COPPER_USED_KEY, SPLIT_CONSOLIDATE_CURRENCY_KEY]:
            split_currency(window, values)
            if (event == SPLIT_CONSOLIDATE_CURRENCY_KEY):
                window[SPLIT_CURRENCIES_USED_PANEL].update(visible=values[event])
        if event == PARTY_SIZE_KEY:
            if len(values[event]) == 0:
                continue
            if values[event][-1] not in '0123456789':
                window[event].update(values[event][:-1])
            if int(values[event]) > int(20):
                window[event].update(str(int(20)))
            split_currency(window, values)
        if event in [MATH_PLATINUM_INPUT_1_KEY, MATH_GOLD_INPUT_1_KEY, MATH_ELECTRUM_INPUT_1_KEY, MATH_SILVER_INPUT_1_KEY, MATH_COPPER_INPUT_1_KEY,
                        MATH_PLATINUM_INPUT_2_KEY, MATH_GOLD_INPUT_2_KEY, MATH_ELECTRUM_INPUT_2_KEY, MATH_SILVER_INPUT_2_KEY, MATH_COPPER_INPUT_2_KEY]:
            # Input validation
            if len(values[event]) == 0:
                continue
            if values[event][-1] not in '0123456789':
                window[event].update(values[event][:-1])
            if int(values[event])>= int(1e9):
                window[event].update(str(int(1e9)-1))
            add_currency(window, values)
        if event in [MATH_PLATINUM_USED_KEY, MATH_GOLD_USED_KEY, MATH_ELECTRUM_USED_KEY, MATH_SILVER_USED_KEY, MATH_COPPER_USED_KEY, MATH_CONSOLIDATE_CURRENCY_KEY]:
            add_currency(window, values)
            if (event == MATH_CONSOLIDATE_CURRENCY_KEY):
                window[MATH_CURRENCIES_USED_PANEL].update(visible=values[event])
    
    window.close()
    

def main_window() -> sg.Window:
    layout = [
        [sg.Combo(SCREEN_NAMES, key=NAV_COMBO_KEY, enable_events=True, default_value='Combat', size=(20,1))],
        [combat_panel(True), currency_panel(False)],
        [sg.Exit(key=EXIT_BUTTON_KEY)]
    ]

    return sg.Window("D&D Toolbox", layout=layout, element_justification='center')

#region GUI Elements
#region Combat Screen
def combat_panel(visible: bool = False) -> sg.Column:
    layout = [
        [combat_character_panel()],
        [combat_weapon_panel(1), combat_weapon_panel(2)],
        [sg.HorizontalSeparator()],
        [sg.Frame('Results', layout=[
            [combat_weapon_result_panel(1), sg.VerticalSeparator(), combat_weapon_result_panel(2)],
            [sg.Text('Weapon 2 deals equal damage to Weapon 1',key=WEAPON_SUMMARY_KEY, size=(40,1), justification='center')]])]
    ]

    return sg.Column(layout, key=COMBAT_SCREEN_KEY, visible=visible)

def combat_character_panel() -> sg.Column:
    layout = [
        [sg.Text('Character Level:', size=(30, 1), justification='right'),
            sg.Spin([i for i in range(1, 20)], key=CHARACTER_LEVEL_KEY,
                enable_events=True, size=(5,1), auto_size_text=False),
            sg.Text('', size=(22,1))],
        [sg.Text('Attack Stat:', size=(30, 1), justification='right'),
            sg.Spin([i for i in range(1, 30)], initial_value=10,
                key=CHARACTER_ATTACK_STAT_KEY, enable_events=True, size=(5,1),
                auto_size_text=False),
            sg.Text('', size=(22,1))],
        [sg.Text('Additional Damage Modifier:', size=(30, 1), justification='right'),
            sg.Spin([i for i in range(0, 100)], key=CHARACTER_DAMAGE_MOD_KEY,
                enable_events=True, size=(5,1), auto_size_text=False),
                sg.Text('', size=(22,1))],
        [sg.Text('Target AC:', size=(30, 1), justification='right'),
            sg.Spin([i for i in range(1, 30)], initial_value=16, key=TARGET_AC_KEY,
                enable_events=True, size=(5,1), auto_size_text=False),
                sg.Text('', size=(22,1))],
    ]

    return sg.Column(layout, expand_x=True, element_justification='center')

def combat_weapon_panel(index: int) -> sg.Column:
    weapon_values = WeaponType.get_values()
    weapon_values.sort()
    layout = [[sg.Frame(f'Weapon {index}', layout=[
                [sg.Text('Weapon type:', size=(15,1), justification='left'),
                    sg.Combo(weapon_values,
                        default_value=WeaponType.get_display_name(WeaponType.BATTLEAXE),
                        key=f'{WEAPON_TYPE_KEY}-{index}', enable_events=True,
                        readonly=True, size=(20, 1))],
                [sg.Text('Bonus:', size=(15,1), justification='left'),
                    sg.Spin([i for i in range(0, 10)], initial_value=0,
                        key=f'{WEAPON_BONUS_KEY}-{index}', enable_events=True,
                        size=(5,1), auto_size_text=False)],
                [sg.Text('Proficient?', size=(15,1), justification='left'),
                    sg.Checkbox('', key=f'{PROFICIENCY_KEY}-{index}',
                        enable_events=True, default=True)]
                ])],
        [sg.Column(layout=[[sg.Button('Add Damage', key=f'{ADD_WEAPON_DAMAGE_BUTTON_KEY}-{index}',
                size=(12,1))]]),
            sg.Column(layout=[[sg.Button('Remove Damage',
                key=f'{REMOVE_WEAPON_DAMAGE_BUTTON_KEY}-{index}', visible=False, size=(12,1))]])],
    ]
    damage_panels = []
    for panel in range(NUM_DAMAGE_PANELS):
        damage_panels.append([combat_weapon_damage_panel(index, panel + 1, False)])
    
    layout += [
        [sg.Frame('Additional Damage', damage_panels, key=f'{WEAPON_DAMAGE_FRAME_KEY}-{index}', visible=False)],
    ]

    return sg.Column(layout, key=WEAPON_PANEL_KEY + f'-{index}', expand_y=True)

def combat_weapon_damage_panel(parent_index: int, index: int, visible: bool = False) -> sg.Column:
    layout = [
        [sg.Text('Number of dice:', size=(15,1), justification='left'),
            sg.Spin([i for i in range(0, 20)], initial_value=0,
                key=f'{DICE_NUMBER_KEY}-{parent_index}-{index}',
                enable_events=True, size=(5,1), auto_size_text=False)],
        [sg.Text('Damage die:', size=(15,1), justification='left'),
            sg.Combo(Dice.get_values(), default_value=Dice.get_display_name(Dice.D6),
                key=f'{DAMAGE_DIE_KEY}-{parent_index}-{index}', enable_events=True,
                readonly=True, size=(5,1))],
        [sg.Text('Damage type:', size=(15,1), justification='left'),
            sg.Combo(DamageType.get_values(),
                default_value=DamageType.get_display_name(DamageType.ACID),
                key=f'{DAMAGE_TYPE_KEY}-{parent_index}-{index}',
                enable_events=True, readonly=True, size=(12,1))]
    ]

    return sg.Column(layout, key=WEAPON_DAMAGE_PANEL_KEY + f"-{parent_index}-{index}",
            visible=visible, size=(291, 78))

def combat_weapon_result_panel(parent_index: int) -> sg.Column:
    layout = [
        [sg.Text('Hit Bonus:', size=(20,1)),
            sg.Text('0', key=f'{HIT_BONUS_KEY}-{parent_index}', size=(10,1))],
        [sg.Text('Average Damage on Hit:', size=(20,1)),
            sg.Text('0', key=f'{AVG_HIT_DAMAGE_KEY}-{parent_index}', size=(10,1))],
        [sg.Text('Average Damage to Target:', size=(20,1)),
            sg.Text('0', key=f'{AVG_DAMAGE_KEY}-{parent_index}', size=(10,1))]
    ]

    return sg.Column(layout, size=(291, 78), pad=((5, 18), (5,5)))
#endregion

#region Currency Screen
def currency_panel(visible: bool = False) -> sg.Column:
    tabs = [[currency_split_panel(), currency_math_panel()]]
    layout = [[sg.TabGroup(layout=tabs, tab_location='top', border_width=0)]]
    return sg.Column(layout, key=CURRENCY_SCREEN_KEY, visible=visible, element_justification='center')

def currency_split_panel() -> sg.Tab:
    layout = [
        [
            sg.Text('Platinum'),
            sg.Input(key=SPLIT_PLATINUM_INPUT_KEY, default_text=0, enable_events=True, size=(10,1)),
            sg.Text('Gold'),
            sg.Input(key=SPLIT_GOLD_INPUT_KEY, default_text=0, enable_events=True, size=(10,1)),
            sg.Text('Electrum'),
            sg.Input(key=SPLIT_ELECTRUM_INPUT_KEY, default_text=0, enable_events=True, size=(10,1)),
            sg.Text('Silver'),
            sg.Input(key=SPLIT_SILVER_INPUT_KEY, default_text=0, enable_events=True, size=(10,1)),
            sg.Text('Copper'),
            sg.Input(key=SPLIT_COPPER_INPUT_KEY, default_text=0, enable_events=True, size=(10,1)),
        ],
        [
            sg.Text('Party size:'),
            sg.Input(default_text='1', size=(5,1), key=PARTY_SIZE_KEY, enable_events=True)
        ],
        [
            sg.Text('Consolidate currency?'),
            sg.Checkbox('', default=True, key=SPLIT_CONSOLIDATE_CURRENCY_KEY, enable_events=True)
        ],
        [
            sg.pin(sg.Column(layout=[
                [
                    sg.Text('Platinum'),
                    sg.Checkbox('', default=False, key=SPLIT_PLATINUM_USED_KEY, enable_events=True),
                    sg.Text('Gold'),
                    sg.Checkbox('', default=True, key=SPLIT_GOLD_USED_KEY, enable_events=True),
                    sg.Text('Electrum'),
                    sg.Checkbox('', default=False, key=SPLIT_ELECTRUM_USED_KEY, enable_events=True),
                    sg.Text('Silver'),
                    sg.Checkbox('', default=True, key=SPLIT_SILVER_USED_KEY, enable_events=True),
                    sg.Text('Copper'),
                    sg.Checkbox('', default=True, key=SPLIT_COPPER_USED_KEY, enable_events=True, disabled=True)
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
            sg.Text('', key=SPLIT_CURRENCY_RESULTS_KEY, size=(20,1), justification='center')
        ]
    ]

    return sg.Tab('Split', layout=layout, element_justification='center')

def currency_math_panel() -> sg.Tab:
    layout = [
        [
            sg.Text('Platinum'),
            sg.Input(key=MATH_PLATINUM_INPUT_1_KEY, default_text=0, enable_events=True, size=(10,1)),
            sg.Text('Gold'),
            sg.Input(key=MATH_GOLD_INPUT_1_KEY, default_text=0, enable_events=True, size=(10,1)),
            sg.Text('Electrum'),
            sg.Input(key=MATH_ELECTRUM_INPUT_1_KEY, default_text=0, enable_events=True, size=(10,1)),
            sg.Text('Silver'),
            sg.Input(key=MATH_SILVER_INPUT_1_KEY, default_text=0, enable_events=True, size=(10,1)),
            sg.Text('Copper'),
            sg.Input(key=MATH_COPPER_INPUT_1_KEY, default_text=0, enable_events=True, size=(10,1)),
        ],
        [
            sg.Text('Platinum'),
            sg.Input(key=MATH_PLATINUM_INPUT_2_KEY, default_text=0, enable_events=True, size=(10,1)),
            sg.Text('Gold'),
            sg.Input(key=MATH_GOLD_INPUT_2_KEY, default_text=0, enable_events=True, size=(10,1)),
            sg.Text('Electrum'),
            sg.Input(key=MATH_ELECTRUM_INPUT_2_KEY, default_text=0, enable_events=True, size=(10,1)),
            sg.Text('Silver'),
            sg.Input(key=MATH_SILVER_INPUT_2_KEY, default_text=0, enable_events=True, size=(10,1)),
            sg.Text('Copper'),
            sg.Input(key=MATH_COPPER_INPUT_2_KEY, default_text=0, enable_events=True, size=(10,1)),
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
                    sg.Checkbox('', default=True, key=MATH_COPPER_USED_KEY, enable_events=True, disabled=True)
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
            sg.Text('', key=MATH_CURRENCY_RESULTS_KEY, size=(20,1), justification='center')
        ]
    ]

    return sg.Tab('Math', layout=layout, element_justification='center')

#endregion
def change_screen(window: sg.Window, old_layout: int, new_layout: int) -> int:
    if ((0 <= old_layout < len(SCREEN_NAMES)) and (0 <= new_layout < len(SCREEN_NAMES)) and old_layout != new_layout):
        window[f'-screen-{old_layout}-'].update(visible=False)
        window[f'-screen-{new_layout}-'].update(visible=True)
        return new_layout
    else:
        return old_layout

#endregion

#region Combat Screen Functions
def add_weapon_damage(window: sg.Window, parent_index: int):
    # Find first hidden panel
    window[f'{WEAPON_DAMAGE_FRAME_KEY}-{parent_index}'].update(visible=True)
    window[f'{WEAPON_DAMAGE_FRAME_KEY}-{parent_index}'].unhide_row()
    next_index = -1
    parent_col = window[f'{WEAPON_PANEL_KEY}-{parent_index}']
    for index in range(NUM_DAMAGE_PANELS):
        col = window[f'{WEAPON_DAMAGE_PANEL_KEY}-{parent_index}-{index+1}']
        if (not col.visible):
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
    if (next_index == NUM_DAMAGE_PANELS - 1):
        window[f'{ADD_WEAPON_DAMAGE_BUTTON_KEY}-{parent_index}'].update(visible=False)
    window.refresh()

def remove_weapon_damage(window: sg.Window, parent_index: int):
    # Find last visible panel
    next_index = -1
    parent_col = window[f'{WEAPON_PANEL_KEY}-{parent_index}']
    for index in range(NUM_DAMAGE_PANELS, 0, -1):
        col = window[f'{WEAPON_DAMAGE_PANEL_KEY}-{parent_index}-{index}']
        if (col.visible):
            next_index = index
            break
    if next_index < 0:
        window[f'{REMOVE_WEAPON_DAMAGE_BUTTON_KEY}-{parent_index}'].update(visible=False)
        return
    col = window[f'{WEAPON_DAMAGE_PANEL_KEY}-{parent_index}-{next_index}']
    col.hide_row()
    col.update(visible=False)
    window[f'{ADD_WEAPON_DAMAGE_BUTTON_KEY}-{parent_index}'].update(visible=True)
    if (next_index == 1):
        window[f'{REMOVE_WEAPON_DAMAGE_BUTTON_KEY}-{parent_index}'].update(visible=False)
        window[f'{WEAPON_DAMAGE_FRAME_KEY}-{parent_index}'].hide_row()
        window[f'{WEAPON_DAMAGE_FRAME_KEY}-{parent_index}'].update(visible=False)
    window.refresh()

def update_weapon_attack(window: sg.Window, values: dict, index: int):
    weapon_type = WeaponType.convert_display_name(values[f'{WEAPON_TYPE_KEY}-{index}'])
    bonus = int(values[f'{WEAPON_BONUS_KEY}-{index}'])
    extra_damage = []
    for damage_index in range(NUM_DAMAGE_PANELS):
        col = window[f'{WEAPON_DAMAGE_PANEL_KEY}-{index}-{damage_index+1}']
        if (col.visible):
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
    event, values = window.read(timeout=0)
    update_weapon_summary(window, values)

def update_weapon_summary(window, values):
    weapon_damages = []
    for weapon_index in range(1,3):
        weapon_damages.append(float(window[f'{AVG_DAMAGE_KEY}-{weapon_index}'].get()))
    if (abs(weapon_damages[1]) < 0.00001):
        difference = 0.0
    else:
        difference = (weapon_damages[0] - weapon_damages[1]) / weapon_damages[1]
    if abs(difference) < 0.00001:
        summary = f'Weapon 1 deals the same damage as weapon 2'
    elif (difference < 0):
        summary = f'Weapon 1 deals {"{:0.2%}".format(difference)} less damage than weapon 2'
    else:
        summary = f'Weapon 1 deals {"{:0.2%}".format(difference)} more damage than weapon 2'
    window[WEAPON_SUMMARY_KEY].update(value = summary)
    window[WEAPON_SUMMARY_KEY].expand(expand_x = True)


def init_combat_panel(window: sg.Window, values: dict):
    for update_index in range(1,3):
        update_weapon_attack(window, values, update_index)

#endregion

#region Currency Screen Functions
def split_currency(window:sg.Window, values:dict):
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
    if (len(results) <= 1):
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

def add_currency(window:sg.Window, values:dict):
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
    consolidate = values[MATH_CONSOLIDATE_CURRENCY_KEY]
    currencies_used = CurrencyOptions.COPPER
    currencies_used |= CurrencyOptions.SILVER if values[MATH_SILVER_USED_KEY] else CurrencyOptions.COPPER
    currencies_used |= CurrencyOptions.ELECTRUM if values[MATH_ELECTRUM_USED_KEY] else CurrencyOptions.COPPER
    currencies_used |= CurrencyOptions.GOLD if values[MATH_GOLD_USED_KEY] else CurrencyOptions.COPPER
    currencies_used |= CurrencyOptions.PLATINUM if values[MATH_PLATINUM_USED_KEY] else CurrencyOptions.COPPER

    result = currency1 + currency2
    if consolidate:
        result = result.consolidate(currencies_used)
    window[MATH_CURRENCY_RESULTS_KEY].update(str(result))

def init_currency_panel(window: sg.Window, values: dict):
    split_currency(window, values)
    add_currency(window, values)

#endregion

if __name__ == "__main__":
    main()