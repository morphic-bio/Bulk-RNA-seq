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

class OWsalmon(OWBwBWidget):
    name = "salmon"
    description = "salmon"
    priority = 10
    icon = getIconName(__file__,"salmon.png")
    want_main_area = False
    docker_image_name = "biodepot/salmon"
    docker_image_tag = "latest"
    inputs = [("transciptome",str,"handleInputstransciptome"),("alignments",str,"handleInputsalignments"),("outputfiles",str,"handleInputsoutputfiles")]
    outputs = [("outputfiles",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    transcriptome=pset(None)
    outputdirs=pset("salmon-quant")
    alignmentfiles=pset({})
    gtffile=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"salmon")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputstransciptome(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("transciptome", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsalignments(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("alignments", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsoutputfiles(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("outputfiles", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputfiles"):
            outputValue=getattr(self,"outputfiles")
        self.send("outputfiles", outputValue)
