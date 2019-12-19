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
try:
    from PIL import ImageGrab
except:
    import pyscreenshot as ImageGrab
from tk_ToolTip_class101 import CreateToolTip
flush = sys.stdout.flush
from tkinter import font
root = Tk()
sample_text_file = "sample_text.txt"
root.title("Bitmap font viewer")
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
spacesize = 1
font_hsep = 0
font_vsep = 1
font_x0 = 1
font_y0 = 1
allcaps = 0
current_font = 0
superpose_missing_accents = True
accent_vertical_gap = 1
fill_missing_with_unidecode = True
missing_character_character = "?"
def font_name(id=None):
    if(id==None):
        id=current_font
    return FONT_TYPES[id]
    
def save_font_options(): #current_height, current_width):
    filename="fonts"+os.sep+font_name()[:-4]
    f = open(filename+".ini","w")
    f.write(str(font_hsep)+"\n")
    f.write(str(font_vsep)+"\n")
    f.write(str(spacesize)+"\n")
    f.write(str(font_x0)  +"\n")
    f.write(str(font_y0)  +"\n")
    f.write(str(allcaps)  +"\n")
    #f.write(str(current_font)  +"\n")
    f.close()
    #file.write(current_height)
    #file.write(current_width)
    
def load_font_options(filename="default_options",silent=True):
    global font_hsep,\
           font_vsep,\
           spacesize,\
           font_x0  ,\
           font_y0  ,\
           allcaps
    try:
        f = open(filename+".ini","r")
        data = f.readlines()
        f.close()
        newdata = []
        #print(data)
        for x in data:
            try:
                newdata.append(int(x))
            except:
                print(x,"could not be read")
        font_hsep = newdata.pop(0)
        font_vsep = newdata.pop(0)
        spacesize = newdata.pop(0)
        font_x0   = newdata.pop(0)
        font_y0   = newdata.pop(0)
        allcaps   = newdata.pop(0)
        #current_font   = newdata.pop(0)
        update_font()
        return True
    except Exception as e:
        if not silent: print(e)
        return False
        
    #return newdata.pop(0), newdata.pop(0)

def save_current_font():
    filename = "settings.ini"
    f = open(filename,"w")
    f.write(font_name()  +"\n")
    f.close()
    
def load_current_font():
    global current_font
    filename = "settings.ini"
    try:
        f = open(filename,"r")
        data=f.readline().strip()#[int(x) for x in f.realines()]
        f.close()
        current_font = FONT_TYPES.index(data)
    except Exception as e:
        print(e)

def subimage(sheet, l, t, r, b):
    #https://stackoverflow.com/questions/16579674/using-spritesheets-in-tkinter
    #print(l,t,r,b)
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
        

except:
    send_to_clipboard = None
    copy_screenshot_to_clipboard = None
    
    
allchars = "UNINITIALISED"
def reload_chars():
    global allchars
    filename = font_name()[:-4]+".txt"
    with io.open(os.path.join("fonts",filename),'r',encoding='utf8') as f:
        allchars = f.read().replace("\n","")

reload_chars()
    
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
    #print("Allcaps is:",allcaps)
    if(allcaps==1):
        text = text.upper()
    lines = text.split("\n")
    ans = []
    #print("Width:",pixels_width)
    pixels_width = max(FONT_WIDTH+font_hsep,pixels_width)
    #print("Corrected:",pixels_width)
    #print("Font width:",FONT_WIDTH)
    #print("Hsep:",font_hsep)
    #print("Spacesize:",spacesize)
    #flush()
    for line in lines:
        w = 0
        ansline = ""
        line=line.replace(" !","\t!")
        line=line.replace(" ?","\t?")
        words = line.split(" ")
        flush()
        while(len(words)>0):
            word = words.pop(0)
            word = word.replace("\t"," ")
            xlong, xshort = word_width(word)
            if(w+xshort>pixels_width):
                if(ansline == ""):
                    cutword,nextword = cut_word(word,pixels_width)
                    #print("Cut:",cutword,"+",nextword)
                    flush()
                    ansline=cutword
                    word = nextword
                #print("Cut in ",ansline,"+",word)
                ans.append(ansline)
                if(lines_height(len(ans)+1)>pixels_height and leave_early):
                    return ans
                ansline = ""
                words.insert(0,word)
                w=0
            else:
                ansline+=word+" "
                w+=xlong+spacesize
                
        ans.append(ansline)
        if(lines_height(len(ans)+1)>pixels_height and leave_early):
            return ans
    return ans

