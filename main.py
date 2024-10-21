import customtkinter as ck
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Global variables for character data
character_class = ""
character_subclass = ""
character_race = ""
character_subrace = ""
character_background = ""
character_level = 1

# New global variables for base and modified scores
base_scores = {
    "Strength": 10,
    "Dexterity": 10,
    "Constitution": 10,
    "Intelligence": 10,
    "Wisdom": 10,
    "Charisma": 10
}

modified_scores = base_scores.copy()

# Global variables for racial bonuses
racial_bonus_1 = ""
racial_bonus_2 = ""

# Global variables for modifiers
modifiers = {attr: 0 for attr in base_scores.keys()}

# File path for saving/loading character data
character_data_file = 'character_data.json'

def save_character_data():
    character_data = {
        "character_class": character_class,
        "character_subclass": character_subclass,
        "character_race": character_race,
        "character_subrace": character_subrace,
        "character_background": character_background,
        "character_level": character_level,
        "base_scores": base_scores,
        "modified_scores": modified_scores,
        "modifiers": modifiers,
        "racial_bonus_1": racial_bonus_1,
        "racial_bonus_2": racial_bonus_2
    }
    with open(character_data_file, 'w') as f:
        json.dump(character_data, f, indent=4)
    logging.info("Character data saved.")

def load_character_data():
    global character_class, character_subclass, character_race, character_subrace, character_background, character_level, base_scores, modified_scores, modifiers, racial_bonus_1, racial_bonus_2
    if os.path.exists(character_data_file):
        with open(character_data_file, 'r') as f:
            character_data = json.load(f)
            character_class = character_data.get("character_class", "")
            character_subclass = character_data.get("character_subclass", "")
            character_race = character_data.get("character_race", "")
            character_subrace = character_data.get("character_subrace", "")
            character_background = character_data.get("character_background", "")
            character_level = character_data.get("character_level", 1)
            base_scores = character_data.get("base_scores", base_scores)
            modified_scores = character_data.get("modified_scores", modified_scores)
            modifiers = character_data.get("modifiers", modifiers)
            racial_bonus_1 = character_data.get("racial_bonus_1", "")
            racial_bonus_2 = character_data.get("racial_bonus_2", "")
        logging.info("Character data loaded.")

# Load options for class, subclass, race, subrace, and background from JSON files
with open('data/classes.json') as f:
    classes_data = json.load(f)['classes']

with open('data/races.json') as f:
    races_data = json.load(f)['races']

with open('data/backgrounds.json') as f:
    backgrounds_data = json.load(f)['backgrounds']  # Access the list of backgrounds

def calculate_proficiency_bonus(level):
    return (level - 1) // 4 + 2

def calculate_modifier(score):
    return (score - 10) // 2

# Main application window configuration
main = ck.CTk()
main.config(bg="BurlyWood4")
main_size = [1000, 800]
main.geometry(f"{main_size[0]}x{main_size[1]}")
main.title("Main")

load_character_data()

# Save character data on exit
main.protocol("WM_DELETE_WINDOW", lambda: [save_character_data(), main.destroy()])

# Base Frame class to handle common frame attributes
class BaseFrame(ck.CTkFrame):
    def __init__(self, parent, width, height, *args, **kwargs):
        super().__init__(parent, width=width, height=height, border_width=1, border_color="black", *args, **kwargs)
        self.configure(fg_color='navajo white')

