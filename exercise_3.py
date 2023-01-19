from AStar import AStar
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

key = {'L': (-1, 0), 'R': (1, 0), 'U': (0, -1), 'D': (0, 1)}

def plot_route(row):
  if pd.isna(row['route']):  # strand 103 has no route
    return [(row['start_x'], row['start_y'])]
  points = []
  curr = np.array([row['start_x'], row['start_y']])
  for x in row['route']:
    points.append(tuple(curr))
    curr += key.get(x, (0, 0))
  return points

def read_and_cleanup_data():
  """
    Reads and cleans up the neural strand data.
    Traverses all routes in strands to get a list of absolute coordinates.

    Returns:  DataFrame with two columns, indexed by strand number
                object: 'X', 'S', 'F', '.' for Wall, Start, Finish, passable path
                coordinate: (x, y) an absolute coordinate
  """
  # Read the file, create start and route columns from the given data
  df = pd.read_table('challenge_3', sep=' ', names=['start', 'route'])
  # Remove commas from route values
  df['route'] = df['route'].str.replace(',', '')
  # Expand start column to separate start_x and start_y columns
  df = pd.concat((df['start'].str.split(',', expand=True).astype(int), df['route']), axis=1)
  df = df.rename({0: 'start_x', 1: 'start_y'}, axis=1)
  # Traverse the route for each strand to get absolute (x,y) coordinates
  df['coordinate'] = df.apply(plot_route, axis=1)
  # We now have a tuple of all the coordinates for each strand,
  # but we're not really interested in what strand does this coordinate belong to.
  # We would rather view the data as absolute coordinates, so explode!
  df = df.explode('coordinate')
  # Due to exploding the coordinate column, we now have duplicates of routes.
  # We can freely travel to any coordinate other than Wall, Finish or Start.
  # They're always the last coordinate of any given strand, so we can just
  # discard coordinates [0..n-1] for each strand using diff(), and mark them passable.
  df['delta_index'] = df.index.to_series().diff(-1)
  df.iloc[-1, 4] = 0  # diff creates null at [last_row, 'delta_index'], fix
  # Mark all passable coordinates with a dot.
  df.loc[df['delta_index'] == 0, 'route'] = '.'
  df.loc[df['route'].isna(), 'route'] = '.'
  # We still have the full route data for every last index of a strand.
  # Replace where needed with '.', 'X', 'S' or 'F'.
  df['route'] = df['route'].str[-1]
  df['route'] = df['route'].replace(r'[DURL]', '.', regex=True)
  # Finally, remove the unnecessary columns, and rename others.
  df = df.drop(['start_x', 'start_y', 'delta_index'], axis=1)
  df = df.rename({'route': 'object'}, axis=1)
  return df

def visualize_problem(df):
  df['object'] = df['object'].replace({'.': 0, 'X': 1, 'S': 2, 'F': 3})
  df['x'], df['y'] = zip(*df['coordinate'].values)
  df.plot.scatter('x', 'y', c='object', cmap='seismic')
  plt.show()

def solve_problem(df):
  # Use A* to solve the problem.
  # Filter walls out, they're really the same as having no route at all.
  nodes = df.loc[df['object'] != 'X', 'coordinate'].tolist()
  start = df.loc[df['object'] == 'S', 'coordinate'].iloc[0]
  goal = df.loc[df['object'] == 'F', 'coordinate'].iloc[1]
  return AStar().solve(nodes, start, goal)

if __name__ == '__main__':
  df = read_and_cleanup_data()
  # visualize_problem(df)
  print(solve_problem(df))
