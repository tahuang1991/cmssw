import FWCore.ParameterSet.Config as cms

# Hack to add "test" directory to the python path.
import sys, os
sys.path.insert(0, os.path.join(os.environ['CMSSW_BASE'],
                                'src/L1Trigger/CSCTriggerPrimitives/test'))

process = cms.Process("L1CSCTriggerPrimitivesReader")

process.source = cms.Source("PoolSource",
    # fileNames = cms.untracked.vstring("file:lcts.root"),
    # fileNames = cms.untracked.vstring("file:/data0/slava/test/lcts_muminus_pt50_emul_CMSSW_3_9_0_pre1.root"),
    #fileNames = cms.untracked.vstring("file:lcts_muminus_pt50_emul_CMSSW_6_1_0_pre2.root")
    fileNames = cms.untracked.vstring("file:outl1.root")
    #fileNames = cms.untracked.vstring("/store/data/Run2015D/SingleMuon/RAW/v1/000/256/734/00000/8200C0B8-0F5E-E511-80B2-02163E014415.root")

)
from  InputFileHelpers import *
#Inputdir = ['/eos/uscms/store/user/tahuang/SingleMuon/SingleMuon_2015D_v1_256734/161101_170853/0000/']
#Inputdir = ['/eos/uscms/store/user/tahuang/SingleMuon/SingleMuon_2016H_v1_281976/161012_220915/0000/']
#Inputdir = ['/eos/uscms/store/user/tahuang/SingleMuon_Run2MC_GEN_SIM_DIGI_L1_DIGI2RAW/SingleMuonPt100_MC_GEN_SIM_DIGI_L1_DIGI2RAW_updatetimeBitForBxZero/161103_024426/0000/']
#Inputdir = ['/eos/uscms/store/user/tahuang/SingleMuon_Run2MC_GEN_SIM_DIGI_L1_DIGI2RAW/L1REPACK_RAW2DIGI_0919/160920_153918/0000/']
Inputdir = ['/fdata/hepx/store/user/tahuang/SingleMu_80X_200k_Pt100_Endcaponly_run2MC_L1_adjustALCTCLCTBXboth8_OldOffsets/SingleMu_80X_200k_Pt100_Endcaponly_run2MC_L1_adjustALCTCLCTBXboth8_OldOffsets/171107_194204/0000/']
process = useInputDir(process, Inputdir)
#process.PoolSource.fileNames = ['/store/relval/CMSSW_3_1_0_pre7/RelValSingleMuPt100/GEN-SIM-DIGI-RAW-HLTDEBUG/IDEAL_31X_v1/0004/EE15A7EC-E641-DE11-A279-001D09F29321.root']

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100000)
)
# For LogTrace to take an effect, compile using
# > scram b -j8 USER_CXXFLAGS="-DEDM_ML_DEBUG"
#process.MessageLogger = cms.Service("MessageLogger",
#    destinations = cms.untracked.vstring("debug"),
#    #	untracked vstring categories     = { "lctDigis" }
#    #	untracked vstring debugModules   = { "*" }
#    #	untracked PSet debugmessages.txt = {
#    #	    untracked string threshold = "DEBUG"
#    #	    untracked PSet INFO     = {untracked int32 limit = 0}
#    #	    untracked PSet DEBUG    = {untracked int32 limit = 0}
#    #	    untracked PSet lctDigis = {untracked int32 limit = 10000000}
#    #	}
#    debug = cms.untracked.PSet(
#        threshold = cms.untracked.string("DEBUG"),
#        extension = cms.untracked.string(".txt"),
#        lineLength = cms.untracked.int32(132),
#        noLineBreaks = cms.untracked.bool(True)
#    ),
#    #debugModules = cms.untracked.vstring("lctreader")
#    debugModules = cms.untracked.vstring("*")
#)
#
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '80X_dataRun2_Prompt_v11', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_v14', '')


# Enable floating point exceptions
#process.EnableFloatingPointExceptions = cms.Service("EnableFloatingPointExceptions")
#process.Tracer = cms.Service("Tracer")

process.TFileService = cms.Service("TFileService",
    #fileName = cms.string('TPEHists_run2015D_v1_256734.root')
    fileName = cms.string('TPEHists_80x_adjustALCTCLCTBXboth8_OldOffsets_reemulation_MC_20180129.root')
)

# CSC Trigger Primitives emulator
# ===============================
process.load("L1Trigger.CSCTriggerPrimitives.cscTriggerPrimitiveDigis_cfi")
#print process.cscTriggerPrimitiveDigis.commonParam
#process.cscTriggerPrimitiveDigis.alctParam07.verbosity = 3
#process.cscTriggerPrimitiveDigis.clctParam07.verbosity = 3
#process.cscTriggerPrimitiveDigis.tmbParam.verbosity = 3
process.cscTriggerPrimitiveDigis.CSCComparatorDigiProducer = "muonCSCDigis:MuonCSCComparatorDigi"
process.cscTriggerPrimitiveDigis.CSCWireDigiProducer = "muonCSCDigis:MuonCSCWireDigi"


process.load("CSCTriggerPrimitivesReader_cfi")
process.lctreader.debug = False
#process.lctreader.dataLctsIn = False
#- For official RelVal samples
process.lctreader.CSCLCTProducerEmul = "cscTriggerPrimitiveDigis"
#process.lctreader.CSCLCTProducerEmul = "simCscTriggerPrimitiveDigis"
#process.lctreader.CSCComparatorDigiProducer = cms.InputTag("muonCSCDigis","MuonCSCComparatorDigi")
#process.lctreader.CSCWireDigiProducer = cms.InputTag("simMuonCSCDigis","MuonCSCWireDigi")
#process.lctreader.CSCLCTProducerData = cms.untracked.string("simMuonCSCDigis")
#
# Output
# ======
process.output = cms.OutputModule("PoolOutputModule",
    #fileName = cms.untracked.string("/data0/slava/test/lcts_run122909.root"),
    fileName = cms.untracked.string("lcts_MC_test.root"),
    outputCommands = cms.untracked.vstring("keep *", 
        "drop *_DaqSource_*_*")
)


process.p = cms.Path(process.cscTriggerPrimitiveDigis * process.lctreader)
#process.endp = cms.EndPath(process.output)
#process.p = cms.Path(process.lctreader)
