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

class OWstarIndex(OWBwBWidget):
    name = "starIndex"
    description = "Construct indices for STAR aligner "
    priority = 11
    icon = getIconName(__file__,"starIndex.png")
    want_main_area = False
    docker_image_name = "biodepot/multistar"
    docker_image_tag = "latest"
    inputs = [("Trigger",str,"handleInputsTrigger"),("starversion",str,"handleInputsstarversion"),("genomeDir",str,"handleInputsgenomeDir"),("sjdbGTFfile",str,"handleInputssjdbGTFfile"),("genomeFastaFile",str,"handleInputsgenomeFastaFile"),("skipIndex",str,"handleInputsskipIndex")]
    outputs = [("genomeDir",str),("starversion",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    rmode=pset("genomeGenerate")
    genomeDir=pset(None)
    genomeFastaFile=pset(None)
    genomeChrBinNbits=pset("18")
    genomeSAindexNbases=pset(14)
    genomeSAsparseD=pset(1)
    genomeSuffixLengthMax=pset(-1)
    runThreadN=pset(1)
    sjdbGTFfile=pset(None)
    sjdbFileChrStartEnd =pset([])
    sjdbGTFchrPrefix =pset("chr")
    sjdbGTFfeatureExon=pset("exon")
    sjdbGTFtagExonParentTranscript=pset("transcript_id")
    sjdbGTFtagExonParentGene=pset("gene_id")
    sjdbOverhang=pset(100)
    sjdbScore=pset(2)
    sjdbInsertSave =pset("Basic")
    starversion=pset("2.7.11a")
    overwrite=pset(False)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"starIndex")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsstarversion(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("starversion", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsgenomeDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("genomeDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputssjdbGTFfile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("sjdbGTFfile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsgenomeFastaFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("genomeFastaFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsskipIndex(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("skipIndex", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"genomeDir"):
            outputValue=getattr(self,"genomeDir")
        self.send("genomeDir", outputValue)
        outputValue=None
        if hasattr(self,"starversion"):
            outputValue=getattr(self,"starversion")
        self.send("starversion", outputValue)
