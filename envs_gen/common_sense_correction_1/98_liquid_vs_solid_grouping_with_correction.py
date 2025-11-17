from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 98_liquid_vs_solid_grouping_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        Containers: coaster and tray
        Objects: can, shampoo, red_block, blue_block, book
        Distractors: calculator, hammer, alarm-clock, microphone, shoe
        """
        # Add containers to the environment
        self.coaster = self.add_actor("coaster", "coaster")
        self.tray = self.add_actor("tray", "tray")
        
        # Add task-specific objects
        self.can = self.add_actor("can", "can")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.red_block = self.add_actor("red_block", "red_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.book = self.add_actor("book", "book")
        
        # Add distractor objects
        distractor_list = ["calculator", "hammer", "alarm-clock", "microphone", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions to complete the task.
        The task includes a recovery step for the shampoo placement.
        """
        # 1. Place can on coaster (beverage container)
        success = self.pick_and_place(self.can, self.coaster)
        print("Place can on coaster:", success)
        if not success:
            return self.info

        # 2. Place shampoo on tray (wrong action - personal care container)
        success = self.pick_and_place(self.shampoo, self.tray)
        print("Place shampoo on tray (wrong):", success)
        if not success:
            return self.info

        # 3. Recover shampoo to coaster (correct placement)
        success = self.pick_and_place(self.shampoo, self.coaster)
        print("Recover shampoo to coaster:", success)
        if not success:
            return self.info

        # 4. Place red_block on tray (solid square toy)
        success = self.pick_and_place(self.red_block, self.tray)
        print("Place red_block on tray:", success)
        if not success:
            return self.info

        # 5. Place blue_block on tray (solid square toy)
        success = self.pick_and_place(self.blue_block, self.tray)
        print("Place blue_block on tray:", success)
        if not success:
            return self.info

        # 6. Place book on tray (paper-based reading material)
        success = self.pick_and_place(self.book, self.tray)
        print("Place book on tray:", success)
        if not success:
            return self.info

        return self.info  # Return final state if all actions succeed

    def check_success(self):
        """
        Verify if all objects are in their correct final positions.
        Returns True if the task is successfully completed.
        """
        # Check if all objects are in their correct containers
        if (self.check_on(self.can, self.coaster) and
            self.check_on(self.shampoo, self.coaster) and
            self.check_on(self.red_block, self.tray) and
            self.check_on(self.blue_block, self.tray) and
            self.check_on(self.book, self.tray)):
            return True
        return False
