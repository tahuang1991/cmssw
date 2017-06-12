# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: l1Ntuple0913 -s RAW2DIGI --era=Run2_2016 --customise=L1Trigger/Configuration/customiseReEmul.L1TReEmulFromRAW --customise=L1Trigger/Configuration/customiseUtils.L1TTurnOffUnpackStage2GtGmtAndCalo --conditions=80X_dataRun2_Prompt_v11 -n 20 --data --no_output --filein=/store/data/Run2016G/ZeroBias/RAW/v1/000/278/986/00000/12104D7A-0065-E611-B62C-FA163E52E986.root
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('RAW2DIGI',eras.Run2_2016)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring('/store/data/Run2016G/ZeroBias/RAW/v1/000/278/986/00000/12104D7A-0065-E611-B62C-FA163E52E986.root'),
    #fileNames = cms.untracked.vstring('/store/data/Run2015D/SingleMuon/RAW/v1/000/256/734/00000/8200C0B8-0F5E-E511-80B2-02163E014415.root'),
    fileNames = cms.untracked.vstring('/store/mc/RunIISpring16DR80/JPsiToMuMu_Pt20to100-pythia8-gun/GEN-SIM-RAW/PU2016_Classic_withHLT_80X_mcRun2_asymptotic_v14-v1/100000/02CF1BE1-4671-E611-96CE-44A84225C911.root'),
    #fileNames = cms.untracked.vstring('/store/data/Run2016H/SingleMuon/RAW/v1/000/284/042/00000/*.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('l1Ntuple0913 nevts:20'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition
process.FEVTDEBUGoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    outputCommands = cms.untracked.vstring('drop *',
                                           'keep *_simCscTriggerPrimitiveDigis_*_*',
                                           'keep *_csctfDigis_*_*',
                                           'keep *_simEmtfDigis_*_*',
                                           'keep *_emtfStage2Digis_*_*',
					   'keep CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_*_*_*',
                                           'keep *_muonCSCDigis_*_*',
                                           'keep *_simMuon*_*_*'
                                           ),
    #eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('outl1.root'),
    splitLevel = cms.untracked.int32(0)
    )
# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_dataRun2_Prompt_v11', '')


#CSC Trigger Primitives reader
# =============================
process.load("CSCTriggerPrimitivesReader_cfi")
process.lctreader.debug = cms.untracked.bool(True)
#process.lctreader.CSCLCTProducerData = cms.untracked.string("emtfStage2Digis")
process.TFileService = cms.Service("TFileService",
	    fileName = cms.string('TPEHists_Run2016H.root')
	)

"""
process.MessageLogger = cms.Service("MessageLogger",
    destinations = cms.untracked.vstring('debug',
					 'Info',
					 'Warn'),
    debug = cms.untracked.PSet(
        extension = cms.untracked.string(".txt"),
        threshold = cms.untracked.string("DEBUG"),
        #threshold = cms.untracked.string("INFO"),
	#limit = cms.untracked.int32(1),
        lineLength = cms.untracked.int32(132),
        noLineBreaks = cms.untracked.bool(True)
    ),
    Info = cms.untracked.PSet(
        extension = cms.untracked.string(".txt"),
	#limit = cms.untracked.int32(-1),
        threshold = cms.untracked.string("INFO")
	),
    Warn = cms.untracked.PSet(
        extension = cms.untracked.string(".txt"),
	#limit = cms.untracked.int32(-1),
        threshold = cms.untracked.string("WARNING")
	),
    # debugModules = cms.untracked.vstring("*")
    debugModules = cms.untracked.vstring("cscTriggerPrimitiveDigis", 
        "lctreader")
)
"""

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.output_step = cms.EndPath(process.FEVTDEBUGoutput)
process.lctreader_step = cms.Path(process.lctreader)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.endjob_step)

# customisation of the process.

# Automatic addition of the customisation function from L1Trigger.Configuration.customiseReEmul
from L1Trigger.Configuration.customiseReEmul import L1TReEmulFromRAW 

#print "before add L1ReEmul ",process.schedule
#call to customisation function L1TReEmulFromRAW imported from L1Trigger.Configuration.customiseReEmul
process = L1TReEmulFromRAW(process)

#print "add L1ReEmul ",process.schedule
# Automatic addition of the customisation function from L1Trigger.Configuration.customiseUtils
from L1Trigger.Configuration.customiseUtils import L1TTurnOffUnpackStage2GtGmtAndCalo 

#call to customisation function L1TTurnOffUnpackStage2GtGmtAndCalo imported from L1Trigger.Configuration.customiseUtils
process = L1TTurnOffUnpackStage2GtGmtAndCalo(process)

# End of customisation functions
process.schedule.append(process.lctreader_step)

print "all modules",process.schedule

