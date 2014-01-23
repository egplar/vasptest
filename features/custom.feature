Feature: Custom modifications
    Test some NSC/SNIC custom modifications of the VASP binaries

    # Check that VASP can find the global vdW kernel file
    Scenario: Si-vdW
        Given that the POTCAR MD5 is 4e058592231fc4e091ac0c92d87797b0
        When I run VASP with a maximum of 8 ranks
        Then the total energy should be -31.98734087 +/- 1.0e-5 eV
            and self consistency should be reached in 12 iterations
            and the Fermi energy should be 5.530596 +/- 0.01 eV
            and the pressure should be 31.80 +/- 0.1 kB
            and the point group symmetry should be T_d
            and the XML output should be valid

    # Check that VASP is compiled with -DLONGCHAR
    # This job will not complete otherwise
    Scenario: Fe-4x4x4
        Given that the POTCAR MD5 is adbd1768cd2384d3107d7a5469a5da60
        When I run VASP with a maximum of 64 ranks
        Then self consistency should be reached in 1 iterations
            and the point group symmetry should be O_h
            and the XML output should be valid

    # This job should not stop if we have compiled with -DnoSTOPCAR
    Scenario: Fe-stop
        Given that the POTCAR MD5 is adbd1768cd2384d3107d7a5469a5da60
            and a STOPCAR file is present
        When I run VASP with a maximum of 8 ranks
        Then the total energy should be -8.231456 +/- 1.0e-5 eV
            and self consistency should be reached in 16 iterations
            and the Fermi energy should be 9.629837 +/- 0.01 eV
            and the pressure should be -39.29 +/- 0.1 kB
            and the magnetic moment should be 2.2095 +/- 0.01 uB
            and the point group symmetry should be O_h
            and the XML output should be valid
