# Load the Pandas libraries with alias 'pd'
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
# Read data from file 'filename.csv'

datos = pd.read_csv("process_modbus_table.csv")
# Preview the first 5 lines of the loaded data
datos.sample(10)
datos.describe()