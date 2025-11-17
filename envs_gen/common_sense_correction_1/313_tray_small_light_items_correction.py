from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 313_tray_small_light_items_correction(Imagine_Task):
    def load_actors(self):
        # Add the tray container
        self.tray = self.add_actor("tray", "tray")
        # Add required objects
        self.red_block = self.add_actor("red_block", "red_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.stapler = self.add_actor("stapler", "stapler")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        # Add distractors
        distractor_list = ['olive-oil', 'jam-jar', 'milk-box', 'french_fries']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place red_block on tray
        success = self.pick_and_place(self.red_block, self.tray)
        print("Pick and place red_block:", success)
        if not success:
            return self.info

        # Place blue_block on tray
        success = self.pick_and_place(self.blue_block, self.tray)
        print("Pick and place blue_block:", success)
        if not success:
            return self.info

        # Place stapler on tray
        success = self.pick_and_place(self.stapler, self.tray)
        print("Pick and place stapler:", success)
        if not success:
            return self.info

        # Wrongly place pot-with-plant on tray
        success = self.pick_and_place(self.pot_with_plant, self.tray)
        print("Pick and place pot-with-plant (wrong):", success)
        if not success:
            return self.info

        # Correct by placing pot-with-plant on table
        success = self.pick_and_place(self.pot_with_plant, self.table)
        print("Pick and place pot-with-plant (recovery):", success)
        if not success:
            return self.info

        # Place dumbbell on table
        success = self.pick_and_place(self.dumbbell, self.table)
        print("Pick and place dumbbell:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check correct items are on the tray
        on_tray = (
            self.check_on(self.red_block, self.tray) and
            self.check_on(self.blue_block, self.tray) and
            self.check_on(self.stapler, self.tray)
        )
        # Check pot-with-plant is not on tray and is on table
        pot_correct = (
            not self.check_on(self.pot_with_plant, self.tray) and
            self.check_on(self.pot_with_plant, self.table)
        )
        # Check dumbbell is on table
        dumbbell_correct = self.check_on(self.dumbbell, self.table)

        return on_tray and pot_correct and dumbbell_correct
