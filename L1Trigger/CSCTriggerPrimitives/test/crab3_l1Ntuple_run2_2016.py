from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()
#section general
config.General.requestName = 'RAW2DIGI_Run2016H_284035_20161103'
config.General.workArea = 'RAW2DIGI_Run2016H'#working dir 
config.General.transferOutputs = True
config.General.transferLogs = True

#section JobType
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'l1Ntuple_run2_2016_RAW2DIGI.py'
config.JobType.maxMemoryMB = 2000
config.JobType.maxJobRuntimeMin = 1440 # 1440min = 24hours
config.JobType.numCores = 1
config.JobType.allowUndistributedCMSSW = True
#config.JobType.generator
#config.JobType.pyCfgParams
#config.JobType.inputFiles


#section Data
#config.Data.inputDataset = '/SLHC23_patch1_2023Muon_gen_sim_Pt2_50_1M/tahuang-SLHC25_patch1_2023Muon_1M_L1_PU0_Pt2_50_updategemeta-1bf93df4dfbb43dc918bd6e47dedbf79/USER'
#config.Data.inputDataset = '/SingleMuon/Run2016G-v1/RAW'
config.Data.inputDataset = '/SingleMuon/Run2016H-v1/RAW'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'LumiBased'
config.Data.inputDBS = 'global'
config.Data.unitsPerJob = 100
config.Data.outLFNDirBase = '/store/user/tahuang/'
config.Data.publication = False
#import FWCore.PythonUtilities.LumiList as LumiList
#process.source.lumisToProcess = LumiList.LumiList(filename = 'goodList.json').getVLuminosityBlockRange()
#config.Data.runRange = '278820-278820' # '193093-194075'
config.Data.runRange = '284035-284035'
config.Data.outputDatasetTag = 'SingleMuon_2016H_v1_284035_20161103'
config.Site.storageSite = 'T3_US_FNALLPC'
