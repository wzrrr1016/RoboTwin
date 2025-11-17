from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 368_discard_heavy_tools_with_one_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        Includes containers, objects, and distractors.
        """
        # Add containers and main objects
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.drill = self.add_actor("drill", "drill")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.mug = self.add_actor("mug", "mug")
        self.hammer = self.add_actor("hammer", "hammer")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        
        # Add distractor objects to the environment
        distractors = ["pot-with-plant", "tissue-box", "alarm-clock", "book", "apple"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Execute the robot's task sequence:
        1. Wrongly place blue_block in dustbin
        2. Recover blue_block to table
        3. Place heavy repair tools (drill, hammer) in dustbin
        4. Place small toys (blue_block) and drinkware (mug) on table
        5. Leave screwdriver on table
        """
        # Wrong action: put blue_block into dustbin
        success = self.pick_and_place(self.blue_block, self.dustbin)
        print("Pick blue_block into dustbin (wrong):", success)
        if not success:
            return self.info

        # Recovery: put blue_block back on table
        success = self.pick_and_place(self.blue_block, self.table)
        print("Recover blue_block to table:", success)
        if not success:
            return self.info

        # Put heavy repair tools into dustbin
        success = self.pick_and_place(self.drill, self.dustbin)
        print("Pick drill into dustbin:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.hammer, self.dustbin)
        print("Pick hammer into dustbin:", success)
        if not success:
            return self.info

        # Put drinkware and small toys on table
        success = self.pick_and_place(self.mug, self.table)
        print("Put mug on table:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.screwdriver, self.table)
        print("Put screwdriver on table:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if all objects are in their correct final positions:
        - Heavy tools (drill, hammer) in dustbin
        - Small toys (blue_block) and drinkware (mug) on table
        - Screwdriver on table
        """
        return (
            self.check_on(self.drill, self.dustbin) and
            self.check_on(self.hammer, self.dustbin) and
            self.check_on(self.mug, self.table) and
            self.check_on(self.screwdriver, self.table) and
            self.check_on(self.blue_block, self.table)
        )
