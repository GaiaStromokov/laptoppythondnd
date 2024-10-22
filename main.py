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

# Global variable for skill proficiencies
skill_proficiencies = {}

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
        "racial_bonus_2": racial_bonus_2,
        "skills": skill_proficiencies
    }
    with open(character_data_file, 'w') as f:
        json.dump(character_data, f, indent=4)
    logging.info("Character data saved.")

def load_character_data():
    global character_class, character_subclass, character_race, character_subrace, character_background, character_level, base_scores, modified_scores, modifiers, racial_bonus_1, racial_bonus_2, skill_proficiencies
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
            skill_proficiencies = character_data.get("skills", {})
        logging.info("Character data loaded.")

# Load options for class, subclass, race, subrace, and background from JSON files
with open('data/classes.json') as f:
    classes_data = json.load(f)['classes']

with open('data/races.json') as f:
    races_data = json.load(f)['races']

with open('data/backgrounds.json') as f:
    backgrounds_data = json.load(f)['backgrounds']

def calculate_proficiency_bonus(level):
    return (level - 1) // 4 + 2

def calculate_modifier(score):
    return (score - 10) // 2

# Main application window configuration
main = ck.CTk()
main.config(bg="BurlyWood4")

main_size = [main.winfo_screenwidth(), main.winfo_screenheight()]
main.geometry(f"{main_size[0]}x{main_size[1]}")
main.title("Main")

