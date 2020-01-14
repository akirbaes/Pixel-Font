    
class QuickIni:
    def __init__(self, name):
        self.filename = name
        self.values=dict()
    def __iadd__(self,pair):
        #Usage: ini+= "variable", value
        name, value = pair
        self.values[name]=value
        return self
    def set(self,name,value):
        self.values[name]=value
    def save(self):
        f = open(self.filename,"w")
        for name, value in self.values.items():
            f.write(str(name)+" = "+str(value)+"\n")
        f.close()
    def load(self):
        f = open(self.filename,"r")
        #print(self.filename)
        data = f.readlines()
        f.close()
        self.values=dict()
        for line in data:
            #print(repr(line))
            try:
                name,value = line.strip().split("=")
                name=name.strip()
                try:
                    value = int(value)
                except:
                    try:
                        value = float(value)
                    except:
                        value = value.strip()
                self.values[name]=value
            except: continue
        return self
    def get(self,name,default):
        return self.values.get(name,default)
    def __truediv__(self,name):
        #Usage: variable = ini/"variable"/default
        #Without the defaut you will only get the temporary structure
        class _DefaultIni_:
            def __init__(self,parent,name):
                self.parent=parent
                self.name=name
            def __truediv__(self,value):
                return self.parent.values.get(self.name,value)
        return _DefaultIni_(self,name)
    def __floordiv__ (self,name):
        #Usage: try: variable = ini//"variable"
        #No default provided, should raise an error when missing
        if(isinstance(name,tuple)):
            name,default = name
            return self.values.get(name,default)
        return self.values[name] 
        
    #There's a problem wih the 0<ini<"variable" gt stuff: it gets simplified away 
    #(0<ini)<"variable" works, but since the idea was to have less to write...
    # def __gt__(self,name):
        # return self.values.get(name)
    # def __lt__(self,other):
        # class _DefaultIni_:
            # def __init__(self,parent,value):
                # print("Creating defaultini",value)
                # self.parent=parent
                # self.value=value
            # def __lt__(self,name):
                # print("Help")
            # def __gt__(self,name):
                # print("Default",self.value,"receives",name)
                # return self.parent.values.get(name,self.value)
        # return _DefaultIni_(self,other)