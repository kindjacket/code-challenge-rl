
from spatial_utils import move_to_absolute
from state import State

state = State()
vehicle_destination_map = {}
for vehicle in state.vehicles:
    vehicle_destination_map[vehicle.name] = None

for i in range(1000):
    move_to_absolute(state.vehicles[0],state.buildings[6])
    state.loop()
