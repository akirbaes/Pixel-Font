# -*- coding: utf-8 -*-
import sys, os
#https://stackoverflow.com/questions/24835155/pyw-and-pythonw-does-not-run-under-windows-7
if sys.executable.endswith("pythonw.exe"):
  sys.stdout = open(os.devnull, "w");
  sys.stderr = open(os.path.join(os.getenv("TEMP"), "stderr-"+os.path.basename(sys.argv[0])), "w")
import io
import json
import os
from tkinter import *
import tkinter as tk
import datetime
import traceback
from quickini import QuickIni
try:
    from PIL import ImageGrab
except:
    import pyscreenshot as ImageGrab
from tk_ToolTip_class101 import CreateToolTip
flush = sys.stdout.flush
from tkinter import font
import font_to_data
root = Tk()
sample_text_file = "sample_text.txt"
root.title("Pixel font viewer")
root.iconbitmap("appicon.ico")
root.configure(background="grey")

root.geometry("300x160")
#DEF_FRAME = (128,128)
DEF_CANVAS = (640,480)
DEF_TEXTAREA = (80,5)
DEF_TEXTWINDOW = (256,256)
DEF_BUTTONSROW = 16

FONT_TYPES = []
for file in os.listdir("fonts"):
    if file.endswith(".png"):
        FONT_TYPES.append(file)
#print(FONT_TYPES)
font12 = font.Font(family='Arial', size=12)
font12 = 'TkFixedFont'

ALLcharacters = []

textwindow = None
optionswindow = None


def update_font(font_id = None):
    if(font_id==None):
        font_id = current_font
    global FONT_WIDTH, FONT_HEIGHT, FONT_BACKGROUND
    FONT_WIDTH = ALLcharacters[current_font]["width"]
    FONT_HEIGHT = ALLcharacters[current_font]["height"]
    def rgb_to_hex(r,g,b):
        return (("#%02x%02x%02x") % (r, g, b))
    FONT_BACKGROUND = rgb_to_hex(*ALLcharacters[current_font]["background"])
    
#Nonwithstanding existing .ini file
FONT_WIDTH = 2
FONT_HEIGHT = 4
FONT_BACKGROUND = "black"
SKIP_MISSING = True
spacesize = 1
font_hsep = 0
font_vsep = 1
font_x0 = 1
font_y0 = 1
force_case = 0
superpose_missing_accents = True
accent_vertical_gap = 1
fill_missing_with_unidecode = True
missing_character_character = "?"

current_font = 0

current_kerning = 1
kerning_data = "BBox"
temp_kernings = dict()

LEFT_ALIGN = 0
CENTER_ALIGN = 1
RIGHT_ALIGN = 2
JUSTIFY_ALIGN = 3
alignment = JUSTIFY_ALIGN

def font_name(id=None):
    if(id==None):
        id=current_font
    return FONT_TYPES[id]

    
def save_font_options(): #current_height, current_width):
    filename="fonts"+os.sep+font_name()[:-4]+".ini"
    ini = QuickIni(filename)
    ini+= "font_hsep",font_hsep
    ini+= "font_vsep",font_vsep
    ini+= "spacesize",spacesize
    ini+= "capsstate",force_case
    ini+= "kerning",current_kerning
    ini.save()
    if(isinstance(kerning_data,dict)):
        save_json(kerning_filename(current_font,current_kerning),kerning_data)
    
def load_font_options(filename="default_options",silent=True):
    try:
        global font_hsep,\
               font_vsep,\
               spacesize,\
               force_case,\
               current_kerning
        filename="fonts"+os.sep+font_name()[:-4]+".ini"
        ini = QuickIni(filename)
        ini.load()
        
        font_hsep = ini.get("font_hsep",1)
        font_vsep = ini.get("font_vsep",2)
        spacesize = 3>ini>"spacesize"
        force_case   = 0>ini>"capsstate"
        current_kerning  = 1>ini>"kerning"
        update_font()
        set_kerning(current_kerning)
    except Exception as e:
        print(e)
        pass

def save_global_options():
    filename = "settings.ini"    
    ini = QuickIni(filename)
    ini += "font_name",font_name()
    ini += "font_x0",font_x0
    ini += "font_y0",font_y0
    #ini += "current_height",current_height
    #ini += "current_width",current_width
    ini.save()
    
def load_global_options():
    global current_font, font_x0, font_y0
    filename = "settings.ini"
    ini = QuickIni(filename)
    try:
        ini.load()
    except:
        pass
    current_font = FONT_TYPES.index(ini.get("font_name",font_name()).strip())
    font_x0 = ini/("font_x0",7)
    font_y0 = ini/("font_y0",7)

def subimage(sheet, l, t, r, b):
    #https://stackoverflow.com/questions/16579674/using-spritesheets-in-tkinter
    dst = tk.PhotoImage()
    dst.tk.call(dst, 'copy', sheet, '-from', l, t, r, b, '-to', 0, 0)
    return dst

def screenshot(canvas,text):
    #https://stackoverflow.com/questions/47653748/performing-imagegrab-on-tkinter-screen
    #print(box)
    flush()
    time = str(datetime.datetime.now()).replace(":","-")
    image_name = text[:10]+"_"+time+".png"
    image_name = os.path.join("images",image_name)
    #Avoid the weird window that appears during the imagegrab
    rx,ry = root.winfo_x(), root.winfo_y()
    ww = root.winfo_screenwidth()
    rw = root.winfo_width()
    #root.geometry(("+%d+%d")%(ww/2+rw/2, ry))
    #root.update_idletasks()
        
    box = (canvas.winfo_rootx(),canvas.winfo_rooty(),canvas.winfo_rootx()+canvas.winfo_width(),canvas.winfo_rooty() + canvas.winfo_height())
    shot = ImageGrab.grab(box)
    shot.save(image_name)
    
    #root.geometry(("+%d+%d")%(rx , ry))
    #root.update_idletasks()
    
    return image_name
    
