#!/bin/bash
# *****************************************************************************
#   Description: Script to import VASP POTCARs into the test suite
#     1st argument is path to a folder, usually called "potpaw_PBE.52",
#     where VASP keeps its PBE POTCAR files.
#
#   Copyright 2011-2014 Peter Larsson
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# *****************************************************************************

echo "Creating working directory ./PAWSCRATCH"
mkdir PAWSCRATCH

# Now, I only use the latest PBE POTCARs, which can be downloaded from the VASP site.

if [ -d "$1" ]; then
	# PBE POTCARs
	for element in "Cu_pv" "Fe_pv" "Fe" "Li_sv" "O" "Mg_pv" "Mo" "S" "Pb_d" "Si" "Ti" "Ce" "Si_GW" ; do
		# Uncompress POTCAR only if none exists
		if [[ -f "$1/$element/POTCAR.Z" && ! -f "$1/$element/POTCAR" ]]; then
			gunzip $1/$element/POTCAR.Z
		fi

		# Copy POTCAR
		if [[ -f "$1/$element/POTCAR" ]]; then
			cp $1/$element/POTCAR PAWSCRATCH/POTCAR.PBE.$element
		else
			echo "Could not find POTCAR for $element in $1/LDA directory."
		fi
	done
else
	echo "Could not find the PBE POTCAR directory."
fi

function pbe_potcar {
	for element in "$@"; do
		suffix=`echo $@ | tr -d ' '`
		cat PAWSCRATCH/POTCAR.PBE.$element >> PAWSCRATCH/POTCAR.$suffix
	done
}

# CeO2
echo "Making POTCAR for CeO2"
pbe_potcar "Ce" "O"
cp PAWSCRATCH/POTCAR.CeO input/CeO2/POTCAR

# Cu-fcc
echo "Making POTCAR for Cu-fcc"
cp PAWSCRATCH/POTCAR.PBE.Cu_pv input/Cu-fcc/POTCAR

# Fe-bcc
echo "Making POTCAR for Fe-bcc"
cp PAWSCRATCH/POTCAR.PBE.Fe_pv input/Fe-bcc/POTCAR

# Fe-4x4x4
echo "Making POTCAR for Fe-4x4x4"
cp PAWSCRATCH/POTCAR.PBE.Fe_pv input/Fe-4x4x4/POTCAR

# Fe-stop
echo "Making POTCAR for Fe-stop"
cp PAWSCRATCH/POTCAR.PBE.Fe_pv input/Fe-stop/POTCAR

# Li2FeSiO4
echo "Making POTCAR for Li2FeSiO4"
pbe_potcar "Li_sv" "Fe" "Si" "O"
cp PAWSCRATCH/POTCAR.Li_svFeSiO input/Li2FeSiO4/POTCAR

# Mg2Mo6S8
echo "Making POTCAR for Mg2Mo6S8"
pbe_potcar "Mg_pv" "Mo" "S"
cp PAWSCRATCH/POTCAR.Mg_pvMoS input/MgMoS/POTCAR

# PbO2 cell
echo "Making POTCAR for PbO2"
pbe_potcar "Pb_d" "O"
cp PAWSCRATCH/POTCAR.Pb_dO input/PbO2/POTCAR

# Si-cd
echo "Making POTCAR for Si"
cp PAWSCRATCH/POTCAR.PBE.Si input/Si-cd/POTCAR
cp PAWSCRATCH/POTCAR.PBE.Si input/Si-dos/POTCAR
cp PAWSCRATCH/POTCAR.PBE.Si_GW input/Si-GW/POTCAR
cp PAWSCRATCH/POTCAR.PBE.Si input/Si-hybrid/POTCAR
cp PAWSCRATCH/POTCAR.PBE.Si input/Si-parchg/POTCAR
cp PAWSCRATCH/POTCAR.PBE.Si input/Si-vdW/POTCAR

# Si geoopt
echo "Making POTCARs for Si geoopt suite"
cp PAWSCRATCH/POTCAR.PBE.Si input/Si-cd.opt/POTCAR
cp PAWSCRATCH/POTCAR.PBE.Si input/Si-cd.opt2/POTCAR
cp PAWSCRATCH/POTCAR.PBE.Si input/Si-cd.opt3/POTCAR
cp PAWSCRATCH/POTCAR.PBE.Si input/Si-cd.opt4/POTCAR
cp PAWSCRATCH/POTCAR.PBE.Si input/Si-cd.opt5/POTCAR

# SO3
echo "Making POTCAR for SO3"
pbe_potcar "S" "O"
cp PAWSCRATCH/POTCAR.SO input/SO3/POTCAR

# TiO2
echo "Making POTCAR for TiO2"
pbe_potcar "Ti" "O"
cp PAWSCRATCH/POTCAR.TiO input/TiO2-rutile/POTCAR

# Delete workdir
echo "Removing working directory ./PAWSCRATCH"
rm -fr PAWSCRATCH
