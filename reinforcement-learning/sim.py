from action_space import get_action_space
from spatial_utils import move_to_absolute
from state import State

state = State()

# vehicle_destination_map = {}
# for vehicle in state.vehicles:
#     vehicle_destination_map[vehicle.name] = None


for i in range(1000):
    action_space = get_action_space(state)
    state.loop()
