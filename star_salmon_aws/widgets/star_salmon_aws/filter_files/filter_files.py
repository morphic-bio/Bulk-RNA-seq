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

class OWfilter_files(OWBwBWidget):
    name = "filter_files"
    description = "alpine bash with wget curl gzip bzip2"
    priority = 1
    icon = getIconName(__file__,"bash.png")
    want_main_area = False
    docker_image_name = "biodepot/bash_utilities"
    docker_image_tag = "alpine-3.17.1__24884064__91e2e7b9__1a66801e"
    inputs = [("inputdir",str,"handleInputsinputdir"),("Trigger",str,"handleInputsTrigger")]
    outputs = [("fastqfiles",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    inputdir=pset(None)
    fastqfiles=pset([])
    pattern=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"filter_files")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsinputdir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputdir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"fastqfiles"):
            outputValue=getattr(self,"fastqfiles")
        self.send("fastqfiles", outputValue)
