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

box = mb.Box(lengths=[1.5115, 1.5115, 1.5115])

box_of_i2= mb.fill_box(compound=i2, n_compounds=n, box=box)
box_of_i2.energy_minimize(steps=1000, algorithm='md', forcefield='GAFF')
box_of_i2.save('iodine.xyz')
with open('iodine.xyz', 'r') as fin:
    data = fin.read().splitlines(True)
with open('iodine.xyz', 'w') as fout:
    fout.writelines(data[2:])



