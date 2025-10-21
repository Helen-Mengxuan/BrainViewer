# BrainViewer

Easy-to-Use, Automated Visualization of Brain Images

Quality control for skull-stripped anatomical T1 images. 
<br>
<img width="1192" height="532" alt="Screen Shot 2025-10-10 at 11 01 17 PM" src="https://github.com/user-attachments/assets/abfdeaeb-9084-421c-a64a-559de3783c86" />
<br>

<br>
Quality control for skull-stripped fieldmap magnitude images. 
<br>
<img width="1191" height="522" alt="Screen Shot 2025-10-10 at 11 03 21 PM" src="https://github.com/user-attachments/assets/3b5df404-1bf9-45fc-92b9-3a7e798faa93" />

<br>

How to use:
1. Use the bet command with the -o option in FSL to generate the overlay.nii.gz images.
2. Place all overlay images (with filenames containing each subject’s ID) that require skull-stripping inspection into the same folder. Replace “path/to/folder” with the actual path to this folder.
3. Run BrainViewer.py.
4. Use the Previous or Next buttons to navigate between subjects.
5. To start with a specific subject (especially useful for large datasets) enter the subject ID in the text box and click Go. The subject ID displayed at the top indicates which subject’s image is currently shown.
6. Click Start to begin viewing images in different orientations, Pause to stop, and Restart to begin again from the top of the list.
7. This program can also be easily modified for inspecting images for other purposes.
