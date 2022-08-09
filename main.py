import sys

from PySide2.QtGui import (QVector3D)
from PySide2.Qt3DCore import (Qt3DCore)
from PySide2.Qt3DExtras import (Qt3DExtras)

import copy

from PySide2.QtCore import(Property, Signal)


from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide2.QtWidgets import QLineEdit, QVBoxLayout, QWidget

from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QFormLayout,QListWidget, QPushButton


from PySide2.QtWidgets import QComboBox
from PySide2.QtWidgets import QLabel

from PySide2.QtGui import QColor

from PySide2.QtCore import(Property, Signal, Slot, QObject)

from model import *

from collections import defaultdict


import random



class Entity(Qt3DCore.QEntity):
    def __init__(self,rootEntity=None):
        print(type(rootEntity))
        super(Entity, self).__init__(rootEntity)
        # store the references to the compoents
        self._transform = Qt3DCore.QTransform()
        self._mesh = None
        self._material = Qt3DExtras.QPhongMaterial(rootEntity)

        self.addComponent(self._material)
        self.addComponent(self._transform)

    def setRootEntity(self,rootEntity):
        self.rootEntity = rootEntity
        self._material = Qt3DExtras.QPhongMaterial(self.rootEntity)
        self.addComponent(self._material)

    def set_shape(self,id,shape_info):
        if shape_info["shape"] == "Sphere":
            radius = shape_info["radius"]
            self._mesh = Qt3DExtras.QSphereMesh()
            self._mesh.setRadius(radius)
            self.addComponent(self._mesh)

        if shape_info["shape"] == "Cuboid":
            x,y,z = shape_info["lengths"]
            self._mesh = Qt3DExtras.QCuboidMesh()
            self._mesh.setXExtent(x)
            self._mesh.setYExtent(y)
            self._mesh.setZExtent(z)
            self.addComponent(self._mesh)


    def remove(self):
        self.setRootEntity(None)
        self.removeComponent(self._transform)
        self.removeComponent(self._mesh)
        self.removeComponent(self._material)

    def set_position(self,id,position):
        x,y,z = position
        self._transform.setTranslation(QVector3D(x,y,z))

    def get_position(self):
        pass

        #shapeChanged = Signal(int,dict)
    def set_rgb(self,id,rgb):
        print('received')
        r,g,b = rgb
        self._material.setDiffuse(QColor(r,g,b));
        print("after set")
        print(self._material.diffuse().getRgb())

    def get_rgb(self):
        r,g,b,a = self._material.diffuse().getRgb()
        return (r,g,b)


class ObjectView(Qt3DExtras.Qt3DWindow):
    def __init__(self,parent=None):
        super(ObjectView, self).__init__()
        # Objects
        self.rootEntity = Qt3DCore.QEntity()
        self.setRootEntity(self.rootEntity)
        self.entities = {}
        # Camera
        self.camera().lens().setPerspectiveProjection(45, 16 / 9, 0.1, 1000)
        self.camera().setPosition(QVector3D(0, 0, 40))
        self.camera().setViewCenter(QVector3D(0, 0, 0))
        # Controller
        self.camController = Qt3DExtras.QFirstPersonCameraController(self.rootEntity)
        self.camController.setLinearSpeed(50)
        self.camController.setLookSpeed(180)
        self.camController.setCamera(self.camera())



    def insert(self,id,entity):
        self.entities[id] = entity
        return

    def get_object(self,id):
        return

    def remove(self,id):
        if id not in self.entities: return
        self.entities[id].remove()
        del self.entities[id]


    #def set_position(self,id,pos):
        #return
        #x,y,z = pos
        #self.entity._transform.setTranslation(QVector3D(x,y,z))

    #def get_position(self,id):
        #return
        #pass

    #def set_rgb(self,id,rgb):
        #return
        #r,g,b = rgb
        #self.entity._material.setDiffuse(QColor(r,g,b));

    #def get_rgb(self,id):
        #return
        #r,g,b,a = entity._material.diffuse().getRgb()
        #return (r,g,b)



    #{"shape":"Sphere", "size":{"radius":3.0}, "rgb":[122,0,255], "name":"my big sphere!!!", "position":[-11,25,3.1], "orientation":[1,2.0,-1],}
    #{"shape":"Cubiod", "size":{"height":3.0,"length":2.4, "width":0.1}, "rgb":[122,0,255], "name":"my big sphere!!!", "position":[-11,25,3.1], "orientation":[1,2.0,-1],}

