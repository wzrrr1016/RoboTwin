from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 354_toy_and_hygiene_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add the shoe_box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add required objects
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.red_block = self.add_actor("red_block", "red_block")
        self.drill = self.add_actor("drill", "drill")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        
        # Add distractors
        distractors = ['baguette', 'jam-jar', 'olive-oil', 'apple', 'chips-tub']
        self.add_distractors(distractors)

    def play_once(self):
        # Place pink_block into shoe_box
        success = self.pick_and_place(self.pink_block, self.shoe_box)
        print("Pick place pink_block:", success)
        if not success:
            return self.info
        
        # Place red_block into shoe_box
        success = self.pick_and_place(self.red_block, self.shoe_box)
        print("Pick place red_block:", success)
        if not success:
            return self.info
        
        # Wrong action: Place drill into shoe_box
        success = self.pick_and_place(self.drill, self.shoe_box)
        print("Pick place drill (wrong):", success)
        if not success:
            return self.info
        
        # Recovery: Place drill back on table
        success = self.pick_and_place(self.drill, self.table)
        print("Recover drill to table:", success)
        if not success:
            return self.info
        
        # Place tissue-box into shoe_box
        success = self.pick_and_place(self.tissue_box, self.shoe_box)
        print("Pick place tissue-box:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        # Check if all correct items are in the shoe_box
        correct_items_in_shoe = (
            self.check_on(self.pink_block, self.shoe_box) and
            self.check_on(self.red_block, self.shoe_box) and
            self.check_on(self.tissue_box, self.shoe_box)
        )
        
        # Check if the drill is back on the table
        drill_on_table = self.check_on(self.drill, self.table)
        
        return correct_items_in_shoe and drill_on_table