try:
    import win32clipboard
    
    #global send_to_clipboard, copy_screenshot_to_clipboard
    def send_to_clipboard(clip_type, data):
        #https://stackoverflow.com/questions/7050448/write-image-to-windows-clipboard-in-python-with-pil-and-win32clipboard/7052068#7052068
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()
    
    def copy_screenshot_to_clipboard(canvas):
        #Avoid the weird window that appears during the imagegrab
        rx,ry = root.winfo_x(), root.winfo_y()
        ww = root.winfo_screenwidth()
        rw = root.winfo_width()
        #root.geometry(("+%d+%d")%(ww/2+rw/2, ry))
        #root.update_idletasks()
        
        box = (canvas.winfo_rootx(),canvas.winfo_rooty(),canvas.winfo_rootx()+canvas.winfo_width(),canvas.winfo_rooty() + canvas.winfo_height())
        shot = ImageGrab.grab(box)
        
        #root.geometry(("+%d+%d")%(rx , ry))
        #root.update_idletasks()
        
        output = io.BytesIO()
        shot.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        
        send_to_clipboard(win32clipboard.CF_DIB, data)
        

except Exception as e:
    print(e)
    send_to_clipboard = None
    copy_screenshot_to_clipboard = None
    print("Clipboard capabilities not enabled, try\n\t pip install pywin32")

    

def touch_kerning_generate(fontid=None):
    #x-axis touch
    if(fontid==None):
        fontid = current_font
    background = tuple(ALLcharacters[fontid]["background"])
    kerning_data = dict()
    #print(ALLcharacters)
    for first in tuple(ALLcharacters[fontid]): 
        if(len(first)==1):
            for sec in tuple(ALLcharacters[fontid]): 
                if(len(sec)==1) :
                    leftimage = ALLcharacters[fontid][first]
                    rightimage = ALLcharacters[fontid][sec]
                    lw, lh = leftimage.width(), leftimage.height()
                    rw, rh = rightimage.width(), rightimage.height()
                    limit = int(min(rw/2,lw/2))
                    kerning = limit
                    for j in range(min(lh, rh)):
                        li = 0
                        while(li<kerning and tuple(leftimage.get(lw-li-1,j))==background):
                            li+=1
                        if(background==(0,0,0) and list(leftimage.get(lw-li-1,j))[::-1]>[0,0,255]):
                            li-=1 #Non-red END pixel on black bakground
                        ri = 0
                        while(li+ri<kerning and tuple(rightimage.get(ri,j))==background):
                            ri+=1
                        kerning = min(kerning, li+ri)
                    if(kerning!=0):
                        kerning_data[first+sec]=kerning
    return kerning_data
from math import ceil, floor, sqrt
def diagonal_touch_kerning_generate(fontid=None):
    #throw diagonals to avoid
    if(fontid==None):
        fontid = current_font
    background = tuple(ALLcharacters[fontid]["background"])
    kerning_data = dict()
    #print(ALLcharacters)
    for first in tuple(ALLcharacters[fontid]): 
        if(len(first)==1):
            for sec in tuple(ALLcharacters[fontid]): 
                if(len(sec)==1) :
                    leftimage = ALLcharacters[fontid][first]
                    rightimage = ALLcharacters[fontid][sec]
                    lw, lh = leftimage.width(), leftimage.height()
                    rw, rh = rightimage.width(), rightimage.height()
                    limit = int(min(rw/2,lw/2))
                    kerning = limit
                    leftsides = [limit]*lh
                    for j in range(lh):
                        li = 0
                        while(li<kerning and tuple(leftimage.get(lw-li-1,j))==background):
                            li+=1
                        if(background==(0,0,0) and list(leftimage.get(lw-li-1,j))[::-1]>[0,0,255]):
                            li-=1 #Non-red END pixel on black bakground
                        #if(background==(0,0,0)):
                        #    li-=1
                        leftsides[j]=li
                    for j in range(rh):
                        ri = 0
                        while(ri<kerning and tuple(rightimage.get(ri,j))==background):
                            ri+=1
                        for lj in range(lh):
                            li = leftsides[lj]+floor(abs(lj-j)*0.95)
                            kerning = min(kerning, li+ri)
                        # kerning = min(leftsides)+ri
                    if(kerning!=0):
                        kerning_data[first+sec]=kerning
    return kerning_data
                    
def distance_touch_kerning_generate(fontid=None,distance=None):
    #distance
    if(distance==None):
        distance=font_hsep
    if(fontid==None):
        fontid = current_font
    background = tuple(ALLcharacters[fontid]["background"])
    kerning_data = dict()
    #print(ALLcharacters)
    for first in tuple(ALLcharacters[fontid]): 
        if(len(first)==1):
            for sec in tuple(ALLcharacters[fontid]): 
                if(len(sec)==1) :
                    leftimage = ALLcharacters[fontid][first]
                    rightimage = ALLcharacters[fontid][sec]
                    lw, lh = leftimage.width(), leftimage.height()
                    rw, rh = rightimage.width(), rightimage.height()
                    limit = int(min(rw/2,lw/2))
                    kerning = limit
                    leftsides = [limit]*lh
                    for j in range(lh):
                        li = 0
                        while(li<kerning and tuple(leftimage.get(lw-li-1,j))==background):
                            li+=1
                        if(background==(0,0,0) and list(leftimage.get(lw-li-1,j))[::-1]>[0,0,255]):
                            li-=1 #Non-red END pixel on black bakground
                        leftsides[j]=li
                    for j in range(rh):
                        ri = 0
                        while(ri<kerning and tuple(rightimage.get(ri,j))==background):
                            ri+=1
                        for lj in range(lh):
                            dy=abs(lj-j)*0.95
                            dx=leftsides[lj]+ri
                            if(dy<=distance):
                                kerning = min(kerning, floor(dx-sqrt(distance**2-dy**2)))
                    if(kerning+font_hsep!=0):
                        kerning_data[first+sec]=kerning+font_hsep
    return kerning_data
