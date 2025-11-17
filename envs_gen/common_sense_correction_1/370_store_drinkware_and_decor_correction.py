from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 370_store_drinkware_and_decor_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the shoe box container, target objects, and distractors.
        """
        # Add the shoe box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects that need to be placed
        self.mug = self.add_actor("mug", "mug")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        
        # Add distractors to the environment
        distractor_list = ["calculator", "screwdriver", "toycar", "markpen", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions to complete the task.
        This includes both correct placements and error recovery.
        """
        # Place decorative/drinking items into the shoe box
        success = self.pick_and_place(self.french_fries, self.shoe_box)
        print("Place french_fries:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.mug, self.shoe_box)
        print("Place mug:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.sand_clock, self.shoe_box)
        print("Place sand-clock:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.cup_without_handle, self.shoe_box)
        print("Place cup_without_handle:", success)
        if not success:
            return self.info
        
        # Wrong placement (hamburg into shoe box) followed by recovery
        success = self.pick_and_place(self.hamburg, self.shoe_box)
        print("Place hamburg (wrong):", success)
        if not success:
            return self.info
        
        # Recovery: Place hamburg on top of the shoe box
        success = self.pick_and_place(self.hamburg, self.shoe_box)
        print("Recover hamburg:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully by checking:
        1. Decorative/drinking items are in the shoe box
        2. Hot foods are on top of the shoe box
        """
        # Check if all decorative/drinking items are in the shoe box
        # and hot foods are on top of the shoe box
        if (self.check_on(self.mug, self.shoe_box) and
            self.check_on(self.sand_clock, self.shoe_box) and
            self.check_on(self.cup_without_handle, self.shoe_box) and
            self.check_on(self.french_fries, self.shoe_box) and
            self.check_on(self.hamburg, self.shoe_box)):
            return True
        return False
