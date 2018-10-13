import io
filename = "special_chars.txt"
allchars = ""
with io.open(filename,'r',encoding='utf8') as f:
	allchars = f.read().replace("\n","")
	
def get_char_ascii_index(character):
	return allchars.find(character)
	
def get_char_from_number(charnum):
	if(charnum<0 or charnum>=len(allchars)):
		return None
	return allchars[charnum]

from PIL import Image
fontimage = Image.open("MiniRed_WideMNW.png")

x_sep = y_sep = 6
x0 = 1
y0 = 1
font_height = 4
font_width = 2 #or 3, the test is there

char_and_size = dict()
char_pos_size = dict()

for i in range(16):
	for j in range(8):
		charx, chary = x0+i*x_sep, y0+j*y_sep
		#right border
		rb = charx+1
		width = 1
		for w in range(4):
			pixel = fontimage.getpixel((rb,chary+w))
			if(pixel!=(0,0,0)):
				width = 2
		rb = charx+2
		for w in range(4):
			pixel = fontimage.getpixel((rb,chary+w))
			if(pixel!=(0,0,0)):
				width = 3
		#bottom border
		bb = chary + 4
		height = 4
		for h in range(width):
			pixel = fontimage.getpixel((charx+h,bb))
			if(pixel!=(0,0,0)):
				height = 5
		character_index = i + j*16
		char_and_size[get_char_from_number(character_index)]=(width,height)
		char_pos_size[get_char_from_number(character_index)]=[charx,chary,width,height]
		#Json uses lists so following the same

with io.open("charsizes.txt",'w',encoding='utf8') as f:
	f.write(str(char_and_size))
with io.open("charpossizes.txt",'w',encoding='utf8') as f:
	f.write("{\n")
	
	keys = [key for key in char_pos_size]
	for key in keys:
		f.write('\t'+repr(key)+' : '+str(char_pos_size[key]))
		#MUST use double-quotes for json
		if(key!=keys[-1]):
			f.write(",")
		f.write("\n")
	f.write("}")
#Was just a bad idea due to the \ and " and ' lying around. Works if opening it manually in python, but not for json because of " 
import json
jsonform = json.dumps(char_pos_size,indent=4,separators=(',', ': '))
print(repr(jsonform)) #same thing, but with lists instead of tuples [Edit] changed
with io.open("WIDEcharpossizes.json",'w',encoding='utf8') as f:
	f.write(jsonform)
with io.open("WIDEcharpossizes.json",'r',encoding='utf8') as f:
	newdict = json.load(f)

#with io.open("charpossizes.txt",'r',encoding='utf8') as f:
#	newdict2 = json.load(f)
#print(repr(newdict))
#print(newdict == newdict2)