# InfoFrame class for character information
class InfoFrame(BaseFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, width=200, height=255, *args, **kwargs)

        self.setup_widgets()  # Set up widgets on the InfoFrame

    def setup_widgets(self):
        # Creating widgets inside InfoFrame
        self.header = ck.CTkLabel(self, font=("Arial", 12), width=180, height=30, justify='center', fg_color='ivory2', text="Character Info")
        self.level_label = ck.CTkLabel(self, font=("Arial", 12), width=65, height=30, justify='center', fg_color='ivory2', text="Level")

        # Level display label
        self.level_var = ck.IntVar(value=character_level)
        self.level_display = ck.CTkLabel(self, font=("Arial", 12), width=30, height=30, justify='center', fg_color='ivory2', textvariable=self.level_var)

        # Level increment button
        self.levelinc = ck.CTkButton(self, text="+", width=18, height=15, fg_color="green", font=("Arial", 5), command=self.increment_level)
        self.leveldec = ck.CTkButton(self, text="-", width=18, height=15, fg_color="red", font=("Arial", 5), command=self.decrement_level)

        self.pb_label = ck.CTkLabel(self, font=("Arial", 12), width=25, height=30, justify='center', fg_color='ivory2', text="PB")
        self.pb_value = ck.CTkLabel(self, font=("Arial", 12), width=30, height=30, justify='center', fg_color='ivory2', textvariable=ck.IntVar(value=calculate_proficiency_bonus(character_level)))  # Dynamically updated PB

        # Dropdowns for Class, Subclass, etc.
        self.class_label = ck.CTkLabel(self, font=("Arial", 12), width=65, height=30, justify='center', fg_color='ivory2', text="Class")
        self.class_dd = ck.CTkComboBox(self, font=("Arial", 12), width=110, height=30, justify='center', fg_color='ivory2', values=[cls['name'] for cls in classes_data], state='readonly', command=self.save_class)
        self.class_dd.set(character_class)  # Set default class from saved data

        self.subclass_label = ck.CTkLabel(self, font=("Arial", 12), width=65, height=30, justify='center', fg_color='ivory2', text="Subclass")
        self.subclass_dd = ck.CTkComboBox(self, font=("Arial", 12), width=110, height=30, justify='center', fg_color='ivory2', values=[''], state='readonly', command=self.save_subclass)
        self.subclass_dd.set(character_subclass)

        # Disable subclass dropdown if the level is less than 3
        if character_level < 3:
            self.subclass_dd.configure(state='disabled')
        else:
            self.update_subclass_options()

        # Dropdown for Race
        self.race_label = ck.CTkLabel(self, font=("Arial", 12), width=65, height=30, justify='center', fg_color='ivory2', text="Race")
        self.race_dd = ck.CTkComboBox(self, font=("Arial", 12), width=110, height=30, justify='center', fg_color='ivory2', values=[race['name'] for race in races_data], state='readonly', command=self.save_race)
        self.race_dd.set(character_race)

        # Dropdown for Subrace
        self.subrace_label = ck.CTkLabel(self, font=("Arial", 12), width=65, height=30, justify='center', fg_color='ivory2', text="Subrace")
        self.subrace_dd = ck.CTkComboBox(self, font=("Arial", 12), width=110, height=30, justify='center', fg_color='ivory2', values=[''], state='readonly', command=self.save_subrace)
        self.subrace_dd.set(character_subrace)

        # Dropdown for Background
        self.background_label = ck.CTkLabel(self, font=("Arial", 12), width=65, height=30, justify='center', fg_color='ivory2', text="Background")
        self.background_dd = ck.CTkComboBox(self, font=("Arial", 12), width=110, height=30, justify='center', fg_color='ivory2', values=backgrounds_data, state='readonly', command=self.save_background)
        self.background_dd.set(character_background)

        # Positioning widgets within the InfoFrame using place
        self.header.place(x=10, y=10)
        self.level_label.place(x=10, y=45)
        self.level_display.place(x=80, y=45)
        self.levelinc.place(x=110, y=45)  # Positioning the level increment button directly to the right of the level display
        self.leveldec.place(x=110, y=60)  # Positioning the level decrement button directly below the increment button
        self.pb_label.place(x=130, y=45)
        self.pb_value.place(x=160, y=45)

        self.class_label.place(x=10, y=80)
        self.class_dd.place(x=80, y=80)

        self.subclass_label.place(x=10, y=115)
        self.subclass_dd.place(x=80, y=115)

        self.race_label.place(x=10, y=150)
        self.race_dd.place(x=80, y=150)

        self.subrace_label.place(x=10, y=185)
        self.subrace_dd.place(x=80, y=185)

        self.background_label.place(x=10, y=220)
        self.background_dd.place(x=80, y=220)

    # Method to save class
    def save_class(self, event=None):  # event is optional for manual calls
        global character_class
        character_class = self.class_dd.get()
        logging.info(f"Class changed to {character_class}")
        self.update_subclass_options()
        abilities_frame.update_class_abilities()  # Update class abilities when class changes

    # Method to save subclass
    def save_subclass(self, event=None):  # event is optional for manual calls
        global character_subclass
        character_subclass = self.subclass_dd.get()
        logging.info(f"Subclass changed to {character_subclass}")

    # Method to save race
    def save_race(self, event=None):  # event is optional for manual calls
        global character_race
        character_race = self.race_dd.get()
        logging.info(f"Race changed to {character_race}")
        self.update_subrace_options()
        abilities_frame.update_racial_abilities()  # Update racial abilities when race changes

    # Method to save subrace
    def save_subrace(self, event=None):  # event is optional for manual calls
        global character_subrace
        character_subrace = self.subrace_dd.get()
        logging.info(f"Subrace changed to {character_subrace}")
        abilities_frame.update_racial_abilities()  # Update racial abilities when subrace changes

    # Method to save background
    def save_background(self, event=None):  # event is optional for manual calls
        global character_background
        character_background = self.background_dd.get()
        logging.info(f"Background changed to {character_background}")

    # Method to increment level
    def increment_level(self):
        global character_level
        if character_level < 20:  # Ensure level doesn't go beyond 20
            character_level += 1
            self.level_var.set(character_level)
            self.update_proficiency_bonus()
            self.update_subclass_state()
            abilities_frame.update_class_abilities()  # Update class abilities when level changes

    # Method to decrement level
    def decrement_level(self):
        global character_level
        if character_level > 1:  # Prevent level from going below 1
            character_level -= 1
            self.level_var.set(character_level)
            self.update_proficiency_bonus()
            self.update_subclass_state()
            abilities_frame.update_class_abilities()  # Update class abilities when level changes

    # Method to update subclass options based on selected class
    def update_subclass_options(self):
        selected_class = self.class_dd.get()
        for cls in classes_data:
            if cls['name'] == selected_class:
                self.subclass_dd.configure(values=cls['subclasses'])
                self.subclass_dd.set('')  # Reset subclass selection
                break

    # Method to update subrace options based on selected race
    def update_subrace_options(self):
        selected_race = self.race_dd.get()
        for race in races_data:
            if race['name'] == selected_race:
                self.subrace_dd.configure(values=race['subraces'])
                self.subrace_dd.set('')  # Reset subrace selection
                break

    # Method to update subclass state (enable or disable based on level)
    def update_subclass_state(self):
        if character_level >= 3:
            self.subclass_dd.configure(state='normal')
            self.update_subclass_options()
        else:
            self.subclass_dd.configure(state='disabled')
            self.subclass_dd.set('')  # Clear the subclass if level is below 3

    # Method to update proficiency bonus when level changes
    def update_proficiency_bonus(self):
        self.pb_value.configure(text=calculate_proficiency_bonus(character_level))

