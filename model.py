# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass


from PySide2.QtCore import(Property, Signal, Slot, QObject)
from PySide2.QtGui import (QVector3D)

import json
import random


class ObjectData(QObject):
    counter = 0
    def __init__(self,data=None):
        super(ObjectData,self).__init__()

        if data != None:
            self.data = data
            return

        ObjectData.counter += 1
        print("increase")
        self.data = {
            "shape":None,
            "rgb":tuple([random.randint(0,255) for i in range(3)]),
            "position":tuple([random.uniform(-10,10) for i in range(3)]),
            "quaternion":([random.gauss(0, 1) for i in range(3)] + [random.uniform(-180,180)]),
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

        try:
            X,Y,Z = map(float,pos)
            pos = X,Y,Z
        except:
            print("position value error")
            return
        self.data["position"] = pos
        id = self.getId()
        print("ObjectData.setPosition emits",id,pos)
        self.positionChanged.emit(id,pos)

    def setColor(self, rgb):
        #print('entering set color')
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
        print("ObjectData.setColor emits",id,rgb)
        self.colorChanged.emit(id,rgb)

    def setName(self, name):
        if name == self.data["name"]:	return
        self.data["name"] = name
        id = self.getId()
        print("ObjectData.setName emits",id,name)
        self.nameChanged.emit(id,name)

    def setShape(self, shape_info):
        if "shape" not in shape_info: raise
        if shape_info["shape"] == "Sphere":
            self.setSphere(shape_info["radius"])
        if shape_info["shape"] == "Cuboid":
            self.setCuboid(shape_info["lengths"])

    def setSphere(self, radius):
        if self.data["shape"] == "Sphere" and radius == self.data["radius"]: return
        try:
            radius = float(radius)
            if radius <= 0:
                raise
        except:
            print("radius value error")
            return
        shape_info = {"shape":"Sphere", "radius":radius}
        self.data.update(shape_info)
        id = self.getId()
        print("ObjectData.setSphere emits",id,shape_info)
        self.shapeChanged.emit(id,shape_info)

    def setCuboid(self, lengths):
        if self.data["shape"] == "Cuboid" and lengths == self.data["lengths"]: return
        try:
            a,b,c = map(float,lengths)
            if a <= 0 or b <= 0 or c <= 0:
                raise
            lengths = (a,b,c)
        except Exception as e:
            print(e)
            print("lengths value error")
            return
        shape_info = {"shape":"Cuboid", "lengths":lengths}
        self.data.update(shape_info)
        id = self.getId()
        print("ObjectData.setCuboid emits",id,shape_info)
        self.shapeChanged.emit(id,shape_info)

    def setOrientation(self, quaternion):
        try:
            a,b,c,d = map(float,quaternion)
            quaternion = a,b,c,d
        except:
            print("rotation parameter error")
            return
        self.data["quaternion"] = quaternion
        print("ObjectData.setOrientation emits",id,quaternion)
        self.orientationChanged.emit(id,quaternion)


    positionChanged = Signal(int,tuple)
    orientationChanged = Signal(int,tuple)
    colorChanged = Signal(int,tuple)
    shapeChanged = Signal(int,dict)
    nameChanged = Signal(int,str)

"""
{"shape":"Sphere", "size":{"radius":3.0}, "rgb":[122,0,255], "name":"my big sphere!!!", "position":[-11,25,3.1], "quaternion":(1,2.0,-1,1)}
{"shape":"Cubiod", "size":{"height":3.0,"length":2.4, "width":0.1}, "rgb":[122,0,255], "name":"my big sphere!!!", "position":[-11,25,3.1], "quaternion":(1,2.0,-1,1)}
"""

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
    backup = "/tmp/3DView.json"


    def __init__(self):
        super(ObjectModel,self).__init__()
        self.objects = {}
        self.focussed = -1

    def focus(self,id):
        if(self.focussed == id):	return
        self.focussed = id
        print("ObjectModel.focus", id)
        self.Focus.emit(id)

    def save_to_json(self):
        buffer = dict()
        buffer["id_counter"] = ObjectData.counter
        buffer["objects"] = {}


        for id,object in self.objects.items():
            buffer["objects"][id] = object.data
        return json.dumps(buffer)

    def load_from_json(self,data):
        try:
            data = json.loads(data)
            ObjectData.counter = data["id_counter"]
            objects = data["objects"]
            for id,object in objects.items():
                self.insert(ObjectData(object))
        except:
            raise
            print("local storage error")
            return

    def save(self,backup):
        js_data = self.save_to_json()
        with open(backup,'w') as file:
            file.write(js_data)

    def load(self,backup):
        js_data = None
        try:
            with open(backup,'r') as file:
                js_data = file.read()
            self.load_from_json(js_data)
        except Exception as e:
            print(e)
            return

    def insert(self,object = None):
        if object != None:
            id = object.getId()
            self.objects[id] = object
            print("ObjectModel.insert emits",id,object)
            self.Insert.emit(id,object)
            self.save(ObjectModel.backup)
            return

        if random.randint(0,1) == 0:
            self.insert(SphereData())
        else:
            self.insert(CuboidData())
    
    def remove(self,id):
        if self.objects.get(id) == None:
            return
        object = self.objects[id]
        if(id == self.focussed):
            self.focus(-1)

        print("ObjectModel.remove emits",id)
        self.Remove.emit(id)
        del self.objects[id]
        self.save(ObjectModel.backup)
        return object

    def set_name(self,id,name):
        if id not in self.objects:
            return
        object = self.objects[id]
        object.setName(name)
        self.save(ObjectModel.backup)

    def update(self,buffer):
        id = self.focussed
        if id == -1 or id not in self.objects:	return

        object = self.objects[id]
        #if "name" in buffer: object.setName(buffer["name"])
        if "shape" in buffer: object.setShape(buffer)
        if "rgb" in buffer: object.setColor(buffer["rgb"])
        if "quaternion" in buffer: object.setOrientation(buffer["quaternion"])
        if "position" in buffer: object.setPosition(buffer["position"])

        self.save(ObjectModel.backup)
        self.objects[id] = object

        print("ObjectModel.update emmits",id)
        self.Update.emit(id)

    def get(self,id):
        if id in self.objects: return self.objects[id]
        return None
    
    def print(self):
        for id in self.objects:
            print(self.objects[id].data)
