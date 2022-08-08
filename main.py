import sys

from PySide2.QtGui import (QGuiApplication,  QVector3D)
from PySide2.Qt3DCore import (Qt3DCore)
from PySide2.Qt3DExtras import (Qt3DExtras)

class Window(Qt3DExtras.Qt3DWindow):
    def __init__(self):
        super(Window, self).__init__()

        # Camera
        self.camera().lens().setPerspectiveProjection(45, 16 / 9, 0.1, 1000)
        self.camera().setPosition(QVector3D(0, 0, 40))
        self.camera().setViewCenter(QVector3D(0, 0, 0))

        self.createScene()

        self.setRootEntity(self.rootEntity)

    def createScene(self):
        self.rootEntity = Qt3DCore.QEntity()

        self.material = Qt3DExtras.QPhongMaterial(self.rootEntity)

        # Cuboid
        self.cuboidEntity = Qt3DCore.QEntity(self.rootEntity)
        self.cuboidMesh = Qt3DExtras.QCuboidMesh()
        self.cuboidMesh.setXExtent(3)


        self.initalTransform = Qt3DCore.QTransform()
        self.initalTransform.setTranslation(QVector3D(0, 5, 0))

        self.cuboidEntity.addComponent(self.cuboidMesh)
        self.cuboidEntity.addComponent(self.initalTransform)
        self.cuboidEntity.addComponent(self.material)

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    view = Window()
    view.show()
    sys.exit(app.exec_())
