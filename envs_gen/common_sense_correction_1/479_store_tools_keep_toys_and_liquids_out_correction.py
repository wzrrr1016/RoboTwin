from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 479_store_tools_keep_toys_and_liquids_out_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Add the wooden_box as a container.
        - Add the relevant objects: knife, hammer, shampoo, toycar.
        - Add distractor objects as specified in the task description.
        """
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.knife = self.add_actor("knife", "knife")
        self.hammer = self.add_actor("hammer", "hammer")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.toycar = self.add_actor("toycar", "toycar")
        distractor_list = ["calculator", "alarm-clock", "book", "shoe", "apple"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        - Pick and place the knife into the wooden_box.
        - Attempt to place the toycar into the wooden_box (wrong action).
        - Recover by placing the toycar on the table.
        - Pick and place the hammer into the wooden_box.
        - Pick and place the shampoo on the table.
        """
        # Step 1: Place knife into wooden_box
        success = self.pick_and_place(self.knife, self.wooden_box)
        print("Pick and place knife:", success)
        if not success:
            return self.info

        # Step 2: Wrong action - place toycar into wooden_box
        success = self.pick_and_place(self.toycar, self.wooden_box)
        print("Wrong placement of toycar:", success)

        # Step 3: Recovery - place toycar on the table
        success = self.pick_and_place(self.toycar, self.table)
        print("Recovery placement of toycar:", success)
        if not success:
            return self.info

        # Step 4: Place hammer into wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Pick and place hammer:", success)
        if not success:
            return self.info

        # Step 5: Place shampoo on the table
        success = self.pick_and_place(self.shampoo, self.table)
        print("Pick and place shampoo:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Sharp/heavy tools (knife, hammer) must be in the wooden_box.
        - Children's toys (toycar) and liquid personal-care items (shampoo) must be on the table.
        """
        if (self.check_on(self.knife, self.wooden_box) and
            self.check_on(self.hammer, self.wooden_box) and
            self.check_on(self.toycar, self.table) and
            self.check_on(self.shampoo, self.table)):
            return True
        return False