from statistics import median
def touch_average_kerning_generate(fontid=None):
    #Inspired by Shoebox's description of their algorithm (not at all similar)
    #x-axis average
    if(fontid==None):
        fontid = current_font
    background = tuple(ALLcharacters[fontid]["background"])
    #print(ALLcharacters)
    kerning_data = dict()
    kernings = []
    for first in tuple(ALLcharacters[fontid]): 
        if(len(first)==1):
            for sec in tuple(ALLcharacters[fontid]): 
                if(len(sec)==1) :
                    leftimage = ALLcharacters[fontid][first]
                    rightimage = ALLcharacters[fontid][sec]
                    lw, lh = leftimage.width(), leftimage.height()
                    rw, rh = rightimage.width(), rightimage.height()
                    left_limit = floor(lw*2/3)
                    right_limit = floor(rw*2/3)
                    avsum = 0
                    avdiv = 0
                    for j in range(min(lh, rh)):
                        li = 0
                        while(li<left_limit and tuple(leftimage.get(lw-li-1,j))==background):
                            li+=1
                        if(background==(0,0,0) and list(leftimage.get(lw-li-1,j))[::-1]>[0,0,255]):
                            li-=1 #Non-red END pixel on black bakground ##SHOULDN'T be used on those anyway
                        ri = 0
                        while(ri<right_limit and tuple(rightimage.get(ri,j))==background):
                            ri+=1
                        if(li<left_limit and ri<right_limit):
                            avsum += li+ri
                            avdiv += 1
                            
                    if(avdiv>0):
                        kerning = round(avsum/avdiv)
                    else:
                        kerning = int(min(rw/2,lw/2))
                    kernings.append(kerning)
                    kerning_data[first+sec]=kerning
    zero_kerning = median(kernings)
    for first in tuple(ALLcharacters[fontid]): 
        if(len(first)==1):
            for sec in tuple(ALLcharacters[fontid]): 
                if(len(sec)==1) :
                    kerning_data[first+sec]-=zero_kerning
    for k in list(kerning_data.keys()):
        if(kerning_data[k]==0):
            kerning_data.pop(k)
    return kerning_data
                    
def text_data_measure(text_data):
    measured_width = 0
    for line in text_data:
        measured_width=max(text_data_line_width(line),measured_width)
    measured_height = lines_height(len(text_data))
    #print(len(text_data),"lines")
    #print(text_data)
    return measured_width,measured_height
    

try:    from unidecode import unidecode
except Exception as e: print(e)
#https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string

letter_bases={
    "áàâäãå":"a",
    "ÁÀÂÄÃÅ":"A",
    "éèêë"  :"e",
    "ÉÈÊË"  :"E",
    "iíìîï"  :"ı",
    "İÍÌÎÏ"  :"I",
    "óòôöõ" :"o",
    "ÓÒÔÖÕ" :"O",
    "úùûü"  :"u",
    "ÚÙÛÜ"  :"U",
    "ÿ"     :"y",
    "Ÿ"     :"Y",
    "ñ"     :"n",
    "Ñ"     :"N"
}
accent_bases={
"áÁéÉíÍóÓúÚ"    :"´",
"àÀèÈìÌòÒùÙ"    :"`",
"âÂêÊîÎôÔûÛ"    :"^",
"äÄëËïÏöÖüÜÿŸ"  :"¨",
"åÅ"            :"°",
"ãÃõÕñÑ"        :"~"

}

	
all_accents="áÁéÉíÍóÓúÚàÀèÈìÌòÒùÙâÂêÊîÎôÔûÛäÄëËïÏöÖüÜÿŸåÅãÃõÕñÑ"
all_accents="ÀÁÂÃÄÅÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜàáâãäåèéêëìíîïñòóôõöùúûüÿŸ"
#https://www.fonts.com/content/learning/fontology/level-3/signs-and-symbols/accents

def image_top(image):
    background = tuple(ALLcharacters[current_font]["background"])
    for j in range(image.height()):
        for i in range(image.width()):
            color = tuple(image.get(i,j))
            if(color!=background):
                # print(color,background)
                return j
    return 0
    
def image_bottom(image):
    background = tuple(ALLcharacters[current_font]["background"])
    for j in range(image.height()):
        for i in range(image.width()):
            color = tuple(image.get(i,image.height()-j-1))
            if(color!=background):
                # print(color,background)
                return image.height()-j
    return image.height()


def get_char_image(char):
    return ALLcharacters[current_font].get(char,None)

def lines_height(lines):
    return lines*FONT_HEIGHT+(max(0,lines-1))*font_vsep
    
def word_width(word):
    xlong = 0
    for char in word:
        if(char == " "):
            xlong+=spacesize
        else:
            xlong+=get_char_width(char)+font_hsep
    xshort = xlong
    for i in range(len(word)-1,-1,-1):
        if(word[i]==" "):
            xshort-=spacesize
        else:
            break
    xshort-=font_hsep
    return xlong, xshort
    
def cut_word(word,pixels_width):
    cutoff = len(word)
    for i in range(len(word)):
        xlong,xshort = word_width(word[:i])
        if(xshort>pixels_width):
            cutoff=i-1
            #print(xshort,word[:cutoff])
            break
    cutoff=max(cutoff,1)
    return word[:cutoff], word[cutoff:]
    
def wrap_text(pixels_width, pixels_height, text, leave_early = False):
    #print("force_case is:",force_case)
    if(force_case==1):
        text = text.upper()
    elif(force_case==2):
        text = text.lower()
        
    text=text.replace(" !","\t!")
    text=text.replace(" ?","\t!")
    lines = text.split("\n")
    
    #print("Width:",pixels_width)
    pixels_width = max(FONT_WIDTH+font_hsep,pixels_width)
    #print("Corrected:",pixels_width)
    #print("Font width:",FONT_WIDTH)
    #print("Hsep:",font_hsep)
    #print("Spacesize:",spacesize)
    #flush()
    datalines = []
    for textline in lines:
        current_width = 0
        current_line = []
        words = textline.split(" ")
        
        while(len(words)>0):
            word = words.pop(0)
            word = word.replace("\t"," ")
            word_data = []
            for i,letter in enumerate(word):
                letter = word[i]
                if(i+1==len(word)):
                    next_letter=None
                else:
                    next_letter = word[i+1]
                word_data.extend(determine_character(letter,next_letter,missing_character_character))
            word_width = text_data_line_width(word_data)-font_hsep
            if(current_width+word_width<=pixels_width):
                #Word fits
                current_width+=word_width+font_hsep+determine_character(" ")[0][1]
                current_line.extend(word_data)
                current_line.extend(determine_character(" "))
            elif(current_width==0):
                #Pixel width too small for even one word
                word_width = 0
                result_index = 0
                for index,(chr,shift) in enumerate(word_data):
                    word_width+=shift
                    if(word_width>pixels_width):
                        break
                    result_index = index
                partial_word = word_data[:result_index+1] ###What about accents? #We are already in a special case anyway
                #print("PARTIAL WORD:",word[:result_index+1])
                words.insert(0,word[result_index+1:])
                
                
                # text_data_trim_end_spaces(partial_word)
                # text_data_trim_lead_spaces(partial_word)
                datalines.append(partial_word)
                current_width = 0
                current_line=[]
            else:
                #First word of next line
                text_data_trim_end_spaces(current_line)
                # text_data_trim_lead_spaces(current_line)
                datalines.append(current_line)
                current_width = 0
                current_line=[]
                words.insert(0,word)
        if(current_width>0):
            #No more words to process in line.
            text_data_trim_end_spaces(current_line)
            # text_data_trim_lead_spaces(current_line)
            datalines.append(current_line)
            current_width=0
            current_line=[]
                
        if(lines_height(len(datalines)+1)>pixels_height and leave_early):
            #print("early",datalines)
            return datalines
            
    #print("Datalines",len(datalines),datalines)
    return datalines
    
