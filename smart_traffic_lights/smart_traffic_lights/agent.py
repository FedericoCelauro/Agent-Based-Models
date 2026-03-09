import mesa
import enum


class Direction(enum.Enum):
    EAST = (1, 0)
    NORTH = (0, 1)


class LightState(enum.Enum):
    RED = 0
    GREEN = 1


class TrafficLightAgent(mesa.Agent):
    """
    An agent representing a single traffic light.

    Attributes:
        state (LightState): The current state of the light (RED or GREEN).
        direction (Direction): The flow of traffic this light controls.
    """

    def __init__(self, model: mesa.Model, state: LightState, direction: Direction):
        super().__init__(model)
        self.state = state
        self.direction = direction

    def step(self):
        # Traffic lights are passive; the Controller changes their state.
        pass


class CarAgent(mesa.Agent):
    """
    An agent representing a car in the grid.

    Attributes:
        direction (Direction): The direction the car is traveling.
        wait_time (int): Accumulator for time steps spent not moving.
    """

    def __init__(self, model: mesa.Model, direction: Direction):
        super().__init__(model)
        self.direction = direction
        self.total_wait_time = 0
        self.red_light_wait_time = 0

    def step(self):
        """
        Determines if the car can move forward based on obstacles and lights.
        """

        # Calculate the next coordinate based on direction
        next_x = (self.pos[0] + self.direction.value[0]) % self.model.grid.width
        next_y = (self.pos[1] + self.direction.value[1]) % self.model.grid.height
        next_pos = (next_x, next_y)

        can_move = True
        stopped_by_red_light = False
        cell_contents = self.model.grid.get_cell_list_contents([next_pos])

        for obj in cell_contents:
            if isinstance(obj, CarAgent):
                can_move = False
                break
            elif isinstance(obj, TrafficLightAgent):
                # Only stop if the light controls our direction and is red
                if obj.direction == self.direction and obj.state == LightState.RED:
                    can_move = False
                    stopped_by_red_light = True
                    break

        if can_move:
            self.model.grid.move_agent(self, next_pos)
        else:
            self.total_wait_time += 1
            if stopped_by_red_light:
                self.red_light_wait_time += 1
