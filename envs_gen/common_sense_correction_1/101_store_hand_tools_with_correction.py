from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 101_store_hand_tools_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the shoe box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add the main objects
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.hammer = self.add_actor("hammer", "hammer")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        
        # Add distractor objects
        distractor_list = ["apple", "book", "toycar", "tissue-box", "chips-tub"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # 1. Pick screwdriver and place into shoe_box
        success = self.pick_and_place(self.screwdriver, self.shoe_box)
        print("Pick screwdriver:", success)
        if not success:
            return self.info

        # 2. Pick pot-with-plant and place into shoe_box (wrong action)
        success = self.pick_and_place(self.pot_with_plant, self.shoe_box)
        print("Pick pot-with-plant (wrong):", success)
        if not success:
            return self.info

        # 3. Recovery: Pick pot-with-plant from shoe_box and place on table
        success = self.pick_and_place(self.pot_with_plant, self.table)
        print("Recover pot-with-plant:", success)
        if not success:
            return self.info

        # 4. Pick hammer and place into shoe_box
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Pick hammer:", success)
        if not success:
            return self.info

        # 5. Pick dumbbell and place on table
        success = self.pick_and_place(self.dumbbell, self.table)
        print("Pick dumbbell:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if repair tools are in the shoe box
        screwdriver_in = self.check_on(self.screwdriver, self.shoe_box)
        hammer_in = self.check_on(self.hammer, self.shoe_box)
        
        # Check if non-repair items are NOT in the shoe box
        pot_out = not self.check_on(self.pot_with_plant, self.shoe_box)
        dumbbell_out = not self.check_on(self.dumbbell, self.shoe_box)
        
        # Return success if all conditions are met
        return screwdriver_in and hammer_in and pot_out and dumbbell_out