def determine_character(letter,next_letter=None,missing_letter_character=None):
    #returns a list of characters (because of accents)
    accent_image = None
    accent_width = None
    accent_shift = None
    kerning = 0
    if(letter==" "):
        return [(None,spacesize)]
    else:
        char_image = get_char_image(letter)
        if(char_image==None and letter in all_accents and superpose_missing_accents):
            #Returns a [Base, Accent] pair
            try:
                letter_base, accent_base = None, None
                for key in letter_bases:
                    if(letter in key):
                        letter_base=letter_bases[key]
                        break
                for key in accent_bases:
                    if(letter in key):
                        accent_base=accent_bases[key]
                        break
                char_image = get_char_image(letter_base) or get_char_image(unidecode(letter_base))
                accent_image = get_char_image(accent_base)
                accent_width = get_char_width(accent_base)
                #print("Accented letter:",letter_base,"+",accent_base)
                
                #canvas.create_image(x, y, anchor=NW, image=letter_image)
                top=image_top(char_image)
                bottom = image_bottom(accent_image)
                # print("Top:",top," - Bottom:",bottom)
                #bottom=accent_image.height()
                h_shift = round(float(char_image.width()-accent_image.width())/2)
                accent_shift = top-bottom-accent_vertical_gap
                # print("Width letter:",get_char_width(letter_base)," - Width accent:",get_char_width(accent_base))
                # print("h_shift:",h_shift)
                #canvas.create_image(x+h_shift, y+v_shift, anchor=NW, image=accent_image)
                
            except Exception as e:
                import traceback
                print(e)
                traceback.print_exc()
        
        if(letter=="I" and get_char_image("İ")!=None):
            char_image = get_char_image("İ")
            letter = "İ"
            
        if(char_image==None and letter=="I" and get_char_image("İ")!=None):
            #In case the text contains I but only İ is given, it is replaceable
            char_image = get_char_image("İ")
            letter = "İ"
            
        if(char_image==None and fill_missing_with_unidecode):
            # print("Could not find replacement for ",letter)
            letter=unidecode(letter)
            char_image = get_char_image(letter)
            # print(letter,char_image)
            
        if(char_image==None):
            #print("Could not find character",letter,"in",ALLcharacters[current_font])
            if(SKIP_MISSING):
                return([])
            elif(missing_letter_character==None):
                return [(None,spacesize)]
            else:
                return determine_character(missing_letter_character,next_letter,None)
            
        if(char_image!=None):
            width = char_image.width()
            
            if(isinstance(kerning_data,dict)):
                kerning = kerning_data.get(letter+str(next_letter),0)
            elif(current_kerning==K_BBOX):
                kerning==0
            elif(current_kerning==K_MONO):
                width = FONT_WIDTH
                kerning = 0
            if(accent_image):
                decal = (width-accent_width)//2
                return [(char_image,decal),((accent_image,accent_shift),width-kerning+font_hsep-decal)]
            else:
                return [(char_image,width-kerning+font_hsep)]
    return []
    

            
def text_data_line_width(text_data_line):
    x=0
    for ch_image,shift in text_data_line:
        x+=shift
    return x

def text_data_count_spaces(text_data_line):
    count = 0
    for ch_image,shift in text_data_line:
        if ch_image==None:
            count+=1
    return count
def text_data_trim_end_spaces(text_data_line):
    while(text_data_line and text_data_line[-1][0]==None):
        text_data_line.pop(-1)
def text_data_trim_lead_spaces(text_data_line):
    while(text_data_line and text_data_line[0][0]==None):
        text_data_line.pop(0)

def draw_text_data(canvas,drawarea_width,text_data,vscroll=None):
    #Draw the text data that already has been kerned and wrapped by the previous function
    #print("Received",text_data)
    #print("Draw it in",drawarea_width)
    y=font_y0
    for line in text_data:
        #print("Line",y,line)
        #print("Before trim:")
        #print(line)
        text_data_trim_end_spaces(line)
        text_data_trim_lead_spaces(line)
        #print("After trim:")
        #print(line)
        x=font_x0
        linewidth = text_data_line_width(line)-font_hsep
        if(alignment==CENTER_ALIGN):
            x+=(drawarea_width-linewidth)//2
        elif(alignment==RIGHT_ALIGN):
            x+=drawarea_width-linewidth
        elif(alignment==JUSTIFY_ALIGN):
            align_missing = drawarea_width-linewidth
            align_shifted=0
            align_counter=0
            align_step = align_missing/max(text_data_count_spaces(line),1)
        for ch_image,shift in line:
            if(ch_image!=None):
                if(isinstance(ch_image,tuple)):
                    #accent with height
                    ch_image,height = ch_image
                    canvas.create_image(x, y+height, anchor=NW, image=ch_image)
                else:
                    canvas.create_image(x, y, anchor=NW, image=ch_image)
            x+=shift
            if(alignment==JUSTIFY_ALIGN and ch_image==None):
                #On spaces, fill the missing void by integer amount until the max amount is reached
                align_counter+=align_step
                difference = min(round(align_counter-align_shifted),align_missing-align_shifted)
                align_shifted+=difference
                x+=difference 
                #SHOULD not justify is single line doesn't reach the end.
                #Only justify if wrapped around - so more infos are needed
        y+=FONT_HEIGHT+font_vsep
    
