The name of my term project is “Pattern Pal”. 
It is a program that introduces the fun art of geometric patterns and tessellations to the user, inspired by geometric patterns found in Islamic and Arabic art and culture.
The program begins by showing the user a spread of pattern templates that they can choose to create their pattern from or the option to create draw their own pattern using the mouse.
The user also can trace a found image including self portraits and draw on top of that as well, provided that the image is of small size and has a white background. 
Then the user has the option to tessellate their pattern into different combinations of a grid using recursion to create an interesting tessellation effect. 
At the end, the user can save their created tesellation as an image onto their hard drive.

When running this project in an editor, the user only needs to open the file that is named "OpeningScreen", as all the other files are imported into this main file and
the app runs from there.

The only external libraries that need to be installed are PIL and Tkinter, and those are already called in the code base files, so there should be no need to call the file.
If the user wants to import an image to be traced, the image must be placed in the same folder that all the code base files are in, and ideally should be 200 by 200 pixels
so that the code continues to run robustly. 

Note: To navigate through the different app modes and use the features, different commands on the keyboard must be used.
Pressing 'g' shows the help mode that outlines all the commands. By pressing 'Enter', the user can also move back and forth between drawing and tesellating the grid.
By pressing 'Escape', the user can switch to a different template than the one chosen when first launching the program. 
By pressing 'o' and 'i', the user can also save existing data using JSON as a text file in the same folder with the codebase and open up that same file again.

Sample image files are included in this folder to test the trace feature on.
