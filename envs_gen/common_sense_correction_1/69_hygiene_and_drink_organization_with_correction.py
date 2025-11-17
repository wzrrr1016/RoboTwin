from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 69_hygiene_and_drink_organization_with_correction(Imagine_Task):
    def load_actors(self):
        # Create required containers and objects
        self.tray = self.add_actor("tray", "tray")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.bottle = self.add_actor("bottle", "bottle")
        self.can = self.add_actor("can", "can")
        
        # Add distractor objects to the environment
        distractor_list = ["alarm-clock", "mouse", "screwdriver", "small-speaker", "red_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Pick shampoo and place it into tray
        success = self.pick_and_place(self.shampoo, self.tray)
        print("Pick shampoo:", success)
        if not success:
            return self.info

        # Step 2: Pick can and place it into tray
        success = self.pick_and_place(self.can, self.tray)
        print("Pick can:", success)
        if not success:
            return self.info

        # Step 3: Wrong action - Pick tissue-box and place it into bottle
        success = self.pick_and_place(self.tissue_box, self.bottle)
        print("Wrong placement of tissue-box:", success)
        if not success:
            return self.info

        # Step 4: Recovery - Pick tissue-box from bottle and place it into tray
        success = self.pick_and_place(self.tissue_box, self.tray)
        print("Recovery of tissue-box:", success)
        if not success:
            return self.info

        # Step 5: Pick bottle and place it into tray
        success = self.pick_and_place(self.bottle, self.tray)
        print("Pick bottle:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify all required objects are on the tray
        return (
            self.check_on(self.shampoo, self.tray) and
            self.check_on(self.tissue_box, self.tray) and
            self.check_on(self.bottle, self.tray) and
            self.check_on(self.can, self.tray)
        )
