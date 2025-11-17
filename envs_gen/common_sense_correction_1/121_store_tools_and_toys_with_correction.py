from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 121_store_tools_and_toys_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Create the shoe_box container.
        - Add the required objects: pink_block, knife, bread, stapler.
        - Add distractor objects to the environment.
        """
        # Create the shoe_box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add the required objects
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.knife = self.add_actor("knife", "knife")
        self.bread = self.add_actor("bread", "bread")
        self.stapler = self.add_actor("stapler", "stapler")

        # Add distractor objects
        distractor_list = ["calculator", "alarm-clock", "book", "tissue-box", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm.
        - Place pink_block into the shoe_box.
        - Place bread into the shoe_box (wrong action).
        - Recover by placing bread back on the table.
        - Place knife into the shoe_box.
        - Place stapler into the shoe_box.
        """
        # Place pink_block into the shoe_box
        success = self.pick_and_place(self.pink_block, self.shoe_box)
        print("Place pink_block:", success)
        if not success:
            return self.info

        # Wrongly place bread into the shoe_box
        success = self.pick_and_place(self.bread, self.shoe_box)
        print("Wrongly place bread:", success)
        if not success:
            return self.info

        # Recovery: Place bread back on the table
        success = self.pick_and_place(self.bread, self.table)
        print("Recover bread:", success)
        if not success:
            return self.info

        # Place knife into the shoe_box
        success = self.pick_and_place(self.knife, self.shoe_box)
        print("Place knife:", success)
        if not success:
            return self.info

        # Place stapler into the shoe_box
        success = self.pick_and_place(self.stapler, self.shoe_box)
        print("Place stapler:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - All small tools and toys (pink_block, knife, stapler) are in the shoe_box.
        - Perishable food (bread) is not in the shoe_box.
        """
        if (self.check_on(self.pink_block, self.shoe_box) and
            self.check_on(self.knife, self.shoe_box) and
            self.check_on(self.stapler, self.shoe_box) and
            not self.check_on(self.bread, self.shoe_box)):
            return True
        return False
