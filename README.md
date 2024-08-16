# Bitmap Pixel Font Visualizer

### Load a pixel font sheet easily and start typing text with it!

![Screenshot of the program at 04-12-19](images/readme/program_screenshot_04-12-19.png)

## Download standalone executable: [\[↓\]Pixel Font Vizualizer.zip](https://github.com/akirbaes/Pixel-Font/releases)

Otherwise:

> PIL: `pip install pillow`
>
> pyscreenshot: `pip install pyscreenshot`
>
> win32clipboard (optional): `pip install pywin32`
>
> `python font_visualizer.pyw`

Then just add your fonts to the /fonts folder to use them in the program!

## Features

* Easily visualize and tweak your pixel-font text

* Take pictures, copy to clipboard, or use the generated JSON to load it elsewhere

* Generate missing accents

* Letter spacing/automatic kerning options (offsets generated as separate JSON)

![Letter Spacing/Kerning algos: Fixed Width, Bounding Box, Pack in X, Diagonals Fit, Pixel Distance, Average Area](images/readme/compact_kerningalgospresent.png)


## What's needed:

- the font's image (preferably transparent PNG) with all characters spaced out evenly.

>**tekitou_gold**.png 
> 
>![Gold-looking pixel font](images/readme/tekitou_gold.png)

- a .txt of the same name with all the characters in the font image in the right place.

>**tekitou_gold**.txt  
>~~~~
>ABCDEFGHİJ
>KLMNOPQRST
>UVWXYZ
>,.!?()'
>´`^¨I
>~~~~

### And that's all!

font_visualizer.py in the root will scan for .png in the /fonts folder and load them. You can now use them to show text!

>![Pangram texts using the pixel font](images/readme/gold_pangrams.png)

The text is customizable and there are many options to change. Options are saved per-font!

![Visual of the options window](images/readme/optionswindow_screenshot_08-01-20.png)


## Accents

If you provide acute, grave, circumflex, diacritic, tilde accent characters, they can be used to generate accented vowels without your explicit input. However, you have to provide the image of a dotless i (ı) if you want accented i to work correctly.

|Handwriting_accents.txt | Handwriting_accents.png |
|:--------------------------------------------------------|:---------------------------|
 | ![Showing the included characters](images/readme/handwriting_accents_parts.png) |  `abcdefghijklm` <br>  `nopqrstuvwxyz`  <br> `ABCDEFGHIJKLM`  <br> `NOPQRSTUVWXYZ`  <br> ``ı^´`¨°~``    |

Result:

>![Showing off the accents capabilities](images/readme/accents_showoff.png)

If you are unhappy with the result, you can still provide the accented characters yourself.

## Generated files:

* YourFont.ini will contain basic font options (horizontal and vertical separations, size of space character, case changes, used spacing/kerning arlgorithm).

* YourFont.json will contain the position of every letter in YourFont.png in the form of 'A' : [x, y, width, height] where 'A' is a string of length 1, plus some other data (background color, max width and height).

*  YourFont.Kern\* will contain the offset for each kerning pair it detected in the form of "AZ" : offset where "AZ3 is a string of length 2. To add to the horizontal separation found in YourFont.ini and the width of the character found in YourFont.json.

## Other secrets: 

- Fixed Width mode uses the widest available character at hsep=0. 

- Hsep is not added to space size.

- The font character size is aligned horizontally based on the leftmost and rightmost pixel for each character. If you want some control over the alignment, put "aligned" in the file name to align based on the pixel accross all characters that is the most on the left.

- The .json file of your font's name is automatically generated the first time you use it. It contains all the positions of your characters (x,y,w,h), and the background color. You can edit it if you still feel that the automatic cropping failed. 

- Same for the kerning values, but they are only re-generated if you click "Save Options".

----

# Notable fonts

The main purpose of the application was to visualise custom-made pixel fonts. Here are some of my creations:


## **My handwriting**

>![Font of my handwriting](fonts/my_handwriting_v2.png) 

This font is based on my handwriting. It was scanned and cut up in pieces. 

## **Dancing font**

>![Animated font of my handwriting](images/readme/dancing_font.gif)

