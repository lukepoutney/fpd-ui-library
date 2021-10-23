**FPD UI**

Welcome to our Graphical implementation of the Fast Pixelated Detector (fpd) python library!

First of all we would like to acknowledge Dr. Gary Paterson who created the FPD library that we implement here.

**1. Pre-requisites** 

This software can be used in one of two ways. If you would like to modify or extend its functionality you can clone this repository and use the program by running fpdui.py.
Alternatively, if you wish to use a packaged version of the software you can find OS specific downloadeds here:
https://www.dropbox.com/sh/1a9uk65tvwgnihm/AABQ_KYBRZ5bJ-2UgLOBLJJba?dl=0

**2. Installing**

***Developer versions:***

requirements include installations of:
- Python >= 3.6
- anaconda3
- pip

**Note:** MAC, windows and Linux have near identical installation processes, with the exception being the need to use python in place of python 3 for terminal commands for Windows and Linux
windows / linux: python
mac: python3

installation:

1.	Install python 3: https://www.python.org/downloads/

If you are unsure how to check if you have python 3 installed, open the terminal application and type the following command: 
-	python3 --version

2.	Install pip (to python 3):

Again, we can check if pip is installed using pip --version. This should display a path to where python 3 is installed. If pip is not installed execute the following commands:
-	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
-	python3 get-pip.py

3.	Install anaconda 3: https://www.anaconda.com/distribution/
- Once anaconda is installed a terminal restart will be required

Anaconda is only used to help install the llvmlite package

4.	Pull/download from our GitLab repository: https://stgit.dcs.gla.ac.uk/tp3-2019-cs16/cs16-main


5.	Run fpdui.py from the terminal, you will have to navigate to this files location to run the command
-	python3 fpdui.py
This will check you have all the required packages and if not will run an install script
Upon first launch you may encounter an errors due to the generation of the settings data. To fix this simply close the program and reopen it.


6.	Complete. Now whenever you would like to run the application just run fpdui.py via command line.

Packaging Versions:
Download the packaging files here:
https://www.dropbox.com/sh/1a9uk65tvwgnihm/AABQ_KYBRZ5bJ-2UgLOBLJJba?dl=0

place the .spec file inside the program folder and run it.
Once complete open the dist and fpdui folders and inside create 2 folders called dask and hyperspy.
Place the other 2 .yaml files in their respective folders. You can now run this packaged version using the fpdui.exe file located in this same folder

**3. Using FpdUI**

	**NOTE**
	the open window button at the bottom of 

	a. Opening an mib file:
		1. Click File in the toolbar
		2. Click Open .mib file
		3. Select the mib file in the file browser
			i. No .hdr of the same name
				1. Select the fdr file you wish to use
			ii. Not using a dm3
				1. If you wish to select the scanXalu and scanYalu manually you must select this option in the options menu
				2. When you open an mib file you will be prompted to insert these values
			iii. Using a dm3
				1. If you wish to use a dm3 file instead of manually entering scanXalu and scanYalu you must select this option in 
				the options menu
				2. Select Open .dm3 file
				3. Select the .dm3 file in the file browser
	
    b. Opening an hdf5 file
		1. Click File in the toolbar
		2. Click Open .hdf5
		3. Select the hdf5 file in the file browser

	c. Changing options
		1. Downsampling real and reciprocal space
			i. These parameters set the level of downsampling you wish to use for your file
		2. Databrowser scan x and y size
			i. IF you have chosen not to use a dm3 file you can change the scanXalu and scaYalu parameters here
			ii. IF you have chosen to use a dm3 file these parameters will not do anything
		3. Use dmi file
			i. This lets you specify if you wish to use a dm3 file or not
 		4. Plot graphs in window
			i. This allows you to specify whether you want the graphs to load in the program or as separate windows  
		5. Advanced options
			i. This allows you to specify whether you want to manually insert the parameters to many of the fpd library functions
			or use the defaults we have implemented. 

	d. Browsing the data
		1. Once the data is loaded, navigate to the Basic Data tab and click Browse Data
	
	e. Diffraction Pattern Center Exploring
		1. Once the data is loaded, navigate to the Basic Data tab
		2. To find the diffraction pattern center click the Find Diffraction Pattern Center button
			i. IF you have selected to see advanced options, you will be presented a options menu to select parameters
			ii. IF not the diffraction pattern center will be calculated with default parameters
			iii. Either way you will see the graphical output and can judge if the calculations are accurate
			iV. If you feel the DPC is not accurate, pressing the button again will override the previous calculation
		3. To generate an aperture click the Generate Aperture button
			i. If you judge this aperture to be unsatisfactory, pressing the button again will override the previous
		4. To calculate the Centre Of Mass navigate to the DPC Explorer tab and press the Calculate Center of Mass button
			i. This will show you the output of values, but you do not have to remember them as they will be 
			automatically passed to the Browse center of mass function	
		5. To perform descan correction press the Descan Correction button
			i. If you think the descan correction is incorrect, you can simply run the function again and it will replace the previous correction
        6. To perform Magnetic correction press the Magnetic Correction button
        7. To perform image rotation press the Image Rotation button
		8. To Browse the Center of Mass press the DPC Explorer button
            i. You will be able to select which dataset you would like to use - meaning you can compare the data before and after image rotation, for example		
	
	f. DPC by phase correlation
        ** NOTE ** These functions have been split over two tabs to prevent too many buttons appearing on one tab.
        The relevant tabs are "Phase Correlation" and "DPC data view"
		1. Find similar images can accept an aperture if one has been created
		2. To find the disc centre use the find disc centre and so on for the Phase correlation tab
		3. Once phase correlation has been found, you can perform corrections on the data or visualise it in the next tab
		4. If you wish to use the Visualisation with the 4-D Data you will need to have performed magnetic correction on the data.


	g. Virtual Annular Darkfield 
		1. To find the diffraction pattern center press the Find DPC button
		2. To calculate Virtual Annular Darkfield press the Calculate VADF button
		3. To load a VADF calculation press the load VADF button
		4. To save a VADF calculation press the save VADF button
		5. To show the VADF calculation output press Plot VADF button
		6. There is also an option to save the VADF nav image as a raw numpy array file and a bitmap, using the save button embedded on the output.