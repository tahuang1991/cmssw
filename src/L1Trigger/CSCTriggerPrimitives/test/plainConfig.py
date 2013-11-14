import FWCore.ParameterSet.Config as cms

process = cms.Process("CSCTPEmulator")

process.source = cms.Source("DaqSource",
    readerPluginName = cms.untracked.string('CSCFileReader'),
    readerPset = cms.untracked.PSet(
        RUI01 = cms.untracked.vstring('/local/data/csc_00000001_EmuRUI01_ME11Test_ShortCosmicsRun6144s_000_130501_121902_UTC.raw', 
            '/local/data/csc_00000001_EmuRUI01_ME11Test_ShortCosmicsRun6144s_001_130501_121902_UTC.raw'),
        firstEvent = cms.untracked.int32(0),
        FED750 = cms.untracked.vstring('RUI01')
    )
)
process.cscTriggerPrimitiveDigis = cms.EDProducer("CSCTriggerPrimitivesProducer",
    MaxBX = cms.int32(9),
    MinBX = cms.int32(3),
    tmbSLHC = cms.PSet(
        mpcBlockMe1a = cms.uint32(0),
        tmbCrossBxAlgorithm = cms.untracked.uint32(1),
        alctTrigEnable = cms.uint32(0),
        tmbDropUsedClcts = cms.untracked.bool(False),
        verbosity = cms.untracked.int32(0),
        matchEarliestClctME11Only = cms.untracked.bool(False),
        tmbL1aWindowSize = cms.uint32(7),
        tmbEarlyTbins = cms.untracked.int32(4),
        clctTrigEnable = cms.uint32(0),
        tmbDropUsedAlcts = cms.untracked.bool(False),
        clctToAlct = cms.untracked.bool(False),
        matchTrigWindowSize = cms.uint32(3),
        tmbReadoutEarliest2 = cms.untracked.bool(False),
        matchEarliestAlctME11Only = cms.untracked.bool(False),
        maxME11LCTs = cms.untracked.uint32(2),
        matchTrigEnable = cms.uint32(1)
    ),
    CSCComparatorDigiProducer = cms.InputTag("muonCSCDigis","MuonCSCComparatorDigi"),
    clctParamMTCC = cms.PSet(
        clctDriftDelay = cms.uint32(2),
        clctMinSeparation = cms.uint32(10),
        clctPidThreshPretrig = cms.uint32(2),
        clctFifoTbins = cms.uint32(12),
        verbosity = cms.untracked.int32(0),
        clctNplanesHitPretrig = cms.uint32(4),
        clctHitPersist = cms.uint32(6),
        clctFifoPretrig = cms.uint32(7),
        clctNplanesHitPattern = cms.uint32(1)
    ),
    debugParameters = cms.untracked.bool(True),
    mpcSLHC = cms.PSet(
        mpcMaxStubs = cms.untracked.uint32(3)
    ),
    alctSLHC = cms.PSet(
        alctAccelMode = cms.uint32(0),
        alctGhostCancellationSideQuality = cms.untracked.bool(True),
        alctTrigMode = cms.uint32(2),
        verbosity = cms.untracked.int32(0),
        alctDriftDelay = cms.uint32(2),
        alctNplanesHitAccelPretrig = cms.uint32(3),
        alctNarrowMaskForR1 = cms.untracked.bool(True),
        alctL1aWindowWidth = cms.uint32(7),
        alctNplanesHitPattern = cms.uint32(4),
        alctNplanesHitAccelPattern = cms.uint32(4),
        alctHitPersist = cms.untracked.uint32(6),
        alctGhostCancellationBxDepth = cms.untracked.int32(1),
        alctFifoTbins = cms.uint32(16),
        alctNplanesHitPretrig = cms.uint32(3),
        alctEarlyTbins = cms.untracked.int32(4),
        alctUseCorrectedBx = cms.untracked.bool(True),
        alctPretrigDeadtime = cms.untracked.uint32(0),
        alctFifoPretrig = cms.uint32(10)
    ),
    alctParamMTCC = cms.PSet(
        alctAccelMode = cms.uint32(0),
        alctTrigMode = cms.uint32(2),
        verbosity = cms.untracked.int32(0),
        alctL1aWindowWidth = cms.uint32(3),
        alctNplanesHitAccelPretrig = cms.uint32(2),
        alctDriftDelay = cms.uint32(3),
        alctNplanesHitPattern = cms.uint32(4),
        alctNplanesHitAccelPattern = cms.uint32(4),
        alctFifoTbins = cms.uint32(16),
        alctNplanesHitPretrig = cms.uint32(2),
        alctFifoPretrig = cms.uint32(10)
    ),
    clctParamOldMC = cms.PSet(
        clctDriftDelay = cms.uint32(2),
        clctMinSeparation = cms.uint32(10),
        clctPidThreshPretrig = cms.uint32(2),
        clctFifoTbins = cms.uint32(12),
        verbosity = cms.untracked.int32(0),
        clctNplanesHitPretrig = cms.uint32(2),
        clctHitPersist = cms.uint32(6),
        clctFifoPretrig = cms.uint32(7),
        clctNplanesHitPattern = cms.uint32(4)
    ),
    alctParamOldMC = cms.PSet(
        alctAccelMode = cms.uint32(1),
        alctTrigMode = cms.uint32(3),
        verbosity = cms.untracked.int32(0),
        alctL1aWindowWidth = cms.uint32(5),
        alctNplanesHitAccelPretrig = cms.uint32(2),
        alctDriftDelay = cms.uint32(3),
        alctNplanesHitPattern = cms.uint32(4),
        alctNplanesHitAccelPattern = cms.uint32(4),
        alctFifoTbins = cms.uint32(16),
        alctNplanesHitPretrig = cms.uint32(2),
        alctFifoPretrig = cms.uint32(10)
    ),
    tmbParam = cms.PSet(
        alctTrigEnable = cms.uint32(0),
        verbosity = cms.untracked.int32(2),
        tmbDropUsedAlcts = cms.untracked.bool(True),
        tmbEarlyTbins = cms.untracked.int32(4),
        mpcBlockMe1a = cms.uint32(0),
        tmbL1aWindowSize = cms.uint32(7),
        matchTrigWindowSize = cms.uint32(7),
        tmbReadoutEarliest2 = cms.untracked.bool(True),
        clctTrigEnable = cms.uint32(0),
        matchTrigEnable = cms.uint32(1)
    ),
    commonParam = cms.PSet(
        gangedME1a = cms.untracked.bool(False),
        isTMB07 = cms.bool(True),
        isMTCC = cms.bool(False),
        isSLHC = cms.untracked.bool(False),
        smartME1aME1b = cms.untracked.bool(False),
        disableME1a = cms.untracked.bool(False),
        disableME42 = cms.untracked.bool(False)
    ),
    CSCWireDigiProducer = cms.InputTag("muonCSCDigis","MuonCSCWireDigi"),
    checkBadChambers = cms.untracked.bool(True),
    alctParam07 = cms.PSet(
        alctAccelMode = cms.uint32(0),
        alctTrigMode = cms.uint32(2),
        verbosity = cms.untracked.int32(2),
        alctDriftDelay = cms.uint32(2),
        alctNplanesHitAccelPretrig = cms.uint32(3),
        alctNarrowMaskForR1 = cms.untracked.bool(False),
        alctL1aWindowWidth = cms.uint32(7),
        alctNplanesHitPattern = cms.uint32(4),
        alctNplanesHitAccelPattern = cms.uint32(4),
        alctHitPersist = cms.untracked.uint32(6),
        alctFifoTbins = cms.uint32(16),
        alctNplanesHitPretrig = cms.uint32(3),
        alctEarlyTbins = cms.untracked.int32(4),
        alctFifoPretrig = cms.uint32(10)
    ),
    clctSLHC = cms.PSet(
        clctPretriggerTriggerZone = cms.untracked.uint32(5),
        clctMinSeparation = cms.uint32(5),
        clctPidThreshPretrig = cms.uint32(4),
        clctDriftDelay = cms.uint32(2),
        clctFifoTbins = cms.uint32(12),
        verbosity = cms.untracked.int32(0),
        useDynamicStateMachineZone = cms.untracked.bool(True),
        clctNplanesHitPretrig = cms.uint32(3),
        clctHitPersist = cms.uint32(4),
        clctStartBxShift = cms.untracked.int32(0),
        clctStateMachineZone = cms.untracked.uint32(8),
        useDeadTimeZoning = cms.untracked.bool(True),
        clctFifoPretrig = cms.uint32(7),
        clctNplanesHitPattern = cms.uint32(4),
        clctUseCorrectedBx = cms.untracked.bool(True)
    ),
    clctParam07 = cms.PSet(
        clctDriftDelay = cms.uint32(2),
        clctMinSeparation = cms.uint32(10),
        clctPidThreshPretrig = cms.uint32(2),
        clctFifoTbins = cms.uint32(12),
        verbosity = cms.untracked.int32(2),
        clctNplanesHitPretrig = cms.uint32(3),
        clctHitPersist = cms.uint32(4),
        clctStartBxShift = cms.untracked.int32(0),
        clctFifoPretrig = cms.uint32(7),
        clctNplanesHitPattern = cms.uint32(4)
    )
)