K_BBOX = 1
K_MONO = 0
K_PACKX = 2
K_DIAG = 3
K_DIST = 4
K_AVGAREA = 5
K_CUSTOM = 6
KERNING_TYPES = ("Fixed Width","Bounding Box","Pack in X","Diagonal Fit","Distance","Average Area")
def kerning_full_name(kerning_id):
    return KERNING_TYPES[kerning_id]

def kerning_filename(font_id,kerning_id):
    compact_names = ("Mono","BBox","PackX","Diag","Dist","AvgArea","Custom")
    filename = font_name(font_id)[:-4] + ".Kern" + compact_names[kerning_id] 
    if(kerning_id==K_DIST):
        filename+=str(font_hsep)
    return filename
    
def set_kerning(kerning_id):
    #Order: remember temp kerning, load existing kerning, regenerate kerning.
    font_id = current_font
    global kerning_data, current_kerning
    kerning_data = temp_kernings.get(kerning_filename(font_id,kerning_id),None)
    if(kerning_data==None):
        try:
            kerning_data = load_json(kerning_filename(font_id,kerning_id))
        except:
            kerning_generate = ["BBox","Mono",touch_kerning_generate,diagonal_touch_kerning_generate,distance_touch_kerning_generate,touch_average_kerning_generate]
            if not isinstance(kerning_generate[kerning_id],str):
                kerning_data = kerning_generate[kerning_id](font_id)
            else:
                kerning_data=kerning_generate
            temp_kernings[kerning_filename(font_id,kerning_id)]=kerning_data
    current_kerning = kerning_id 

def load_json(filename):
    with io.open(os.path.join("fonts",filename),'r',encoding='utf8') as f:
        jsondict = json.load(f)
    return jsondict
    
def save_json(filename,dict_data):
    jsonform = json.dumps(dict_data,indent=4,separators=(',', ': '))
    with io.open(os.path.join("fonts",filename),'w',encoding='utf8') as f:
        f.write(jsonform)
        

def load_mini_fonts():
    working_fonts=[]
    for FONTNAME in FONT_TYPES:
        
        #Load WIDE
        fontbase = PhotoImage(file=os.path.join("fonts",FONTNAME))
        fontdata = dict()
        posdict_generated = False
        tries = 0
        while tries < 2:
            tries +=1
            try:
                with io.open(os.path.join("fonts",FONTNAME[:-4]+".json"),'r',encoding='utf8') as f:
                    posdict = json.load(f)
                    
                for key in posdict:
                    if(len(key)==1):
                        #character
                        x,y,w,h = posdict[key]
                        fontdata[key] = subimage(fontbase, x, y, x+w, y+h)#or y+posdict["height"] not much difference
                    else:
                        #background, width, height
                        fontdata[key]=posdict[key]
                ALLcharacters.append(fontdata)
                s = str(fontdata).encode(sys.stdout.encoding or "utf-8", "replace")
                working_fonts.append(FONTNAME)
                #touch_kerning_generate(len(ALLcharacters)-1)
                tries = 2
                #print(FONTNAME,s)    
            except Exception as e:
                if(posdict_generated):
                    print("Could not load",FONTNAME,"due to:")
                    print(e)
                    #traceback.print_exc()
                    print("-"*10)
                else:
                    try:
                        print("New font detected:")
                        font_to_data.generate_data("fonts"+os.sep+FONTNAME)
                        print("Generated",FONTNAME[:-4]+".json")
                        posdict_generated = True
                    except Exception as e:
                        print("Could not generate font data for",FONTNAME,", is the descriptive .txt missing?")
                        print(e)
                        traceback.print_exc()
                        print("-"*10)
                    #Generate the json the first time the font is loaded
    FONT_TYPES[:]=working_fonts
    update_font()
    #print(current_font,font_name(),ALLcharacters[current_font]["background"])
    
def get_char_width(character):
    try:
        return get_char_image(character).width()
    except Exception as e:
        # print("Could not find character in font",character,font_name())
        return ALLcharacters[current_font]["width"]
                
def load_special_chars(frame,textarea):
    filename = "button_special_chars.txt"
    with io.open(filename,'r',encoding='utf8') as f:
        text = f.read()
        
        charsframe = Frame(frame, bg="gray20")
        charsframe.pack(fill=BOTH, expand=YES)
        counter = 0;
        for character in text:
            def char_command(current_char):
                def place_char():
                    textarea.insert(INSERT,current_char)
                    textarea.event_generate("<Key>")
                return place_char
            counter += 1
            if(counter > DEF_BUTTONSROW):
                charsframe = Frame(frame, bg="gray20")
                charsframe.pack(fill=BOTH, expand=YES)
                counter=1
            button = Button(charsframe,text=character,command=char_command(character),font=font12)
            button.pack(side = LEFT)
            