def measure(wrapped_text):
    measured_width = 0
    measured_height = 0
    for index, line in enumerate(wrapped_text):
        xlong,xshort=word_width(line)
        measured_width = max(xshort,measured_width)
    measured_height = lines_height(len(wrapped_text))
    return measured_width,measured_height

try:    from unidecode import unidecode
except Exception as e: print(e)
#https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string

letter_bases={
    "áàâäãå":"a",
    "ÁÀÂÄÃÅ":"A",
    "éèêë"  :"e",
    "ÉÈÊË"  :"E",
    "íìîï"  :"ı",
    "ÍÌÎÏ"  :"I",
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

def draw_text(canvas,wrapped_text,vscroll=None):
    if(vscroll==None):
        top=0
        bottom=float("inf")
    else:
        top,bottom=vscroll.get()
        top=top*len(wrapped_text)
        bottom=bottom*len(wrapped_text)
    for index, line in enumerate(wrapped_text):
        x=font_x0
        y=font_y0+index*(FONT_HEIGHT+font_vsep)
    
        #if(y>canvas.winfo_height()):
        #    break #FIND A BETTER WAY TO OPTIMISE THIS
        """if(index<top):
            continue
        if(index>bottom):
            break"""
        for letter in line:
            if(letter==" "):
                x+=spacesize
            else:
                char_image = get_char_image(letter)
                if(char_image==None and letter in all_accents and superpose_missing_accents):
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
                        if(char_image.width()>accent_image.width()):
                            letter = unidecode(letter_base)
                        else:
                            letter = accent_base
                        
                        #print("Accented letter:",letter_base,"+",accent_base)
                        
                        #canvas.create_image(x, y, anchor=NW, image=letter_image)
                        top=image_top(char_image)
                        bottom = image_bottom(accent_image)
                        # print("Top:",top," - Bottom:",bottom)
                        #bottom=accent_image.height()
                        h_shift = round(float(char_image.width()-accent_image.width())/2)
                        v_shift = top-bottom-accent_vertical_gap
                        
                        # print("Width letter:",get_char_width(letter_base)," - Width accent:",get_char_width(accent_base))
                        # print("h_shift:",h_shift)
                        canvas.create_image(x+h_shift, y+v_shift, anchor=NW, image=accent_image)
                    except Exception as e:
                        pass
                        #print(e)
                if(char_image==None and fill_missing_with_unidecode):
                    # print("Could not find replacement for accent",letter)
                    letter=unidecode(letter)
                    char_image = get_char_image(letter)
                    # print(letter,char_image)
                if(char_image==None):
                    #print("Could not find character",letter,"in",ALLcharacters[current_font])
                    letter=missing_character_character
                    char_image = get_char_image(letter)
                if(char_image!=None):
                    canvas.create_image(x, y, anchor=NW, image=char_image)
                x+=get_char_width(letter)+font_hsep

def load_mini_fonts():
    working_fonts=[]
    for FONTNAME in FONT_TYPES:
        
        #Load WIDE
        fontbase = PhotoImage(file=os.path.join("fonts",FONTNAME))
        fontdata = dict()
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
            #print(FONTNAME,s)    
        except Exception as e:
            print("Could not load",FONTNAME,"due to:")
            print(e)
            print("-"*10)
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
        #leftframe = Frame(leftframeall)
        #leftframe.pack(side=TOP)
        #rightframe = Frame(rightframeall)
        #rightframe.pack(side=TOP)
        
        Label(leftframe,text="Horizontal separation").pack(side=TOP)
        hsepvar = IntVar(value=font_hsep)
        Spinbox(leftframe,textvariable = hsepvar,width=3, from_=-64, to=64).pack(side=TOP)
        def hsepfun(*args):
            global font_hsep
            font_hsep = hsepvar.get()
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
        Spinbox(rightframe,textvariable = spvar,width=3, from_=0, to=128).pack(side=TOP)
        def spfun(*args):
            global spacesize
            spacesize = spvar.get()
            size_callback()
        spvar.trace("w",spfun)
        
        
        Label(leftframe,text="Force capitalization").pack(side=TOP)
        capvar = IntVar(value=allcaps)
        Checkbutton(leftframe,text="",variable = capvar).pack(side=TOP)
        def capfun(*args):
            global allcaps
            allcaps = capvar.get()
            size_callback()
        capvar.trace("w",capfun)
        
        
        Button(rightframe,text="Save options",command=save_font_options).pack(side=BOTTOM)
        def load_and_update(*args):
            load_font_options("fonts"+os.sep+font_name()[:-4]) #Try to load specific options, otherwise do nothing
            size_callback()
            hsepvar.set(font_hsep)
            vsepvar.set(font_vsep)
            x0var.set(font_x0)
            y0var.set(font_y0)
            spvar.set(spacesize)
            capvar.set(allcaps)
            #ftvar.set(FONT_TYPES[current_font])
            

        undobutton = Button(leftframe,text="Undo changes",command=load_and_update)
        undobutton.pack(side=BOTTOM)
        CreateToolTip(undobutton,"Load last saved options")
        
        
        Label(leftframe,text="Font type:").pack(side=BOTTOM)
        ftvar = StringVar(value = font_name())
        sb = Spinbox(rightframe, width=22, values=FONT_TYPES,textvariable = ftvar)
        sb.pack(side=BOTTOM)
        sb.delete(0,"end")
        sb.insert(0,font_name()) #for some reason, doesn't get the right default value
        #print(sb.get())
        def ftfun(*args):
            global current_font
            current_font = FONT_TYPES.index(ftvar.get())
            save_current_font()
            load_and_update() #changing fonts can change the options
            update_font()
            size_callback()
        ftvar.trace("w",ftfun)
        
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
        load_current_font()
        if(not load_font_options("fonts"+os.sep+font_name()[:-4])):
            #Try to load specific options, otherwise load default ones
            load_font_options(silent=False)
    except Exception as e:
        print(e)
        pass
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
        draw_text(mycanvas,wrap_text(int(widthBox.get()),int(heightBox.get()),text=windowText.get()),vbar)
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
        wrapped_text = wrap_text(int(widthBox.get()),int(heightBox.get()),text=windowText.get(),leave_early=False)
        w,h = measure(wrapped_text)
        #print("Measure answer:",w,h)
        #print("Widthbox:",widthBox.get(),heightBox.get())
        #print("Canvas:",mycanvas.winfo_width(),mycanvas.winfo_height())
        #try:
        #    print("Text:",wrapped_text[0])
        #except:
        #    pass
        #flush()
        widthVar.set(w)#min(w,root.winfo_screenwidth()-root.winfo_width()-root.winfo_x()+mycanvas.winfo_width()))
        heightVar.set(h)#min(h,root.winfo_screenheight()-root.winfo_height()-root.winfo_y()+mycanvas.winfo_height()))
        
        
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
    
    #OPTIONS [TODO]
    #Entries for hsep, vsep, spacesize
    #Toggle for crop image to fit text, or crop all?
    #[TODO]starting position
    #[TODO] other font
    #[TODO] all caps or not
    
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