process.muonCSCDigis = cms.EDProducer("CSCDCCUnpacker",
    PrintEventNumber = cms.untracked.bool(False),
    UseExaminer = cms.bool(True),
    Debug = cms.untracked.bool(False),
    ErrorMask = cms.uint32(0),
    InputObjects = cms.InputTag("rawDataCollector"),
    UseFormatStatus = cms.bool(True),
    ExaminerMask = cms.uint32(535557110),
    UnpackStatusDigis = cms.bool(False),
    VisualFEDInspect = cms.untracked.bool(False),
    FormatedEventDump = cms.untracked.bool(False),
    UseSelectiveUnpacking = cms.bool(True),
    VisualFEDShort = cms.untracked.bool(False)
)


process.lctreader = cms.EDAnalyzer("CSCTriggerPrimitivesReader",
    printps = cms.bool(True),
    dataIsAnotherMC = cms.untracked.bool(False),
    dataLctsIn = cms.bool(True),
    CSCComparatorDigiProducer = cms.InputTag("muonCSCDigis","MuonCSCComparatorDigi"),
    CSCLCTProducerEmul = cms.untracked.string('cscTriggerPrimitiveDigis'),
    CSCLCTProducerData = cms.untracked.string('muonCSCDigis'),
    isMTCCData = cms.bool(False),
    debug = cms.untracked.bool(True),
    CSCWireDigiProducer = cms.InputTag("muonCSCDigis","MuonCSCWireDigi"),
    checkBadChambers = cms.untracked.bool(True),
    CSCSimHitProducer = cms.InputTag("g4SimHits","MuonCSCHits"),
    emulLctsIn = cms.bool(True)
)


