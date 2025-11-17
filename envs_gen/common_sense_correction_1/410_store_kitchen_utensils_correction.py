from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 410_store_kitchen_utensils_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Adds the wooden_box as a container.
        - Adds the relevant objects: knife, fork, teanet, and shoe.
        - Adds distractor objects as specified in the task description.
        """
        # Add the wooden box as a container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add the relevant objects
        self.knife = self.add_actor("knife", "knife")
        self.fork = self.add_actor("fork", "fork")
        self.teanet = self.add_actor("teanet", "teanet")
        self.shoe = self.add_actor("shoe", "shoe")

        # Add distractor objects
        distractor_list = ['calculator', 'toycar', 'dumbbell', 'alarm-clock', 'stapler']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        - First, place the shoe into the wooden_box (wrong action).
        - Then, recover the shoe by placing it back on the table.
        - Finally, place the correct kitchen and dining utensils (fork, knife, teanet) into the wooden_box.
        """
        # Wrong action: place shoe into wooden_box
        success = self.pick_and_place(self.shoe, self.wooden_box)
        print("Place shoe into box:", success)
        if not success:
            return self.info

        # Recovery: pick shoe from box and place on table
        success = self.pick_and_place(self.shoe, self.table)
        print("Recover shoe to table:", success)
        if not success:
            return self.info

        # Correct actions: place utensils into wooden_box
        success = self.pick_and_place(self.fork, self.wooden_box)
        print("Place fork:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.knife, self.wooden_box)
        print("Place knife:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.teanet, self.wooden_box)
        print("Place teanet:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - All correct utensils (fork, knife, teanet) must be in the wooden_box.
        - The shoe must be on the table (not in the wooden_box).
        """
        if (self.check_on(self.fork, self.wooden_box) and
            self.check_on(self.knife, self.wooden_box) and
            self.check_on(self.teanet, self.wooden_box) and
            self.check_on(self.shoe, self.table)):
            return True
        return False
