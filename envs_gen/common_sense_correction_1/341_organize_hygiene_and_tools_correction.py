from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 341_organize_hygiene_and_tools_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Add the fluted_block as the organizer container.
        - Add the required objects: shampoo, tissue-box, stapler, and screwdriver.
        - Add distractor objects to the environment.
        """
        # Add the organizer container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add personal-care and disposable paper items
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add metal hand tools
        self.stapler = self.add_actor("stapler", "stapler")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        
        # Add distractor objects
        distractors = ["chips-tub", "jam-jar", "shoe", "small-speaker", "red_block"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        - Place personal-care and disposable paper items into the organizer.
        - Place metal hand tools on top of the organizer.
        """
        # Place shampoo into the organizer
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Shampoo placed:", success)
        if not success:
            return self.info

        # Place tissue-box into the organizer
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Tissue box placed:", success)
        if not success:
            return self.info

        # Place stapler on top of the organizer
        success = self.pick_and_place(self.stapler, self.fluted_block)
        print("Stapler placed:", success)
        if not success:
            return self.info

        # Place screwdriver on top of the organizer
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Screwdriver placed:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully.
        - Check if shampoo and tissue-box are in the organizer.
        - Check if stapler and screwdriver are on top of the organizer.
        """
        if (self.check_on(self.shampoo, self.fluted_block) and
            self.check_on(self.tissue_box, self.fluted_block) and
            self.check_on(self.stapler, self.fluted_block) and
            self.check_on(self.screwdriver, self.fluted_block)):
            return True
        return False
