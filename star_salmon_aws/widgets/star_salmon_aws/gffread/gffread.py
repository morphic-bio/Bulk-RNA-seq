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

class OWgffread(OWBwBWidget):
    name = "gffread"
    description = "Enter and output a file"
    priority = 10
    icon = getIconName(__file__,"gffread.jpg")
    want_main_area = False
    docker_image_name = "biodepot/gffread"
    docker_image_tag = "latest"
    inputs = [("gtffile",str,"handleInputsgtffile"),("genomefile",str,"handleInputsgenomefile"),("outputfile",str,"handleInputsoutputfile"),("trigger",str,"handleInputstrigger"),("skipGFF",str,"handleInputsskipGFF")]
    outputs = [("outputfile",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    genomefile=pset(None)
    gtffile=pset(None)
    outputfile=pset(None)
    overwritefiles=pset(False)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"gffread")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsgtffile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("gtffile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsgenomefile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("genomefile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsoutputfile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("outputfile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputstrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsskipGFF(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("skipGFF", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputfile"):
            outputValue=getattr(self,"outputfile")
        self.send("outputfile", outputValue)