class AttributesFrame(BaseFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, width=230, height=265, *args, **kwargs)  # Reduced width
        self.setup_widgets()

    def setup_widgets(self):
        # Header for the AttributesFrame
        header = ck.CTkLabel(self, font=("Arial", 14), width=210, height=30, justify='center', fg_color='ivory2', text="Attributes")
        header.place(x=10, y=10)

        attributes = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        for i, attribute in enumerate(attributes):
            y_position = 50 + i * 35  # Adjust y position for each row

            name_label = ck.CTkLabel(self, font=("Arial", 12), width=80, height=30, justify='center', fg_color='ivory2', text=attribute)
            name_label.place(x=10, y=y_position)

            base_score_dd = ck.CTkComboBox(self, font=("Arial", 12), width=50, height=30, justify='center', fg_color='ivory2', values=[str(i) for i in range(1, 21)], command=lambda value, attr=attribute: self.update_base_score(attr, value))  # Smaller dropdown
            base_score_dd.set(str(base_scores[attribute]))
            base_score_dd.place(x=95, y=y_position)

            score_label = ck.CTkLabel(self, font=("Arial", 12), width=30, height=30, justify='center', fg_color='ivory2', textvariable=ck.StringVar(value=str(modified_scores[attribute])))
            score_label.place(x=150, y=y_position)

            modifier_label = ck.CTkLabel(self, font=("Arial", 12), width=30, height=30, justify='center', fg_color='ivory2', textvariable=ck.StringVar(value=str(modifiers[attribute])))
            modifier_label.place(x=190, y=y_position)

    def update_base_score(self, attribute, value):
        base_scores[attribute] = int(value)
        self.update_modified_score(attribute)

    def update_modified_score(self, attribute):
        # Calculate the modified score including racial bonuses
        bonus_1 = 2 if racial_bonus_2 == attribute else 0
        bonus_2 = 1 if racial_bonus_1 == attribute else 0
        modified_scores[attribute] = base_scores[attribute] + bonus_1 + bonus_2
        # Calculate the modifier
        modifiers[attribute] = calculate_modifier(modified_scores[attribute])
        # Update the score and modifier labels
        self.setup_widgets()