# Set the window to the top left of the screen
main.geometry("+0+0")

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
        self.setup_widgets()

    def setup_widgets(self):
        self.header = ck.CTkLabel(self, font=("Helvetica", 12), width=180, height=30, justify='center', fg_color='ivory2', text="Character Info")
        self.level_label = ck.CTkLabel(self, font=("Helvetica", 12), width=65, height=30, justify='center', fg_color='ivory2', text="Level")

        self.level_var = ck.IntVar(value=character_level)
        self.level_display = ck.CTkLabel(self, font=("Helvetica", 12), width=30, height=30, justify='center', fg_color='ivory2', textvariable=self.level_var)

        self.levelinc = ck.CTkButton(self, text="+", width=18, height=15, fg_color="green", font=("Helvetica", 5), command=self.increment_level)
        self.leveldec = ck.CTkButton(self, text="-", width=18, height=15, fg_color="red", font=("Helvetica", 5), command=self.decrement_level)

        self.pb_label = ck.CTkLabel(self, font=("Helvetica", 12), width=25, height=30, justify='center', fg_color='ivory2', text="PB")
        self.pb_value = ck.CTkLabel(self, font=("Helvetica", 12), width=30, height=30, justify='center', fg_color='ivory2', textvariable=ck.IntVar(value=calculate_proficiency_bonus(character_level)))

        self.class_label = ck.CTkLabel(self, font=("Helvetica", 12), width=65, height=30, justify='center', fg_color='ivory2', text="Class")
        self.class_dd = ck.CTkComboBox(self, font=("Helvetica", 12), width=110, height=30, justify='center', fg_color='ivory2', values=[cls['name'] for cls in classes_data], state='readonly', command=self.save_class)
        self.class_dd.set(character_class)

        self.subclass_label = ck.CTkLabel(self, font=("Helvetica", 12), width=65, height=30, justify='center', fg_color='ivory2', text="Subclass")
        self.subclass_dd = ck.CTkComboBox(self, font=("Helvetica", 12), width=110, height=30, justify='center', fg_color='ivory2', values=[''], state='readonly', command=self.save_subclass)
        self.subclass_dd.set(character_subclass)

        if character_level < 3:
            self.subclass_dd.configure(state='disabled')
        else:
            self.update_subclass_options()

        self.race_label = ck.CTkLabel(self, font=("Helvetica", 12), width=65, height=30, justify='center', fg_color='ivory2', text="Race")
        self.race_dd = ck.CTkComboBox(self, font=("Helvetica", 12), width=110, height=30, justify='center', fg_color='ivory2', values=[race['name'] for race in races_data], state='readonly', command=self.save_race)
        self.race_dd.set(character_race)

        self.subrace_label = ck.CTkLabel(self, font=("Helvetica", 12), width=65, height=30, justify='center', fg_color='ivory2', text="Subrace")
        self.subrace_dd = ck.CTkComboBox(self, font=("Helvetica", 12), width=110, height=30, justify='center', fg_color='ivory2', values=[''], state='readonly', command=self.save_subrace)
        self.subrace_dd.set(character_subrace)

        self.background_label = ck.CTkLabel(self, font=("Helvetica", 12), width=65, height=30, justify='center', fg_color='ivory2', text="Background")
        self.background_dd = ck.CTkComboBox(self, font=("Helvetica", 12), width=110, height=30, justify='center', fg_color='ivory2', values=backgrounds_data, state='readonly', command=self.save_background)
        self.background_dd.set(character_background)

        self.header.place(x=10, y=10)
        self.level_label.place(x=10, y=45)
        self.level_display.place(x=80, y=45)
        self.levelinc.place(x=110, y=45)
        self.leveldec.place(x=110, y=60)
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

    def save_class(self, event=None):
        global character_class
        character_class = self.class_dd.get()
        logging.info(f"Class changed to {character_class}")
        self.update_subclass_options()
        abilities_frame.update_class_abilities()

    def save_subclass(self, event=None):
        global character_subclass
        character_subclass = self.subclass_dd.get()
        logging.info(f"Subclass changed to {character_subclass}")

    def save_race(self, event=None):
        global character_race
        character_race = self.race_dd.get()
        logging.info(f"Race changed to {character_race}")
        self.update_subrace_options()
        abilities_frame.update_racial_abilities()

    def save_subrace(self, event=None):
        global character_subrace
        character_subrace = self.subrace_dd.get()
        logging.info(f"Subrace changed to {character_subrace}")
        abilities_frame.update_racial_abilities()

    def save_background(self, event=None):
        global character_background
        character_background = self.background_dd.get()
        logging.info(f"Background changed to {character_background}")

    def increment_level(self):
        global character_level
        if character_level < 20:
            character_level += 1
            self.level_var.set(character_level)
            self.update_proficiency_bonus()
            self.update_subclass_state()
            abilities_frame.update_class_abilities()
            admin_frame.check_for_asi_or_feat()

    def decrement_level(self):
        global character_level
        if character_level > 1:
            character_level -= 1
            self.level_var.set(character_level)
            self.update_proficiency_bonus()
            self.update_subclass_state()
            abilities_frame.update_class_abilities()
            admin_frame.check_for_asi_or_feat()

    def update_subclass_options(self):
        selected_class = self.class_dd.get()
        for cls in classes_data:
            if cls['name'] == selected_class:
                self.subclass_dd.configure(values=cls['subclasses'])
                self.subclass_dd.set('')
                break

    def update_subrace_options(self):
        selected_race = self.race_dd.get()
        for race in races_data:
            if race['name'] == selected_race:
                self.subrace_dd.configure(values=race['subraces'])
                self.subrace_dd.set('')
                break

    def update_subclass_state(self):
        if character_level >= 3:
            self.subclass_dd.configure(state='normal')
            self.update_subclass_options()
        else:
            self.subclass_dd.configure(state='disabled')
            self.subclass_dd.set('')

    def update_proficiency_bonus(self):
        self.pb_value.configure(text=calculate_proficiency_bonus(character_level))

