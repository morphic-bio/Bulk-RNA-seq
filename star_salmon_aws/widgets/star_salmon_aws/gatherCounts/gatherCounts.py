import os
import glob
import sys
import functools
import jsonpickle
from collections import OrderedDict
from Orange.widgets import widget, gui, settings
import Orange.data
from Orange.data.io import FileFormat
from DockerClient import DockerClient
from BwBase import OWBwBWidget, ConnectionDict, BwbGuiElements, getIconName, getJsonName
from PyQt5 import QtWidgets, QtGui

class OWgatherCounts(OWBwBWidget):
    name = "gatherCounts"
    description = "Gathers counts from star/salmon workflow"
    priority = 13
    icon = getIconName(__file__,"startodeseq2.png")
    want_main_area = False
    docker_image_name = "biodepot/gathercounts"
    docker_image_tag = "cbbd690a__21b9851b__e5512470"
    inputs = [("countsDir",str,"handleInputscountsDir"),("alignsDir",str,"handleInputsalignsDir"),("tablesDir",str,"handleInputstablesDir"),("trigger",str,"handleInputstrigger")]
    outputs = [("tablesDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    countsDir=pset(None)
    alignsDir=pset(None)
    tablesDir=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"gatherCounts")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputscountsDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("countsDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsalignsDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("alignsDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputstablesDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("tablesDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputstrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"tablesDir"):
            outputValue=getattr(self,"tablesDir")
        self.send("tablesDir", outputValue)