process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('lct.root'),
    outputCommands = cms.untracked.vstring('keep *', 
        'drop *_DaqSource_*_*')
)


process.p = cms.Path(process.muonCSCDigis+process.cscTriggerPrimitiveDigis+process.lctreader)


process.MessageLogger = cms.Service("MessageLogger",
    suppressInfo = cms.untracked.vstring(),
    debugs = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    suppressDebug = cms.untracked.vstring(),
    cout = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    cerr_stats = cms.untracked.PSet(
        threshold = cms.untracked.string('WARNING'),
        output = cms.untracked.string('cerr'),
        optionalPSet = cms.untracked.bool(True)
    ),
    warnings = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    default = cms.untracked.PSet(

    ),
    statistics = cms.untracked.vstring('cerr_stats'),
    cerr = cms.untracked.PSet(
        INFO = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        noTimeStamps = cms.untracked.bool(False),
        FwkReport = cms.untracked.PSet(
            reportEvery = cms.untracked.int32(1),
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(10000000)
        ),
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000)
        ),
        Root_NoDictionary = cms.untracked.PSet(
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(0)
        ),
        threshold = cms.untracked.string('DEBUG'),
        FwkJob = cms.untracked.PSet(
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(0)
        ),
        FwkSummary = cms.untracked.PSet(
            reportEvery = cms.untracked.int32(1),
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(10000000)
        ),
        optionalPSet = cms.untracked.bool(True)
    ),
    FrameworkJobReport = cms.untracked.PSet(
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        optionalPSet = cms.untracked.bool(True),
        FwkJob = cms.untracked.PSet(
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(10000000)
        )
    ),
    suppressWarning = cms.untracked.vstring(),
    errors = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    destinations = cms.untracked.vstring('warnings', 
        'errors', 
        'infos', 
        'debugs', 
        'cout', 
        'cerr'),
    debugModules = cms.untracked.vstring('cscTriggerPrimitiveDigis', 
        'lctreader'),
    infos = cms.untracked.PSet(
        optionalPSet = cms.untracked.bool(True),
        Root_NoDictionary = cms.untracked.PSet(
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(0)
        ),
        placeholder = cms.untracked.bool(True)
    ),
    categories = cms.untracked.vstring('FwkJob', 
        'FwkReport', 
        'FwkSummary', 
        'Root_NoDictionary'),
    fwkJobReports = cms.untracked.vstring('FrameworkJobReport')
)