Three separate handwritten fonts scanned and aligned to make an animation. My program doesn't actually take in account animation, so they are effectively three fonts with shared proportions.

## **Future Cipher**

>![Font of my cipher](fonts/futurescript_25_bold.png) 

A basic replacement cipher based on deformations of latin script.

## **Subpixel fonts**


|Font![separator](images/readme/thin_line.png) Sampletext | Preview photo |Description|
|:---------|--|:-------|
|![2x4 micro ascii font](images/readme/µRed_mono.png) ![µRed sample](images/readme/µred_mono_sample.png)|<img src="images/readme/µred_mono_photo.jpg" width="550"> | **µRed_Mono** (pronounced Micro-Red) has a fixed size of 2x4. Probably close to the most compact font possible outside of a 3x3.|
|![Variable width and height micro ascii font](images/readme/µRed_wide_tall.png)![µRed sample](images/readme/µred_v2_sample.png)|<img src="images/readme/µred_v2_photo.jpg" width="550">|**µRed_v2** has variable width to allow for characters like W, M, N, H to be more readable. Characters like "g", "p", "q" and "," also hang one pixel lower for aesthetic purposes. |
|![Cursive micro ascii font](images/readme/µCursive.png)![µCursive sample](images/readme/µcursive_sample.png) |<img src="images/readme/µcursive_photo.jpg" width="550">| **µCursive** is a mostly 3x5 cursive-style subpixel font that is somehow very readable (and green!). |
|![3x3 alphanumeric font](images/readme/3x3_alphanum.png) ![3x3 sample](images/readme/3x3_alphanum_sample.png)|<img src="images/readme/3x3_alphanum_photo.jpg" width="550">| 3x3 alphanumeric font improved by using subpixels. |
|![4x5 standard font](images/readme/standard_small_mono.png) ![4x5 sample](images/readme/4x5_small_mono_sample.png)|<img src="images/readme/4x5_small_mono_photo.jpg" width="550">| 4x5 very basic font using subpixels for the edges. |



The font set uses RGB subpixels to represent letters, so it needs colors to work. The rightmost pixels is always at most red, so two letters can be adjacent without a pixel of separation and still be reasonably readable, since there are still two empty subpixels between the letters. **This makes the mono version as compact as a 1 pixel wide font in practice!**

The name "µRed" (Micro Red) is based on the small size (smaller than regular pixel fonts), and the red appearance. The color red appears often  because of how a lot of letter shapes cover just the leftmost subpixel. The font works on a black background. While the negative (cyan on white background) is possible I find it harder to read. You can see here what you could see if you could separate the subpixels:

![MicroRed zoomed in by multiplying the subpixels](images/readme/µRed_wide.fullpixels_full_color.png)

One last property is that zooming in the font digitally will render it unreadable (due to the subpixels being turned into whole pixels) especially if the characters are close together. Interesting for hiding messages "in plain sight" or messing with people. Real-life magnifying glass can be considered as an alternative for zooming! Otherwise, you will have to lean closer to your screen which can cause eyes strain. 

### Example:

| ![Example of output text](images/readme/hideous_screenshot.png) | `I am the most hideous creature in the realm. ☺♫` <br/> `A more abject appearance you will not find. ☻♪` <br/> `I have fallen countless times, and yet I am here. ▼↓` <br/> `Is it not proof that I possess the stone of life? ♥☼`|
|:------|:----------|

If you simply zoom into it, the subpixels will smudge and become unreadable:

![Text zoomed in by scaling the pixels (unreadable)](images/readme/hideous_screenshot._x6.png)

If you could zoom into it while maintaining the subpixels structure, this is how it would look:

![Text zoomed in by multiplying the subpixels](images/readme/hideous_screenshot.fullpixels_full_color.png)

I'm not the first (nor the last) to play with the idea. [Examples: Militext](https://news.ycombinator.com/item?id=18702900), [TinyFont](https://mrl.nyu.edu/~perlin/homepage2006/tinyfont/), etc. I originally created the ascii 2x4 mono red font around 2016 (based on the file's date on my old computer). I was planning to debut it in a game, then time passed... The font is still being tweaked and extended over time with more characters and better readability in mind. The cursive version is a recent addition. 

