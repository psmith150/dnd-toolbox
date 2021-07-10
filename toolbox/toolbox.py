from enum import auto
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import VerticalSeparator
from combat import WeaponType, Dice, DamageType, Weapon, Damage, WeaponAttack

# GUI Constants
THEME = 'Dark Grey 13'
WEAPON_TYPE_KEY = 'weapon-type'
WEAPON_BONUS_KEY = 'weapon-bonus'
EXIT_BUTTON_KEY = 'exit'
CHARACTER_LEVEL_KEY = 'character-level'
CHARACTER_ATTACK_STAT_KEY = 'character-attack-stat'
CHARACTER_DAMAGE_MOD_KEY = 'character-damage-mod'
TARGET_AC_KEY = 'target-ac'
WEAPON_PANEL_KEY = 'weapon-panel'
ADD_WEAPON_DAMAGE_BUTTON_KEY = 'add-weapon-damage'
REMOVE_WEAPON_DAMAGE_BUTTON_KEY = 'remove-weapon-damage'
WEAPON_DAMAGE_PANEL_KEY = 'weapon-damage-panel'
DICE_NUMBER_KEY = 'dice-number'
DAMAGE_DIE_KEY = 'damage-die'
DAMAGE_TYPE_KEY = 'damage-type'
PROFICIENCY_KEY = 'proficient'
HIT_BONUS_KEY = 'hit-bonus'
AVG_HIT_DAMAGE_KEY = 'avg-hit-damage'
AVG_DAMAGE_KEY = 'avg-damage'
WEAPON_DAMAGE_FRAME_KEY = 'weapon-damage-frame'

DAMAGE_CALCULATION_EVENTS = [CHARACTER_LEVEL_KEY, CHARACTER_ATTACK_STAT_KEY,
    CHARACTER_DAMAGE_MOD_KEY, TARGET_AC_KEY, WEAPON_TYPE_KEY, WEAPON_BONUS_KEY,
    DICE_NUMBER_KEY, DAMAGE_DIE_KEY, DAMAGE_TYPE_KEY, PROFICIENCY_KEY]

NUM_DAMAGE_PANELS = 3

def main():
    sg.theme(THEME)
    window = main_window()
    first_read = False

    while True:
        if (not first_read):
            event, values = window.read(timeout=10)
        else:
            event, values = window.read()
        print(event, values)
        if (not first_read):
            first_read = True
            init_combat_panel(window, values)
        if event == sg.WINDOW_CLOSED or event == EXIT_BUTTON_KEY:
            break
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
    
    window.close()
    

def main_window() -> sg.Window:
    layout = [
        [sg.Text("Nav placeholder")],
        [combat_panel()],
        [sg.Exit(key=EXIT_BUTTON_KEY)]
    ]

    return sg.Window("D&D Toolbox", layout=layout, element_justification='center')

def combat_panel() -> sg.Column:
    layout = [
        [character_panel()],
        [weapon_panel(1), weapon_panel(2)],
        [sg.HorizontalSeparator()],
        [sg.Frame('Results', layout=[[weapon_result_panel(1), sg.VerticalSeparator(), weapon_result_panel(2)]])]
    ]

    return sg.Column(layout)

def character_panel() -> sg.Column:
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

def weapon_panel(index: int) -> sg.Column:
    layout = [[sg.Frame(f'Weapon {index}', layout=[
                [sg.Text('Weapon type:', size=(15,1), justification='left'),
                    sg.Combo(WeaponType.get_values(),
                        default_value=WeaponType.get_display_name(WeaponType.CLUB),
                        key=WEAPON_TYPE_KEY + f"-{index}", enable_events=True,
                        readonly=True, size=(20, 1))],
                [sg.Text('Bonus:', size=(15,1), justification='left'),
                    sg.Spin([i for i in range(0, 10)], initial_value=0,
                        key=WEAPON_BONUS_KEY + f"-{index}", enable_events=True,
                        size=(5,1), auto_size_text=False)],
                [sg.Text('Proficient?', size=(15,1), justification='left'),
                    sg.Checkbox('', key=PROFICIENCY_KEY + f'-{index}',
                        enable_events=True, default=True)]
                ])],
        [sg.Column(layout=[[sg.Button('Add', key=ADD_WEAPON_DAMAGE_BUTTON_KEY + f'-{index}')]]),
            sg.Column(layout=[[sg.Button('Remove', key=REMOVE_WEAPON_DAMAGE_BUTTON_KEY + f'-{index}', visible=False)]])],
    ]
    damage_panels = []
    for panel in range(NUM_DAMAGE_PANELS):
        damage_panels.append([weapon_damage_panel(index, panel + 1, False)])
    
    layout += [
        [sg.Frame('Additional Damage', damage_panels, key=f'{WEAPON_DAMAGE_FRAME_KEY}-{index}', visible=False)],
    ]

    return sg.Column(layout, key=WEAPON_PANEL_KEY + f'-{index}', expand_y=True)

