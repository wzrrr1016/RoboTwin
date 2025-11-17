from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 419_drink_and_personalcare_organization_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the environment.
        Containers: coaster, fluted_block
        Objects: can, shampoo, microphone, mouse, tissue-box
        Distractors: baguette, apple, shoe, book, pot-with-plant
        """
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects to be manipulated
        self.can = self.add_actor("can", "can")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.microphone = self.add_actor("microphone", "microphone")
        self.mouse = self.add_actor("mouse", "mouse")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractors to the environment
        distractor_list = ["baguette", "apple", "shoe", "book", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions to complete the task.
        Actions:
        1. Place can on coaster
        2. Place shampoo on coaster (wrong placement)
        3. Move shampoo from coaster to fluted_block (recovery)
        4. Place microphone on fluted_block
        5. Place mouse on fluted_block
        6. Place tissue-box on fluted_block
        """
        # Place can on coaster
        success = self.pick_and_place(self.can, self.coaster)
        print("Place can on coaster:", success)
        if not success:
            return self.info

        # Place shampoo on coaster (wrong placement)
        success = self.pick_and_place(self.shampoo, self.coaster)
        print("Place shampoo on coaster (wrong):", success)
        if not success:
            return self.info

        # Move shampoo to fluted_block (recovery)
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Move shampoo to fluted_block:", success)
        if not success:
            return self.info

        # Place microphone on fluted_block
        success = self.pick_and_place(self.microphone, self.fluted_block)
        print("Place microphone on fluted_block:", success)
        if not success:
            return self.info

        # Place mouse on fluted_block
        success = self.pick_and_place(self.mouse, self.fluted_block)
        print("Place mouse on fluted_block:", success)
        if not success:
            return self.info

        # Place tissue-box on fluted_block
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Place tissue-box on fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully by checking:
        - Can is on coaster
        - Shampoo, microphone, mouse, and tissue-box are on fluted_block
        """
        can_on_coaster = self.check_on(self.can, self.coaster)
        shampoo_on_fluted = self.check_on(self.shampoo, self.fluted_block)
        mic_on_fluted = self.check_on(self.microphone, self.fluted_block)
        mouse_on_fluted = self.check_on(self.mouse, self.fluted_block)
        tissue_on_fluted = self.check_on(self.tissue_box, self.fluted_block)
        
        return can_on_coaster and shampoo_on_fluted and mic_on_fluted and mouse_on_fluted and tissue_on_fluted
