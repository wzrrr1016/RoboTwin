from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 88_dispose_perishables_and_reuse_tools_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required actors in the simulation environment."""
        # Add the dustbin container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add the main objects to be manipulated
        self.toycar = self.add_actor("toycar", "toycar")
        self.apple = self.add_actor("apple", "apple")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.drill = self.add_actor("drill", "drill")
        
        # Add distractor objects to the environment
        distractor_list = ['pot-with-plant', 'alarm-clock', 'small-speaker', 'shoe', 'book']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions to complete the task."""
        # 1. Place toycar (disposable toy) into dustbin
        success = self.pick_and_place(self.toycar, self.dustbin)
        print("Place toycar:", success)
        if not success:
            return self.info

        # 2. Wrong action: Place screwdriver (durable tool) into dustbin
        success = self.pick_and_place(self.screwdriver, self.dustbin)
        print("Wrong place screwdriver:", success)
        if not success:
            return self.info

        # 3. Recovery: Pick screwdriver from dustbin and place on top
        success = self.pick_and_place(self.screwdriver, self.dustbin)
        print("Recover screwdriver:", success)
        if not success:
            return self.info

        # 4. Place apple (perishable food) into dustbin
        success = self.pick_and_place(self.apple, self.dustbin)
        print("Place apple:", success)
        if not success:
            return self.info

        # 5. Place drill (durable tool) on top of dustbin
        success = self.pick_and_place(self.drill, self.dustbin)
        print("Place drill:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully."""
        # Check if disposable toy (toycar) is inside dustbin
        toycar_in = not self.check_on(self.toycar, self.dustbin)
        
        # Check if perishable food (apple) is inside dustbin
        apple_in = not self.check_on(self.apple, self.dustbin)
        
        # Check if durable tool (screwdriver) is on top of dustbin
        screwdriver_on = self.check_on(self.screwdriver, self.dustbin)
        
        # Check if durable tool (drill) is on top of dustbin
        drill_on = self.check_on(self.drill, self.dustbin)
        
        # Return True only if all conditions are met
        return toycar_in and apple_in and screwdriver_on and drill_on