def weapon_damage_panel(parent_index: int, index: int, visible: bool = False) -> sg.Column:
    layout = [
        [sg.Text('Number of dice:', size=(15,1), justification='left'),
            sg.Spin([i for i in range(0, 20)], initial_value=0,
                key=DICE_NUMBER_KEY + f"-{parent_index}-{index}",
                enable_events=True, size=(5,1), auto_size_text=False)],
        [sg.Text('Damage die:', size=(15,1), justification='left'),
            sg.Combo(Dice.get_values(), default_value=Dice.get_display_name(Dice.D6),
                key=DAMAGE_DIE_KEY + f"-{parent_index}-{index}", enable_events=True,
                readonly=True, size=(5,1))],
        [sg.Text('Damage type:', size=(15,1), justification='left'),
            sg.Combo(DamageType.get_values(),
                default_value=DamageType.get_display_name(DamageType.ACID),
                key=DAMAGE_TYPE_KEY + f"-{parent_index}-{index}",
                enable_events=True, readonly=True, size=(12,1))]
    ]

    return sg.Column(layout, key=WEAPON_DAMAGE_PANEL_KEY + f"-{parent_index}-{index}",
            visible=visible, size=(291, 78))

def weapon_result_panel(parent_index: int) -> sg.Column:
    layout = [
        [sg.Text('Hit Bonus:', size=(20,1)),
            sg.Text('0', key=HIT_BONUS_KEY + f"-{parent_index}", size=(10,1))],
        [sg.Text('Average Damage on Hit:', size=(20,1)),
            sg.Text('0', key=AVG_HIT_DAMAGE_KEY + f"-{parent_index}", size=(10,1))],
        [sg.Text('Average Damage to Target:', size=(20,1)),
            sg.Text('0', key=AVG_DAMAGE_KEY + f"-{parent_index}", size=(10,1))]
    ]

    return sg.Column(layout, size=(291, 78), pad=((5, 18), (5,5)))

def add_weapon_damage(window: sg.Window, parent_index: int):
    # Find first hidden panel
    window[f'{WEAPON_DAMAGE_FRAME_KEY}-{parent_index}'].update(visible=True)
    window[f'{WEAPON_DAMAGE_FRAME_KEY}-{parent_index}'].unhide_row()
    next_index = -1
    parent_col = window[WEAPON_PANEL_KEY + f'-{parent_index}']
    for index in range(NUM_DAMAGE_PANELS):
        col = window[WEAPON_DAMAGE_PANEL_KEY + f'-{parent_index}-{index+1}']
        if (not col.visible):
            next_index = index
            break
    if next_index < 0:
        window[ADD_WEAPON_DAMAGE_BUTTON_KEY + f'-{parent_index}'].update(visible=False)
        return
    col = window[WEAPON_DAMAGE_PANEL_KEY + f'-{parent_index}-{next_index+1}']
    col.unhide_row()
    col.update(visible=True)
    window[REMOVE_WEAPON_DAMAGE_BUTTON_KEY + f'-{parent_index}'].update(visible=True)
    if (next_index == NUM_DAMAGE_PANELS - 1):
        window[ADD_WEAPON_DAMAGE_BUTTON_KEY + f'-{parent_index}'].update(visible=False)
    window.refresh()

def remove_weapon_damage(window: sg.Window, parent_index: int):
    # Find last visible panel
    next_index = -1
    parent_col = window[WEAPON_PANEL_KEY + f'-{parent_index}']
    for index in range(NUM_DAMAGE_PANELS, 0, -1):
        col = window[WEAPON_DAMAGE_PANEL_KEY + f'-{parent_index}-{index}']
        if (col.visible):
            next_index = index
            break
    if next_index < 0:
        window[REMOVE_WEAPON_DAMAGE_BUTTON_KEY + f'-{parent_index}'].update(visible=False)
        return
    col = window[WEAPON_DAMAGE_PANEL_KEY + f'-{parent_index}-{next_index}']
    col.hide_row()
    col.update(visible=False)
    window[ADD_WEAPON_DAMAGE_BUTTON_KEY + f'-{parent_index}'].update(visible=True)
    if (next_index == 1):
        window[REMOVE_WEAPON_DAMAGE_BUTTON_KEY + f'-{parent_index}'].update(visible=False)
        window[f'{WEAPON_DAMAGE_FRAME_KEY}-{parent_index}'].hide_row()
        window[f'{WEAPON_DAMAGE_FRAME_KEY}-{parent_index}'].update(visible=False)
    window.refresh()

def update_weapon_attack(window: sg.Window, values: dict, index: int):
    weapon_type = WeaponType.convert_display_name(values[f'{WEAPON_TYPE_KEY}-{index}'])
    bonus = int(values[f'{WEAPON_BONUS_KEY}-{index}'])
    extra_damage = []
    for damage_index in range(NUM_DAMAGE_PANELS):
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

def init_combat_panel(window: sg.Window, values: dict):
    for update_index in range(1,3):
        update_weapon_attack(window, values, update_index)

if __name__ == "__main__":
    main()