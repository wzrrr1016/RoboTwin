# ====================== PROMPT =============================

BASIC_INFO = '''
In this environment, distance 1 indicates 1 meter long. Pose is representated as 7 dimention, [x, y, z, qw, qx, qy, qz].
For a 7-dimensional Pose object, you can use Pose.p to get the [x, y, z] coordinates and Pose.q to get the [qw, qx, qy, qz] quaternion orientation.
All functions which has parameter actor, and all of actor should be in the Actor object.
In the world coordinate system, the positive directions of the xyz coordinate axes are right, front, and upper respectively, so the direction vectors on the right, front,
and upper sides are [1,0,0], [0,1,0], [0,0,1] respectively. In the same way, we can get the unit vectors of the left side, back side and down side.
Each actor in the environment has one or more functional points, which are specific locations designed for interactions. 
Access functional points using actor.get_functional_point(point_id, return_type), where return_type can be "pose", "p", or "q".
'''

CODE_TEMPLATE = '''
from envs._base_task import Base_Task  
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class $TASK_NAME$(Imagine_Task):
    def load_actors(self):
        pass
        
    def play_once(self):
        pass
    
    def check_success(self):
    pass
'''

AVAILABLE_ENV_FUNCTION_LOAD_ACTORS = {
    "add_actor":
    "def def add_actor(self, object_type, object_name):\
        create an actor of an object (eg. plate, bowl...) to the environment.\
        Args:\
        object_type: The type of the object to be added, eg. plate \
        object_name: The name of the object to be added, eg. plate_0\
        return: actor",
    "add_distractor":
    "def add_distractor(self, object_list):\
        Args:\
        object_list: create distractor objects to the environment."
}

AVAILABLE_ENV_FUNCTION_PLAY_ONCE = {
    "pick_and_place":
    "def pick_and_place(self, object, container)\
        pick an object and place it in the container.\
        Args:\
        object: The object to be picked and placed\
        container: The container to be placed in\
        return success"
}

AVAILABLE_ENV_FUNCTION_CHECK_SUCCESS = {
    "check_grasp":
    "def check_grasp(self, object)\
        check if the object is grasped by the arm.\
        Args:\
        object: The object to be checked\
        return success",
    "check_on":
    "def check_on(self,object,container)\
        check if the object is on the container.\
        Args:\
        object: The object to be checked\
        container: The container to be checked\
        return success"
}

FUNCTION_EXAMPLE = '''
First you need to complete the load_actors function, which is used to load the actors into the environment. 
You can use the following functions to load actors:

add_actor: Add an actor to the environment.
add_distractor: Add distractor objects to the environment.

For example:
```python
    def load_actors(self):

        self.plate = self.add_actor("plate","plate")
        self.apple = self.add_actor("apple","apple")
        self.fruit = self.add_actor("fruit","fruit")
        self.bottle = self.add_actor("bottle","bottle")
        self.can = self.add_actor("can","can")
        distractor_list = ["bottle", "shampoo", "bread", "calculator"]
        self.add_distractors(distractor_list)
```

Next, you need to complete the play_once function, which is used to define the action of the robot arm. 

pick_and_place: Pick up an object and place it in the container.

For example:
```python
    def play_once(self):
        success = self.pick_and_place(self.apple, self.plate)
        print("pick place apple:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.bottle, self.plate)
        print("pick place bottle:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.can, self.plate)
        print("pick place can:", success)
        if not success:
            return self.info
```

Finally, you need to complete the check_success function, which is used to check the success of the action.

check_grasp: Check if the actor is grasped by the arm.
check_on: Check if the actor is on the container.

For example:
```python
    def check_success(self):
        if self.check_on(self.bottle, self.plate) and self.check_on(self.can, self.plate):
            return True
        return False
```

The complete code is as follow:

```python
class {task_name}(Imagine_Task):
    def load_actors(self):

        self.plate = self.add_actor("plate","plate")
        self.apple = self.add_actor("apple","apple")
        self.fruit = self.add_actor("fruit","fruit")
        self.bottle = self.add_actor("bottle","bottle")
        self.can = self.add_actor("can","can")

    def play_once(self):
        success = self.pick_and_place(self.bottle, self.plate)
        print("pick place bottle:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.can, self.plate)
        print("pick place can:", success)
        if not success:
            return self.info

    def check_success(self):
        if self.check_on(self.bottle, self.plate) and self.check_on(self.can, self.plate):
            return True
        return False
```
All the available object types are:

CONTAINERS:
    "plate", "tray", "wooden_box", "dustbin", "fluted_block", "shoe_box", "coaster",

OBJECTS able to pick:
    "hammer", "microphone", "bottle", "can", "cup", "cup_with_handle", "cup_without_handle", "pot-with-plant",
    "apple", "hamburg", "bread", "french_fries", "toycar", "tissue-box", "scanner", "drill", "screwdriver", "fork",
    "knife", "mug", "shoe", "book", "sand-clock", "alarm-clock", "mouse", "stapler", "shampoo", "bell", "dumbbell", "teanet",
    "red_block", "blue_block", "green_block", "yellow_block", "purple_block", "orange_block", "pink_block",

You can use the 'self.table' to get the table actor in the environment and you don't need to create a table in load_actor().
'''
