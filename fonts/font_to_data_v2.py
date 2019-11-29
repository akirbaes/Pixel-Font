import io
from PIL import Image
#INPUT: filename of the characters list
#there must exist a FILENAME.XXX image and a FILENAME[chars].txt file containing the characters represented 
#(pad with spaces if a line doesn't go until the end)
files = "maxred.png", "µRed_mono.png", "µRed_wide.png", "Formula.png", "Formula_16.png", "badlydrawn.png"

def generate_data(fontimage_file):
    fontimage = Image.open(fontimage_file).convert('RGB')
    image_width, image_height = fontimage.size

    #INPUT: the characters that appear in the font, in order
    filename = fontimage_file[:-4]+"[chars].txt"
    with io.open(filename,'r',encoding='utf8') as f:
        allchars = f.read()
    #print(allchars)

    #allchars = "ABCDEFGHIJKLM\nNOPQRSTUVWXYZ"
    allchars=allchars.strip("\n")

    charlines = allchars.split("\n")
    chars_vertical_count = len(charlines)
    y_sep = image_height//chars_vertical_count

    #determine background color by majority
    def majority_color(image):
        image_width, image_height = image.size
        colors_counter = dict()
        for x in range(image_width):
            for y in range(image_height):
                    pixel = image.getpixel((x,y))
                    colors_counter[pixel]=colors_counter.get(pixel,-1)+1
        maxcount = 0
        majority_color = (0,0,0)
        for color in colors_counter:
            if(colors_counter[color]>maxcount):
                majority_color=color
                maxcount=colors_counter[majority_color]
        return majority_color
    #
    background_color = majority_color(fontimage)
    print(fontimage_file,background_color)
    #background_color = (0,0,0) #if doesn't work
    #print("background_color=",background_color)

    char_pos_size = dict()
    char_pos_size["background"]=background_color
    
    #Determine the boundaries of the character
    char_horizontal_count = 0
    for line in charlines:
        char_horizontal_count=max(char_horizontal_count,len(line))
    x_sep = image_width//char_horizontal_count
       
    for j, line in enumerate(charlines):
        for i, character in enumerate(line):
            charx = i*x_sep
            chary = j*y_sep
            x0 = x_sep
            y0 = y_sep
            x1 = 0
            y1 = 0
            
            for dy in range(y_sep):
                for dx in range(x_sep):
                    pixel = fontimage.getpixel((charx+dx,chary+dy))
                    if(pixel!=background_color):
                        if("µ" in fontimage_file) and not(pixel[1]==0 and pixel[2]==0 and pixel[0]>1):
                            #If subpixels, pixels other than red are bigger
                            dx+=1
                        x0 = min (dx, x0)
                        y0 = min (dy, y0)
                        x1 = max (dx, x1)
                        y1 = max (dy, y1)
            
            #print(character,charx,chary,x1>x0 and y1>y0)
            if(x1>=x0 and y1>=y0):
                char_pos_size[character] = [charx,chary,x0,y0,x1,y1]
                #Character fits into this box as [X+X0,Y+Y0,X+X1,Y+Y1]
                #charx, chary show the position compared to other characters
            
    font_width = 0
    font_height = 0
    origin_x = float("inf") #top-left of the box regardless of char size
    origin_y = float("inf")
    
    for key in char_pos_size:
        if(len(key)==1):
            cx,cy,x0,y0,x1,y1 = char_pos_size[key]
            font_width = max(font_width,x1-x0+1)
            font_height = max(font_height,y1-y0+1)
            origin_x = min(origin_x,x0)
            origin_y = min(origin_y,y0)
            
    #shift everything by origin for neat cut
    #hence, x0 and y0 should be 0 most of the time
    #except for things like underscore
    #so we just include the shift in the size and drop x0,y0
    #Because we only really needed one height, and all the widths for our purposes
    for key in char_pos_size:
        if(len(key)==1):
            cx,cy,x0,y0,x1,y1 = char_pos_size[key]
            if("mono" in fontimage_file):
                #If mono, all characters must have the same size
                char_pos_size[key] = cx+origin_x,cy+origin_y,font_width,font_height
            else:
                char_pos_size[key] = cx+origin_x,cy+origin_y,x1-origin_x+1,y1-origin_y+1
    
    char_pos_size["width"]=font_width
    char_pos_size["height"]=font_height
    
    import json
    jsonform = json.dumps(char_pos_size,indent=4,separators=(',', ': '))
    #print(repr(jsonform)) 
    with io.open(fontimage_file[:-4]+"[posiz].json",'w',encoding='utf8') as f:
        f.write(jsonform)
    with io.open(fontimage_file[:-4]+"[posiz].json",'r',encoding='utf8') as f:
        newdict = json.load(f)
        
    return char_pos_size
        
if __name__ == "__main__":
    import sys
    if(len(sys.argv)>1):
        try:
            generate_data(sys.argv[1])
            input("Done! Press any key...")
        except Exception as e:
            print(e)
            input("Error! Press any key...")
            raise(e)
    else:
        for filename in files:
            generate_data(filename)