process.TFileService = cms.Service("TFileService",
    fileName = cms.string('TPEHists.root')
)


process.CSCGeometryESModule = cms.ESProducer("CSCGeometryESModule",
    appendToDataLabel = cms.string(''),
    useDDD = cms.bool(False),
    debugV = cms.untracked.bool(False),
    useGangedStripsInME1a = cms.bool(True),
    alignmentsLabel = cms.string(''),
    useOnlyWiresInME1a = cms.bool(False),
    useRealWireGeometry = cms.bool(True),
    useCentreTIOffsets = cms.bool(False),
    applyAlignment = cms.bool(True)
)


process.CaloGeometryBuilder = cms.ESProducer("CaloGeometryBuilder",
    SelectedCalos = cms.vstring('HCAL', 
        'ZDC', 
        'CASTOR', 
        'EcalBarrel', 
        'EcalEndcap', 
        'EcalPreshower', 
        'TOWER')
)


process.CaloTopologyBuilder = cms.ESProducer("CaloTopologyBuilder")


process.CaloTowerGeometryFromDBEP = cms.ESProducer("CaloTowerGeometryFromDBEP",
    applyAlignment = cms.bool(False),
    hcalTopologyConstants = cms.PSet(
        maxDepthHE = cms.int32(3),
        maxDepthHB = cms.int32(2),
        mode = cms.string('HcalTopologyMode::LHC')
    )
)


process.CastorDbProducer = cms.ESProducer("CastorDbProducer")


process.CastorGeometryFromDBEP = cms.ESProducer("CastorGeometryFromDBEP",
    applyAlignment = cms.bool(False)
)


process.DTGeometryESModule = cms.ESProducer("DTGeometryESModule",
    appendToDataLabel = cms.string(''),
    fromDDD = cms.bool(False),
    applyAlignment = cms.bool(True),
    alignmentsLabel = cms.string('')
)


process.EcalBarrelGeometryFromDBEP = cms.ESProducer("EcalBarrelGeometryFromDBEP",
    applyAlignment = cms.bool(True)
)


process.EcalElectronicsMappingBuilder = cms.ESProducer("EcalElectronicsMappingBuilder")


process.EcalEndcapGeometryFromDBEP = cms.ESProducer("EcalEndcapGeometryFromDBEP",
    applyAlignment = cms.bool(True)
)


process.EcalLaserCorrectionService = cms.ESProducer("EcalLaserCorrectionService")


process.EcalPreshowerGeometryFromDBEP = cms.ESProducer("EcalPreshowerGeometryFromDBEP",
    applyAlignment = cms.bool(True)
)


process.EcalTrigTowerConstituentsMapBuilder = cms.ESProducer("EcalTrigTowerConstituentsMapBuilder",
    MapFile = cms.untracked.string('Geometry/EcalMapping/data/EndCap_TTMap.txt')
)


process.GlobalTrackingGeometryESProducer = cms.ESProducer("GlobalTrackingGeometryESProducer")


process.HcalAlignmentEP = cms.ESProducer("HcalAlignmentEP")


process.HcalGeometryFromDBEP = cms.ESProducer("HcalGeometryFromDBEP",
    applyAlignment = cms.bool(True),
    hcalTopologyConstants = cms.PSet(
        maxDepthHE = cms.int32(3),
        maxDepthHB = cms.int32(2),
        mode = cms.string('HcalTopologyMode::LHC')
    )
)