class AttributesFrame(BaseFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, width=230, height=265, *args, **kwargs)
        self.setup_widgets()

    def setup_widgets(self):
        header = ck.CTkLabel(self, font=("Helvetica", 14), width=210, height=30, justify='center', fg_color='ivory2', text="Attributes")
        header.place(x=10, y=10)

        attributes = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        for i, attribute in enumerate(attributes):
            y_position = 50 + i * 35

            name_label = ck.CTkLabel(self, font=("Helvetica", 12), width=80, height=30, justify='center', fg_color='ivory2', text=attribute)
            name_label.place(x=10, y=y_position)

            base_score_dd = ck.CTkComboBox(self, font=("Helvetica", 12), width=50, height=30, justify='center', fg_color='ivory2', values=[str(i) for i in range(1, 21)], command=lambda value, attr=attribute: self.update_base_score(attr, value))
            base_score_dd.set(str(base_scores[attribute]))
            base_score_dd.place(x=95, y=y_position)

            score_label = ck.CTkLabel(self, font=("Helvetica", 12), width=30, height=30, justify='center', fg_color='ivory2', textvariable=ck.StringVar(value=str(modified_scores[attribute])))
            score_label.place(x=150, y=y_position)

            modifier_label = ck.CTkLabel(self, font=("Helvetica", 12), width=30, height=30, justify='center', fg_color='ivory2', textvariable=ck.StringVar(value=str(modifiers[attribute])))
            modifier_label.place(x=190, y=y_position)

    def update_base_score(self, attribute, value):
        base_scores[attribute] = int(value)
        self.update_modified_score(attribute)

    def update_modified_score(self, attribute):
        bonus_1 = 2 if racial_bonus_2 == attribute else 0
        bonus_2 = 1 if racial_bonus_1 == attribute else 0
        modified_scores[attribute] = base_scores[attribute] + bonus_1 + bonus_2
        modifiers[attribute] = calculate_modifier(modified_scores[attribute])
        self.setup_widgets()
        self.update_skill_modifiers()

    def update_all_modified_scores(self):
        for attribute in base_scores.keys():
            self.update_modified_score(attribute)

    def update_skill_modifiers(self):
        for skill, ability in skills_frame.skills:
            skills_frame.skill_modifiers[skill] = skills_frame.calculate_skill_modifier(skill, ability)
        skills_frame.setup_widgets()
class AdminFrame(BaseFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, width=400, height=700, *args, **kwargs)
        self.setup_widgets()

    def setup_widgets(self):
        # Header
        admin_header = ck.CTkLabel(
            self, font=("Helvetica", 16, "bold"), width=380, height=30,
            justify='center', fg_color='ivory2', text="Admin - Character Choices"
        )
        admin_header.place(x=10, y=10)

        # Racial Bonuses Block
        self.setup_racial_bonus_widgets()

        # Class Proficiencies Block
        self.setup_proficiency_widgets()

        # ASI/Feat selection based on levels
        self.setup_asi_and_feat_widgets()

    def setup_racial_bonus_widgets(self):
        attributes = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

        # Label for Racial Bonuses
        racial_bonus_header = ck.CTkLabel(self, text="Racial Bonus:", font=("Helvetica", 12, "bold"))
        racial_bonus_header.place(x=10, y=50)
        
        dropdown_plus_1 = ck.CTkComboBox(
            self, font=("Helvetica", 12), width=100, values=attributes,
            command=self.update_racial_bonus_1
        )
        dropdown_plus_1.place(x=10, y=80)

        dropdown_plus_2 = ck.CTkComboBox(
            self, font=("Helvetica", 12), width=100, values=attributes,
            command=self.update_racial_bonus_2
        )
        dropdown_plus_2.place(x=10, y=110)

        

    def setup_proficiency_widgets(self):
        proficiencies = ["Athletics", "Acrobatics", "Arcana", "History", "Insight", "Perception", "Stealth"]

        # Label for Class Proficiencies
        class_prof_header = ck.CTkLabel(self, text="Class Proficiencies", font=("Helvetica", 12, "bold"))
        class_prof_header.place(x=10, y=140)

        # Two Dropdowns for choosing proficiencies side by side
        prof_dropdown_1 = ck.CTkComboBox(
            self, font=("Helvetica", 12), width=100, values=proficiencies,
            command=lambda prof: self.select_proficiency(prof, slot=1)
        )
        prof_dropdown_1.place(x=10, y=170)

        prof_dropdown_2 = ck.CTkComboBox(
            self, font=("Helvetica", 12), width=100, values=proficiencies,
            command=lambda prof: self.select_proficiency(prof, slot=2)
        )
        prof_dropdown_2.place(x=10, y=200)

    def setup_asi_and_feat_widgets(self):
        levels_with_asi = [4, 8, 12, 16, 19]
        attributes = ["Str", "Dex", "Con", "Int", "Wis", "Cha"]
        feats = ["Alert", "Actor", "Athlete", "Charger", "Crossbow Expert", "Dungeon Delver"]

        current_y = 50  # Starting position for ASI/Feat blocks

        for level in levels_with_asi:
            if character_level >= level:
                # Header for ASI/Feat choice per level
                label_choice = ck.CTkLabel(self, text=f"Level {level} ASI/Feat:", font=("Helvetica", 12, "bold"))
                label_choice.place(x=160, y=current_y)

                # Dropdown to select ASI or feat
                asi_feat_choice = ck.CTkComboBox(
                    self, font=("Helvetica", 12), width=100,
                    values=["ASCI", "Feat"],
                    command=lambda choice, lvl=level: self.show_asi_or_feat(choice, lvl, attributes, feats, current_y -270)
                )
                asi_feat_choice.place(x=160, y=current_y+30)
                current_y += 60

    def show_asi_or_feat(self, choice, level, attributes, feats, y_position):
        # Clear previous selection widgets at this position
        for widget in self.winfo_children():
            if widget.winfo_y() == y_position:
                widget.place_forget()

        if choice == "ASCI":
            # Two dropdowns for ASI, side by side
            asi_dropdown_1 = ck.CTkComboBox(
                self, font=("Helvetica", 12), width=60, values=attributes, 
                command=lambda value: self.update_ability_score(value, level, slot=1)
            )
            asi_dropdown_1.place(x=270, y=y_position)

            asi_dropdown_2 = ck.CTkComboBox(
                self, font=("Helvetica", 12), width=60, values=attributes,
                command=lambda value: self.update_ability_score(value, level, slot=2)
            )
            asi_dropdown_2.place(x=330, y=y_position)

        elif choice == "Feat":
            # Single dropdown for Feat
            feats_dropdown = ck.CTkComboBox(
                self, font=("Helvetica", 12), width=100, values=feats,
                command=lambda feat: self.update_feat_choice(feat, level)
            )
            feats_dropdown.place(x=270, y=y_position)

    def update_racial_bonus_2(self, value):
        global racial_bonus_2
        racial_bonus_2 = value
        logging.info(f"Racial bonus +2 updated to {racial_bonus_2}")
        attributes_frame.update_all_modified_scores()

    def update_racial_bonus_1(self, value):
        global racial_bonus_1
        racial_bonus_1 = value
        logging.info(f"Racial bonus +1 updated to {racial_bonus_1}")
        attributes_frame.update_all_modified_scores()

    def update_ability_score(self, value, level, slot):
        logging.info(f"Level {level} ASI slot {slot} increased for {value}")

    def update_feat_choice(self, feat, level):
        logging.info(f"Level {level} selected feat: {feat}")

    def select_proficiency(self, proficiency, slot):
        logging.info(f"Selected proficiency {slot}: {proficiency}")


