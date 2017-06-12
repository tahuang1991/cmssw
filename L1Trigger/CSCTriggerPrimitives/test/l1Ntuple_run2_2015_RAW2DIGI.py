# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: l1Ntuple_run2_2015 -s RAW2DIGI --era=Run2_25ns --customise=L1Trigger/Configuration/customiseReEmul.L1TReEmulFromRAW2015 --conditions=auto:run2_data -n 20 --data --no_output --filein=out_raw.root
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('RAW2DIGI',eras.Run2_25ns)

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
    fileNames = cms.untracked.vstring('/store/data/Run2015D/SingleMuon/RAW/v1/000/256/629/00000/1CD00EF3-6E5C-E511-B06A-02163E01384D.root',
				      '/store/data/Run2015D/SingleMuon/RAW/v1/000/256/630/00000/0025E06B-825C-E511-85F3-02163E012339.root',
				      '/store/data/Run2015D/SingleMuon/RAW/v1/000/256/630/00000/242367E6-815C-E511-A8C7-02163E013996.root',
				      '/store/data/Run2015D/SingleMuon/RAW/v1/000/256/630/00000/56D7B006-825C-E511-8BA3-02163E0144F5.root',
				      '/store/data/Run2015D/SingleMuon/RAW/v1/000/256/630/00000/A02653E9-815C-E511-B609-02163E012A0E.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('l1Ntuple_76X nevts:20'),
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
                                           'keep *_emtf*_*_*',
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
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

#CSC Trigger Primitives reader
# =============================
process.load("CSCTriggerPrimitivesReader_cfi")
process.lctreader.debug = cms.untracked.bool(True)
#process.lctreader.CSCLCTProducerData = cms.untracked.string("emtfStage2Digis")

process.TFileService = cms.Service("TFileService",
	    fileName = cms.string('TPEHists_Run2015D.root')
	)


# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.output_step = cms.EndPath(process.FEVTDEBUGoutput)
process.lctreader_step = cms.Path(process.lctreader)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.endjob_step)

# customisation of the process.

# Automatic addition of the customisation function from L1Trigger.Configuration.customiseReEmul
from L1Trigger.Configuration.customiseReEmul import L1TReEmulFromRAW2015 

#call to customisation function L1TReEmulFromRAW2015 imported from L1Trigger.Configuration.customiseReEmul
process = L1TReEmulFromRAW2015(process)

# End of customisation functions

process.schedule.append(process.lctreader_step)

print "all modules",process.schedule

