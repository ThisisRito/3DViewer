import sys

from PySide2.QtGui import (QGuiApplication,  QVector3D)
from PySide2.Qt3DCore import (Qt3DCore)
from PySide2.Qt3DExtras import (Qt3DExtras)

class Window(Qt3DExtras.Qt3DWindow):
    def __init__(self):
        super(Window, self).__init__()

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

        self.material = Qt3DExtras.QPhongMaterial(self.rootEntity)
        self.initalTransform = Qt3DCore.QTransform()
        self.initalTransform.setTranslation(QVector3D(0, 5, 0))

        # Cuboid
        self.cuboidEntity = Qt3DCore.QEntity(self.rootEntity)
        self.cuboidMesh = Qt3DExtras.QCuboidMesh()
        self.cuboidMesh.setXExtent(3)
        self.cuboidEntity.addComponent(self.cuboidMesh)
        self.cuboidEntity.addComponent(self.initalTransform)
        self.cuboidEntity.addComponent(self.material)

        # Sphere
        self.sphereEntity = Qt3DCore.QEntity(self.rootEntity)
        self.sphereMesh = Qt3DExtras.QSphereMesh()
        self.sphereMesh.setRadius(1)
        self.sphereEntity.addComponent(self.sphereMesh)
        self.sphereEntity.addComponent(self.material)


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    view = Window()
    view.show()
    sys.exit(app.exec_())
