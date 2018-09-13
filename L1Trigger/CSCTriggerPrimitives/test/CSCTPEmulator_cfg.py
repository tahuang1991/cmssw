# Configuration file to unpack CSC digis, run Trigger Primitives emulator,
# and compare LCTs in the data with LCTs found by the emulator.
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
process = cms.Process("CSCTPEmulator", eras.Run2_2018)

process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(10000)
)

# Add "test" directory to the python path.
import sys, os
sys.path.insert(0, os.path.join(os.environ['CMSSW_BASE'], 'src/L1Trigger/CSCTriggerPrimitives/test'))

print len(sys.argv)
if len(sys.argv) == 5: # 0 is cmsRun, 1 is CSCTPEmulator_cfg.py, 2 is file_list, 3 is producer output, 4 is output;
    file_with_list = sys.argv[2]
else:
    sys.exit('need a file list as only argument')
file_obj = open(file_with_list)
input_list = [l for l in file_obj.readlines()]
print input_list

process.source = cms.Source("PoolSource",
     fileNames = cms.untracked.vstring(
      input_list
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/000D683C-78AF-E811-903A-FA163E102682.root', 
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/00161186-6DAF-E811-A264-FA163E1D4484.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/003D5548-4FAF-E811-8519-FA163EB6E388.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/009F1819-5EAF-E811-9523-FA163EDD7BE8.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/00E13B41-80AF-E811-B455-FA163E756B33.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/00EBEF08-73AF-E811-9200-02163E019FD6.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/00EFCD84-74AF-E811-870F-FA163EC01FA2.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/021744B8-50AF-E811-834E-FA163EB6E388.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0219268F-59AF-E811-B869-02163E01A17A.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0230772E-52AF-E811-8383-FA163E3487CA.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/02BBD50E-5BAF-E811-A5B9-FA163E6498B7.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/02CA223B-78AF-E811-BDBC-FA163E992582.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/02CD360B-73AF-E811-BE7C-FA163EF1AD57.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/02D622CE-79AF-E811-8356-FA163E909D3A.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/02D62C2B-7CAF-E811-BB29-FA163EB132D4.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/02E41C0E-73AF-E811-8E99-FA163E688D1A.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/042D2565-78AF-E811-81FA-FA163E4E487A.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/04342167-78AF-E811-A6D9-A4BF0114CCA8.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0461F222-78AF-E811-831F-02163E019FA5.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/04767239-7CAF-E811-AC4E-FA163E9666C9.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/04937EF9-79AF-E811-9367-02163E00C216.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/04E9EE17-7CAF-E811-809E-FA163E986BD2.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0606CACA-60AF-E811-AE66-FA163EBEC730.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/063DB207-73AF-E811-A7CD-FA163ED7C19F.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/064E069A-71AF-E811-9CFD-FA163E910130.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0695A408-78AF-E811-9973-FA163E8F2C56.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/06B06627-5EAF-E811-84C3-FA163E96DBF1.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/06F7B988-7BAF-E811-9206-FA163E5EF973.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/08040509-65AF-E811-AC41-FA163E157982.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/08146997-71AF-E811-8509-FA163E6F82B9.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/08175E00-7AAF-E811-B77F-02163E00CA3E.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0826BE34-7CAF-E811-A37C-02163E017F0E.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/08309DC6-79AF-E811-B9A2-FA163EEABC98.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/083A89E2-76AF-E811-9A1B-FA163ECF8DB3.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/084E428D-59AF-E811-98A4-FA163EA094DE.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0891B297-5FAF-E811-BC1D-FA163EBF471A.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/089A2437-7CAF-E811-934B-FA163E016D86.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/08AF2B5D-80AF-E811-9741-02163E017755.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/08B634FA-5FAF-E811-A9DB-FA163E192946.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/08CA4C8E-59AF-E811-8B38-02163E01A11D.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/08D092B4-7DAF-E811-BF0A-FA163E5EF973.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0A2A0716-5BAF-E811-99C3-FA163E08DA61.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0A6C1656-6FAF-E811-9701-FA163E6FD671.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0A9A431D-75AF-E811-8A7D-FA163EB66698.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0ABEB290-55AF-E811-9553-FA163E4AE5F5.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0AE2868F-59AF-E811-B90B-FA163E0AB732.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0AF0D49A-56AF-E811-A34C-FA163E331CDA.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0AF13443-52AF-E811-A677-FA163E331CDA.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0AFBCC39-78AF-E811-9A92-FA163E99485E.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0C03E0E9-5FAF-E811-927D-02163E01507D.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0C082646-4FAF-E811-98FC-FA163E1290D7.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0C575C93-6DAF-E811-8CA0-FA163EAFB571.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0C61B138-78AF-E811-B923-FA163EB4462D.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0C797C51-7CAF-E811-80ED-FA163ECAC68D.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0CC67F29-5EAF-E811-B5F6-02163E01A03B.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0CC7990D-73AF-E811-9B4C-FA163E43EA04.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0CE7942A-7CAF-E811-B949-FA163E28C879.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0E1083D6-4DAF-E811-93A1-FA163E5B9932.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0E139586-65AF-E811-BD8D-02163E00ACD8.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0E23772B-7EAF-E811-8FC2-02163E019FF2.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0E4261AC-71AF-E811-8225-FA163E6536A6.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0EC983D5-76AF-E811-AD93-FA163E96F2FF.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/0ED0BD43-4FAF-E811-81A1-FA163EED9E90.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1028B891-61AF-E811-A0E3-A4BF0127B2B3.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1043B7A0-56AF-E811-A3DD-FA163ED96F18.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/107EE1D8-7CAF-E811-8290-02163E017F02.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/10F6E308-73AF-E811-BC3A-FA163ED7C19F.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1242C944-4FAF-E811-B536-FA163E14986C.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/127EC2BD-5AAF-E811-BBDF-FA163E1E361C.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/12843513-55AF-E811-ADB6-FA163EA96792.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/12A7AFCE-79AF-E811-8525-FA163E941955.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/12B3B982-78AF-E811-A4C2-FA163E205A29.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/12BFDC49-78AF-E811-814F-FA163ECE7C6A.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/12C13195-7BAF-E811-8E94-FA163EBA301F.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/12D89AF7-7FAF-E811-8EC9-FA163E3D1715.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1411B73E-78AF-E811-846D-FA163EB88691.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/141D5EB0-67AF-E811-84C2-02163E012E12.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1466859D-78AF-E811-926C-FA163EDD9B9E.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/148B45B7-65AF-E811-A135-02163E00B997.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1609209E-56AF-E811-B2E1-A4BF012CBE43.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/16122B25-7AAF-E811-863C-FA163EB4EA3A.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1649D1A2-56AF-E811-BF72-FA163E1BFD9F.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1675F120-73AF-E811-9294-02163E01659A.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1676241A-55AF-E811-AEE0-FA163EE70C42.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/168CD3DF-79AF-E811-AC55-FA163E3DF9DF.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/16965296-71AF-E811-8A3D-FA163E93DE0C.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/16D202EC-7FAF-E811-B4CC-FA163EDA17B6.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/180BA3C1-79AF-E811-81B9-FA163E62E0F4.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/185FC7D0-56AF-E811-9DAF-FA163E72410C.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/187ABC46-80AF-E811-B034-FA163E15865B.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/18B1A6ED-76AF-E811-AFAD-FA163E58F6C6.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/18B845D4-76AF-E811-832E-FA163E3AA2A6.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/18BD10AC-74AF-E811-A5E3-FA163E8E60D2.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/18E5E6A2-61AF-E811-8485-FA163E0B9045.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1A24B617-55AF-E811-AA23-FA163EACD9E0.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1A4EBDC3-59AF-E811-A5A0-02163E012E27.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1A56BCEC-60AF-E811-A3FF-02163E00B36A.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1A86E5D0-64AF-E811-A171-FA163E8BA02A.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1A9D3812-73AF-E811-94B4-02163E014BBF.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1C2E4B19-80AF-E811-9C50-FA163E29485B.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1C608E10-73AF-E811-92B8-FA163E941955.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1C881819-5EAF-E811-A2E3-FA163EED890D.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1C906B15-66AF-E811-B7A9-02163E00B1EE.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1C92D942-78AF-E811-85E2-02163E015152.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1CAE382B-7EAF-E811-893D-FA163EA56DEB.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1CCF925D-80AF-E811-989C-FA163ED4DF6E.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1CDE7489-6DAF-E811-A1D8-FA163EAB144C.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1E095327-6FAF-E811-AC00-FA163EF96DF1.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1E19A62B-58AF-E811-9289-FA163E9BE5CE.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1E50E5B7-50AF-E811-9ED8-FA163E85453E.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1E6D4B90-59AF-E811-9C85-02163E01A062.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1E79188D-74AF-E811-A6BB-FA163EE00996.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1E82AC8D-59AF-E811-9C9E-FA163EF08FCB.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/1EE3BCDC-4DAF-E811-88B2-FA163EE70C42.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2007D4BF-50AF-E811-AA28-FA163EB6100A.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/201DF25A-72AF-E811-BE54-FA163EB27A3D.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2040E40C-7EAF-E811-9615-02163E010BE0.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2066829E-5FAF-E811-B085-FA163E946965.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2095B4A6-78AF-E811-81EE-FA163E72EEB6.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/20963911-7EAF-E811-B28B-FA163E78589E.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/209B7A7B-78AF-E811-A9AF-FA163EB9878F.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/20A35093-5FAF-E811-9E2B-FA163E559492.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/20C21D0C-73AF-E811-916E-FA163E31CB60.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/20CA6392-7BAF-E811-A423-FA163EEC88AE.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/20D5B642-7CAF-E811-B6A7-FA163E80686C.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/20DF4C8E-59AF-E811-88FD-FA163E7C3F50.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/222CFE86-74AF-E811-AE10-FA163ED228CE.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2237223B-78AF-E811-94AB-FA163E01EC67.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/22398940-78AF-E811-9E10-FA163E8F2C56.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/225547E3-78AF-E811-A3B2-02163E017FBB.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2273DAB9-50AF-E811-9B12-FA163E7D17FA.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/227B97CA-52AF-E811-9EEB-FA163EBB5B8D.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/22978DA0-56AF-E811-A316-FA163EB94ED3.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/22A525A0-60AF-E811-B750-FA163EB47669.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/22B35B4A-4FAF-E811-B635-FA163ECCE6F0.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/22E64AA3-56AF-E811-A601-FA163E2415B4.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/246E0BAE-56AF-E811-ACF1-FA163E0DF5F2.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2476A29B-56AF-E811-A174-02163E01A10A.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/247AEA8D-59AF-E811-A01F-FA163E1FDB57.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/24A2B996-6DAF-E811-9D7C-02163E015105.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/24AB0749-78AF-E811-8A6B-02163E01A14B.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/24B7B22F-80AF-E811-8DB6-FA163E5BBDF8.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/24D413EE-7FAF-E811-97D4-FA163E62E0F4.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/24D554DF-74AF-E811-87BC-FA163E85E011.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/24D94BD3-76AF-E811-91FE-FA163E80686C.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/24EAA33B-78AF-E811-A4EE-FA163E737251.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/24F2B855-78AF-E811-8D35-FA163E5D2DA7.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/260CBF53-80AF-E811-85CA-FA163E23FAFC.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2650D837-58AF-E811-9410-FA163E961462.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/285AA7A4-74AF-E811-B70C-02163E015C90.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/28744CBE-50AF-E811-AC35-FA163EE69449.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/288FAB98-56AF-E811-BCBD-FA163E2FAD1B.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/28D1B075-78AF-E811-B5AA-FA163E32F580.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/28E64B49-4FAF-E811-B790-FA163E6A841B.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2A16C317-55AF-E811-B00C-FA163E09F985.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2A298F09-7AAF-E811-9282-FA163E462EB9.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2A81CA06-80AF-E811-B68F-FA163E27657E.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2A8BDFDD-4DAF-E811-A4F5-FA163EA11AEF.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2A9529C9-6DAF-E811-BDE7-02163E012F0F.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2AB48942-52AF-E811-AF87-FA163E64D776.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2AD66E21-58AF-E811-AA6F-FA163EBDFAA3.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2C9CE33C-78AF-E811-A3FD-FA163EEC88AE.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2CA352EB-76AF-E811-A294-FA163EBAEAC5.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2CCD3A23-73AF-E811-8306-02163E010E08.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2CD15C93-5FAF-E811-B364-FA163E559492.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2E149CC2-79AF-E811-8553-FA163E252833.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2E927AA2-56AF-E811-9543-FA163E47312B.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2EBA308F-59AF-E811-A0F6-FA163E89DF43.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2EE48B14-5EAF-E811-9BC1-FA163EEB45BD.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2EE5334C-78AF-E811-ACA4-FA163EA91F95.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2EEC5E3D-78AF-E811-9BEF-FA163E48FCFB.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/2EF5AB96-78AF-E811-B9A6-FA163E0693A0.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/30286454-7DAF-E811-98B4-FA163E556552.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/320A1B1E-73AF-E811-B18C-FA163EA91F95.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/322A95F4-7FAF-E811-BDCB-FA163E0639A2.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/324A528E-59AF-E811-85B0-FA163E531E24.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/32DC6915-5BAF-E811-85C1-FA163E6D9DFD.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/32EED1A0-5FAF-E811-8E4B-FA163E5436A5.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/32F0AF47-7EAF-E811-9D83-FA163E336245.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/341F5E88-77AF-E811-A3BE-FA163E17CAA2.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/344191C8-64AF-E811-B9FD-FA163E033F78.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/34AD273F-78AF-E811-A4CA-FA163ED4597D.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/34F6EB95-5FAF-E811-BA33-02163E010F1A.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/36B085B0-7BAF-E811-BFC5-02163E017F02.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/36BF12E3-4DAF-E811-A546-FA163EC24AA6.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/36E31B80-74AF-E811-98B8-FA163EB19AA2.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/36E48F32-52AF-E811-879A-FA163E33F482.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/36EE8ABF-79AF-E811-AB9B-FA163E4F3B21.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/38366B8D-6DAF-E811-8C9D-FA163E4440F5.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/387E7B95-71AF-E811-8F10-FA163E918B1C.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/388578A3-78AF-E811-8627-FA163E3D2BEF.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/389E599F-78AF-E811-BE98-FA163EC9EB0E.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/38D9C3EB-6DAF-E811-9D0A-FA163E9D0FC3.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/3A0CCDD2-4DAF-E811-9D78-FA163ECF8DB3.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/3A0FFA9E-56AF-E811-AC42-FA163EB6F202.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/3A34C018-5BAF-E811-9174-FA163EDEBCD1.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/3A391890-59AF-E811-AD7B-FA163ECA5AC1.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/3A6028DB-59AF-E811-AE81-FA163E984001.root',
#      'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/322/118/00000/3AA3711C-78AF-E811-9C32-FA163EF87070.root'
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/4EBDBAC5-D8A6-E811-9D47-FA163E147082.root', 
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/94338DBE-D8A6-E811-97DC-FA163E6B427B.root', 
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/46368DBE-D8A6-E811-BD7C-FA163E6B427B.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/E0E964C1-D8A6-E811-AE4E-FA163EECEDCF.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/A4DC520C-DAA6-E811-844B-FA163E9142A0.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/D26118E0-D8A6-E811-B336-FA163E2EE3A8.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/481944BE-D8A6-E811-9C5B-FA163EC8DFDC.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/AC3523CD-D8A6-E811-887C-FA163EAB6554.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/56001B0F-DAA6-E811-9006-FA163E814B6A.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/5C8F1B6E-DBA6-E811-A8D9-FA163E8DC37A.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/FE7EB818-DAA6-E811-A806-FA163E7121A5.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/8C3A3272-DBA6-E811-BFDA-FA163E5FA5D4.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/2424B212-DAA6-E811-AD48-FA163E6EC3E9.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/CC68247B-DBA6-E811-B987-02163E0176C6.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/209F1C76-DBA6-E811-8ACF-FA163EFD8406.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/AE117A90-DBA6-E811-8F54-02163E01A154.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/FC1F7273-DBA6-E811-A66F-FA163E061B87.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/245FD378-DBA6-E811-8AF5-FA163EEFB5F4.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/A807426F-DBA6-E811-B945-FA163E9F932A.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/8099C388-DBA6-E811-B5D3-FA163E53EEFE.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/B2EC7876-DBA6-E811-AD67-FA163E108BAA.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/18A51D72-DBA6-E811-A60D-FA163EC92B39.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/165E3B70-DBA6-E811-974D-FA163E225AB4.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/C0380874-DBA6-E811-ADA1-FA163E1C00B3.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/2C028F76-DBA6-E811-AC6C-FA163ED07727.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/AC0F4376-DBA6-E811-BABD-02163E01A17C.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/923CAEC4-DCA6-E811-B9DD-FA163ED59DED.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/3015E379-DBA6-E811-ACA9-FA163E6C72EF.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/F078DC7A-DBA6-E811-8C26-FA163E51BE90.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/FE2C32C6-DCA6-E811-AB0B-FA163E1B9BC3.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/70C85DC4-DCA6-E811-8BBC-FA163EB83C02.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/E81ECCC3-DCA6-E811-916C-FA163E5755B1.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/54F2F074-DBA6-E811-9ECF-FA163E2EE3A8.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/1A95A5C4-DCA6-E811-A7F1-FA163EE2EC5A.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/08B5BAC4-DCA6-E811-903E-FA163E9B9A21.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/C266E674-DBA6-E811-974F-FA163EF478A0.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/7A674076-DBA6-E811-994A-02163E01A17C.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/C4633374-DBA6-E811-9C6A-FA163E94348E.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/D4774782-DBA6-E811-AFD6-FA163E170ECE.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/50034073-DBA6-E811-B5C9-FA163E33E510.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/F4373578-DBA6-E811-B0CE-FA163EDAA2B4.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/FE3CCAC8-DCA6-E811-91CF-FA163EBF76CA.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/B0FFD57F-DCA6-E811-8E42-FA163E7AD6B5.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/CCF11D8F-DBA6-E811-9693-02163E010CB1.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/B4AFE288-DBA6-E811-A267-FA163E4642C6.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/18F47FD3-DCA6-E811-93A5-02163E010DF8.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/321/710/00000/547E9ADA-DBA6-E811-B0A2-FA163E72BD86.root'

#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/D423BAA4-BF95-E811-A79C-FA163EDE5CFD.root', 
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/D468DACE-A395-E811-91D1-FA163E7E5BB3.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/D4E2AFC2-A195-E811-B337-FA163E395E49.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/D4F0F450-BB95-E811-8BC9-FA163E0AB4C0.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/D6000C0C-AA95-E811-8CEC-FA163EDF749C.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/D6730242-AB95-E811-896E-02163E00C478.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/D67596AD-B395-E811-A472-FA163E5BDB45.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/D68F63E6-AC95-E811-951F-FA163E5B30F8.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/D6E7BB7B-AD95-E811-BD03-FA163E354E33.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/D8E11E7E-A695-E811-9C7E-FA163E2E5B91.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/D8E799BF-B695-E811-B968-FA163E60A5FD.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/D8FD2983-B695-E811-A545-FA163E825C6B.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/DA1130CB-A795-E811-ADD8-02163E010F05.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/DA4B7D1D-B595-E811-A168-FA163E7CAD4F.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/DA6D6EC4-BE95-E811-9BD8-FA163E41C7B0.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/DA82EECD-A295-E811-A64F-FA163E138F08.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/DC24D32B-BC95-E811-9546-FA163E8A3060.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/DC46BE82-AD95-E811-91D6-FA163E4EF997.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/DC55CD7D-B295-E811-9448-FA163E102682.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/DCBD0C38-BF95-E811-936F-02163E019F19.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/DCE626AA-BE95-E811-87FF-FA163ED03425.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/DCF45D97-A095-E811-A4A4-FA163EBE4F8C.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/DE13AB90-B195-E811-926D-FA163E592A6F.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/DE250E90-A695-E811-A23C-FA163ED2DE85.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/DE6254BD-B495-E811-AD81-FA163EE6485C.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/DE693E17-B595-E811-B725-FA163E548540.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/DEB7947C-A695-E811-B36C-FA163E97A487.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E00CDF65-BC95-E811-BB73-FA163EFA355F.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E05464B2-BB95-E811-81DA-FA163E3EE95B.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E0606FC1-B895-E811-ADD5-FA163EF93AEC.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E066F300-B895-E811-A733-FA163E64634F.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E0B98B38-B895-E811-B1AA-FA163ED5F2E4.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E22384DF-AC95-E811-9A92-FA163EC64BA5.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E2291D46-BB95-E811-9B25-FA163EE6286A.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E267DD6D-A495-E811-A490-FA163ECB3C90.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E26F2CAD-BD95-E811-8E2F-FA163E2DB2A3.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E2806E90-B995-E811-9F65-FA163E2E65AB.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E2816322-B495-E811-A647-FA163E44FC66.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E2B723A5-BD95-E811-AB37-FA163E230A11.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E2C56865-AF95-E811-A5F4-FA163E20E52E.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E2DBD220-B595-E811-85C9-FA163E9D8D04.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E42A422A-AF95-E811-B959-FA163E78BFE5.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E447E1E8-BB95-E811-A672-A4BF0114CB20.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E47BEDFB-B395-E811-B0F7-02163E0164E1.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E4DC1F9E-AB95-E811-A342-FA163E862C57.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E6955780-B395-E811-8CEA-FA163E5874FD.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E6AA4821-B795-E811-AE35-FA163EFE9C39.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E80F7199-BE95-E811-99E5-FA163EABE0AA.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E833DBD1-B195-E811-B17D-FA163EC3CDA2.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/E86F5F8B-AB95-E811-ABEB-02163E00B8BA.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/EA5981A5-B095-E811-9E85-FA163E85FA06.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/EA88845F-B095-E811-8A38-FA163E862C57.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/EA8BFA31-BF95-E811-9B83-FA163E39A19D.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/EC59BF16-AA95-E811-834D-FA163EEF5766.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/EC7B84C3-A295-E811-AB2F-FA163E356356.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/EC9E91CA-A295-E811-8659-FA163E741841.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/ECC43DDF-AC95-E811-B4FD-FA163E09BE42.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/ECC62B56-AF95-E811-B358-FA163E777246.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/ECDFEC3B-B895-E811-A1C9-FA163EB7B53C.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/EE192A0D-A595-E811-AA50-FA163E471DF7.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/EE3FF1CC-A795-E811-8CB5-FA163E6A17B9.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/EE4D28A4-BD95-E811-A037-02163E010DC5.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/EE73138A-B295-E811-8C75-02163E016CFB.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/EE89FFC9-A795-E811-9F18-FA163E536B65.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/EEB9B5F3-B095-E811-B5B9-02163E017755.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/EEFE6043-BC95-E811-8ADE-FA163E99485E.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F0109BA8-BD95-E811-9998-FA163E80C212.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F07BD50C-AA95-E811-8158-FA163E0BCDBC.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F09331E1-AC95-E811-9C6D-FA163ED919B8.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F09CB028-BA95-E811-8D91-FA163E3CEA02.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F216A4C2-A195-E811-A5CE-FA163E592A6F.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F21F748A-A695-E811-A66A-02163E01A01E.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F2AF5A7B-AD95-E811-B1FF-FA163EE01A64.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F2F71F67-6D96-E811-AAB7-FA163EC82417.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F42253C7-AD95-E811-A036-FA163EC43B85.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F433BFD7-B695-E811-88C2-FA163EE72A6E.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F4B8C3B5-B895-E811-85C9-FA163ECFA4D9.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F619E976-AB95-E811-BE0A-FA163E3CEA02.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F658C678-B095-E811-A0BF-FA163ED03425.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F669CF79-B395-E811-B247-FA163EE8287C.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F808DDAC-B395-E811-9772-02163E019EEF.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F837FE02-B895-E811-911D-FA163EAC4CED.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F83C3809-AA95-E811-9F15-FA163ED2DE85.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F8C5C8B8-B395-E811-A02C-FA163E76E4F3.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/F8CC34EC-B795-E811-833A-FA163E1E24E8.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/FA2405CD-A795-E811-B975-FA163EB7A855.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/FA5BB6CC-AB95-E811-BC3B-FA163E302745.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/FA76D5B3-B795-E811-A902-02163E014DA0.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/FA7E5796-A095-E811-AD7E-FA163E56D1F9.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/FA9DFDC4-A295-E811-95D8-FA163EAC9FC3.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/FA9E07C5-A195-E811-8B22-02163E01A01A.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/FAD6CD98-B195-E811-8D58-FA163EE655A1.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/FAD7515E-A395-E811-AB07-FA163E1ED108.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/FAEAF2FD-9F95-E811-A761-FA163E336D90.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/FC014FE0-B695-E811-BD41-FA163E77F338.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/FC0E37E0-AD95-E811-9F2E-FA163E862C57.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/FC2A6453-BF95-E811-95CC-FA163EC417AB.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/FCBF028D-B195-E811-A178-FA163E55CE78.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/FCDBD7C3-A295-E811-94C0-FA163E354E33.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/FCE07AC1-A295-E811-8374-FA163E64F48C.root',
#         'file:/eos/cms//store/data/Run2018D/SingleMuon/RAW/v1/000/320/688/00000/FEF10072-B395-E811-A886-FA163E1A61E2.root'
     )
)

