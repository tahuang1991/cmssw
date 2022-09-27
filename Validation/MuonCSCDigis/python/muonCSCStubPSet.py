import FWCore.ParameterSet.Config as cms

muonCSCStubPSet = cms.PSet(
    #csc CLCT pre-trigger
    cscCLCTPreTrigger = cms.PSet(
        verbose = cms.int32(0),
        inputTag = cms.InputTag("simCscTriggerPrimitiveDigis"),
        minBX = cms.int32(4),
        maxBX = cms.int32(10),
        minNHitsChamber = cms.int32(3),
    ),
    #csc CLCT, central BX 7, bx match window was 3, now is 7
    cscCLCT = cms.PSet(
        verbose = cms.int32(0),
        inputTag = cms.InputTag("simCscTriggerPrimitiveDigis"),
        minBX = cms.int32(4), 
        maxBX = cms.int32(10),
        minNHitsChamber = cms.int32(4),
    ),
    #csc ALCT, central BX 3 in CMSSW, bx match window was 3, now is 7
    cscALCT = cms.PSet(
        verbose = cms.int32(0),
        inputTag = cms.InputTag("simCscTriggerPrimitiveDigis"),
        minBX = cms.int32(0),
        maxBX = cms.int32(6),
        minNHitsChamber = cms.int32(4),
    ),
    #csc LCT, central BX 8, bx match window was 3, now is 7
    cscLCT = cms.PSet(
        verbose = cms.int32(0),
        inputTag = cms.InputTag("simCscTriggerPrimitiveDigis"),
        minBX = cms.int32(5),
        maxBX = cms.int32(11),
        minNHitsChamber = cms.int32(4),
        matchTypeTight = cms.bool(True),
        addGhosts = cms.bool(False)
    ),
    #csc LCT, central BX 8, bx match window was 3, now is 7
    cscMPLCT = cms.PSet(
        verbose = cms.int32(0),
        inputTag = cms.InputTag("simCscTriggerPrimitiveDigis","MPCSORTED"),
        minBX = cms.int32(5),
        maxBX = cms.int32(11),
        minNHitsChamber = cms.int32(4),
    ),
)
