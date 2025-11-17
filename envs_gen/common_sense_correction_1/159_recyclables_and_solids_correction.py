from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 159_recyclables_and_solids_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment"""
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add objects to be sorted
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.bottle = self.add_actor("bottle", "bottle")
        self.stapler = self.add_actor("stapler", "stapler")
        self.can = self.add_actor("can", "can")
        
        # Add distractor objects
        distractor_list = ['pot-with-plant', 'alarm-clock', 'shoe', 'baguette', 'small-speaker']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sorting task with recovery from initial error"""
        # Initial wrong placement (bottle in wooden_box)
        success = self.pick_and_place(self.bottle, self.wooden_box)
        print("Wrong placement of bottle into wooden_box:", success)
        if not success:
            return self.info

        # Recovery: Move bottle to correct container
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Recovery: bottle to fluted_block:", success)
        if not success:
            return self.info

        # Place can in correct container
        success = self.pick_and_place(self.can, self.fluted_block)
        print("Place can onto fluted_block:", success)
        if not success:
            return self.info

        # Place blue block in wooden box
        success = self.pick_and_place(self.blue_block, self.wooden_box)
        print("Place blue_block into wooden_box:", success)
        if not success:
            return self.info

        # Place yellow block in wooden box
        success = self.pick_and_place(self.yellow_block, self.wooden_box)
        print("Place yellow_block into wooden_box:", success)
        if not success:
            return self.info

        # Place stapler in wooden box
        success = self.pick_and_place(self.stapler, self.wooden_box)
        print("Place stapler into wooden_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify that all objects are in their correct containers"""
        return (
            self.check_on(self.bottle, self.fluted_block) and
            self.check_on(self.can, self.fluted_block) and
            self.check_on(self.blue_block, self.wooden_box) and
            self.check_on(self.yellow_block, self.wooden_box) and
            self.check_on(self.stapler, self.wooden_box)
        )
