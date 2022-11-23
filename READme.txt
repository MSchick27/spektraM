#############################
Software is still in progress         so be aware of error or updates to occure :)
#############################

All files except the project.json and Readme files are important for the software to run without problems.


pip install -r requirements.txt

packages which are relevant for the python Code are:
scipy, numpy, os, filedialog, tkinter , PIL, matplotlib, json


---------------------------------Recommendations for a smooth process:---------------------------------
-press buttons only once

buttons
-Plot plots data onto the canvas
-clear, clears plot

-axis:  
Press Button and press twice on the canvas to set ax-limits
Confirm points with left or middle mouse button
Right click deletes points




---------------------------------Further Things:---------------------------------
Author:
Maximilian Schick

pyinstaller --noconfirm --onefile --windowed 
--add-data "PATH spektraM/fitwindow:fitwindow/" 
--add-data "PATH spektraM/initval:initval/" 
--add-data "PATH irspectra:irspectra/" 
--add-data "PATH spektraM/pics:pics/" 
"PATH spectraM.py"


pip freeze creates requirements.txt