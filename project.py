import flow
import os
from shutil import copyfile
from subprocess import call
import shutil
class Project(flow.FlowProject):
    pass

#@Project.label
#def melted(job):
#    return job.isfile('melt.run1a.dat')

@Project.label
def has_input_files(job):
    return (job.isfile('md.inp'))

@Project.label
def md_computed(job):
    return (job.isfile("md.out"))


# For equilibration, only run out of prod1 directory
#@Project.label
#def prod1(job):
#    return(job.statepoint()['Prod']==1)


# This project operation will run the melting stage of the VLE
@Project.operation
@Project.post(md_computed)
#@Project.pre(has_input_files)
#@Project.pre(prod1)
def run_config(job):
    # Information for running slurm job
    home  = job.workspace()
    print("HOME: {}".format(home))


    scr='/panfs/roc/scratch/singh891/signac/cp2k/iodine-test/{}'.format(job.get_id())
    if os.path.isdir(scr):
     shutil.rmtree(scr)

    os.mkdir(scr)
    copyfile('{}/md.inp'.format(home),'{}/md.inp'.format(scr))

    copyfile('{}/iodine.xyz'.format(home),'{}/iodine.xyz'.format(scr))
    copyfile('project.py','{}/project.py'.format(scr))
    os.chdir(scr)
    # Call topmon
    print("starting cp2k")
    #call("~/test-cp2k/cp2k/exe/Linux-x86-64-intel/cp2k.popt -i md.inp -o md.out",shell=True)
    call("mpirun -np 1 ~/test-cp2k/cp2k/exe/Linux-x86-64-intel/cp2k.popt -i md.inp -o md.out",shell=True)
    print("Complete!")

    # Copy output files to avoid overwriting
    copyfile("{}/md.out".format(scr),job.fn("md.out"))
   # copyfile("{}/config1a.dat".format(scr),job.fn("melt.config1a.dat"))
    #copyfile("{}/config1a.dat".format(scr),job.fn("fort.77"))

if __name__ == '__main__':
    Project().main()
