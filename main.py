import sys

from PySide2.QtGui import (QVector3D)
from PySide2.Qt3DCore import (Qt3DCore)
from PySide2.Qt3DExtras import (Qt3DExtras)

from PySide2.QtCore import(Property, Signal)


from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide2.QtWidgets import QLineEdit, QVBoxLayout, QWidget

from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QFormLayout,QListWidget, QPushButton

from PySide2.QtCore import(Property, Signal)


import random


class Entity(Qt3DCore.QEntity):
    counter = 0
    def __init__(self,rootEntity):
        super(Entity, self).__init__(rootEntity)
        self._transform = Qt3DCore.QTransform()
        self.addComponent(self._transform)
        self._mesh = None
        self._material = None
        self.ID = str(Entity.counter)
        Entity.counter += 1

    def setPosition(self,x=None,y=None,z=None):
        x,y,z = [random.uniform(-10,10) for i in range(3)]
        self._transform.setTranslation(QVector3D(x,y,z))

    def getPosition():
        pass

    def setMesh(self,mesh):
        self._mesh = mesh
        self.addComponent(mesh)

    def setMaterial(self,material):
        self._material = material
        self.addComponent(material)

    def getID(self):
        return "Entity "+self.ID



class ObjView(Qt3DExtras.Qt3DWindow):
    def __init__(self,parent=None):
        super(ObjView, self).__init__()

        self.createScene()
        # Camera
        self.camera().lens().setPerspectiveProjection(45, 16 / 9, 0.1, 1000)
        self.camera().setPosition(QVector3D(0, 0, 40))
        self.camera().setViewCenter(QVector3D(0, 0, 0))
        # Controller
        self.camController = Qt3DExtras.QFirstPersonCameraController(self.rootEntity)
        self.camController.setLinearSpeed(50)
        self.camController.setLookSpeed(180)
        self.camController.setCamera(self.camera())


    def createScene(self):
        self.rootEntity = Qt3DCore.QEntity()
        self.setRootEntity(self.rootEntity)
        self.entites = []


class AttributesPanelController():
    def __init__(self):
        self._attributes = {}
        self.widget = QWidget()
        self.widget.setFixedWidth(250)
        self.widget.setLayout(QFormLayout())
        self.panel = self.widget.layout()

    def setAttributes(self,attributes):
        self._attributes = attributes
        while self.panel.rowCount() > 0:
            self.panel.removeRow(0)

        for attribute,value in attributes.items():
            print(type(attribute),type(value))
        self.panel.addRow(attribute,QLineEdit(str(value)))

    def getAttributes(self):
        return self._attributes

    attributesChanged = Signal()
    attributes = Property(dict, getAttributes, setAttributes, notify=attributesChanged)



class ObjWidget(QWidget):
    def __init__(self,par=None):
        super(ObjWidget, self).__init__(par)

        self.buttonLayout = QVBoxLayout()
        self.addCuboidButton =  QPushButton("Add Cuboid")
        self.addSphereButton =  QPushButton("Add Sphere")
        self.delButton = QPushButton("delete")

        self.buttonLayout.addWidget(self.addCuboidButton)
        self.buttonLayout.addWidget(self.addSphereButton)
        self.buttonLayout.addWidget(self.delButton)

        self.buttonWidget = QWidget()
        self.buttonWidget.setLayout(self.buttonLayout)

        self.list_widget = QListWidget();

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonWidget)
        self.layout.addWidget(self.list_widget)

        self.setLayout(self.layout);
        self.setFixedWidth(100)

    def getSelectedItem(self):
        return self.list_widget.currentItem()

    def getSelectedID(self):
        return self.list_widget.currentItem().text()

    def takeItem(self, row):
        return self.list_widget.takeItem(row)




class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("3DViewer")

        self.list_widget = ObjWidget()

        self.view = ObjView()
        self.view_container = QWidget.createWindowContainer(self.view)
        self.view_container.setParent(self);
        self.view_container.setFixedWidth(1000)
        self.view_container.setFixedHeight(600)

        self.panel_controller = AttributesPanelController();


        self.layout = QHBoxLayout()
        self.layout.addWidget(self.list_widget)

        self.list_widget.addCuboidButton.clicked.connect(self.add_cuboid_is_clicked)
        self.list_widget.addSphereButton.clicked.connect(self.add_sphere_is_clicked)
        self.list_widget.delButton.clicked.connect(self.delete_button_is_clicked)

        self.layout.addWidget(self.view_container)
        self.layout.addWidget(self.panel_controller.widget);
        #self.panel_controller.setAttributes({"asdasd":123123,"qweqw":124312})

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def add_cuboid_is_clicked(self):
        obj_view = self.view
        entity = Entity(obj_view.rootEntity)
        entity.setPosition(0,0,0)
        entity.setMesh(Qt3DExtras.QCuboidMesh())
        entity.setMaterial(Qt3DExtras.QPhongMaterial(obj_view.rootEntity))
        obj_view.entites.append(entity)
        self.list_widget.list_widget.addItem(entity.getID())

    def add_sphere_is_clicked(self):
        obj_view = self.view
        entity = Entity(obj_view.rootEntity)
        entity.setPosition(0,0,0)
        entity.setMesh(Qt3DExtras.QSphereMesh())
        entity.setMaterial(Qt3DExtras.QPhongMaterial(obj_view.rootEntity))
        obj_view.entites.append(entity)
        self.list_widget.list_widget.addItem(entity.getID())

    def delete_button_is_clicked(self):
        selected_ID = self.list_widget.getSelectedID()
        for i,entity in enumerate(self.view.entites):
            if entity.getID() == selected_ID:
                entity.setParent(None)
                del self.view.entites[i]
                self.list_widget.takeItem(i)
                break

if __name__ == '__main__':
    #app = QGuiApplication(sys.argv)
    app = QApplication(sys.argv)
    main_window = MainWindow();
    main_window.show()
    sys.exit(app.exec_())