process.MuonDetLayerGeometryESProducer = cms.ESProducer("MuonDetLayerGeometryESProducer")


process.RPCGeometryESModule = cms.ESProducer("RPCGeometryESModule",
    useDDD = cms.untracked.bool(False),
    compatibiltyWith11 = cms.untracked.bool(True)
)


process.SiStripRecHitMatcherESProducer = cms.ESProducer("SiStripRecHitMatcherESProducer",
    ComponentName = cms.string('StandardMatcher'),
    NSigmaInside = cms.double(3.0)
)


process.StripCPEfromTrackAngleESProducer = cms.ESProducer("StripCPEESProducer",
    ComponentType = cms.string('StripCPEfromTrackAngle'),
    ComponentName = cms.string('StripCPEfromTrackAngle')
)


process.TrackerRecoGeometryESProducer = cms.ESProducer("TrackerRecoGeometryESProducer")


process.ZdcGeometryFromDBEP = cms.ESProducer("ZdcGeometryFromDBEP",
    applyAlignment = cms.bool(False)
)


process.fakeForIdealAlignment = cms.ESProducer("FakeAlignmentProducer",
    appendToDataLabel = cms.string('fakeForIdeal')
)


process.hcalTopologyIdeal = cms.ESProducer("HcalTopologyIdealEP",
    Exclude = cms.untracked.string(''),
    appendToDataLabel = cms.string(''),
    hcalTopologyConstants = cms.PSet(
        maxDepthHE = cms.int32(3),
        maxDepthHB = cms.int32(2),
        mode = cms.string('HcalTopologyMode::LHC')
    )
)


process.hcal_db_producer = cms.ESProducer("HcalDbProducer",
    file = cms.untracked.string(''),
    dump = cms.untracked.vstring('')
)


process.idealForDigiCSCGeometry = cms.ESProducer("CSCGeometryESModule",
    appendToDataLabel = cms.string('idealForDigi'),
    useDDD = cms.bool(False),
    debugV = cms.untracked.bool(False),
    useGangedStripsInME1a = cms.bool(True),
    alignmentsLabel = cms.string('fakeForIdeal'),
    useOnlyWiresInME1a = cms.bool(False),
    useRealWireGeometry = cms.bool(True),
    useCentreTIOffsets = cms.bool(False),
    applyAlignment = cms.bool(False)
)


process.idealForDigiDTGeometry = cms.ESProducer("DTGeometryESModule",
    appendToDataLabel = cms.string('idealForDigi'),
    fromDDD = cms.bool(False),
    applyAlignment = cms.bool(False),
    alignmentsLabel = cms.string('fakeForIdeal')
)


process.idealForDigiTrackerGeometry = cms.ESProducer("TrackerDigiGeometryESModule",
    appendToDataLabel = cms.string('idealForDigi'),
    fromDDD = cms.bool(False),
    trackerGeometryConstants = cms.PSet(
        ROCS_X = cms.int32(0),
        ROCS_Y = cms.int32(0),
        upgradeGeometry = cms.bool(False),
        BIG_PIX_PER_ROC_Y = cms.int32(2),
        BIG_PIX_PER_ROC_X = cms.int32(1),
        ROWS_PER_ROC = cms.int32(80),
        COLS_PER_ROC = cms.int32(52)
    ),
    applyAlignment = cms.bool(False),
    alignmentsLabel = cms.string('fakeForIdeal')
)


process.siPixelQualityESProducer = cms.ESProducer("SiPixelQualityESProducer",
    ListOfRecordToMerge = cms.VPSet(cms.PSet(
        record = cms.string('SiPixelQualityFromDbRcd'),
        tag = cms.string('')
    ), 
        cms.PSet(
            record = cms.string('SiPixelDetVOffRcd'),
            tag = cms.string('')
        ))
)


process.siStripGainESProducer = cms.ESProducer("SiStripGainESProducer",
    printDebug = cms.untracked.bool(False),
    appendToDataLabel = cms.string(''),
    APVGain = cms.VPSet(cms.PSet(
        Record = cms.string('SiStripApvGainRcd'),
        NormalizationFactor = cms.untracked.double(1.0),
        Label = cms.untracked.string('')
    ), 
        cms.PSet(
            Record = cms.string('SiStripApvGain2Rcd'),
            NormalizationFactor = cms.untracked.double(1.0),
            Label = cms.untracked.string('')
        )),
    AutomaticNormalization = cms.bool(False)
)


