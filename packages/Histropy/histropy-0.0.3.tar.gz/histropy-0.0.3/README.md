# **1. Installation**
The code for Histropy can be downloaded at https://github.com/SMenon-14/Histropy.

After downloading the ZIP file and unzipping it, the Histropy program can be run through the command line or terminal. Before the Histropy code can be run, the following packages need to be downloaded. Navigate to the command line or terminal and then run the following commands.

## **Windows**
pip install matplotlib<br />
pip install easygui<br />
pip install tabulate<br />
pip install numpy<br />

## **Mac OS**
pip3 install matplotlib<br />
pip3 install easygui<br />
pip3 install tabulate<br />
pip3 install numpy

## **Windows**
cd to the Histropy-main folder through the command line
Run the command python Histropy.py

## **Mac OS**
cd to the Histropy-main folder through the command line
Run the command python3 Histropy.py
<img width="681" alt="Screenshot 2024-06-13 at 1 55 40 PM" src="https://github.com/SMenon-14/Histropy/assets/96715758/70791984-4c7f-4d66-a69a-a8c12c560c47">

This command will open up a file dialogue. When prompted, select an image to open in Histropy (in either JPG, PNG, GIF, BMP, or TIFF formats). 
# **2. Basics**
The scale can be switched between linear and log base 10 using the buttons in the Scale selection space.

The y-limit of the histogram can be set using the textbox in the Scale selection space. 

The upper and lower bounds for the calculation range can be set either by clicking on the histogram itself (the dark blue line is the lower bound and the cyan line is the upper bound) or by entering values directly into the textboxes in the Intensity Range selection space.

This range can be used for segmentation and performing calculations over specific ranges (peaks) of the image.
The histogram coordinates that the mouse is hovering over can be seen in the bottom right corner of the window (this can be used when trying to click on the histogram to set the range).
 
The calculations will automatically update as the Intensity Range is updated
 
Histograms can be overlaid by clicking the “Add Image” button in the Histogram Overlays selection space. This will bring up a file dialogue where the user can select another image to overlay (in either JPG, PNG, GIF, BMP, or TIFF formats).
 
Histogram overlays can be removed using the “Clear Overlays” button.

# **3. Histropy Buttons**
<img width="281" alt="Screenshot 2024-06-13 at 2 00 07 PM" src="https://github.com/SMenon-14/Histropy/assets/96715758/ea0069f6-f90a-4ef4-9bf5-a7499631b372">

## Zoom
When the magnifying glass button is clicked, you can drag a rectangle over the histogram to zoom in on a portion of the histogram. Note that to use the Intensity Range bound-setting function, you must click off the zoom button first.
## Axes Pan
When the axes button is clicked, you can  slide the axes of the histogram to pan across it (right, left, up and down). Once again, to use the Intensity Range bound-setting function you must click off the zoom button first.
## Undo, Redo, and Home
The Arrow buttons will undo or redo an action taken by the zoom and axes pan buttons. The Home button will fully reset the histogram to its original state. 
## Save
The floppy disk button will save a PNG image of the full Histropy workspace as it is when the corresponding button is clicked.

**Note: The button with the sliders is obsolete**
