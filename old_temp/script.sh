
cd {{ project.config.project_dir }}
#!/bin/bash  -l

module purge
module load mkl
module load fftw
module load intel/cluster/2018
module load python
{% for operation in operations %}
{{ operation.cmd }}
{% endfor %}
