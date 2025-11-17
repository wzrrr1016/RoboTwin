from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 22_store_heavy_and_dangerous_items_with_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the simulation environment."""
        # Add the wooden box container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add the main objects
        self.drill = self.add_actor("drill", "drill")
        self.knife = self.add_actor("knife", "knife")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.shoe = self.add_actor("shoe", "shoe")
        
        # Add distractor objects
        distractor_list = ["calculator", "book", "toycar", "tissue-box", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions for the task."""
        # 1. Place drill into wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("Place drill:", success)
        if not success:
            return self.info

        # 2. Place shoe into wooden_box (wrong action)
        success = self.pick_and_place(self.shoe, self.wooden_box)
        print("Place shoe (wrong):", success)
        if not success:
            return self.info

        # 3. Recover shoe by placing it on wooden_box (not inside)
        success = self.pick_and_place(self.shoe, self.wooden_box)
        print("Recover shoe:", success)
        if not success:
            return self.info

        # 4. Place knife into wooden_box
        success = self.pick_and_place(self.knife, self.wooden_box)
        print("Place knife:", success)
        if not success:
            return self.info

        # 5. Place dumbbell into wooden_box
        success = self.pick_and_place(self.dumbbell, self.wooden_box)
        print("Place dumbbell:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully."""
        # Check that all heavy/dangerous items are in the box
        # and the wearable item (shoe) is on the box (not inside)
        return (
            self.check_on(self.drill, self.wooden_box) and
            self.check_on(self.knife, self.wooden_box) and
            self.check_on(self.dumbbell, self.wooden_box) and
            self.check_on(self.shoe, self.wooden_box)
        )
