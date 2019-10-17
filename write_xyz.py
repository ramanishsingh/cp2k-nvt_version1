import signac
import os
from subprocess import call
def write_xyz(NATOMS,L,fileout="box.py"):
        file = """

import mbuild as mb
class I2(mb.Compound):
    def __init__(self):
        super(I2, self).__init__()

        iodine1= mb.Particle(pos=[0.0, 0.0, 0.0], name='I')
        iodine2= mb.Particle(pos=[0.8, 0.0, 0.0], name='I')
        self.add([iodine2,iodine1])
        self.add_bond((iodine2,iodine1))

i2 = I2()
i2.energy_minimize(steps=100, algorithm='steep', forcefield='GAFF')


box_of_i2= mb.fill_box(compound=i2, n_compounds={}, box=[0,0,0,{},{},{}])
box_of_i2.energy_minimize(steps=100, algorithm='md', forcefield='GAFF')
box_of_i2.save('iodine.xyz')
with open('iodine.xyz', 'r') as fin:
    data = fin.read().splitlines(True)
with open('iodine.xyz', 'w') as fout:
    fout.writelines(data[2:])
""".format(NATOMS,L,L,L)

        with open(fileout,"w") as out:
                out.write(file)


proj = signac.get_project()

def write_job_xyz(job):

    # State point values stored as: Temp
        N = job.statepoint()['N']
        L = job.statepoint()['L']
        #print(type(N))

        write_xyz(N,L,fileout=job.fn("box.py"))
        #import box.py
        #python box.py



for job in proj:
        write_job_xyz(job)



for job in proj:
        home  = job.workspace()
        print("HOME: {}".format(home))
        os.chdir(home)
        call(["python", "box.py"])
