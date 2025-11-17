from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 243_discard_tools_with_recovery(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Containers: dustbin
        - Objects: toycar, book, screwdriver, stapler
        - Distractors: apple, baguette, pot-with-plant, chips-tub, alarm-clock
        """
        # Add the dustbin container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add target objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.book = self.add_actor("book", "book")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.stapler = self.add_actor("stapler", "stapler")
        
        # Add distractor objects
        distractor_list = ["apple", "baguette", "pot-with-plant", "chips-tub", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in sequence:
        1. Place screwdriver in dustbin
        2. Place stapler in dustbin
        3. (Wrong) Place toycar in dustbin
        4. (Recovery) Move toycar from dustbin to book
        """
        # Place metal tools in dustbin
        success = self.pick_and_place(self.screwdriver, self.dustbin)
        print("pick place screwdriver:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.stapler, self.dustbin)
        print("pick place stapler:", success)
        if not success:
            return self.info
            
        # Wrong action - toycar in dustbin
        success = self.pick_and_place(self.toycar, self.dustbin)
        print("pick place toycar (wrong):", success)
        if not success:
            return self.info
            
        # Recovery action - move toycar to book
        success = self.pick_and_place(self.toycar, self.book)
        print("pick place toycar (recovery):", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - Screwdriver and stapler are in dustbin
        - Toycar is on book (not in dustbin)
        """
        return (
            self.check_on(self.screwdriver, self.dustbin) and
            self.check_on(self.stapler, self.dustbin) and
            self.check_on(self.toycar, self.book)
        )
