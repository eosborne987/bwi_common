from qt_gui.plugin import Plugin
from python_qt_binding.Qt import KeepAspectRatio
from python_qt_binding.QtGui import QFrame, QHBoxLayout, QLabel, QLineEdit, \
                                    QPixmap, QPushButton, QTextBrowser, QVBoxLayout, \
                                    QWidget
# from python_qt_binding.QtCore import SIGNAL

def clear_layout(layout):
    # Clear all subfunction buttons.
    while layout.count():
        item = layout.takeAt(0)
        item.widget().deleteLater()

class LocationFunction(object):

    def __init__(self):
        self.subfunction_buttons = None
        self.current_subfunction = "Edit Location"

    def handleSubfunctionReset(self, 
                               widget,
                               subfunction_layout,
                               values_layout,
                               subfunction_button_callback,
                               image_objects,
                               image_label):

        if self.subfunction_buttons is not None:
            del self.subfunction_buttons[:]

        self.subfunction_buttons = []

        # Add all the necessary buttons to the subfunction layout.
        for button_text in ['Add Location', 'Remove Location']:
            button = QPushButton(button_text, widget)
            button.clicked[bool].connect(subfunction_button_callback)
            button.setCheckable(True)
            subfunction_layout.addWidget(button)
            self.subfunction_buttons.append(button)

        # When this function is engaged, 
        clear_layout(values_layout)

        # TODO display all the current locations that we know about. Until then, clear everything that is drawn on the
        # image.
        if len(image_objects) != 0:
            del image_objects[:]

        # Handle mouse event
        image_label.mousePressEvent = self.handleMouseEvent

    def handleMouseEvent(self, event):
        # TODO depending on the subfunction pressed, do something useful here. 
        # If not adding/removing a location here, allowing editing a selected location here.
        print "Mouse pressed at " + str(event.pos().x()) + "," + str(event.pos().y())

    def handleNewSubfunction(self,
                             widget,
                             source,
                             value_edit_callback):

        # Ensure that all buttons apart from the current subfunction are depressed.
        for button in self.subfunction_buttons:
            if button != source:
                button.setChecked(False)

        # Switch to add/remove depending on the subfunction button pressed.
        self.current_subfunction = source.text()

class DoorFunction(object):

    def __init__(self):
        self.subfunction_buttons = None
        self.current_subfunction = "Edit Door"

    def handleSubfunctionReset(self, 
                               widget,
                               subfunction_layout,
                               values_layout,
                               subfunction_button_callback,
                               image_objects,
                               image_label):

        if self.subfunction_buttons is not None:
            del self.subfunction_buttons[:]

        self.subfunction_buttons = []

        # Add all the necessary buttons to the subfunction layout.
        for button_text in ['Add Door', 'Remove Door']:
            button = QPushButton(button_text, widget)
            button.clicked[bool].connect(subfunction_button_callback)
            button.setCheckable(True)
            subfunction_layout.addWidget(button)
            self.subfunction_buttons.append(button)

        # When this function is engaged, 
        clear_layout(values_layout)

        # TODO display all the current locations that we know about. Until then, clear everything that is drawn on the
        # image.
        if len(image_objects) != 0:
            del image_objects[:]

        # Handle mouse event
        image_label.mousePressEvent = self.handleMouseEvent

    def handleMouseEvent(self, event):
        # TODO depending on the subfunction pressed, do something useful here. 
        # If not adding/removing a location here, allowing editing a selected location here.
        print "Mouse pressed at " + str(event.pos().x()) + "," + str(event.pos().y())

    def handleNewSubfunction(self,
                             widget,
                             source,
                             value_edit_callback):

        # Ensure that all buttons apart from the current subfunction are depressed.
        for button in self.subfunction_buttons:
            if button != source:
                button.setChecked(False)

        # Switch to add/remove depending on the subfunction button pressed.
        self.current_subfunction = source.text()

