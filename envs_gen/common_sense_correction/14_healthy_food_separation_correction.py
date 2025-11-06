from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 14_healthy_food_separation_correction(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.tray = self.add_actor("tray", "tray")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Load food objects
        self.bread = self.add_actor("bread", "bread")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Load non-food object (not part of the task)
        self.stapler = self.add_actor("stapler", "stapler")

    def play_once(self):
        # Step 1: Place bread into dustbin (wrong action)
        success = self.pick_and_place(self.bread, self.dustbin)
        print("pick place bread into dustbin:", success)
        if not success:
            return self.info
        
        # Step 2: Recovery: pick bread from dustbin and place into tray
        success = self.pick_and_place(self.bread, self.tray)
        print("pick place bread into tray:", success)
        if not success:
            return self.info
        
        # Step 3: Place hamburg into dustbin (unhealthy)
        success = self.pick_and_place(self.hamburg, self.dustbin)
        print("pick place hamburg into dustbin:", success)
        if not success:
            return self.info
        
        # Step 4: Place french fries into dustbin (unhealthy)
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("pick place french fries into dustbin:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if bread is on tray (healthy)
        bread_on_tray = self.check_on(self.bread, self.tray)
        # Check if hamburg is on dustbin (unhealthy)
        hamburg_on_dustbin = self.check_on(self.hamburg, self.dustbin)
        # Check if french fries is on dustbin (unhealthy)
        french_fries_on_dustbin = self.check_on(self.french_fries, self.dustbin)
        
        return bread_on_tray and hamburg_on_dustbin and french_fries_on_dustbin
