import numpy as np
import pandas as pd
import math
def find_sharpness(numpy_array):
    #Convert array to dataframe
    y,x= np.nonzero(numpy_array)
    df = pd.DataFrame({'x':x,'y':y})
    x0 = df['x'].sum()/df['x'].count()
    y0 = df['y'].sum()/df['y'].count()
    df = df[(df['x']!=0)&(df['y']!=0)].reset_index(drop=True) # to avoid divide by 0 errors later
    #Calculate polar coordinates
    df['x_rel'] = df['x'] - x0
    df['y_rel'] = df['y'] - y0
    df['angle'] = df.apply(lambda row:math.atan2(row['y_rel'],row['x_rel']),axis=1)
    df['distance'] = df.apply(lambda row:math.sqrt(row['y_rel']**2 + row['x_rel']**2),axis=1)
    global_max = df['distance'].max()
    #Find max for each bin
    num_bins = 180
    bin_edges = np.linspace(-math.pi/2, math.pi/2, num_bins + 1)
    bins = pd.IntervalIndex.from_breaks(bin_edges,name='Angle_bin')
    df.index = pd.cut(df['angle'],bins)
    max_df = df.groupby(level=0,observed=False)['distance'].max()
    max_diff = []
    for i in range(0,len(max_df)-1):
        max_diff.append(abs(max_df.iloc[i]-max_df.iloc[i+1])/global_max)
    return max(max_diff) if max_diff else 0