from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 195_tray_perishables_and_drink_containers_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Tray as the container
        - Yellow and blue blocks as toy blocks
        - Bread as a soft perishable food
        - Bottle as a portable drink container
        - Distractors to add complexity to the environment
        """
        # Add the tray container
        self.tray = self.add_actor("tray", "tray")
        
        # Add toy blocks
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        
        # Add soft perishable food and drink container
        self.bread = self.add_actor("bread", "bread")
        self.bottle = self.add_actor("bottle", "bottle")
        
        # Add distractors to the environment
        distractor_list = ['calculator', 'dumbbell', 'shoe', 'stapler', 'alarm-clock']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the simulation:
        1. Wrongly place yellow_block on tray
        2. Recover by moving yellow_block to blue_block
        3. Place bread and bottle on tray
        """
        # 1. Wrong action: Place yellow_block on tray (should be avoided)
        success = self.pick_and_place(self.yellow_block, self.tray)
        print("Pick yellow_block and place into tray (wrong):", success)
        if not success:
            return self.info

        # 2. Recovery action: Move yellow_block from tray to blue_block
        success = self.pick_and_place(self.yellow_block, self.blue_block)
        print("Recovery: Pick yellow_block and place onto blue_block:", success)
        if not success:
            return self.info

        # 3. Place bread on tray (soft perishable food)
        success = self.pick_and_place(self.bread, self.tray)
        print("Pick bread and place into tray:", success)
        if not success:
            return self.info

        # 4. Place bottle on tray (portable drink container)
        success = self.pick_and_place(self.bottle, self.tray)
        print("Pick bottle and place into tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - Bread and bottle are on the tray
        - Yellow_block and blue_block are NOT on the tray
        """
        # Check if bread and bottle are on the tray
        if not (self.check_on(self.bread, self.tray) and self.check_on(self.bottle, self.tray)):
            return False

        # Ensure solid toy blocks are NOT on the tray
        if self.check_on(self.yellow_block, self.tray):
            return False
        if self.check_on(self.blue_block, self.tray):
            return False

        return True