def create_textwindow(root,textvariable):
    global textwindow
    
    
    if textwindow == None or not textwindow.winfo_exists():
        textwindow = Toplevel()
        textwindow.title("Text input")
        mainframe = Frame(textwindow, bg="gray10")
        mainframe.pack(fill=BOTH, expand=YES)
        textarea = Text(mainframe, width=DEF_TEXTAREA[0], height=DEF_TEXTAREA[1],bg="black", fg="white",insertbackground="white")
        
        textarea.insert(END, textvariable.get())
        line=textvariable.get().count("\n")
        column=len((textvariable.get().split())[-1])
        #https://stackoverflow.com/questions/3215549/set-cursor-position-in-a-text-widget
        textarea.mark_set("insert", "%d.%d" % (line + 1, column + 1))
        
        textarea.pack(side=TOP,fill=BOTH, expand=YES)
        textarea.focus_force()
        textarea.lower()
        def update_text(*args):
            textarea.after(100, lambda:
                textvariable.set(textarea.get('1.0', 'end-1c'))
                )
            textwindow.title("Text input (*)")
        textarea.bind("<Key>", update_text)
        textwindow.important = textarea
        
        bottomFrame = Frame(textwindow, bg="gray10")
        bottomFrame.pack(side=BOTTOM,fill=X)
        load_special_chars(bottomFrame,textarea)
        
        
        
        dx = 8
        textwindow.geometry(("+%d+%d")%(
            root.winfo_x()+root.winfo_width()+2*dx,root.winfo_y()+root.winfo_height()-DEF_TEXTWINDOW[1]))
            
        textwindow.geometry(("%dx%d")%(DEF_TEXTWINDOW[0],DEF_TEXTWINDOW[1]))
            
        textarea.previous_text = textarea.get('1.0', 'end-1c')
        
        def save_text_loop():
            current_text = textarea.get('1.0', 'end-1c')
            if(textarea.previous_text != current_text):
                with io.open(sample_text_file,'w',encoding='utf8') as f:
                    f.write(current_text)
            textwindow.title("Text input")
            textarea.after(5000, save_text_loop)
                
        textarea.after(5000, save_text_loop)
    elif(textwindow!=None and textwindow.winfo_exists()):
        dx = textwindow.winfo_rootx()-textwindow.winfo_x()
        #print(dx)
        #flush()
        textwindow.important.focus_force()
        textwindow.geometry(("+%d+%d")%(
            root.winfo_x()+root.winfo_width()+2*dx,root.winfo_y()+root.winfo_height()-textwindow.winfo_height()))

def create_optionswindow(root,size_callback):
    global optionswindow
    
    if optionswindow == None or not optionswindow.winfo_exists():
        optionswindow = Toplevel(root)
        optionswindow.title("Change options")
        mainframe = Frame(optionswindow, bg="gray10")
        mainframe.pack(fill=BOTH, expand=YES)
        
        leftframe = Frame(mainframe)
        leftframe.pack(side=LEFT,fill=BOTH, expand=YES)
        rightframe = Frame(mainframe)
        rightframe.pack(side=RIGHT,fill=BOTH, expand=YES)
        
        
        
        
        recapbglabel = Label(rightframe,text="Font bg: ")
        recapbglabel.pack(side=TOP)
        recapsizelabel = Label(rightframe,text="Size : ")
        recapsizelabel.pack(side=TOP)
        
        
        
        Label(leftframe,text="Font type:").pack(side=TOP)
        ftvar = StringVar(value = font_name())
        sb = Spinbox(leftframe, width=22, values=FONT_TYPES,textvariable = ftvar)
        sb.pack(side=TOP)
        sb.delete(0,"end")
        sb.insert(0,font_name()) #for some reason, doesn't get the right default value
        #print(sb.get())
        def ftfun(*args):
            global current_font
            current_font = FONT_TYPES.index(ftvar.get())
            save_global_options()
            update_font(current_font)
            load_and_update() #changing fonts can change the options
            set_kerning(current_kerning)
            size_callback()
        ftvar.trace("w",ftfun)
        CreateToolTip(sb,"\n".join(reversed(FONT_TYPES)))
        
        def recaplabel_update():
            recapbglabel.config(text="Font bg: "+str(FONT_BACKGROUND))
            recapsizelabel.config(text="Size: "+str(FONT_WIDTH)+"×"+str(FONT_HEIGHT))
        recaplabel_update()
        
        Label(leftframe,text="Horizontal separation").pack(side=TOP)
        hsepvar = IntVar(value=font_hsep)
        Spinbox(leftframe,textvariable = hsepvar,width=3, from_=-64, to=64).pack(side=TOP)
        def hsepfun(*args):
            global font_hsep
            font_hsep = hsepvar.get()
            if(current_kerning==K_DIST):
                set_kerning(current_kerning)
            size_callback()
        hsepvar.trace("w",hsepfun)
        
        Label(rightframe,text="Vertical separation").pack(side=TOP)
        vsepvar = IntVar(value=font_vsep)
        Spinbox(rightframe,textvariable = vsepvar,width=3, from_=-64, to=64).pack(side=TOP)
        def vsepfun(*args):
            global font_vsep
            font_vsep = vsepvar.get()
            size_callback()
        vsepvar.trace("w",vsepfun)
        
        Label(leftframe,text="Border width").pack(side=TOP)
        x0var = IntVar(value=font_x0)
        Spinbox(leftframe,textvariable = x0var,width=3, from_=0, to=64).pack(side=TOP)
        def x0fun(*args):
            global font_x0
            font_x0 = x0var.get()
            size_callback()
        x0var.trace("w",x0fun)
        
        Label(rightframe,text="Border height").pack(side=TOP)
        y0var = IntVar(value=font_y0)
        Spinbox(rightframe,textvariable = y0var,width=3, from_=0, to=64).pack(side=TOP)
        def y0fun(*args):
            global font_y0
            font_y0 = y0var.get()
            size_callback()
        y0var.trace("w",y0fun)
        
        Label(rightframe,text="Space character width").pack(side=TOP)
        spvar = IntVar(value=spacesize)
        
        spaceframe = Frame(rightframe)
        spaceframe.pack(side=TOP)
        
        Spinbox(spaceframe,textvariable = spvar,width=3, from_=0, to=128).pack(side=LEFT)
        def spfun(*args):
            global spacesize
            spacesize = spvar.get()
            size_callback()
        spvar.trace("w",spfun)
        
        def setmonospace(*args):
            spvar.set(FONT_WIDTH+font_hsep)
        Button(spaceframe,text="Width+HSep",command=setmonospace).pack(side=LEFT)
        
        
        Label(leftframe,text="Convert case").pack(side=TOP)
        capvar = IntVar(value=force_case)
        #Checkbutton(leftframe,text="",variable = capvar).pack(side=TOP)
        radioframe=Frame(leftframe)
        for index,text in enumerate(("No","CAP","low")):
            rb = Radiobutton(radioframe, text=text,variable=capvar, value=index)
            rb.pack(side=LEFT)
        def capfun(*args):
            global force_case
            force_case = capvar.get()
            size_callback()
        radioframe.pack(side=TOP)
        capvar.trace("w",capfun)
        capvar.set(force_case)
        
        
        
        Label(leftframe,text="Alignment").pack(side=TOP)
        alignvar = IntVar(value=alignment)
        #Checkbutton(leftframe,text="",variable = capvar).pack(side=TOP)
        radioframe=Frame(leftframe)
        for index,text in enumerate(("←","→←","→","↔")):
            rb = Radiobutton(radioframe, text=text,variable=alignvar, value=index)
            rb.pack(side=LEFT)
        def alignfun(*args):
            global alignment
            alignment = alignvar.get()
            size_callback()
        radioframe.pack(side=TOP)
        alignvar.trace("w",alignfun)
        alignvar.set(force_case)
        
        
        
        
        def save_and_clean():
            save_font_options()
            #clean_unused_kerning[TODO]
        Button(rightframe,text="Save options",command=save_and_clean).pack(side=BOTTOM)
        
        def load_and_update(*args):
            load_font_options("fonts"+os.sep+font_name()[:-4]) #Try to load specific options, otherwise do nothing
            size_callback()
            hsepvar.set(font_hsep)
            vsepvar.set(font_vsep)
            x0var.set(font_x0)
            y0var.set(font_y0)
            spvar.set(spacesize)
            capvar.set(force_case)
            kernvar.set(kerning_full_name(current_kerning))
            recaplabel_update()
            #ftvar.set(FONT_TYPES[current_font])
            

        undobutton = Button(leftframe,text="Undo changes",command=load_and_update)
        undobutton.pack(side=BOTTOM)
        CreateToolTip(undobutton,"Load last saved options")
        
        Label(leftframe,text="Letters spacing:").pack(side=BOTTOM)
        kernvar = StringVar(value = kerning_full_name(current_kerning))
        sk = Spinbox(rightframe, width=22, values=KERNING_TYPES,textvariable=kernvar)
        sk.pack(side=BOTTOM)
        sk.delete(0,"end")
        sk.insert(0,kerning_full_name(current_kerning)) #for some reason, doesn't get the right default value
        def kfun(*args):
            global current_kerning
            current_kerning=KERNING_TYPES.index(kernvar.get())
            set_kerning(current_kerning)
            size_callback()
        kernvar.trace("w",kfun)
        CreateToolTip(sk,"\n".join(reversed(KERNING_TYPES)))
        
        
        ftvar.set(font_name())
        
        
        """
        Label(rightframe,text="AAAAAAAAA").pack()
        XXXXX = IntVar(value=YYYYYY)
        Spinbox(rightframe,textvariable = XXXXX,width=3, from_=0, to=10).pack()
        def XXXXXfun(*args):
            YYYYYY = XXXXX.get()
            change_callback()
        XXXXX.trace("w",change_callback)
        
        Label(leftframe,text="AAAAAAAAA").pack()
        XXXXX = IntVar(value=YYYYYY)
        Spinbox(leftframe,textvariable = XXXXX,width=3, from_=0, to=10).pack()
        def XXXXXfun(*args):
            YYYYYY = XXXXX.get()
            change_callback()
        XXXXX.trace("w",change_callback)"""
    
            
        
        dx = 8
        optionswindow.geometry(("+%d+%d")%(
            root.winfo_x()+root.winfo_width()+2*dx,root.winfo_y()))
    elif(optionswindow!=None and optionswindow.winfo_exists()):
        dx = optionswindow.winfo_rootx()-optionswindow.winfo_x()
        #print(dx)
        #flush()
        optionswindow.focus_force()
        optionswindow.geometry(("+%d+%d")%(
            root.winfo_x()+root.winfo_width()+2*dx,root.winfo_y()))
        
        