class ObjectFunction(object):

    def __init__(self):
        self.subfunction_buttons = None
        self.current_subfunction = "Edit Object"

    def handleSubfunctionReset(self, 
                               widget,
                               subfunction_layout,
                               values_layout,
                               subfunction_button_callback,
                               image_objects,
                               image_label):

        if self.subfunction_buttons is not None:
            del self.subfunction_buttons[:]

        self.subfunction_buttons = []

        # Add all the necessary buttons to the subfunction layout.
        for button_text in ['Add Object', 'Remove Object']:
            button = QPushButton(button_text, widget)
            button.clicked[bool].connect(subfunction_button_callback)
            button.setCheckable(True)
            subfunction_layout.addWidget(button)
            self.subfunction_buttons.append(button)

        # When this function is engaged, 
        clear_layout(values_layout)

        # TODO display all the current locations that we know about. Until then, clear everything that is drawn on the
        # image.
        if len(image_objects) != 0:
            del image_objects[:]

        # Handle mouse event
        image_label.mousePressEvent = self.handleMouseEvent

    def handleMouseEvent(self, event):
        # TODO depending on the subfunction pressed, do something useful here. 
        # If not adding/removing a location here, allowing editing a selected location here.
        print "Mouse pressed at " + str(event.pos().x()) + "," + str(event.pos().y())

    def handleNewSubfunction(self,
                             widget,
                             source,
                             value_edit_callback):

        # Ensure that all buttons apart from the current subfunction are depressed.
        for button in self.subfunction_buttons:
            if button != source:
                button.setChecked(False)

        # Switch to add/remove depending on the subfunction button pressed.
        self.current_subfunction = source.text()

class LogicalMarkerPlugin(Plugin):

    def __init__(self, context):
        super(LogicalMarkerPlugin, self).__init__(context)

        # TODO read in map file and data directory.
        # Give QObjects reasonable names
        self.setObjectName('LogicalMarkerPlugin')

        # Create QWidget
        self._widget = QWidget()
        self._master_layout = QVBoxLayout(self._widget)

        # Main Functions - Doors, Locations, Objects
        self._function_layout = QHBoxLayout(self._widget)
        self._master_layout.addLayout(self._function_layout)
        self.function_buttons = []
        self.current_function = None
        for button_text in ['Doors', 'Locations', 'Objects']:
            button = QPushButton(button_text, self._widget)
            button.clicked[bool].connect(self.handle_function_button)
            button.setCheckable(True)
            self._function_layout.addWidget(button)
            self.function_buttons.append(button)

        self.functions = {}
        self.functions['Doors'] = DoorFunction()
        self.functions['Locations'] = LocationFunction()
        self.functions['Objects'] = ObjectFunction()

        self._master_layout.addWidget(self.HLine)

        self._subfunction_layout = QHBoxLayout(self._widget)
        self._master_layout.addLayout(self._subfunction_layout)
        self.current_subfunction = None

        self._master_layout.addWidget(self.HLine)

        # TODO figure out how to update the map image, and how to read in the map file.
        self.map_image = None
        self._image_label = QLabel(self._widget)
        # myPixmap = QPixmap(self.map_image)
        # myScaledPixmap = myPixmap.scaled(self._image_label.size(), KeepAspectRatio)
        # self._image_label.setPixmap(myScaledPixmap)

        self._master_layout.addWidget(self.HLine)

        self._values_layout = QHBoxLayout(self._widget)
        self._master_layout.addLayout(self._values_layout)

        self._widget.setObjectName('LogicalMarkerPluginUI')
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        context.add_widget(self._widget)

        #self.connect(self._widget, SIGNAL("update"), self.update)

    def HLine(self):
        """
        http://stackoverflow.com/questions/5671354/how-to-programmatically-make-a-horizontal-line-in-qt
        """
        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        return hline

    def handle_function_button(self):
        source = self.sender()

        if source.text() == self.current_function:
            source.setChecked(True)
            return

        # Depress all other buttons.
        for button in self.function_buttons:
            if button != source:
                button.setChecked(False)

        self.current_function = source.text()

        self.reset_subfunction(False)
        #self.update()

    def reset_subfunction(self, trigger_update):

        # Clear all subfunction buttons.
        clear_layout(self._subfunction_layout)

        if self.current_function is not None:
            self.functions[self.current_function].handleSubfunctionReset(self._widget, 
                                                                         self._subfunction_layout, 
                                                                         self._values_layout,
                                                                         self.handle_subfunction_button,
                                                                         self._drawn_objects,
                                                                         self._image_label)

        self.current_subfunction = None

        # if trigger_update:
        #     self.update()

    def handle_subfunction_button(self):
        source = self.sender()

        if source.text() == self.current_subfunction:
            source.setChecked(True)
            return

        # I believe pressing a button should never change what's drawn on the image.
        self.functions[self.current_function].handleNewSubfunction(self._widget,
                                                                   source,
                                                                   self._values_layout,
                                                                   self.handle_value_edit)

        self.current_subfunction = source.text()
        # self.update()


    def shutdown_plugin(self):
        pass

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.set_value(k, v)
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass

    #def trigger_configuration(self):
        # Comment in to signal that the plugin has a way to configure
        # This will enable a setting button (gear icon) in each dock widget title bar
        # Usually used to open a modal configuration dialog
