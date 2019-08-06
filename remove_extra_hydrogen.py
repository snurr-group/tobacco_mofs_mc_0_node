from ase.io import read
import pymatgen as pm
from pymatgen.analysis.local_env import CrystalNN
import warnings
from pymatgen.io import ase as pm_ase
import os
bridge = pm_ase.AseAtomsAdaptor()
directory = '/home/zlc6394/tobacco_mc_0'
#directory = '/home/zlc6394/tobacco_mc_0'
write_dir = '/home/zlc6394/removed_hydrogen_mc_0'
for files in os.listdir(directory):
	if (os.path.exists(write_dir + '/' + files) == False):
		os.chdir(directory)
		asemof = read(files)
		mof = bridge.get_structure(asemof)
		#mof = pm.Structure.from_file('bor_sym_3_mc_0_sym_4_mc_1_L_19.cif',primitive=False) #read CIF as-is
		nn_object = CrystalNN(x_diff_weight=0) #can optionally set search_cutoff=None

		#ignore warnings about specifying oxidation states
		with warnings.catch_warnings():
			warnings.simplefilter('ignore')
			badidx = []
			#loop through every atom to get the coord num
			for atomidx in range(len(mof)):
				atom = mof[atomidx]
				if atom.species_string == "H" :
					local_env = nn_object.get_nn_info(mof,atomidx)
					coord_num = len(local_env)
					#for a in local_env: 
					#	print("connected atom is", a['site'].species_string)
					if not coord_num or coord_num != 1 or local_env[0]['site'].species_string == "Cu":
						badidx.append(atomidx)

#	for i in badidx:
			mof.remove_sites(badidx)
			os.chdir(write_dir)
			print("Hey! It is writing stuff!")
			mof.to(filename = files)
