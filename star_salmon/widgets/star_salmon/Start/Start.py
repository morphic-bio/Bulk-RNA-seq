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

class OWStart(OWBwBWidget):
    name = "Start"
    description = "Enter workflow parameters and start"
    priority = 10
    icon = getIconName(__file__,"start.png")
    want_main_area = False
    docker_image_name = "biodepot/gdc-mrna-start"
    docker_image_tag = "alpine_3.12__59b7cb77"
    outputs = [("work_dir",str),("genome_dir",str),("genome_file",str),("annotation_file",str),("geneinfo",str),("bypass_star_index",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    work_dir=pset(None)
    genome_dir=pset(None)
    genome_file=pset(None)
    annotation_file=pset(None)
    geneinfo=pset(None)
    bypass_star_index=pset(True)
    downloadindexlink=pset(False)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"Start")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"work_dir"):
            outputValue=getattr(self,"work_dir")
        self.send("work_dir", outputValue)
        outputValue=None
        if hasattr(self,"genome_dir"):
            outputValue=getattr(self,"genome_dir")
        self.send("genome_dir", outputValue)
        outputValue=None
        if hasattr(self,"genome_file"):
            outputValue=getattr(self,"genome_file")
        self.send("genome_file", outputValue)
        outputValue=None
        if hasattr(self,"annotation_file"):
            outputValue=getattr(self,"annotation_file")
        self.send("annotation_file", outputValue)
        outputValue=None
        if hasattr(self,"geneinfo"):
            outputValue=getattr(self,"geneinfo")
        self.send("geneinfo", outputValue)
        outputValue=None
        if hasattr(self,"bypass_star_index"):
            outputValue=getattr(self,"bypass_star_index")
        self.send("bypass_star_index", outputValue)
