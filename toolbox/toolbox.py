import PySimpleGUI as sg
from combat import WeaponType, Dice, DamageType

# GUI Constants
THEME = 'Dark Blue 3'
WEAPON_TYPE_KEY = 'weapon-type'
WEAPON_BONUS_KEY = 'weapon-bonus'
EXIT_BUTTON_KEY = 'exit'

def main():
    sg.theme(THEME)
    window = main_window()

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == EXIT_BUTTON_KEY:
            break
    
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
        [weapon_panel()]
    ]

    return sg.Column(layout)

def weapon_panel() -> sg.Column:
    layout = [
        [sg.Text('Weapon type:'), sg.Combo(WeaponType.get_values(), default_value=WeaponType.get_display_name(WeaponType.CLUB), key=WEAPON_TYPE_KEY, enable_events=True, readonly=True)],
        [sg.Text('Bonus:'), sg.Input(default_text=0, key=WEAPON_BONUS_KEY, enable_events=True)]
    ]

    return sg.Column(layout)

def weapon_damage_panel() -> sg.Column:
    layout = [
        [sg.Text('Number of dice:'), sg.Input(default_text=1)],
        [sg.Text('Damage die:'), sg.Combo(Dice.get_values(), default_value=Dice.get_display_name(Dice.D6), enable_events=True, readonly=True)],
        [sg.Text('Weapon type:'), sg.Combo(DamageType.get_values(), default_value=DamageType.get_display_name(DamageType.BLUDGEONING), enable_events=True, readonly=True)]
    ]

    return sg.Column(layout)

if __name__ == "__main__":
    main()