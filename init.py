import signac
import pandas as pd

# Project initialization
iodine = signac.init_project('iodine')

statepoints = pd.read_csv('iodine.inp', sep='\s+')

for statepoint in statepoints.to_dict(orient='records'):
    # Rename Temp[K] to Temp
    statepoint['Temp'] = statepoint.pop('Temp[K]')
    iodine.open_job(statepoint).init()
