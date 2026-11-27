import pandas as pd
import numpy as np

stages = [4.28, 9.91, 10.51, 12.66, 16.93, 21.08, 24.41, 25.23, 25.73, 27.27, 30.51, 31.37, 32.01, 33.8, 34.84, 34.9, 35.56, 36.42, 36.43, 37.52, 37.93, 39.15, 43.85, 50.22, 55.16, 57.44]
s = pd.Series(stages)
m = s.median()
print('type(m):', type(m), repr(m))
print('round(float(m), 2):', round(float(m), 2))
print('round(m, 2):', round(m, 2))
print(f'format 2f: {m:.2f}')
print(f'float format 2f: {float(m):.2f}')
