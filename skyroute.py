from graph_search import bfs, dfs
from vc_metro import vc_metro
from vc_landmarks import vc_landmarks
from landmark_choices import landmark_choices

employee_ids = ['11111', '22222', '33333', '44444', '55555', '66666', '77777', '88888', '99999', '00000']
landmark_string = ''
stations_under_construction = []
for letter, landmark in landmark_choices.items():
  landmark_string += '{0} - {1}\n'.format(letter, landmark)

def greet():
  print('Hi there and welcome to SkyRoute!')
  print('We\'ll help you find the shortest route between the following Vancouver landmarks:\n' + landmark_string)

def skyroute():
  greet()
  new_route()
  goodbye()

def set_start_and_end(start_point, end_point):
  if start_point:
    change_point = input("What would you like to change? You can enter 'o' for 'origin', 'd' for 'destination', or 'b' for 'both': ")
    if change_point == 'b':
      start_point = get_start()
      end_point = get_end()
    elif change_point == 'o':
      start_point = get_start()
    elif change_point == 'd':
      end_point = get_end()
    else:
      print("Oops, that isn't 'o', 'd', or 'b'...")
      set_start_and_end(start_point, end_point)
  else:
    start_point = get_start()
    end_point = get_end()
  return start_point, end_point

def get_start():
  start_point_letter = input('Where are you coming from? Type in the corresponding letter: ')
  if start_point_letter in landmark_choices:
    start_point = landmark_choices[start_point_letter]
    return start_point
  else:
    print("Sorry, that's not a landmark we have data on. Let's try this again...")
    return get_start()

def get_end():
  end_point_letter = input('Ok, where are you headed? Type in the corresponding letter: ')
  if end_point_letter in landmark_choices:
    end_point = landmark_choices[end_point_letter]
    return end_point
  else:
    print("Sorry, that's not a landmark we have data on. Let's try this again...")
    return get_end()

##print(set_start_and_end(None, None))

def new_route(start_point = None, end_point = None):
  start_point, end_point = set_start_and_end(start_point, end_point)
  if start_point == end_point:
    print("That's the same place, no traveling needed!")
  else:
    shortest_route = get_route(start_point, end_point)
    if shortest_route is not None: 
      shortest_route_string = '\n'.join(shortest_route)
      print("The shortest metro route from {0} to {1} is:\n{2}".format(start_point, end_point, shortest_route_string))
    else:
      print("Unfortunately, there is currently no path between {0} and {1} due to maintenance.".format(start_point, end_point))
  again = input('Would you like to see another route? Enter y/n: ')
  if again == 'y':
    show_landmarks()
    new_route(start_point, end_point)

def show_landmarks():
  see_landmarks = input('Would you like to see the list of landmarks again? Enter y/n: ')
  if see_landmarks == 'y':
    print(landmark_string)

def goodbye():
  print('Thanks for using SkyRoute!')

def get_route(start_point, end_point):
  start_stations = vc_landmarks[start_point]
  end_stations = vc_landmarks[end_point]
  routes = []
  for start_station in start_stations:
    for end_station in end_stations:
      metro_system = get_active_stations() if stations_under_construction else vc_metro
      if len(stations_under_construction) > 0:
        possible_route = dfs(metro_system, start_station, end_station)
        if possible_route is None:
          continue
      route = bfs(metro_system, start_station, end_station)
      if route:
        routes.append(route)
  if len(routes) > 0:
    shortest_route = min(routes, key = len)
    return shortest_route
  else:
    return None

def get_active_stations():
  updated_metro = vc_metro
  for station_under_construction in stations_under_construction:
    for current_station, neighboring_stations in vc_metro.items():
      if current_station != station_under_construction:
        updated_metro[current_station] -= set(stations_under_construction)
      else:
        updated_metro[current_station] = set([])
  return updated_metro

def employee_update():
  is_employee = input('Are you an employee looking to update a station under construction? Enter y/n: ')
  break_flag = False
  while break_flag == False:
    if is_employee == 'y':
      id = str(input('Please enter your employee id: '))
    else:
      return
    if id in employee_ids:
      while True:
        station = input('Please enter the station that is under construction: ')
        if station not in stations_under_construction and station in vc_metro.keys():
          stations_under_construction.append(station)
        elif station not in vc_metro.keys():
          print('This station is not in the Vancouver system')
        again = input("Would you like to enter another station? Enter y/n: ")
        if again == 'n':
          print('Thanks for the update!')
          break_flag = True
          break
    else:
      try_again = input('This is not a valid employee id. Do you still want to update a station under construction? Enter y/n: ')
      if try_again != 'y':
        break

##print(get_route('Marine Building', 'Vancouver Lookout'))
##stations_under_construction.extend(['Burrard', 'Waterfront'])
##print(stations_under_construction)
employee_update()
skyroute()
##print(get_active_stations())