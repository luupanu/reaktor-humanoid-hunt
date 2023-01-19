import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def plot_route(row):
  if pd.isna(row['route']):
    return [((row['start_x'], row['start_y']))]
  points = []
  key = {'L': (-1, 0), 'R': (1, 0), 'U': (0, -1), 'D': (0, 1)}
  curr = np.array((row['start_x'], row['start_y']))
  for x in row['route']:
    points.append((curr[0], curr[1]))
    curr += key.get(x, (0, 0))
  return points

def visualize_problem():
  # Read the file, create start and route columns
  df = pd.read_table('challenge_3', sep=' ', names=['start', 'route'])
  # Remove commas from route values
  df['route'] = df['route'].str.replace(',', '')
  # Separate start column (x,y) to separate start_x and start_y columns
  df = pd.concat((df['start'].str.split(',', expand=True).astype(int), df['route']), axis=1)
  df = df.rename({0: 'start_x', 1: 'start_y'}, axis=1)
  # Get actual x,y coordinates from the given route
  df['point'] = df.apply(plot_route, axis=1)
  # Explode the point column
  df = df.explode('point')
  # Due to exploding the point column, we have unnecessary duplicates of routes
  # Use diff to know where we actually change between routes
  df['ichange'] = df.index.to_series().diff(-1)
  df.iloc[-1, 4] = 0  # diff creates null at last row, fix
  df['route'] = df['route'].str[-1]
  df.loc[df['ichange'] == 0, 'route'] = 0
  # Now we don't need the full route anymore, just leave the last character
  df.loc[df.route.isnull(), 'route'] = 0
  df.loc[df.route == 'X', 'route'] = 1
  df.loc[df.route == 'S', 'route'] = 2
  df.loc[df.route == 'F', 'route'] = 3
  df['route'] = df['route'].replace(r'[DURL]', 0, regex=True)
  df['x'], df['y'] = zip(*df.point.values)
  df = df.drop(['start_x', 'start_y', 'ichange', 'point'], axis=1)
  df.plot.scatter('x', 'y', c=df.route, colormap='seismic')
  plt.show()

if __name__ == '__main__':
  visualize_problem()