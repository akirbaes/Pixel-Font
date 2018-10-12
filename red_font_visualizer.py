# -*- coding: utf-8 -*-
import io
from tkinter import *
import tkinter as tk
import datetime
import pyscreenshot as ImageGrab
from tk_ToolTip_class101 import CreateToolTip
flush = sys.stdout.flush
from tkinter import font
root = Tk()
sample_text_file = "sample_text.txt"
root.title("Minifont viewer")
root.iconbitmap("2x8_MINI_RED_FONT_EDITOR_ICON.ico")
root.configure(background="black")

root.geometry("160x160")
#DEF_FRAME = (128,128)
DEF_CANVAS = (64,64)
DEF_TEXTAREA = (80,5)
DEF_TEXTWINDOW = (256,256)
DEF_BUTTONSROW = 16

font12 = font.Font(family='Arial', size=12)
font12 = 'TkFixedFont'

characters = [None]*(16*8)
fontbase = PhotoImage(file="minired_sadface.png")

font_width = 2
spacesize = 1
font_hsep = 0

font_height = 4
font_vsep = 1
font_x0 = 0
font_y0 = 0
	
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
	#print(box)
	flush()
	time = str(datetime.datetime.now()).replace(":","-")
	image_name = text[:10]+"_"+time+".png"
	shot = ImageGrab.grab()
	#print(dir(shot))
	#print("W1=",shot.width)
	shot=shot.crop(box)
	#print("W2=",shot.width)
	shot.save(image_name)
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
		box = (canvas.winfo_rootx(),canvas.winfo_rooty(),canvas.winfo_rootx()+canvas.winfo_width(),canvas.winfo_rooty() + canvas.winfo_height())
		
		shot = ImageGrab.grab(box)
		
		output = io.BytesIO()
		shot.convert("RGB").save(output, "BMP")
		data = output.getvalue()[14:]
		output.close()
		
		send_to_clipboard(win32clipboard.CF_DIB, data)
		

except:
	send_to_clipboard = None
	copy_screenshot_to_clipboard = None
	
#def send_to_clipboard(clip_type, data):	
#def copy_screenshot_to_clipboard(mycanvas):

	
filename = "special_chars.txt"
allchars = ""
with io.open(filename,'r',encoding='utf8') as f:
	allchars = f.read().replace("\n","")
	
def get_char_ascii_index(character):
	return allchars.find(character)
	
def get_char_image(charnum):
	if(charnum<=0 or charnum>=len(characters)):
		return None
	return characters[charnum]

def lines_height(lines):
	return lines*font_height+(lines-1)*font_vsep+font_y0
	
def wrap_text(pixels_width, pixels_height, text, leave_early = True):
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
				if(lines_height(len(ans))>pixels_height and leave_early):
					return ans
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
							if(lines_height(len(ans))>pixels_height and leave_early):
								return ans
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
		if(lines_height(len(ans))>pixels_height and leave_early):
			return ans
	return ans

def measure(wrapped_text):
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
				measured_width = max(x-font_hsep,measured_width)
		measured_height = max(measured_height, y+(line!="")*font_height)
	return measured_width,measured_height

def draw_text(canvas,wrapped_text):
	for index, line in enumerate(wrapped_text):
		x=0
		y=index*(font_height+font_vsep)
		for letter in line:
			if(letter==" "):
				x+=spacesize
			else:
				char_image = get_char_image(get_char_ascii_index(letter))
				if(char_image!=None):
					canvas.create_image(x, y, anchor=NW, image=char_image)
				x+=font_width+font_hsep
			if(y>canvas.winfo_height()):
				break

def load_mini_font():
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
				

				
def load_special_chars(frame,textarea):
	filename = "button_special_chars.txt"
	with io.open(filename,'r',encoding='utf8') as f:
		text = f.read()
	
	charsframe = Frame(frame, bg="gray20")
	charsframe.pack(fill=BOTH, expand=YES)
	counter = 0;
	for character in text:
		if(get_char_image(get_char_ascii_index(character))!=None):
			def char_command(current_char):
				def place_char():
					textarea.insert(INSERT,current_char)
					textarea.event_generate("<Key>")
					#print("Inserted ",ord(current_char))
					#flush()
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
			root.winfo_x()+root.winfo_width()+2*dx,root.winfo_y()))
			
		textwindow.geometry(("%dx%d")%(DEF_TEXTWINDOW[0],DEF_TEXTWINDOW[1]))
			
		textarea.previous_text = textarea.get('1.0', 'end-1c')
		
		def save_text():
			current_text = textarea.get('1.0', 'end-1c')
			if(textarea.previous_text != current_text):
				with io.open(sample_text_file,'w',encoding='utf8') as f:
					f.write(current_text)
			textwindow.title("Text input")
			textarea.after(5000, save_text)
				
		textarea.after(5000, save_text)
			
	elif(textwindow!=None and textwindow.winfo_exists()):
		dx = textwindow.winfo_rootx()-textwindow.winfo_x()
		#print(dx)
		#flush()
		textwindow.important.focus_force()
		textwindow.geometry(("+%d+%d")%(
			root.winfo_x()+root.winfo_width()+2*dx,root.winfo_y()))
		
if(__name__ == "__main__"):
	load_mini_font()
	canvaswidth = DEF_CANVAS[0]
	canvasheight = DEF_CANVAS[0]
	
	windowText = StringVar()
	#Default temporary text
	try:
		with io.open(sample_text_file,'r',encoding='utf8') as f:
			windowText.set(f.read())
	except:
		windowText.set("""I am the most hideous creature in the realm. 
A more abject appearance you will not find.

I have fallen countless times before your troops, and yet I am here.
Is it not proof that I possess the stone of life?""".upper())
	
	
	myframe = Frame(root, bg="gray10")
	myframe.pack(fill=BOTH, expand=YES)
	mycanvas = Canvas(myframe,
		width=canvaswidth, height=canvasheight, bg="black", highlightthickness=0)
	
	#https://stackoverflow.com/questions/18736465/how-to-center-a-tkinter-widget
	mycanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
	#mycanvas.pack(fill=BOTH, expand=YES)
	
	mycanvas.current_after = None
	def redraw():
		mycanvas.current_after = None
		mycanvas.delete("all")
		draw_text(mycanvas,wrap_text(int(widthBox.get()),int(heightBox.get()),text=windowText.get()))
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
		mycanvas.config(width=widthVar.get(), height=heightVar.get())
		change_callback()
	
	widthVar.trace("w",sizechange_callback)
	heightVar.trace("w",sizechange_callback)
	
	def fitToText():
		w,h = measure(wrap_text(int(widthBox.get()),int(heightBox.get()),text=windowText.get(),leave_early=False))
		print(w,h)
		widthVar.set(w)
		heightVar.set(h)
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
	
	optionsButton = Button(bottomFrame,text="☼")
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
	myframe.previous_pos = None
	myframe.bind("<B1-Motion>", changesize)
	myframe.bind("<Button-1>", click)
	myframe.bind("<ButtonRelease-1>", unclick)
	
	sizechange_callback()
	
	sys.stdout.flush()
	root.mainloop()