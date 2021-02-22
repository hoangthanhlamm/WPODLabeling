# Image Labeling for WPOD Net

An image labeling tool for WPOD Network.

## Using 

```
python labeling.py <img_dir>
```

Example:

```
python labeling.py data
```

Each image in folder ```img_dir``` is displayed one after another for labeling.
Click on the image to select click-point. 

## Shortcut key 

- ```c```: match the last point with the first one into a cycle
- ```s```: save points labeled to text file
- ```q```: move to the next image
- ```p```: move to the previous image
- ```r```: clear all points label on current image
- ```z```: undo the last action
- ```x```: exit labeling

**Note:** Auto save is not available, so you must save manually with shortcut key ```s``` 
