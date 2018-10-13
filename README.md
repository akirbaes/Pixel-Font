Presenting this 2x4 font:

![2x4 mini ascii font](MiniRed_Mono.png) ![3x4 mini ascii font](MiniRed_WideMNW.png)

It uses RGB subpixels to represent letters with mostly only two pixels of width.

The name "MiniRed" is based on the small size (maybe the smallest "readable" font ever?), and the red appearance. The color red appears often  because of how a lot of letters cover just the leftmost subpixel. The font works on a black background. While the negative (cyan) is possible I find it harder to read.

Due to the right pixels always being red or empty, two letter can be adjacent (no pixel separation) and still be ~readable.

One last property is that zooming in the font digitally will render it unreadable (due to the subpixels being turned into whole pixels). Interesting for hiding messages in 3D textures or messing with people. Real-life magnifying glass can be considered as an alternative for zooming!

----

The repository contains a Python TKinter app to create text images with the Font:

![Example of output text](hideous_screenshot.png)

(There's an older .exe made in GameMaker too)

The text is customizable and there are many options to change:

![Visual of the options window](optionswindow_screenshot.png)


There are two versions of the font: a MONO that's consistently 2 pixels wide, 
and a WIDE version that uses three pixels for letters that are difficult to distinguish otherwise 
like M, N, W...

The font was originally created around 2016 by Akira BAES, 
but it was tweaked and extended over time.