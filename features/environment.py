import os
import subprocess

def before_feature(context,feature):
    context.orgdir = os.getcwd()

def before_scenario(context,scenario):
    # Copy job folder to tmp, We assume that we are in the test root directory
    assert subprocess.call(["cp","-r",context.orgdir+"/input/"+scenario.name,context.orgdir+"/tmp/"]) == 0, "Cannot find the input folder for scenario %s." % scenario.name 

    # Cd to job folder in tmp
    os.chdir(context.orgdir+"/tmp/"+scenario.name)

    # Remove old output files here

def after_scenario(context,scenario):
    os.chdir(context.orgdir)
    # We could clear some files here, like WAVECAR CHGCAR

def after_feature(context,feature):
    os.chdir(context.orgdir)