class AdminFrame(BaseFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, width=200, height=700, *args, **kwargs)
        self.setup_widgets()

    def setup_widgets(self):

        # Header for the AdminFrame
        Adminheader = ck.CTkLabel(self, font=("Arial", 14), width=180, height=30, justify='center', fg_color='ivory2', text="Admin")
        Adminheader.place(x=10, y=10)
        
        RacialBonusheader = ck.CTkLabel(self, font=("Arial", 14), width=180, height=30, justify='center', fg_color='ivory2', text="Racial Bonus")
        RacialBonusheader.place(x=10, y=50)
        attributes = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

        # Label for +2 dropdown
        label_plus_2 = ck.CTkLabel(self, text="+2", font=("Arial", 12))
        label_plus_2.place(x=10, y=90)

        # Dropdown for +2 bonus
        self.dropdown_plus_2 = ck.CTkComboBox(self, font=("Arial", 12), width=100, height=30, justify='center', fg_color='ivory2', values=attributes, command=self.update_racial_bonus_2)
        self.dropdown_plus_2.place(x=30, y=90)

        # Label for +1 dropdown
        label_plus_1 = ck.CTkLabel(self, text="+1", font=("Arial", 12))
        label_plus_1.place(x=10, y=130)

        # Dropdown for +1 bonus
        self.dropdown_plus_1 = ck.CTkComboBox(self, font=("Arial", 12), width=100, height=30, justify='center', fg_color='ivory2', values=attributes, command=self.update_racial_bonus_1)
        self.dropdown_plus_1.place(x=30, y=130)

        # Additional sections for different decision areas
        self.add_section("Section 1", 190)
        self.add_section("Section 2", 230)
        self.add_section("Section 3", 270)

    def add_section(self, title, y_position):
        section_header = ck.CTkLabel(self, font=("Arial", 14), width=180, height=30, justify='center', fg_color='ivory2', text=title)
        section_header.place(x=10, y=y_position)

    def update_racial_bonus_2(self, value):
        global racial_bonus_2
        racial_bonus_2 = value
        logging.info(f"Racial bonus +2 updated to {racial_bonus_2}")
        self.update_all_modified_scores()

    def update_racial_bonus_1(self, value):
        global racial_bonus_1
        racial_bonus_1 = value
        logging.info(f"Racial bonus +1 updated to {racial_bonus_1}")
        self.update_all_modified_scores()

    def update_all_modified_scores(self):
        for attribute in base_scores.keys():
            bonus_1 = 2 if racial_bonus_2 == attribute else 0
            bonus_2 = 1 if racial_bonus_1 == attribute else 0
            modified_scores[attribute] = base_scores[attribute] + bonus_1 + bonus_2
            modifiers[attribute] = calculate_modifier(modified_scores[attribute])
        attributes_frame.setup_widgets()