if(__name__ == "__main__"):
    load_mini_fonts()
    try:
        #canvaswidth,canvasheight=
        load_global_options()
        if(not load_font_options("fonts"+os.sep+font_name()[:-4])):
            #Try to load specific options, otherwise load default ones
            load_font_options(silent=False)
    except Exception as e:
        print(e)
        raise(e)
    canvaswidth = DEF_CANVAS[0]
    canvasheight = DEF_CANVAS[1]
    
    windowText = StringVar()
    #Default temporary text
    try:
        with io.open(sample_text_file,'r',encoding='utf8') as f:
            windowText.set(f.read())
    except:
        windowText.set("""I am the most hideous creature in the realm. 
A more abject appearance you will not find.

I have fallen countless times before your troops, and yet I am here.
Is it not proof that I possess the stone of life?""")
    
    
    myframe = Frame(root, bg="gray10")
    myframe.pack(fill=BOTH, expand=YES)
    canvasframe = Frame(myframe, bg="gray10")
    mycanvas = Canvas(canvasframe,
        width=canvaswidth, height=canvasheight, bg=FONT_BACKGROUND, highlightthickness=0, scrollregion=(0,0,canvaswidth,canvasheight))
        
    hbar=Scrollbar(myframe,orient=HORIZONTAL)
    hbar.pack(side=BOTTOM,fill=X)
    hbar.config(command=mycanvas.xview)
    vbar=Scrollbar(myframe,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    canvasframe.pack(side=LEFT,fill=BOTH, expand=YES)
    vbar.config(command=mycanvas.yview)
    mycanvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    #https://stackoverflow.com/questions/18736465/how-to-center-a-tkinter-widget
    mycanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    #mycanvas.pack(side=TOP)
    #mycanvas.pack(side=LEFT)
    
    mycanvas.current_after = None
    def redraw():
        mycanvas.current_after = None
        mycanvas.delete("all")
        draw_text_data(mycanvas,int(widthBox.get()),wrap_text(int(widthBox.get()),int(heightBox.get()),text=windowText.get()),vbar)
    def change_callback(*args):
        if(mycanvas.current_after != None):
            mycanvas.after_cancel(mycanvas.current_after)
            #If several changes are made in a very little time, don't redraw several times
        mycanvas.current_after = mycanvas.after(5,redraw)
    
    bottomFrame = Frame(root) #Contains several icons
    bottomFrame.pack(side=BOTTOM,fill=X)
    
    coordsFrame = Frame(root) #Contains frame options
    coordsFrame.pack(side=BOTTOM,fill=X)
    
    #WIDTH and HEIGHT areas
    wl = Label(coordsFrame,text="W")
    wl.pack(side=LEFT)
    CreateToolTip(wl,"Width")
    widthVar = IntVar()
    widthVar.set(canvaswidth)
    widthBox = Spinbox(coordsFrame,textvariable = widthVar,width=4, from_=2, to=5120)
    widthBox.pack(side=LEFT)
    
    hl = Label(coordsFrame,text="H")
    hl.pack(side=LEFT)
    CreateToolTip(hl,"Height")
    heightVar = IntVar()
    heightVar.set(canvasheight)
    heightBox = Spinbox(coordsFrame, textvariable = heightVar,width=4, from_=4, to=5120)
    heightBox.pack(side=LEFT)
    
    def sizechange_callback(*args):
        w, h2 = widthVar.get()+font_x0*2, heightVar.get()+font_y0*2
        bottom = bottomFrame.winfo_height()+coordsFrame.winfo_height()+hbar.winfo_height()
        h=min(h2,root.winfo_screenheight()-root.winfo_rooty()-bottom-20)
        mycanvas.config(width=w, height=h, background=FONT_BACKGROUND, scrollregion=(0,0,w,h2))
        dx = root.winfo_rootx()-root.winfo_x()
        
        #if(root.winfo_width()<w or root.winfo_height()-bottom<h):
        fit = ("%dx%d")%(max(160,w+20+vbar.winfo_width()),bottom+h+20)
        #print("Fit to",fit)
        root.geometry(fit)
            
        change_callback()
    
    widthVar.trace("w",sizechange_callback)
    heightVar.trace("w",sizechange_callback)
    
    drag = Label(coordsFrame,text="(?)")
    drag.pack(side=LEFT)
    CreateToolTip(drag,"Drag on the grey area to change the size of the drawing box")
    
    
    def fitToText():
        print("Sent",int(widthBox.get()),int(heightBox.get()))
        wrapped_text_data = wrap_text(int(widthBox.get()),int(heightBox.get()),text=windowText.get(),leave_early=False)
        w,h = text_data_measure(wrapped_text_data)
        w-=font_hsep
        print("Received",w,h)
        wrapped_text_data = wrap_text(w,h,text=windowText.get(),leave_early=False)
        w,h = text_data_measure(wrapped_text_data)
        w-=font_hsep
        print("Received2",w,h)
        #print("Measure answer:",w,h)
        #print("Widthbox:",widthBox.get(),heightBox.get())
        #print("Canvas:",mycanvas.winfo_width(),mycanvas.winfo_height())
        #try:
        #    print("Text:",wrapped_text[0])
        #except:
        #    pass
        #flush()
        widthVar.set(int(w))#min(w,root.winfo_screenwidth()-root.winfo_width()-root.winfo_x()+mycanvas.winfo_width()))
        heightVar.set(int(h))#min(h,root.winfo_screenheight()-root.winfo_height()-root.winfo_y()+mycanvas.winfo_height()))
        
        
    #FIT button
    fitButton = Button(coordsFrame,text="Fit",command=fitToText)
    fitButton.pack(side=RIGHT)
    CreateToolTip(fitButton,"Fit the canvas to the text")
    
    def screenshotCallback():
        filename = screenshot(mycanvas,"Screenshot")
        print("Captured image "+filename)
        flush()    
    
    screenshotButton = Button(bottomFrame,text="[◘]",command = screenshotCallback)
    screenshotButton.pack(side=LEFT)
    CreateToolTip(screenshotButton,"Take a screenshot")
    
    if(copy_screenshot_to_clipboard!=None):
        def clipboardCallback():
            if(copy_screenshot_to_clipboard!=None):
                copy_screenshot_to_clipboard(mycanvas)
                print("Image copied to clipboard")
                flush()
            else:
                print("Clipboard functionality not available. Requires pypiwin32")
                flush()
        clipboardButton = Button(bottomFrame,text="Copy", command = clipboardCallback)
        clipboardButton.pack(side=LEFT)
        CreateToolTip(clipboardButton,"Copy image to clipboard")
    
    def optionsbuttonCallback():
        create_optionswindow(root,sizechange_callback)
        
    optionsButton = Button(bottomFrame,text="☼",command=optionsbuttonCallback)
    optionsButton.pack(side=RIGHT)
    CreateToolTip(optionsButton,"Open Options window")
    
    def textbuttonCallback():
        create_textwindow(root,windowText)
    
    #Text window
    #Freely input the text that will be changed
    textButton = Button(bottomFrame,text="Text",command=textbuttonCallback)
    textButton.pack(side=RIGHT)
    CreateToolTip(textButton,"Open Text input window")
    
    
    windowText.trace("w",change_callback)
    """
    popupButton = Button(bottomFrame,text="α")
    popupButton.pack(side=RIGHT)
    CreateToolTip(popupButton,"Open Special characters window")
    """
        
    
    #def window_resize_event(event):
    #w, h = event.width, event.height
    """if(is_fit_mode()):
        heightVar.set(h)
        widthVar.set(w)
        #heightVar.set(mycanvas.winfo_height())
        #widthVar.set(mycanvas.winfo_width())
        change_callback()
        """
    
    #root.minsize(width=max(mycanvas., height=200)
    #root.maxsize(width=650, height=500)
    #mycanvas.bind("<Configure>", window_resize_event)
    #http://effbot.org/zone/tkinter-window-size.htm
    #myframe.bind("<Configure>", window_resize_event)
    
        
    def click(event):
        x,y = event.x, event.y
        myframe.previous_pos = (x,y)
    def unclick(event):
        myframe.previous_pos = None
    def changesize(event):
        x,y = event.x, event.y
        if(myframe.previous_pos!=None):
            dx,dy = x-myframe.previous_pos[0], y-myframe.previous_pos[1]
            myframe.previous_pos = (x,y)
            widthVar.set(widthVar.get()+dx)
            heightVar.set(heightVar.get()+dy)
    canvasframe.previous_pos = None
    canvasframe.bind("<B1-Motion>", changesize)
    canvasframe.bind("<Button-1>", click)
    canvasframe.bind("<ButtonRelease-1>", unclick)
    
    root.update_idletasks()
    fitToText()
    #sizechange_callback()
    
    
    sys.stdout.flush()
    root.mainloop()