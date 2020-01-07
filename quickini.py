    
class QuickIni:
    def __init__(self, name):
        self.filename = name
        self.values=dict()
    def __iadd__(self,pair):
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
        if(isinstance(name,tuple)):
            name,default = name
            return self.values.get(name,default)
        return self.values[name]
    def __gt__(self,name):
        return self.values.get(name)
    def __lt__(self,other):
        class _DefaultIni_:
            def __init__(self,parent,value):
                self.parent=parent
                self.value=value
            def __gt__(self,name):
                try:
                    return self.parent.values.get(name)
                except:
                    return self.other
        return _DefaultIni_(self,other)