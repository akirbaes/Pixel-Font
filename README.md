# Bitmap Pixel Font Visualizer

Load a pixel font sheet easily and start typing text with it.

/fonts contains the character sheets in .png and their corresponding character content in .txt

>**badlydrawn**.png  
![Badly drawn pixel font](fonts/badlydrawn.png)

>**badlydrawn**[chars].txt  
~~~~
ABCDEFGHIJKLM  
NOPQRSTUVWXYZ  
~~~~

font_to_data.py then generates a .json with the sheet infos (positions, sizes of each character)

>**badlydrawn**[posiz].json  
Position of each character on the image, background color, max width, max height

font_visualizer.py in the root allows to load those fonts and use them to show text.

>![Badly drawn text using the pixel font](images/hideous_drawn.png)

The text is customizable and there are many options to change.

>![Visual of the options window](images/optionswindow_screenshot.png)

----

# The fonts

The main purpose of the application was to visualise some special fonts that required using a (colored) bitmap font type (badlydrawn is just a testing font that's badly drawn).

----

**µRed** (mono and proportional versions) is a 2x4 ascii colored font (and probably the most compact font known outside of a 3x3).

>![2x4 mini ascii font](fonts/µRed_mono.png) ![3x4 mini ascii font](fonts/µRed_wide.png)

It uses RGB subpixels to represent letters with mostly only two pixels of width. Hence, it requires a colored bitmap basis.

Due to the rightmost pixels always being at most red, two letters can be adjacent without pixel separation and still be reasonably readable, since there are still two empty subpixels between the letters. **This makes it as compact as a 1x4 in practice (counting character+separation)!**

The name "µRed" (MicroRed) / "MiniRed" is based on the small size (maybe the smallest "readable" font ever?), and the red appearance. The color red appears often  because of how a lot of letter shapes cover just the leftmost subpixel. The font works on a black background. While the negative (cyan) is possible I find it harder to read.

One last property is that zooming in the font digitally will render it unreadable (due to the subpixels being turned into whole pixels) especially if the characters are close together. Interesting for hiding messages "in plain sight" or messing with people. Real-life magnifying glass can be considered as an alternative for zooming! Otherwise, you will have to lean closer to your screen which can cause eyes strain.

>![Example of output text](images/hideous_screenshot.png) ![Example of digitally zoomed text (X2)](images/hideous_zoomed.png)

There are two versions of the font: a MONO that's consistently 2 pixels wide, 
and a proportional/Wide version that uses three pixels for letters that are difficult to distinguish otherwise 
like M, N, W...

The MiniRed (now µRed) was originally created around 2016 by Akira BAES. It's still being tweaked and extended over time.

----

**Formula and Formula16** are just fonts for a dumb substitution from the Roman alphabet glyphs to a personnal glyphset. 

>![Font formula](fonts/Formula.png) ![Font formula 16](fonts/Formula_16.png)

The glyphs were imagined by deforming hand-written letters (the loop of the e becomes a spike, etc.), or using other mental shortcuts to try to create something esoteric-looking but easy to remember.