class ObjectsController(QObject):
    def __init__(self):
        super(ObjectsController,self).__init__()
        self.view = ObjectView()
        self.model = None
        #self.model.remove.connect(self.remove)

    def setParent(self, parent):
        self.view.setParent(parent)
    def set_model(self, model):
        self.model = model
        print(type(model))
        self.model.Insert.connect(self.insert)
        self.model.Remove.connect(self.remove)
        pass


    def insert(self,id,object):
        entity = Entity(self.view.rootEntity)
        entity.set_shape(id,object.data)
        entity.set_position(id,object.data["position"])
        entity.set_rgb(id,object.data["rgb"])
        self.view.insert(id,entity)

        object.positionChanged.connect(entity.set_position);
        object.colorChanged.connect(entity.set_rgb);
        object.shapeChanged.connect(entity.set_shape);
        pass

    #def update(self,object):
        #pass

    def remove(self,id):
        entity = self.view.entities[id]
        object = self.model.objects[id]
        object.positionChanged.disconnect(entity.set_position);
        object.colorChanged.disconnect(entity.set_rgb);
        object.shapeChanged.disconnect(entity.set_shape);
        self.view.remove(id)
        return

class ListView(QWidget):
    def __init__(self,par=None):
        super(ListView, self).__init__(par)

        self.buttonLayout = QHBoxLayout()
        self.addButton =  QPushButton("+")
        self.delButton = QPushButton("-")
        self.buttonLayout.addWidget(self.addButton)
        self.buttonLayout.addWidget(self.delButton)

        self.buttonWidget = QWidget()
        self.buttonWidget.setLayout(self.buttonLayout)
        self.listWidget = QListWidget();

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonWidget)
        self.layout.addWidget(self.listWidget)
        self.setLayout(self.layout);
        self.setFixedWidth(100)

    def getSelctedRow(self):
        return self.listWidget.currentRow();

    def takeItem(self, row):
        return self.listWidget.takeItem(row)

    def addItem(self, item):
        return self.listWidget.addItem(item);


class ListViewController(QObject):
    def __init__(self):
        super(ListViewController, self).__init__()
        self.view = ListView()
        self.view.setFixedWidth(100)
        self.view.addButton.clicked.connect(self.add_button_is_clicked)
        self.view.delButton.clicked.connect(self.del_button_is_clicked)

        self.ids = []
        self.model = None

        self.view.listWidget.itemDoubleClicked.connect(self.view.listWidget.openPersistentEditor)
        self.view.listWidget.itemChanged.connect(self.item_is_changed)
        self.view.listWidget.itemSelectionChanged.connect(self.focus)


    def focus(self):
        row = self.view.getSelctedRow()
        id = self.ids[row]
        print("calling: focus on", id);
        self.model.focus(id)

    def set_parent(self,par):
        self.view.setParent(par)

    def set_model(self,model):
        self.model = model
        self.model.Insert.connect(self.insert)
        self.model.Remove.connect(self.remove)

    def insert(self, id, object):
        self.ids.append(id)
        name = object.data["name"]
        self.view.addItem(name)
        object.nameChanged.connect(self.change_name_display)
        print("receive")

    def remove(self, id):
        row = self.ids.index(id)
        del self.ids[row]
        self.view.takeItem(row)
        object = self.model.objects[id]
        object.nameChanged.disconnect(self.change_name_display)
        self.model.focus(-1)

    def change_name_display(self,id,name):
        row = self.ids.index(id)
        item = self.view.listWidget.item(row)
        item.setText(name)
        print("name = ", name)
        self.view.listWidget.closePersistentEditor(item)

    def item_is_changed(self,item):
        name = item.text()
        selected_row = self.view.getSelctedRow()
        id = self.ids[selected_row]
        self.model.objects[id].setName(name);

    def add_button_is_clicked(self):
        print("send")
        self.model.insert()

    def del_button_is_clicked(self):
        if(len(self.ids) == 0):	return
        selected_row = self.view.getSelctedRow()
        id = self.ids[selected_row]
        self.model.remove(id)

class DataView(QWidget):
    def __init__(self,par=None):
        super(DataView, self).__init__(par)
        self.layout = QFormLayout()
        self.setFixedWidth(100)
        self.editors = {}

    def clear(self):
        #self.layout = QFormLayout();
        self.editors  = {}
        while self.layout.count() > 0:
            self.layout.removeRow(0)

    def set_dict(self, title, keys, values):
        self.clear()
        if title != None: self.layout.addRow(title,QLabel())
        for key,value in zip(keys,values):
            print(key,value)
            self.editors[key] = QLineEdit(str(value))
            self.layout.addRow(key,self.editors[key])
        print(self.layout.count())

