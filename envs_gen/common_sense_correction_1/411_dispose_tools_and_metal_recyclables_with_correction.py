from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 411_dispose_tools_and_metal_recyclables_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the dustbin container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add the relevant objects
        self.mug = self.add_actor("mug", "mug")
        self.can = self.add_actor("can", "can")
        self.drill = self.add_actor("drill", "drill")
        self.hammer = self.add_actor("hammer", "hammer")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add the specified distractors
        distractor_list = ['pet-collar', 'apple', 'book', 'tissue-box', 'alarm-clock']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Wrong action - pick mug and place into dustbin
        success = self.pick_and_place(self.mug, self.dustbin)
        print("Pick mug into dustbin (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - pick mug from dustbin and place on table
        success = self.pick_and_place(self.mug, self.table)
        print("Recover mug to table:", success)
        if not success:
            return self.info

        # Step 3: Pick can (recyclable metal drink container) into dustbin
        success = self.pick_and_place(self.can, self.dustbin)
        print("Pick can into dustbin:", success)
        if not success:
            return self.info

        # Step 4: Pick drill (heavy tool) into dustbin
        success = self.pick_and_place(self.drill, self.dustbin)
        print("Pick drill into dustbin:", success)
        if not success:
            return self.info

        # Step 5: Pick hammer (heavy tool) into dustbin
        success = self.pick_and_place(self.hammer, self.dustbin)
        print("Pick hammer into dustbin:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        # Verify that the correct items are in the dustbin
        can_in_dustbin = self.check_on(self.can, self.dustbin)
        drill_in_dustbin = self.check_on(self.drill, self.dustbin)
        hammer_in_dustbin = self.check_on(self.hammer, self.dustbin)
        
        # Verify that the mug is not in the dustbin (was recovered)
        mug_not_in_dustbin = not self.check_on(self.mug, self.dustbin)
        
        return can_in_dustbin and drill_in_dustbin and hammer_in_dustbin and mug_not_in_dustbin