class AbilitiesFrame(BaseFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, width=300, height=765, *args, **kwargs)
        self.setup_widgets()

    def setup_widgets(self):
        self.header = ck.CTkLabel(self, font=("Arial", 12), width=280, height=30, justify='center', fg_color='ivory2', text="Features/Abilities")
        self.header.place(x=10, y=10)

        self.racial_abilities_header = ck.CTkLabel(self, font=("Arial", 12), width=280, height=30, justify='center', fg_color='ivory2', text="Racial Abilities")
        self.racial_abilities_header.place(x=10, y=50)

        self.racial_abilities_text = ck.CTkTextbox(self, font=("Arial", 12), width=280, height=100, fg_color='ivory2')
        self.racial_abilities_text.place(x=10, y=90)

        self.class_abilities_header = ck.CTkLabel(self, font=("Arial", 12), width=280, height=30, justify='center', fg_color='ivory2', text="Class Abilities")
        self.class_abilities_header.place(x=10, y=200)

        self.class_abilities_text = ck.CTkTextbox(self, font=("Arial", 12), width=280, height=100, fg_color='ivory2')
        self.class_abilities_text.place(x=10, y=240)

        self.feats_header = ck.CTkLabel(self, font=("Arial", 12), width=280, height=30, justify='center', fg_color='ivory2', text="Feats")
        self.feats_header.place(x=10, y=350)

        self.feats_text = ck.CTkTextbox(self, font=("Arial", 12), width=280, height=100, fg_color='ivory2')
        self.feats_text.place(x=10, y=390)

        self.update_class_abilities()
        self.update_racial_abilities()

    def update_class_abilities(self):
        class_file = f'classes/{character_class.lower()}.json'
        if os.path.exists(class_file):
            with open(class_file, 'r') as f:
                class_data = json.load(f)
                abilities = []
                for level in range(1, character_level + 1):
                    abilities.extend(class_data.get('abilities_per_level', {}).get(str(level), {}).get('features', []))
                abilities_text = "\n".join(abilities)
                self.class_abilities_text.delete('1.0', ck.END)
                self.class_abilities_text.insert(ck.END, abilities_text)
        else:
            self.class_abilities_text.delete('1.0', ck.END)
            self.class_abilities_text.insert(ck.END, f"{character_class} not found")

    def update_racial_abilities(self):
        racial_abilities = self.get_racial_abilities()
        racial_abilities_text = "\n".join(racial_abilities)
        self.racial_abilities_text.delete('1.0', ck.END)
        self.racial_abilities_text.insert(ck.END, racial_abilities_text)

    def get_racial_abilities(self):
        race_file = f'races/{character_race.lower()}.json'
        if os.path.exists(race_file):
            with open(race_file, 'r') as f:
                race_data = json.load(f)
                return race_data.get('abilities', [])
        return []

admin_frame = InfoFrame(main)
admin_frame.place(x=10, y=10)

admin_frame = AdminFrame(main)
admin_frame.place(x=780, y=10)  # Adjust x and y to place it in the far right corner

# Create and place the AttributesFrame
attributes_frame = AttributesFrame(main)
attributes_frame.place(x=220, y=10)

# Create and place the AbilitiesFrame
abilities_frame = AbilitiesFrame(main)
abilities_frame.place(x=460, y=10)

main.mainloop()