class AbilitiesFrame(BaseFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, width=320, height=820, *args, **kwargs)
        self.setup_widgets()

    def setup_widgets(self):
        self.header = ck.CTkLabel(
            self, font=("Helvetica", 16, "bold"), width=300, height=30,
            justify='center', fg_color='ivory2', text="Features & Abilities"
        )
        self.header.place(x=10, y=10)

        self.racial_abilities_header = ck.CTkLabel(
            self, font=("Helvetica", 14, "bold"), width=300, height=30,
            justify='left', fg_color='ivory3', text="Racial Abilities"
        )
        self.racial_abilities_header.place(x=10, y=50)

        self.class_abilities_header = ck.CTkLabel(
            self, font=("Helvetica", 14, "bold"), width=300, height=30,
            justify='left', fg_color='ivory3', text="Class Abilities"
        )
        self.class_abilities_header.place(x=10, y=380)

        self.racial_abilities_text = ck.CTkTextbox(
            self, font=("Helvetica", 12), width=300, height=280,
            wrap='word', fg_color='white', text_color='black', padx=10, pady=10
        )
        self.racial_abilities_text.place(x=10, y=80)

        self.class_abilities_text = ck.CTkTextbox(
            self, font=("Helvetica", 12), width=300, height=380,
            wrap='word', fg_color='white', text_color='black', padx=10, pady=10
        )
        self.class_abilities_text.place(x=10, y=420)

        self.update_racial_abilities()
        self.update_class_abilities()

    def update_racial_abilities(self):
        race_file = f'races/{character_race.lower().replace(" ", "_")}.json'
        abilities_text = ""

        if os.path.exists(race_file):
            with open(race_file, 'r') as f:
                race_data = json.load(f)
                shared_abilities = race_data.get('shared_abilities', {})

                if shared_abilities:
                    abilities_text += "Shared Abilities:\n"
                    for ability_name, ability_info in shared_abilities.items():
                        abilities_text += f"{ability_name}: {ability_info['description']}\n\n"

                if character_subrace:
                    subrace_data = race_data.get('subraces', {}).get(character_subrace, {})
                    subrace_abilities = subrace_data.get('abilities', {})

                    if subrace_abilities:
                        abilities_text += "Subrace Abilities:\n"
                        for ability_name, ability_info in subrace_abilities.items():
                            if isinstance(ability_info, dict):
                                details = ', '.join([f"{k}: {v}" for k, v in ability_info.items()])
                                abilities_text += f"{ability_name}: {details}\n\n"
                            else:
                                abilities_text += f"{ability_name}: {ability_info}\n\n"

        self.racial_abilities_text.delete('1.0', ck.END)
        self.racial_abilities_text.insert(ck.END, abilities_text.strip())

    def update_class_abilities(self):
        class_file = f'classes/{character_class.lower().replace(" ", "_")}.json'
        abilities_text = ""

        if os.path.exists(class_file):
            with open(class_file, 'r') as f:
                class_data = json.load(f)
                abilities = []
                for level in range(1, character_level + 1):
                    level_data = class_data.get('abilities_per_level', {}).get(str(level), {})
                    for feature in level_data.get('features', []):
                        name = feature.get("name")
                        description = feature.get("description")
                        abilities.append(f"{name}: {description}")

                abilities_text = "\n\n".join(abilities)

        self.class_abilities_text.delete('1.0', ck.END)
        self.class_abilities_text.insert(ck.END, abilities_text.strip())

