# From F. Cossutti

import FWCore.ParameterSet.Config as cms

process = cms.Process("EDMtoMEConvert")
process.load("DQMServices.Examples.test.MessageLogger_cfi")

process.load("DQMServices.Components.EDMtoMEConverter_cff")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:mixCollValStep2.root')
)

process.p1 = cms.Path(process.EDMtoMEConverter*process.dqmSaver)
process.DQMStore.referenceFileName = 'mixCollValStandardMM.root'
process.dqmSaver.convention = 'Offline'
process.dqmSaver.workflow = '/ConverterTester/Test/RECO'
