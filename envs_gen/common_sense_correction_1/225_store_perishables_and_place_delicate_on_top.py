from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 225_store_perishables_and_place_delicate_on_top(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Containers: wooden_box
        - Perishable edible foods: apple, french_fries
        - Delicate decorative items: sand-clock
        - Sharp tools: knife
        - Distractors: calculator, shoe, dumbbell, toycar, markpen
        """
        # Add the wooden box as a container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add perishable edible foods
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Add delicate decorative item and sharp tool
        self.sand_clock = self.add_actor("sand-clock", "sand_clock")
        self.knife = self.add_actor("knife", "knife")
        
        # Add distractors to the environment
        distractor_list = ["calculator", "shoe", "dumbbell", "toycar", "markpen"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the simulation environment.
        1. Place apple into wooden_box
        2. Place french_fries into wooden_box
        3. Place knife into wooden_box (wrong action)
        4. Place knife onto wooden_box (recovery action)
        5. Place sand-clock onto wooden_box
        """
        # Place apple into wooden_box
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("Place apple:", success)
        if not success:
            return self.info
        
        # Place french_fries into wooden_box
        success = self.pick_and_place(self.french_fries, self.wooden_box)
        print("Place french fries:", success)
        if not success:
            return self.info
        
        # Wrong action: place knife into wooden_box
        success = self.pick_and_place(self.knife, self.wooden_box)
        print("Place knife (wrong):", success)
        if not success:
            return self.info
        
        # Recovery action: place knife onto wooden_box
        success = self.pick_and_place(self.knife, self.wooden_box)
        print("Place knife (recovery):", success)
        if not success:
            return self.info
        
        # Place sand-clock onto wooden_box
        success = self.pick_and_place(self.sand_clock, self.wooden_box)
        print("Place sand-clock:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully.
        - Perishable edible foods (apple, french_fries) are in the wooden_box
        - Delicate decorative items (sand-clock) and sharp tools (knife) are on the wooden_box
        """
        # Check if apple and french_fries are in the wooden_box
        apple_in = self.check_on(self.apple, self.wooden_box)
        fries_in = self.check_on(self.french_fries, self.wooden_box)
        
        # Check if knife and sand-clock are on the wooden_box
        knife_on = self.check_on(self.knife, self.wooden_box)
        sand_on = self.check_on(self.sand_clock, self.wooden_box)
        
        return apple_in and fries_in and knife_on and sand_on
