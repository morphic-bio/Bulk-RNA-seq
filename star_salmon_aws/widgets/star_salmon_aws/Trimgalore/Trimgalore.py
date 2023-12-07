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

class OWTrimgalore(OWBwBWidget):
    name = "Trimgalore"
    description = "fastqc"
    priority = 5
    icon = getIconName(__file__,"fastqc_icon_100.png")
    want_main_area = False
    docker_image_name = "biodepot/trimgalore"
    docker_image_tag = "latest"
    inputs = [("inputFiles",str,"handleInputsinputFiles"),("basenames",str,"handleInputsbasenames"),("trigger",str,"handleInputstrigger"),("outputDir",str,"handleInputsoutputDir")]
    outputs = [("outputDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    inputFiles=pset([])
    outputDir=pset(None)
    paired=pset(False)
    fastqc=pset(True)
    gzipped=pset(True)
    ncores=pset(1)
    basenames=pset([])
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"Trimgalore")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsinputFiles(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputFiles", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsbasenames(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("basenames", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputstrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsoutputDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("outputDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputDir"):
            outputValue=getattr(self,"outputDir")
        self.send("outputDir", outputValue)
