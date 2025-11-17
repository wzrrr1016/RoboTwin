from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 106_drinkware_perishable_organize_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.apple = self.add_actor("apple", "apple")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.toycar = self.add_actor("toycar", "toycar")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")

        # Add distractors
        distractor_list = ["calculator", "book", "alarm-clock", "microphone", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place cup_with_handle on coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Place cup_with_handle on coaster:", success)
        if not success:
            return self.info

        # Place apple on coaster
        success = self.pick_and_place(self.apple, self.coaster)
        print("Place apple on coaster:", success)
        if not success:
            return self.info

        # Wrong placement of tissue-box on coaster
        success = self.pick_and_place(self.tissue_box, self.coaster)
        print("Wrongly place tissue-box on coaster:", success)
        if not success:
            return self.info

        # Recovery: move tissue-box to fluted_block
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Recover: place tissue-box on fluted_block:", success)
        if not success:
            return self.info

        # Place toycar on fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar on fluted_block:", success)
        if not success:
            return self.info

        # Place dumbbell on fluted_block
        success = self.pick_and_place(self.dumbbell, self.fluted_block)
        print("Place dumbbell on fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all required objects are placed correctly
        if (
            self.check_on(self.cup_with_handle, self.coaster) and
            self.check_on(self.apple, self.coaster) and
            self.check_on(self.tissue_box, self.fluted_block) and
            self.check_on(self.toycar, self.fluted_block) and
            self.check_on(self.dumbbell, self.fluted_block)
        ):
            return True
        return False
