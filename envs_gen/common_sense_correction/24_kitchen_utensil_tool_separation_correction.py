from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 24_kitchen_utensil_tool_separation_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        Adds kitchen utensils, tools, and distractors as specified in the task.
        """
        # Add containers to the environment
        self.tray = self.add_actor("tray", "tray")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add kitchen utensils and tools
        self.fork = self.add_actor("fork", "fork")
        self.knife = self.add_actor("knife", "knife")
        self.hammer = self.add_actor("hammer", "hammer")
        self.drill = self.add_actor("drill", "drill")
        
        # Add distractor objects to the environment
        distractor_list = [
            "calculator", "pet-collar", "table-tennis", 
            "alarm-clock", "sand-clock", "dumbbell"
        ]
        self.add_distractors(distractor_list)
        
        # Final check to ensure all actors are properly placed
        self.check_scene()

    def play_once(self):
        """
        Execute the robot's actions to complete the task:
        - Place kitchen utensils in the tray
        - Place tools in the shoe_box
        - Handle a wrong placement and recovery
        """
        # Place fork in tray
        success = self.pick_and_place(self.fork, self.tray)
        print("Pick place fork:", success)
        if not success:
            return self.info

        # Place knife in tray
        success = self.pick_and_place(self.knife, self.tray)
        print("Pick place knife:", success)
        if not success:
            return self.info

        # Wrong placement: place hammer in tray (should be in shoe_box)
        success = self.pick_and_place(self.hammer, self.tray)
        print("Pick place hammer (wrong):", success)
        if not success:
            return self.info

        # Recovery: move hammer from tray to shoe_box
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Recover hammer to shoe_box:", success)
        if not success:
            return self.info

        # Place drill in shoe_box
        success = self.pick_and_place(self.drill, self.shoe_box)
        print("Pick place drill:", success)
        if not success:
            return self.info

        # Mark the end of the task
        self.add_end()
        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - Kitchen utensils (fork, knife) are in the tray
        - Tools (hammer, drill) are in the shoe_box
        """
        # Check if all objects are in their correct containers
        if (self.check_on(self.fork, self.tray) and
            self.check_on(self.knife, self.tray) and
            self.check_on(self.hammer, self.shoe_box) and
            self.check_on(self.drill, self.shoe_box)):
            return True
        return False
