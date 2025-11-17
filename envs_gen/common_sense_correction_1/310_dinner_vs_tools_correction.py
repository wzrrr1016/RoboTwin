from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 310_dinner_vs_tools_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: plate and wooden_box
        - Objects: fork, bottle, screwdriver, hammer
        - Distractors: pot-with-plant, toycar, alarm-clock, tissue-box, book
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add objects
        self.fork = self.add_actor("fork", "fork")
        self.bottle = self.add_actor("bottle", "bottle")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.hammer = self.add_actor("hammer", "hammer")

        # Add distractors
        distractor_list = ["pot-with-plant", "toycar", "alarm-clock", "tissue-box", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task:
        1. Place the bottle into the wooden_box (wrong action)
        2. Recover by placing the bottle onto the plate
        3. Place the fork onto the plate
        4. Place the screwdriver into the wooden_box
        5. Place the hammer into the wooden_box
        """
        # Step 1: Wrong action - Place bottle into wooden_box
        success = self.pick_and_place(self.bottle, self.wooden_box)
        print("Pick bottle into wooden_box (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - Place bottle onto plate
        success = self.pick_and_place(self.bottle, self.plate)
        print("Recover: bottle to plate:", success)
        if not success:
            return self.info

        # Step 3: Place fork onto plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Fork to plate:", success)
        if not success:
            return self.info

        # Step 4: Place screwdriver into wooden_box
        success = self.pick_and_place(self.screwdriver, self.wooden_box)
        print("Screwdriver to wooden_box:", success)
        if not success:
            return self.info

        # Step 5: Place hammer into wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Hammer to wooden_box:", success)
        if not success:
            return self.info

        return self.info  # Return final state if all actions succeed

    def check_success(self):
        """
        Check if the task is successfully completed:
        - Eating and drinking items (fork, bottle) are on the plate
        - Small hand repair tools (screwdriver, hammer) are in the wooden_box
        """
        if (self.check_on(self.fork, self.plate) and
            self.check_on(self.bottle, self.plate) and
            self.check_on(self.screwdriver, self.wooden_box) and
            self.check_on(self.hammer, self.wooden_box)):
            return True
        return False