process.MessageLogger = cms.Service("MessageLogger",
    destinations = cms.untracked.vstring("debug"),
    debug = cms.untracked.PSet(
        extension = cms.untracked.string(".txt"),
        threshold = cms.untracked.string("DEBUG"),
        lineLength = cms.untracked.int32(132),
        noLineBreaks = cms.untracked.bool(True)
    ),
    # debugModules = cms.untracked.vstring("*")
    debugModules = cms.untracked.vstring("cscTriggerPrimitiveDigis",
        "lctreader")
)

# endcap muon only...
process.load("Geometry.MuonCommonData.muonEndcapIdealGeometryXML_cfi")
# Needed according to Mike Case's e-mail from 27/03.
process.load("Geometry.MuonNumbering.muonNumberingInitialization_cfi")
# flags for modelling of CSC geometry
process.load("Geometry.CSCGeometry.cscGeometry_cfi")

process.load("Configuration/StandardSequences/FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = '102X_dataRun2_Prompt_v1'

# magnetic field (do I need it?)
# ==============================
process.load('Configuration.StandardSequences.MagneticField_38T_cff')

# CSC raw --> digi unpacker
# =========================
process.load("EventFilter.CSCRawToDigi.cscUnpacker_cfi")
process.muonCSCDigis.InputObjects = "rawDataCollector"
# InputObjects = cms.InputTag("cscpacker","CSCRawData")
# for run 566 and 2008 data
# ErrorMask = cms.untracked.uint32(0xDFCFEFFF)

# CSC Trigger Primitives configuration
# ====================================
#process.load("L1TriggerConfig.L1CSCTPConfigProducers.L1CSCTriggerPrimitivesConfig_cff")
#process.load("L1TriggerConfig.L1CSCTPConfigProducers.L1CSCTriggerPrimitivesDBConfig_cff")
#process.prefer("l1csctpdbconfsrc")
#process.l1csctpconf.alctParamMTCC2.alctNplanesHitPretrig = 3
#process.l1csctpconf.alctParamMTCC2.alctNplanesHitAccelPretrig = 3
#process.l1csctpconf.clctParam.clctNplanesHitPretrig = 3
#process.l1csctpconf.clctParam.clctHitPersist = 4
#process.l1csctpconf.alctParamMTCC2.alctDriftDelay = 9
#process.l1csctpconf.alctParamMTCC2.alctL1aWindowWidth = 9

# CSC Trigger Primitives emulator
# ===============================
process.load("L1Trigger.CSCTriggerPrimitives.cscTriggerPrimitiveDigis_cfi")
process.cscTriggerPrimitiveDigis.alctParam07.verbosity = 2
process.cscTriggerPrimitiveDigis.clctParam07.verbosity = 2
process.cscTriggerPrimitiveDigis.tmbParam.verbosity = 2
process.cscTriggerPrimitiveDigis.CSCComparatorDigiProducer = "muonCSCDigis:MuonCSCComparatorDigi"
process.cscTriggerPrimitiveDigis.CSCWireDigiProducer = "muonCSCDigis:MuonCSCWireDigi"
process.cscTriggerPrimitiveDigis.commonParam.isSLHC = cms.bool(False)
process.cscTriggerPrimitiveDigis.commonParam.smartME1aME1b = cms.bool(True)

# CSC Trigger Primitives reader
# =============================
process.load("CSCTriggerPrimitivesReader_cfi")
process.lctreader.debug = True
#process.output = cms.OutputModule("PoolOutputModule",
#    fileName = cms.untracked.string(sys.argv[3]),
#    outputCommands = cms.untracked.vstring("keep *",
#        "drop *_DaqSource_*_*")
#)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string(sys.argv[4])
)

# Scheduler path
# ==============
#process.p = cms.Path(process.myfilter*process.muonCSCDigis*process.cscTriggerPrimitiveDigis*process.lctreader)
process.p = cms.Path(process.muonCSCDigis*process.cscTriggerPrimitiveDigis*process.lctreader)
#process.p = cms.Path(process.muonCSCDigis*process.cscTriggerPrimitiveDigis)
#process.ep = cms.EndPath(process.output)