class PanelView(QWidget):
    def __init__(self,par=None):
        super(PanelView, self).__init__(par)
        self.setFixedWidth(150)

        self.layout = QFormLayout()
        self.name = QLabel()
        self.shape_box = QComboBox()
        self.size_view = DataView()
        self.rgb_view = DataView()
        self.position_view = DataView()
        self.orientation_view = DataView()
        self.apply_button = QPushButton()
        self.apply_button.setText("apply")


    def clear(self):
        #self.layout = QFormLayout()

        while self.layout.count() > 0:
            item = self.layout.itemAt(0)
            self.layout.removeItem(item)
            #self.layout.removeRow(0)

    def display(self, data):
        self.clear()
        print(self.layout.count())

        self.name.setText(data["name"])
        self.shape_box.addItems(["Sphere","Cuboid"])

        if(data["shape"] == "Sphere"):
            self.size_view.set_dict(None,["radius"],[data["radius"]])
            self.shape_box.setCurrentIndex(0)
        else:
            keys = ("length","width","height")
            values = data["lengths"]
            self.size_view.set_dict(None,keys,values)
            self.shape_box.setCurrentIndex(1)

        keys = ("Red","Green","Blue")
        values = data["rgb"]
        self.rgb_view.set_dict("Color",keys,values)

        keys = ("X","Y","Z")
        values = data["position"]
        self.position_view.set_dict("Coordinates",keys,values)


        keys = ("x","y","z")
        values = data["orientation"]
        self.orientation_view.set_dict("Orientation",keys,values)


        self.layout.addRow(self.size_view.layout)
        self.layout.addRow(self.rgb_view.layout)
        self.layout.addRow(self.position_view.layout)
        self.layout.addRow(self.orientation_view.layout)
        self.layout.addRow(self.shape_box)
        self.layout.addRow(self.apply_button)
        self.setLayout(self.layout)

        print(self.layout.count())


class PanelController(QObject):
    def __init__(self):
        super(PanelController,self).__init__()
        self.view = PanelView()
        self.model = None
        self.par = None

    def setParent(self,par):
        self.par = par
        self.view.setParent(par)

    def update_object(self):
        shape = self.view.shape_box.currentText()

        data = defaultdict(None)
        data["shape"] = shape

        buffer = defaultdict(None)

        for key, editor in self.view.size_view.editors.items(): buffer[key] = editor.text();
        for key, editor in self.view.rgb_view.editors.items(): buffer[key] = editor.text();
        for key, editor in self.view.position_view.editors.items(): buffer[key] = editor.text();
        for key, editor in self.view.orientation_view.editors.items(): buffer[key] = editor.text();

        print(buffer)

        if(shape == "Sphere"):
            data["radius"] = buffer["radius"]
        else:
            lengths = (buffer["length"],buffer["width"],buffer["height"])
            data["lengths"] = lengths

        rgb = (buffer["Red"],buffer["Green"],buffer["Blue"])
        position = (buffer["X"],buffer["Y"],buffer["Z"])
        orientation = (buffer["x"],buffer["y"],buffer["z"])

        data["rgb"]=rgb
        data["position"]=position
        data["orientation"]=orientation

        self.model.update(data)

    def update(self,id):
        #self.data = self.model.objects[id].data
        self.view.display(self.model.objects[id].data)



    def set_model(self,model):
        self.model = model
        self.model.Focus.connect(self.change_focus)
        self.model.Update.connect(self.update)

    def change_focus(self,id):
        print("receiving: focus on", id);
        if(id == -1):
            self.view.apply_button.clicked.disconnect(self.update_object)
            self.view.clear()
        else:
            #self.data = copy.deepcopy(self.model.objects[id].data)
            self.view.display(self.model.objects[id].data)
            self.view.apply_button.clicked.connect(self.update_object)
        pass


class MainController(QMainWindow):

    def __init__(self):
        super(MainController, self).__init__()
        self.setWindowTitle("3DViewer")

        self.model = ObjectModel()


        self.objects_controller = ObjectsController()
        self.objects_controller.set_model(self.model)

        self.objects_contianer = QWidget.createWindowContainer(self.objects_controller.view)
        self.objects_contianer.setParent(self);
        self.objects_contianer.setFixedWidth(500)
        self.objects_contianer.setFixedHeight(300)

        self.list_controller = ListViewController()
        self.list_controller.set_model(self.model)

        self.panel_controller = PanelController();
        self.panel_controller.set_model(self.model)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.list_controller.view)
        self.layout.addWidget(self.objects_contianer)
        self.layout.addWidget(self.panel_controller.view);

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)


if __name__ == '__main__':
    #app = QGuiApplication(sys.argv)
    app = QApplication(sys.argv)
    main_window = MainController();
    main_window.show()
    sys.exit(app.exec_())

