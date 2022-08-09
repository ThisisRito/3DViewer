# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

#{"shape":"Sphere", "size":{"radius":3.0}, "rgb":[122,0,255], "name":"my big sphere!!!", "position":[-11,25,3.1], "orientation":[1,2.0,-1],}
#{"shape":"Cubiod", "size":{"height":3.0,"length":2.4, "width":0.1}, "rgb":[122,0,255], "name":"my big sphere!!!", "position":[-11,25,3.1], "orientation":[1,2.0,-1],}
#
#
#
#

from PySide2.QtCore import(Property, Signal, Slot, QObject)
from PySide2.QtGui import (QVector3D)

import random

#todo pure virtual
class ObjectData(QObject):
    counter = 0
    def __init__(self):
        super(ObjectData,self).__init__()
        ObjectData.counter += 1;
        self.data = {
            "shape":None,
            "rgb":tuple([random.randint(0,255) for i in range(3)]),
            "position":tuple([random.uniform(-10,10) for i in range(3)]),
            "orientation":(0,1,0),
            "id": ObjectData.counter,
            "name": None,
        }

    def __eq__(self, other): 
        if not isinstance(other, ObjectData):
            return NotImplemented
        for key in self.data:
            if(not(key in other.data) or self.data[key] != other.data[key]):
                return False
        return True

    def getId(self):
        return self.data["id"]

    def setPosition(self, pos):
        if pos == self.data["position"]:	return
        self.data["position"] = pos
        id = self.getId()
        self.positionChanged.emit(id,pos)

    def setColor(self, rgb):
        print('entering set color')
        if rgb == self.data["rgb"]:	return
        r,g,b = rgb
        try:
            r = int(r)
            g = int(g)
            b = int(b)
            for num in (r,g,b):
                if(num < 0 or num > 255):
                    raise ValueError()
        except:
            print('rgb value error')
            return
        id = self.getId()
        self.data["rgb"] = (r,g,b)
        rgb = r,g,b
        print("sending: color changed on", id);
        self.colorChanged.emit(id,rgb)

    def setName(self, name):
        if name == self.data["name"]:	return
        self.data["name"] = name
        id = self.getId()
        self.nameChanged.emit(id,name)

    def setShape(self, shape_info):
        if self.data["shape"] == "Sphere":
            self.setSphere(self,shape_info["radius"])
        if self.data["shape"] == "Cuboid":
            self.setCuboid(self,shape_info["lengths"])

    def setSphere(self, radius):
        if self.data["shape"] == "Sphere" and raidus == self.data["radius"]: return
        shape_info = {"shape":"Spehre", "radius":radius}
        id = self.getId()
        self.shapeChanged.emit(id,shape_info)

    def setCuboid(self, lengths):
        if self.data["shape"] == "Cuboid" and lengths == self.data["lengths"]: return
        shape_info = {"shape":"Cuboid", "lengths":lengths}
        id = self.getId()
        self.shapeChanged.emit(id,shape_info)

    def setOrientation(self, norm_vector):
        pass

    positionChanged = Signal(int,QVector3D)
    orientationChanged = Signal(int,float,float,float)
    colorChanged = Signal(int,tuple)
    shapeChanged = Signal(int,dict)
    nameChanged = Signal(int,str)


    
class SphereData(ObjectData):
    def __init__(self):
        super(SphereData,self).__init__()
        self.data["shape"] = "Sphere"
        self.data["radius"] = 1.0
        self.data["name"] = "Sphere " + str(self.data["id"])

class CuboidData(ObjectData):
    def __init__(self):
        super(CuboidData,self).__init__()
        self.data["shape"] = "Cuboid"
        self.data["lengths"] = (2.0,2.0,2.0)
        self.data["name"] = "Cuboid " + str(self.data["id"])

class ObjectModel(QObject):

    Insert = Signal(int,ObjectData)
    Update = Signal(int)
    Remove = Signal(int)
    Focus = Signal(int)

    def __init__(self):
        super(ObjectModel,self).__init__()
        self.objects = {}
        self.focussed = -1

    def focus(self,id):
        if(self.focussed == id):	return
        self.focussed = id
        print("sending: focus on", id);
        self.Focus.emit(id)

    def insert(self,object = None):
        if object != None:
            id = object.getId()
            self.objects[id] = object
            self.Insert.emit(id,object)
            return 

        if random.randint(0,1) == 0:
            self.insert(SphereData())
        else:
            self.insert(CuboidData())
    
    def remove(self,id):
        if self.objects.get(id) == None:
            return
        object = self.objects[id]
        self.Remove.emit(id)
        del self.objects[id]
        return object

    def update(self,buffer):
        #Todo check if the update is valid
        id = self.focussed;
        if id == -1 or id not in self.objects:	return

        object = self.objects[id]
        print("updating")
        print(buffer)
        #if "name" in buffer: object.setName(buffer["name"])
        #if "shape" in buffer: object.setShape(buffer["shape"])
        if "rgb" in buffer: object.setColor(buffer["rgb"])
        #if "position" in buffer: object.setPosition(buffer["position"])
        #if "orientation" in buffer: object.setOrientation(buffer["orientation"])

        print(object)

        self.objects[id] = object
        self.Update.emit(id)

    def get(self,id):
        if id in self.objects: return self.objects[id]
        return None
    
    def print(self):
        for id in self.objects:
            print(self.objects[id].data)


class hehe:
    @Slot(int,int)
    def say_some_words(self,words,a):
        print(words)


class Communicate(QObject):
    speak = Signal(int,int)


haha = hehe()

someone = Communicate()
someone.speak.connect(haha.say_some_words)
print(type(someone.speak))
someone.speak.emit(10,20)

