from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 50_drink_related_item_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Create the coaster container
        - Add objects: teanet, apple, bread, bell
        - Add distractor objects
        - Check if the scene is properly set up
        """
        # Create the coaster container
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add objects used in the task
        self.teanet = self.add_actor("teanet", "teanet")
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.bell = self.add_actor("bell", "bell")
        
        # Add distractor objects from the task description
        distractor_list = ["calculator", "pet-collar", "table-tennis", "sand-clock", "shoe", "book"]
        self.add_distractors(distractor_list)
        
        # Final scene validation
        self.check_scene()

    def play_once(self):
        """
        Execute the robot's actions in sequence:
        1. Place teanet on coaster (correct)
        2. Place apple on coaster (wrong action)
        3. Recover apple by placing it on table
        4. Place bread on table
        5. Place bell on table
        """
        # Place teanet on coaster
        success = self.pick_and_place(self.teanet, self.coaster)
        print("Place teanet on coaster:", success)
        if not success:
            return self.info
            
        # Wrong action: place apple on coaster
        success = self.pick_and_place(self.apple, self.coaster)
        print("Place apple on coaster (wrong):", success)
        if not success:
            return self.info
            
        # Recovery: move apple to table
        success = self.pick_and_place(self.apple, self.table)
        print("Recover apple to table:", success)
        if not success:
            return self.info
            
        # Place bread on table
        success = self.pick_and_place(self.bread, self.table)
        print("Place bread on table:", success)
        if not success:
            return self.info
            
        # Place bell on table
        success = self.pick_and_place(self.bell, self.table)
        print("Place bell on table:", success)
        if not success:
            return self.info
            
        # Mark task completion
        self.add_end()
        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - Only the teanet should be on the coaster
        - All other items should not be on the coaster
        """
        # Check if teanet is on coaster
        teanet_on_coaster = self.check_on(self.teanet, self.coaster)
        
        # Check if other items are not on coaster
        apple_not_on_coaster = not self.check_on(self.apple, self.coaster)
        bread_not_on_coaster = not self.check_on(self.bread, self.coaster)
        bell_not_on_coaster = not self.check_on(self.bell, self.coaster)
        
        # Return success if all conditions are met
        return (teanet_on_coaster and 
                apple_not_on_coaster and 
                bread_not_on_coaster and 
                bell_not_on_coaster)