process.siStripLorentzAngleDepESProducer = cms.ESProducer("SiStripLorentzAngleDepESProducer",
    LatencyRecord = cms.PSet(
        record = cms.string('SiStripLatencyRcd'),
        label = cms.untracked.string('')
    ),
    LorentzAngleDeconvMode = cms.PSet(
        record = cms.string('SiStripLorentzAngleRcd'),
        label = cms.untracked.string('deconvolution')
    ),
    LorentzAnglePeakMode = cms.PSet(
        record = cms.string('SiStripLorentzAngleRcd'),
        label = cms.untracked.string('peak')
    )
)


process.siStripQualityESProducer = cms.ESProducer("SiStripQualityESProducer",
    appendToDataLabel = cms.string(''),
    PrintDebugOutput = cms.bool(False),
    ThresholdForReducedGranularity = cms.double(0.3),
    UseEmptyRunInfo = cms.bool(False),
    ReduceGranularity = cms.bool(False),
    ListOfRecordToMerge = cms.VPSet(cms.PSet(
        record = cms.string('SiStripDetVOffRcd'),
        tag = cms.string('')
    ), 
        cms.PSet(
            record = cms.string('SiStripDetCablingRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('RunInfoRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadChannelRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadFiberRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadModuleRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadStripRcd'),
            tag = cms.string('')
        ))
)


process.sistripconn = cms.ESProducer("SiStripConnectivity")


process.trackerGeometryDB = cms.ESProducer("TrackerDigiGeometryESModule",
    appendToDataLabel = cms.string(''),
    fromDDD = cms.bool(False),
    trackerGeometryConstants = cms.PSet(
        ROCS_X = cms.int32(0),
        ROCS_Y = cms.int32(0),
        upgradeGeometry = cms.bool(False),
        BIG_PIX_PER_ROC_Y = cms.int32(2),
        BIG_PIX_PER_ROC_X = cms.int32(1),
        ROWS_PER_ROC = cms.int32(80),
        COLS_PER_ROC = cms.int32(52)
    ),
    applyAlignment = cms.bool(True),
    alignmentsLabel = cms.string('')
)


process.trackerNumberingGeometryDB = cms.ESProducer("TrackerGeometricDetESModule",
    appendToDataLabel = cms.string(''),
    fromDDD = cms.bool(False),
    layerNumberPXB = cms.uint32(16),
    totalBlade = cms.uint32(24)
)


process.trackerTopologyConstants = cms.ESProducer("TrackerTopologyEP",
    tob_rodStartBit = cms.uint32(5),
    tib_str_int_extStartBit = cms.uint32(10),
    tib_layerMask = cms.uint32(7),
    pxf_bladeMask = cms.uint32(63),
    appendToDataLabel = cms.string(''),
    pxb_ladderStartBit = cms.uint32(8),
    pxb_layerStartBit = cms.uint32(16),
    tec_wheelStartBit = cms.uint32(14),
    tib_str_int_extMask = cms.uint32(3),
    tec_ringStartBit = cms.uint32(5),
    tib_moduleStartBit = cms.uint32(2),
    tib_sterMask = cms.uint32(3),
    tid_sideStartBit = cms.uint32(13),
    tid_module_fw_bwStartBit = cms.uint32(7),
    tid_ringMask = cms.uint32(3),
    tob_sterMask = cms.uint32(3),
    tec_petal_fw_bwStartBit = cms.uint32(12),
    tec_ringMask = cms.uint32(7),
    tib_strMask = cms.uint32(63),
    tec_sterMask = cms.uint32(3),
    tec_wheelMask = cms.uint32(15),
    tec_sideStartBit = cms.uint32(18),
    pxb_moduleMask = cms.uint32(63),
    pxf_panelStartBit = cms.uint32(8),
    tid_sideMask = cms.uint32(3),
    tob_moduleMask = cms.uint32(7),
    tid_ringStartBit = cms.uint32(9),
    pxf_sideMask = cms.uint32(3),
    pxb_moduleStartBit = cms.uint32(2),
    pxf_diskStartBit = cms.uint32(16),
    tib_str_fw_bwMask = cms.uint32(3),
    tec_moduleMask = cms.uint32(7),
    tid_sterMask = cms.uint32(3),
    tob_rod_fw_bwMask = cms.uint32(3),
    tob_layerStartBit = cms.uint32(14),
    tec_petal_fw_bwMask = cms.uint32(3),
    tib_strStartBit = cms.uint32(4),
    tec_sterStartBit = cms.uint32(0),
    tid_moduleMask = cms.uint32(31),
    tib_sterStartBit = cms.uint32(0),
    tid_sterStartBit = cms.uint32(0),
    pxf_moduleStartBit = cms.uint32(2),
    pxf_diskMask = cms.uint32(15),
    tob_moduleStartBit = cms.uint32(2),
    tid_wheelStartBit = cms.uint32(11),
    tob_layerMask = cms.uint32(7),
    tid_module_fw_bwMask = cms.uint32(3),
    tob_rod_fw_bwStartBit = cms.uint32(12),
    tec_petalMask = cms.uint32(15),
    pxb_ladderMask = cms.uint32(255),
    tec_moduleStartBit = cms.uint32(2),
    tob_rodMask = cms.uint32(127),
    tec_sideMask = cms.uint32(3),
    pxf_sideStartBit = cms.uint32(23),
    pxb_layerMask = cms.uint32(15),
    tib_layerStartBit = cms.uint32(14),
    pxf_panelMask = cms.uint32(3),
    tib_moduleMask = cms.uint32(3),
    pxf_bladeStartBit = cms.uint32(10),
    tid_wheelMask = cms.uint32(3),
    tob_sterStartBit = cms.uint32(0),
    tid_moduleStartBit = cms.uint32(2),
    tec_petalStartBit = cms.uint32(8),
    tib_str_fw_bwStartBit = cms.uint32(12),
    pxf_moduleMask = cms.uint32(63)
)


process.GlobalTag = cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string(''),
        enableReadOnlySessionOnUpdateConnection = cms.untracked.bool(False),
        idleConnectionCleanupPeriod = cms.untracked.int32(10),
        messageLevel = cms.untracked.int32(0),
        enablePoolAutomaticCleanUp = cms.untracked.bool(False),
        enableConnectionSharing = cms.untracked.bool(True),
        connectionRetrialTimeOut = cms.untracked.int32(60),
        connectionTimeOut = cms.untracked.int32(60),
        authenticationSystem = cms.untracked.int32(0),
        connectionRetrialPeriod = cms.untracked.int32(10)
    ),
    BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
    toGet = cms.VPSet(),
    connect = cms.string('frontier://FrontierProd/CMS_COND_31X_GLOBALTAG'),
    globaltag = cms.string('DESIGN61_V11::All')
)


process.eegeom = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('EcalMappingRcd'),
    firstValid = cms.vuint32(1)
)


process.es_hardcode = cms.ESSource("HcalHardcodeCalibrations",
    toGet = cms.untracked.vstring('GainWidths'),
    hcalTopologyConstants = cms.PSet(
        maxDepthHE = cms.int32(3),
        maxDepthHB = cms.int32(2),
        mode = cms.string('HcalTopologyMode::LHC')
    )
)


process.CSCCommonTrigger = cms.PSet(
    MaxBX = cms.int32(9),
    MinBX = cms.int32(3)
)

process.CondDBSetup = cms.PSet(
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string(''),
        enableReadOnlySessionOnUpdateConnection = cms.untracked.bool(False),
        idleConnectionCleanupPeriod = cms.untracked.int32(10),
        messageLevel = cms.untracked.int32(0),
        enablePoolAutomaticCleanUp = cms.untracked.bool(False),
        enableConnectionSharing = cms.untracked.bool(True),
        connectionRetrialTimeOut = cms.untracked.int32(60),
        connectionTimeOut = cms.untracked.int32(60),
        authenticationSystem = cms.untracked.int32(0),
        connectionRetrialPeriod = cms.untracked.int32(10)
    )
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000000)
)


