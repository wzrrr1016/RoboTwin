from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 277_heavy_repair_tools_storage_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Add the shoe_box as a container.
        - Add the repair tools (drill, screwdriver, hammer) and shampoo as objects.
        - Add distractors as specified in the task description.
        """
        # Add the shoe_box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add the objects to be manipulated
        self.drill = self.add_actor("drill", "drill")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.hammer = self.add_actor("hammer", "hammer")
        self.shampoo = self.add_actor("shampoo", "shampoo")

        # Add distractors to the environment
        distractor_list = ['calculator', 'pot-with-plant', 'small-speaker', 'red_block', 'markpen']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        - Place the drill and hammer into the shoe_box (heavier repair tools).
        - Place the shampoo on the table (not a repair tool).
        - Place the screwdriver into the shoe_box (wrong action), then recover by placing it on the table.
        """
        # Place the drill into the shoe_box
        success = self.pick_and_place(self.drill, self.shoe_box)
        print("Pick drill:", success)
        if not success:
            return self.info

        # Place the screwdriver into the shoe_box (wrong action)
        success = self.pick_and_place(self.screwdriver, self.shoe_box)
        print("Pick screwdriver (wrong):", success)
        if not success:
            return self.info

        # Recover by placing the screwdriver on the table
        success = self.pick_and_place(self.screwdriver, self.table)
        print("Recover screwdriver:", success)
        if not success:
            return self.info

        # Place the hammer into the shoe_box
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Pick hammer:", success)
        if not success:
            return self.info

        # Place the shampoo on the table
        success = self.pick_and_place(self.shampoo, self.table)
        print("Place shampoo:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - The drill and hammer (heavier repair tools) should be in the shoe_box.
        - The screwdriver and shampoo should be on the table.
        """
        if (
            self.check_on(self.drill, self.shoe_box) and
            self.check_on(self.hammer, self.shoe_box) and
            self.check_on(self.screwdriver, self.table) and
            self.check_on(self.shampoo, self.table)
        ):
            return True
        return False