class SkillsFrame(BaseFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, width=220, height=685, *args, **kwargs)
        self.setup_widgets()

    def setup_widgets(self):
        self.header = ck.CTkLabel(self, font=("Helvetica", 12), width=200, height=30, justify='center', fg_color='ivory2', text="Skills")
        self.header.place(x=10, y=10)

        self.skills = [
            ("Acrobatics", "Dexterity"),
            ("Animal Handling", "Wisdom"),
            ("Arcana", "Intelligence"),
            ("Athletics", "Strength"),
            ("Deception", "Charisma"),
            ("History", "Intelligence"),
            ("Insight", "Wisdom"),
            ("Intimidation", "Charisma"),
            ("Investigation", "Intelligence"),
            ("Medicine", "Wisdom"),
            ("Nature", "Intelligence"),
            ("Perception", "Wisdom"),
            ("Performance", "Charisma"),
            ("Persuasion", "Charisma"),
            ("Religion", "Intelligence"),
            ("Sleight of Hand", "Dexterity"),
            ("Stealth", "Dexterity"),
            ("Survival", "Wisdom")
        ]

        self.skill_modifiers = {skill: self.calculate_skill_modifier(skill, ability) for skill, ability in self.skills}

        for i, (skill, ability) in enumerate(self.skills):
            y_position = 50 + i * 35

            skill_label = ck.CTkLabel(self, font=("Helvetica", 12), width=100, height=30, justify='center', fg_color='ivory2', text=skill)
            skill_label.place(x=10, y=y_position)

            proficiency_button = ck.CTkButton(self, text="", width=30, height=30, fg_color="green" if skill_proficiencies.get(skill, False) else "red", command=lambda s=skill: self.toggle_proficiency(s))
            proficiency_button.place(x=120, y=y_position)

            modifier_label = ck.CTkLabel(self, font=("Helvetica", 12), width=50, height=30, justify='center', fg_color='ivory2', textvariable=ck.StringVar(value=self.skill_modifiers[skill]))
            modifier_label.place(x=160, y=y_position)

    def toggle_proficiency(self, skill):
        skill_proficiencies[skill] = not skill_proficiencies.get(skill, False)
        self.setup_widgets()

    def calculate_skill_modifier(self, skill, ability):
        base_modifier = modifiers[ability]
        if skill_proficiencies.get(skill, False):
            return base_modifier + calculate_proficiency_bonus(character_level)
        return base_modifier

Info_frame = InfoFrame(main)
Info_frame.place(x=10, y=10)

admin_frame = AdminFrame(main)
admin_frame.place(x=1100, y=10)

attributes_frame = AttributesFrame(main)
attributes_frame.place(x=220, y=10)

abilities_frame = AbilitiesFrame(main)
abilities_frame.place(x=750, y=10)

skills_frame = SkillsFrame(main)
skills_frame.place(x=460, y=10)

main.mainloop()
