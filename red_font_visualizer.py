# -*- coding: utf-8 -*-
#The font was created 1/06/2016 between 17:48 and 19:41 by Akira BAES and was further edited later on

from tkinter import *
import tkinter as tk
import datetime
import pyscreenshot as ImageGrab
from tk_ToolTip_class101 import CreateToolTip
flush = sys.stdout.flush
root = Tk()
root.geometry("256x256")
root.title("Minifont viewer")
root.configure(background="black")

characters = [None]*(16*8)
fontbase = PhotoImage(file="mini red sadface.png")

font_width = 2
spacesize = 1
font_hsep = 0

font_height = 4
font_vsep = 1
	
textwindow = None
	
def subimage(sheet, l, t, r, b):
	#https://stackoverflow.com/questions/16579674/using-spritesheets-in-tkinter
	#print(l,t,r,b)
	dst = tk.PhotoImage()
	dst.tk.call(dst, 'copy', sheet, '-from', l, t, r, b, '-to', 0, 0)
	return dst

def screenshot(canvas,text):
	#https://stackoverflow.com/questions/47653748/performing-imagegrab-on-tkinter-screen
	box = (canvas.winfo_rootx(),canvas.winfo_rooty(),canvas.winfo_rootx()+canvas.winfo_width(),canvas.winfo_rooty() + canvas.winfo_height())
	print(box)
	flush()
	time = str(datetime.datetime.now()).replace(":","-")
	image_name = text[:10]+"_"+time+".png"
	shot = ImageGrab.grab()
	
	print(dir(shot))
	print("W1=",shot.width)
	shot=shot.crop(box)
	print("W2=",shot.width)
	shot.save(image_name)
	return image_name
	
def get_char_image(charnum):
	if(charnum<=0 or charnum>=len(characters)):
		return None
	return characters[charnum]

def wrap_text(pixels_width, text):
	lines = text.split("\n")
	ans = []
	#print("Width:",pixels_width)
	pixels_width = max(font_width+font_hsep,pixels_width)
	#print("Corrected:",pixels_width)
	#print("Font width:",font_width)
	#print("Hsep:",font_hsep)
	#print("Spacesize:",spacesize)
	flush()
	for line in lines:
		w = 0
		ansline = ""
		line=line.replace(" !","\t!")
		line=line.replace(" ?","\t?")
		words = line.split(" ")
		for word in words:
			word = word.replace("\t"," ")
			lw = len(word)
			
			w2 = w + lw*font_width + (lw-1)*font_hsep + word.count(" ")*(-font_width-font_hsep+spacesize) + spacesize
			
			#print("W2:",repr(word),w2,"Pixels+space:",pixels_width+spacesize)
			if w2>pixels_width + spacesize:
				ans.append(ansline)
				ansline = ""
				w = lw*font_width + (lw-1)*font_hsep + word.count(" ")*(-font_width-font_hsep+spacesize) + spacesize
				while(w>pixels_width + spacesize):
				
					#print("W:",repr(word),w,"Pixels+space:",pixels_width+spacesize)
					#bourrin
					#print(word,w)
					for index in range(len(word)):
						#print("Index:",index)
						word2 = word[:len(word)-index]
						#print("Word 2:",word2)
						lw = len(word2)
						w = lw*font_width + (lw-1)*font_hsep + word.count(" ")*(-font_width-font_hsep+spacesize) + spacesize
						if(w<=pixels_width+spacesize):
							ans.append(word2)
							#print("Appended:",word2)
							word = word[len(word)-index:]
							#print("Remains:",word)
							break
					lw = len(word)
					w = lw*font_width + (lw-1)*font_hsep + word.count(" ")*(-font_width-font_hsep+spacesize) + spacesize
				ansline = word+" "
			else:
				ansline+=word+" "
				w = w2
		ans.append(ansline)
	return ans

def measure(text):
	measured_width = 0
	measured_height = 0
	for index, line in enumerate(wrapped_text):
		x=0
		y=index*(font_height+font_vsep)
		for letter in line:
			if(letter==" "):
				x+=spacesize
			else:
				x+=font_width+font_hsep
				measured_width = min(x-font_hsep,measured_width)
		measured_height = min(measured_height, y+(line!="")*font_height)
	return measured_width,measured_height

def draw_text(canvas,wrapped_text):
	for index, line in enumerate(wrapped_text):
		x=0
		y=index*(font_height+font_vsep)
		for letter in line:
			if(letter==" "):
				x+=spacesize
			else:
				char_image = get_char_image(ord(letter))
				if(char_image!=None):
					canvas.create_image(x, y, anchor=NW, image=char_image)
				x+=font_width+font_hsep

def load_font():
	font_width = 2
	font_hsep = 1
	font_height = 4
	font_vsep = 1
	font_x0 = 1
	font_y0 = 1 
	for x in range(16):
		for y in range(8):
			dx = font_x0 + (font_width+font_hsep) * x
			dy = font_y0 + (font_height+font_vsep) * y
			characters[x+y*16] = \
				subimage(fontbase, dx, dy, dx+font_width, dy+font_height)
				
