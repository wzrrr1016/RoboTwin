from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 26_repair_tool_disposal_correction(Imagine_Task):
    def load_actors(self):
        # Load the dustbin as a container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        # Load the repair tools
        self.hammer = self.add_actor("hammer", "hammer")
        self.drill = self.add_actor("drill", "drill")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        # Load the pot-with-plant (optional, but included in the scene)
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

    def play_once(self):
        # Step 1: Pick hammer and place in dustbin
        success = self.pick_and_place(self.hammer, self.dustbin)
        print("pick place hammer:", success)
        if not success:
            return self.info

        # Step 2: Pick drill and place in dustbin
        success = self.pick_and_place(self.drill, self.dustbin)
        print("pick place drill:", success)
        if not success:
            return self.info

        # Step 3: Pick dumbbell and place in dustbin (wrong action)
        success = self.pick_and_place(self.dumbbell, self.dustbin)
        print("pick place dumbbell:", success)
        if not success:
            return self.info

        # Step 4: Pick dumbbell from dustbin and place on table (recovery)
        success = self.pick_and_place(self.dumbbell, self.table)
        print("pick place dumbbell on table:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if hammer and drill are in the dustbin
        hammer_on_dustbin = self.check_on(self.hammer, self.dustbin)
        drill_on_dustbin = self.check_on(self.drill, self.dustbin)
        # Check if dumbbell is on the table
        dumbbell_on_table = self.check_on(self.dumbbell, self.table)

        return hammer_on_dustbin and drill_on_dustbin and dumbbell_on_table
