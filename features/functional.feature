Feature: Functional
    Test more features of VASP

    # Si G0W0 calculation
    Scenario: Si-GW
        Given that the POTCAR MD5 is 908f33839673b281011b6fe54e91cf3e
        When I run VASP with a maximum of 16 ranks
        Then the OUTCAR file should contain "QP shifts <psi_nk| G(iteration)W_0 |psi_nk>" 
        and the highest occupied quasi-particle energy should be 5.1537 +/- 0.001 eV

    # Run a hybrid calculations
    Scenario: Si-hybrid  
        Given that the POTCAR MD5 is 4e058592231fc4e091ac0c92d87797b0
        When I run VASP with a maximum of 8 ranks
        Then the total energy should be -41.86884258 +/- 1.0e-5 eV
        and self consistency should be reached in 14 iterations
        and the point group symmetry should be T_d
        and the XML output should be valid

    # Make a PARCHG
    # Checks that it doesn't crash due to Intel compiler optimizations
    Scenario: Si-parchg  
        Given that the POTCAR MD5 is 4e058592231fc4e091ac0c92d87797b0
        When I run VASP with a maximum of 8 ranks
        Then a PARCHG file should exist
        and the OUTCAR file should contain "Finished calculating partial charge density"

    # Density of states from non self consistent calculation
    Scenario: Si-dos
        Given that the POTCAR MD5 is 4e058592231fc4e091ac0c92d87797b0
        When I run VASP with a maximum of 8 ranks
        Then a DOSCAR file should exist
        and the Fermi energy should be 5.788867 +/- 0.01 eV
        and self consistency should be reached in 8 iterations
        and the total energy should be -43.35220224 +/- 1.0e-5 eV
        and the DOSCAR file should be identical to the reference file "DOSCAR.ref"

