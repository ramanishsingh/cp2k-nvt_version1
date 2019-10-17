import signac

def write_mdinp(temp,fileout="md.inp"):
	mdinp = """

&GLOBAL
  PROJECT iodine
  RUN_TYPE MD
  ! limit the runs to 5min
  WALLTIME
  ! reduce the amount of IO
  IOLEVEL  LOW
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  STRESS_TENSOR ANALYTICAL
  &DFT
     BASIS_SET_FILE_NAME  /home/siepmann/singh891/cp2k-6.1.0/data/BASIS_MOLOPT
    POTENTIAL_FILE_NAME  /home/siepmann/singh891/cp2k-6.1.0/data/GTH_POTENTIALS

    CHARGE 0
    MULTIPLICITY 1

    &MGRID
    CUTOFF [Ry] 600
    REL_CUTOFF  60
    NGRIDS 4
    &END

    &QS
       ! use the GPW method (i.e. pseudopotential based calculations with the Gaussian and Plane Waves scheme).
       METHOD GPW
       ! default threshold for numerics ~ roughly numerical accuracy of the total energy per electron,
       ! sets reasonable values for all other thresholds.
       EPS_DEFAULT 1.0E-10
       ! used for MD, the method used to generate the initial guess.
       EXTRAPOLATION ASPC
    &END

    &POISSON
       PERIODIC XYZ
    &END

    &PRINT
       ! at the end of the SCF procedure generate cube files of the density
       &E_DENSITY_CUBE OFF
       &END E_DENSITY_CUBE
       ! compute eigenvalues and homo-lumo gap each 10nd MD step
    &END

    ! use the OT METHOD for robust and efficient SCF, suitable for all non-metallic systems.
    &SCF
      SCF_GUESS ATOMIC ! can be used to RESTART an interrupted calculation
      MAX_SCF 30
      EPS_SCF 1.0E-6 ! accuracy of the SCF procedure typically 1.0E-6 - 1.0E-7
      &OT
        ! an accurate preconditioner suitable also for larger systems
        PRECONDITIONER FULL_SINGLE_INVERSE
        ! the most robust choice (DIIS might sometimes be faster, but not as stable).
        MINIMIZER DIIS
      &END OT
      &OUTER_SCF ! repeat the inner SCF cycle 10 times
        MAX_SCF 10
        EPS_SCF 1.0E-6 ! must match the above
      &END
      ! do not store the wfn during MD
      &PRINT
        &RESTART OFF
        &END
      &END
    &END SCF

    ! specify the exchange and correlation treatment
    &XC
      ! use a PBE functional
      &XC_FUNCTIONAL BLYP
      &END XC_FUNCTIONAL
      ! adding Grimme's D3 correction (by default without C9 terms)
      &VDW_POTENTIAL
         POTENTIAL_TYPE PAIR_POTENTIAL
         &PAIR_POTENTIAL
            PARAMETER_FILE_NAME dftd3.dat
            TYPE DFTD3
            REFERENCE_FUNCTIONAL BLYP
            R_CUTOFF [angstrom] 11.00
         &END
      &END VDW_POTENTIAL
    &END XC
  &END DFT

  ! description of the system
  &SUBSYS
    &COORD
    @INCLUDE iodine.xyz
&END COORD
    &KIND I
      BASIS_SET DZVP-MOLOPT-SR-GTH
      POTENTIAL GTH-BLYP-q7
    &END KIND
    &CELL
      ABC 13.751 13.751 13.751
    &END CELL
  &END SUBSYS
&END FORCE_EVAL

! how to propagate the system, selection via RUN_TYPE in the &GLOBAL section
&MOTION
 &GEO_OPT
   OPTIMIZER BFGS ! Good choice for 'small' systems (use LBFGS for large systems)
   MAX_ITER  100
   MAX_DR    [bohr] 0.003 ! adjust target as needed
   &BFGS
   &END
 &END
 &MD
   ENSEMBLE NVT  ! sampling the canonical ensemble, accurate properties might need NVE
   TEMPERATURE [K] {}
   TIMESTEP [fs] 0.5
   STEPS 5
   # GLE thermostat as generated at http://epfl-cosmo.github.io/gle4md
   # GLE provides an effective NVT sampling.
   &THERMOSTAT
     TYPE NOSE
     REGION MASSIVE
     &NOSE
       LENGTH 3
       YOSHIDA 3
       TIMECON [wavenumber_t] 1000.0
       MTS 2
     &END
    &END

&END
  &PRINT
   &STRESS
   &END
   &TRAJECTORY
     &EACH
       MD 10
     &END EACH
   &END TRAJECTORY
   &VELOCITIES OFF
   &END VELOCITIES
   &FORCES OFF
   &END FORCES
   &RESTART_HISTORY
     &EACH
       MD 500
     &END EACH
   &END RESTART_HISTORY
   &RESTART
     BACKUP_COPIES 3
     &EACH
       MD 1
     &END EACH
   &END RESTART
  &END PRINT
&END
""".format(temp)

	with open(fileout,"w") as out:
		out.write(mdinp) 


proj = signac.get_project()

def write_job_mdinp(job):
    # State point values stored as: Temp
	temperature = job.statepoint()['Temp']


    # Write out fort4 file
	write_mdinp(temp=temperature,fileout=job.fn("md.inp"))


for job in proj:
	write_job_mdinp(job)