def create_textwindow(root, textvariable):
	global textwindow
	if textwindow == None or not textwindow.winfo_exists():
		textwindow = Toplevel()
			
		myframe = Frame(root, bg="gray10")
		myframe.pack(fill=BOTH, expand=YES)
		
		
if(__name__ == "__main__"):
	load_font()
	canvaswidth = 32
	canvasheight = 128
	
	windowText = StringVar()
	#Default temporary text
	windowText.set("""I am the most hideous creature in the realm. 
A more abject appearance you will not find.

I have fallen countless times before your troops, and yet I am here.
Is it not proof that I possess the stone of life?""".upper())
	
	
	myframe = Frame(root, bg="gray10")
	myframe.pack(fill=BOTH, expand=YES)
	mycanvas = Canvas(myframe,
		width=canvaswidth, height=canvasheight, bg="black", highlightthickness=0)
	"""
	#load default text
	for x in range(16):
		for y in range(8):
			charnum = 16*y+x
			mycanvas.create_image(x*font_width,y*font_height,image=get_char_image(charnum),anchor=NW)"""
	mycanvas.pack(fill=BOTH, expand=YES)
	
	def change_callback(*args):
		mycanvas.delete("all")
		if(is_fit_mode()):
			draw_text(mycanvas,wrap_text(mycanvas.winfo_width(),text=windowText.get()))
		else:
			draw_text(mycanvas,wrap_text(int(widthBox.get()),text=windowText.get()))
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
	widthBox = Spinbox(coordsFrame,textvariable = widthVar,width=4, from_=2, to=512)
	widthBox.pack(side=LEFT)
	
	hl = Label(coordsFrame,text="H")
	hl.pack(side=LEFT)
	CreateToolTip(hl,"Height")
	heightVar = IntVar()
	heightVar.set(canvasheight)
	heightBox = Spinbox(coordsFrame, textvariable = heightVar,width=4, from_=4, to=512)
	heightBox.pack(side=LEFT)
	
	#The boxes are only active when Fit is disabled
	def sizechange_callback(*args):
		if(is_center_mode()):
			mycanvas.config(width=widthVar.get(), height=heightVar.get())
			change_callback()
	
	widthVar.trace("w",sizechange_callback)
	heightVar.trace("w",sizechange_callback)
	
	#FIT toggle
	modeToggle = IntVar()
	modeToggle.set(False)
	toggleCheck = Checkbutton(coordsFrame, text="Fit", variable=modeToggle)
	toggleCheck.pack(side=LEFT)
	CreateToolTip(toggleCheck,"Fit the window size")
	
	
	def screenshotCallback():
		filename = screenshot(mycanvas,"Screenshot")
		
		print("Captured image "+filename)
		flush()	
	
	screenshotButton = Button(bottomFrame,text="[◘]",command = screenshotCallback)
	screenshotButton.pack(side=LEFT)
	CreateToolTip(screenshotButton,"Take a screenshot")
	
	#[TODO]
	clipboardButton = Button(bottomFrame,text="Copy")
	clipboardButton.pack(side=LEFT)
	CreateToolTip(clipboardButton,"Copy image to clipboard [TODO]")
	
	#OPTIONS [TODO]
	#Entries for hsep, vsep, spacesize
	#Toggle for crop image to fit text
	optionsButton = Button(bottomFrame,text="☼")
	optionsButton.pack(side=RIGHT)
	CreateToolTip(optionsButton,"Open Options window")
	
	#Text window [TODO]
	#Freely input the text that will be changed
	
	textButton = Button(bottomFrame,text="Text")
	textButton.pack(side=RIGHT)
	CreateToolTip(textButton,"Open Text input window")
	
	popupButton = Button(bottomFrame,text="α")
	popupButton.pack(side=RIGHT)
	CreateToolTip(popupButton,"Open Special characters window")
	
		
	
	def window_resize_event(event):
		w, h = event.width, event.height
		if(is_fit_mode()):
			heightVar.set(h)
			widthVar.set(w)
			#heightVar.set(mycanvas.winfo_height())
			#widthVar.set(mycanvas.winfo_width())
			change_callback()
			
		
		#root.minsize(width=max(mycanvas., height=200)
		#root.maxsize(width=650, height=500)
	mycanvas.bind("<Configure>", window_resize_event)
	#http://effbot.org/zone/tkinter-window-size.htm
	#myframe.bind("<Configure>", window_resize_event)
	
	def is_fit_mode():
		return modeToggle.get()
	def is_center_mode():
		return not modeToggle.get()
		
	def mode_toggle_callback(*args):
		if(is_fit_mode()):
			widthBox.config(state='disabled')
			heightBox.config(state='disabled')
			mycanvas.pack(fill=BOTH, expand=NO)
		else:
			widthBox.config(state='normal')
			heightBox.config(state='normal')
			#https://stackoverflow.com/questions/18736465/how-to-center-a-tkinter-widget
			mycanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
			sizechange_callback()
	modeToggle.trace("w",mode_toggle_callback)
	
	
	mode_toggle_callback()
	sizechange_callback()
	
	sys.stdout.flush()
	root.mainloop()