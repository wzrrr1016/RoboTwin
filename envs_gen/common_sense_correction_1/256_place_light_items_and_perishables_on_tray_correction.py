from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 256_place_light_items_and_perishables_on_tray_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment."""
        self.tray = self.add_actor("tray", "tray")
        self.toycar = self.add_actor("toycar", "toycar")
        self.bread = self.add_actor("bread", "bread")
        self.bottle = self.add_actor("bottle", "bottle")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        
        # Add distractor objects
        distractor_list = ['screwdriver', 'pot-with-plant', 'shoe', 'microphone', 'stapler']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions for the task."""
        # 1. Pick toycar and place it onto tray
        success = self.pick_and_place(self.toycar, self.tray)
        print("Pick toycar:", success)
        if not success:
            return self.info

        # 2. Pick bottle and place it onto tray (wrong action)
        success = self.pick_and_place(self.bottle, self.tray)
        print("Pick bottle (wrong):", success)
        if not success:
            return self.info

        # 3. Recovery: Pick bottle from tray and place it back on the table
        success = self.pick_and_place(self.bottle, self.table)
        print("Recover bottle:", success)
        if not success:
            return self.info

        # 4. Pick bread and place it onto tray
        success = self.pick_and_place(self.bread, self.tray)
        print("Pick bread:", success)
        if not success:
            return self.info

        # 5. Pick dumbbell and place it on the table
        success = self.pick_and_place(self.dumbbell, self.table)
        print("Pick dumbbell:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully."""
        # Task success condition: toycar and bread must be on the tray
        return self.check_on(self.toycar, self.tray) and self.check_on(self.bread, self.tray)
