
{% extends base_script %}
{% block project_header %}
#PBS -l walltime=00:10:00,mem=300gb,nodes=5:ppn=24

module purge
module load mkl
module load fftw
module load intel/cluster/2018

date >> execution.log
{{ super() }}
{% endblock %}
