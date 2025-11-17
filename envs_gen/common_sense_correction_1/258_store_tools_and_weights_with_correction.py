from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 258_store_tools_and_weights_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add the required objects
        self.drill = self.add_actor("drill", "drill")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.stapler = self.add_actor("stapler", "stapler")
        self.bread = self.add_actor("bread", "bread")
        
        # Add distractors
        distractor_list = ["pot-with-plant", "alarm-clock", "book", "toycar", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Wrong action: Pick bread and place into wooden_box
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("Wrong pick place bread:", success)
        
        # If successful, need to recover by putting it back on the table
        if success:
            success_recovery = self.pick_and_place(self.bread, self.table)
            print("Recovery bread:", success_recovery)
            if not success_recovery:
                return self.info
        
        # Correct actions: Put tools and heavy items into the wooden_box
        success_drill = self.pick_and_place(self.drill, self.wooden_box)
        print("Pick place drill:", success_drill)
        if not success_drill:
            return self.info
            
        success_dumbbell = self.pick_and_place(self.dumbbell, self.wooden_box)
        print("Pick place dumbbell:", success_dumbbell)
        if not success_dumbbell:
            return self.info
            
        success_stapler = self.pick_and_place(self.stapler, self.wooden_box)
        print("Pick place stapler:", success_stapler)
        if not success_stapler:
            return self.info
            
        return self.info

    def check_success(self):
        # Check if all required items are in the wooden_box
        # and bread is not in the wooden_box
        if (self.check_on(self.drill, self.wooden_box) and
            self.check_on(self.dumbbell, self.wooden_box) and
            self.check_on(self.stapler, self.wooden_box) and
            not self.check_on(self.bread, self.wooden_box)):
            return True
        return False
