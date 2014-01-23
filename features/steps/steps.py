from behave import *
import subprocess
import platform
import os
import re
import math
from xml.etree.ElementTree import ElementTree,SubElement
from itertools import groupby

@given('I have copied "{folder}" to the temporary directory')
def copy_to_temp(context,folder):
    assert subprocess.call(["cp",context.orgdir+"/jobs/"+folder,context.orgdir+"/tmp/"]) == 0

@given(u'that the POTCAR MD5 is {checksum}')
def potcar_md5_check(context,checksum):
    if platform.system() == "Linux":
        # md5sum POTCAR | awk '{print $1}'
        md5sum = subprocess.check_output(["md5sum","POTCAR"]).split()[0]
    elif platform.system() == "Darwin":
        # md5 POTCAR | awk '{print $4}' 
        md5sum = subprocess.check_output(["md5","POTCAR"]).split()[3]
    else:
        assert False
    assert md5sum == checksum

@given(u'a STOPCAR file is present')
def stopcar_file(context):
    assert os.path.isfile("STOPCAR")    

@when(u'I run VASP with a maximum of {maxranks} ranks')
def run_vasp(context,maxranks):
    if "VASPTEST_MODE" in os.environ and os.environ["VASPTEST_MODE"] == "check":
        assert True
    else:
        assert "VASPTEST_EXE" in os.environ, "You need to define how to launch your VASP binary in VASPTEST_EXE."
        command = os.environ["VASPTEST_EXE"]

        # Try to limit the number of ranks when launching an MPI job
        # Look for -n and -np flags, it should cover mpirun, mpiexec.hydra, and aprun 
        m = re.search('\s-np?\s(\d+)\s', command)
        if m != None:
            flag = m.group(0)
            ranks = m.group(1)
            if int(maxranks) < int(ranks):
                newflag = flag.replace(ranks,str(maxranks))
                newcommand = re.sub('\s-np?\s(\d+)\s',newflag,command)
            else:
                newcommand = command
        else:
            # Run serial
            newcommand = command

        job = subprocess.Popen(args=newcommand,shell=True,bufsize=0,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (context.stdout,context.stderr) = job.communicate()
        job.wait()
        context.exitstatus = job.returncode
        assert job.returncode == 0, "VASP exited with error or crashed."

def abs_compare(value,reference,diff):
    # Check if (ref-dif) < value < (ref+dif)
    # Assume text input
    lower = float(reference)-float(diff)
    upper = float(reference)+float(diff)
    return lower < float(value) and float(value) < upper

def shell(command):
    return subprocess.check_output(command,shell=True).strip()

@then(u'the total energy should be {energy} +/- {diff} eV')
def energy_check_absolute(context,energy,diff):
    actual_energy = shell("grep 'free  energy' OUTCAR|awk '{print $5}'|tail -n 1")
    assert abs_compare(actual_energy,energy,diff), "got %s eV instead" % actual_energy

@then(u'self consistency should be reached in {iterations} iterations')
def scf_iteration_check(context,iterations):
    actual_steps = shell("""grep "Iteration" OUTCAR|wc -l""")
    assert int(actual_steps) <= int(iterations), "got %s iterations instead" % actual_steps

@then(u'the total number of SCF iterations should be {iterations}')
def scf_iteration_check_total(context,iterations):
    actual_steps = shell("""grep "Iteration" OUTCAR|wc -l""")
    assert int(actual_steps) == int(iterations), "got %s iterations instead" % actual_steps

@then(u'the number of ionic steps should be {steps}')
def ionic_steps_check(context,steps):
    actual_steps = shell("""grep "free  energy" OUTCAR|wc -l""")
    assert int(actual_steps) == int(steps), "got %s ionic steps instead" % actual_steps

@then(u'the Fermi energy should be {energy} +/- {diff} eV')
def fermi_level_check(context,energy,diff):
    actual_fermi_energy = shell("""grep "Fermi energy" OUTCAR|cut -d ":" -f 3|cut -d ";" -f 1|tail -n 1""")
    assert abs_compare(actual_fermi_energy,energy,diff), "got %s eV instead" % actual_fermi_energy

@then(u'the pressure should be {pressure} +/- {diff} kB')
def pressure_check(context,pressure,diff):
    actual_pressure = shell("""grep "external pressure" OUTCAR|awk '{print $4}'|tail -n 1""")
    assert abs_compare(actual_pressure,pressure,diff), "got %s kB instead" % actual_pressure

@then(u'the xx component of the stress tensor should be {pressure} +/- {diff} kB')
def stress_xx_check(context,pressure,diff):
    actual_pressure = shell("""grep "in kB" OUTCAR|awk '{print $3}'""")
    assert abs_compare(actual_pressure,pressure,diff), "got %s kB instead" % actual_pressure

@then(u'the yy component of the stress tensor should be {pressure} +/- {diff} kB')
def stress_yy_check(context,pressure,diff):
    actual_pressure = shell("""grep "in kB" OUTCAR|awk '{print $4}'""")
    assert abs_compare(actual_pressure,pressure,diff), "got %s kB instead" % actual_pressure

@then(u'the zz component of the stress tensor should be {pressure} +/- {diff} kB')
def stress_zz_check(context,pressure,diff):
    actual_pressure = shell("""grep "in kB" OUTCAR|awk '{print $5}'""")
    assert abs_compare(actual_pressure,pressure,diff), "got %s kB instead" % actual_pressure

@then(u'the xy component of the stress tensor should be {pressure} +/- {diff} kB')
def stress_xy_check(context,pressure,diff):
    actual_pressure = shell("""grep "in kB" OUTCAR|awk '{print $6}'""")
    assert abs_compare(actual_pressure,pressure,diff), "got %s kB instead" % actual_pressure

@then(u'the magnetic moment should be {magmom} +/- {diff} uB')
def magmom_check(context,magmom,diff):
    actual_magmom = shell("""grep "mag=" OSZICAR | sed 's/.*mag= *//'""")
    assert abs_compare(actual_magmom,magmom,diff), "got %s uB instead" % actual_magmom

@then(u'the point group symmetry should be {symmetry}')
def symmetry_check(context,symmetry):
    actual_symmetry = shell("""grep "static configuration" OUTCAR|awk '{print $8}'""")
    if actual_symmetry[-1] == ".":
        # Trim ending period if necessary
        actual_symmetry = actual_symmetry[0:-1]
    assert actual_symmetry == symmetry, "got %s symmetry instead" % actual_symmetry

@then(u'the XML output should be valid')
def xml_check(context):
    try:
        xmltree = ElementTree()
        xmltree.parse("vasprun.xml")
        assert True
    except Exception:
        assert False, "Error parsing vasprun.xml. Corrupted?"

def pbshift(cdiff):
    if abs(cdiff) > 0.5:
        return 1.0-abs(cdiff)
    else:
        return cdiff

@then(u'the RMS of the coordinate differences should be {rms} +/- {diff}')
def coord_check(context,rms,diff):
    natoms = int(subprocess.check_output("grep \"NIONS\" OUTCAR",shell=True).split()[11])

    # Load direct coordinates into matrix
    before = [x.split() for x in subprocess.check_output("grep -A %d -i Direct POSCAR" % (natoms),shell=True).split('\n')[1:]]
    after = [x.split() for x in subprocess.check_output("grep -A %d -i Direct CONTCAR" % (natoms),shell=True).split('\n')[1:]]

    # Convert to float
    before = [[float(x) for x in y] for y in before]
    after = [[float(x) for x in y] for y in after]

    # Flatten lists
    before = [item for sublist in before for item in sublist]
    after = [item for sublist in after for item in sublist]

    # Calc differences
    diffs = [after[i]-before[i] for i in range(len(after))]

    # Compensate for periodic boundary conditions
    diffs = map(pbshift,diffs)

    # Calculate RMS of coords
    actual_rms = math.sqrt(reduce(lambda x,y: x + y*y,diffs,0)/(3.0*natoms))
    assert abs_compare(actual_rms,rms,diff), "got %3.6f instead" % (actual_rms)

@then(u'the length of the A vector should be {length} +/- {diff} A')
def avector_check(context,length,diff):
    actual_length = shell("""head -n 3 CONTCAR|tail -n 1|awk '{print sqrt($1*$1+$2*$2+$3*$3)}'""")
    assert abs_compare(actual_length,length,diff), "got %s instead" % actual_length

@then(u'the length of the B vector should be {length} +/- {diff} A')
def bvector_check(context,length,diff):
    actual_length = shell("""head -n 4 CONTCAR|tail -n 1|awk '{print sqrt($1*$1+$2*$2+$3*$3)}'""")
    assert abs_compare(actual_length,length,diff), "got %s instead" % actual_length
    
@then(u'the length of the C vector should be {length} +/- {diff} A')
def cvector_check(context,length,diff):
    actual_length = shell("""head -n 5 CONTCAR|tail -n 1|awk '{print sqrt($1*$1+$2*$2+$3*$3)}'""")
    assert abs_compare(actual_length,length,diff), "got %s instead" % actual_length

@then(u'a {file} file should exist')
def stopcar_file(context,file):
    assert os.path.isfile(file), "could not find the %s file" % (file)    

@then(u'the {file} file should contain "{text}"')
def outcar_content(context,file,text):
    assert shell("grep \""+text+"\" "+file) != "", "the required text [%s] was not present in %s" % (text,file)

@then(u'the {file} file should be identical to the reference file "{ref}"')
def file_identical(context,file,ref):
    assert shell("diff %s %s" % (file,ref)) == "", "The files %s and %s are not identical" % (file,ref)

@then(u'the highest occupied quasi-particle energy should be {energy} +/- {diff} eV')
def qp_check(context,energy,diff):
    outcar = open("OUTCAR","r")
    lines = outcar.readlines()

    kpoints = [list(group) for k, group in groupby(lines, lambda x: x.find("QP-energies") != -1) if not k]

    max_qp = -1000.0
    for k in kpoints[1:]:
      for l in k[1:-2]:
        # Break scanning for QP-energies if we encounter empty lines
        if l == "\n":
          break
        parts = l.split()
        qp_energy = float(parts[2])
        occup = float(parts[7])
        if qp_energy > max_qp and occup > 0.0:
          max_qp = qp_energy

    assert abs_compare(max_qp,energy,diff), "got %3.6f instead" % max_qp
