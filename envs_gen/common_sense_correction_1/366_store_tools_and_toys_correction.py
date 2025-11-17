from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 366_store_tools_and_toys_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the shoe box (container), the target objects (toycar, screwdriver, hammer, mug),
        and the distractor objects.
        """
        # Add the shoe box as a container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add the target objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.hammer = self.add_actor("hammer", "hammer")
        self.mug = self.add_actor("mug", "mug")

        # Add distractor objects
        distractor_list = ["calculator", "pot-with-plant", "alarm-clock", "book", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        The robot places small repair tools and children's toys into the shoe box,
        and ensures that drinkware (mug) is not placed in the shoe box.
        """
        # Place toycar (children's toy) into the shoe box
        success = self.pick_and_place(self.toycar, self.shoe_box)
        print("Pick toycar:", success)
        if not success:
            return self.info

        # Place screwdriver (small repair tool) into the shoe box
        success = self.pick_and_place(self.screwdriver, self.shoe_box)
        print("Pick screwdriver:", success)
        if not success:
            return self.info

        # Place mug (drinkware) into the shoe box (wrong action)
        success = self.pick_and_place(self.mug, self.shoe_box)
        print("Pick mug (wrong):", success)
        if not success:
            return self.info

        # Recover by placing the mug back on the table
        success = self.pick_and_place(self.mug, self.table)
        print("Recover mug:", success)
        if not success:
            return self.info

        # Place hammer (small repair tool) into the shoe box
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Pick hammer:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The success condition is:
        - toycar, screwdriver, and hammer are in the shoe box
        - mug is on the table (not in the shoe box)
        """
        if (
            self.check_on(self.toycar, self.shoe_box) and
            self.check_on(self.screwdriver, self.shoe_box) and
            self.check_on(self.hammer, self.shoe_box) and
            self.check_on(self.mug, self.table)
        ):
            return True
        return False
