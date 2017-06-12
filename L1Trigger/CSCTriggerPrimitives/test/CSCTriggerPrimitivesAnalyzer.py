#############################################
#validate CSC emulator 
#############################################
import ROOT
import numpy as n
import os
from DataFormats.FWLite import Events, Handle
# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()
ROOT.AutoLibraryLoader.enable()

# Make VarParsing object
# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#VarParsing_Example
from FWCore.ParameterSet.VarParsing import VarParsing
#options = VarParsing ('python')
#options.parseArguments()
## helper for files on dCache/EOS (LPC)
def userInputDir(inputDir):
    theInputFiles = []
    for d in range(len(inputDir)):
        my_dir = inputDir[d]
        if not os.path.isdir(my_dir):
            print "ERROR: This is not a valid directory: ", my_dir
            if d==len(inputDir)-1:
                print "ERROR: No input files were selected"
                exit()
            continue
        ls = os.listdir(my_dir)
	theInputFiles.extend([my_dir + x for x in ls if x.endswith('.root')])
    return theInputFiles   
inputdir = ['/eos/uscms/store/user/tahuang/SingleMuon/SingleMuon_2016H_v1_281976/161012_220915/0000/']
#inputdir = ['/eos/uscms/store/user/tahuang/SingleMuon_Run2MC_GEN_SIM_DIGI_L1_DIGI2RAW/SingleMuonPt100_MC_GEN_SIM_DIGI_L1_DIGI2RAW/160916_001033/0000/']
inputdir = ['/eos/uscms/store/user/tahuang/JPsiToMuMu_Pt20to100-pythia8-gun/JPsiToMuMu_Pt20to100_RAW2DIGI_REL1/170425_054140/0000/']
filelist = userInputDir(inputdir)
#events = Events ('out_sim.root')
events = Events (filelist)
# create handle outside of loop
mpclct_e = Handle('MuonDigiCollection<CSCDetId,CSCCorrelatedLCTDigi>')
mpclct_e_label = "emtfStage2Digis"
emtfhits = Handle('vector<l1t::EMTFHit>')
emtfhits_data = Handle('vector<l1t::EMTFHit>')
emtfextrahits = Handle('vector<l1t::EMTFHitExtra>')
emtftracks = Handle('vector<l1t::EMTFTrack>')
emtftracks_data = Handle('vector<l1t::EMTFTrack>')
emtfextratracks = Handle('vector<l1t::EMTFTrackExtra>')
emtfdigilabel_data = "emtfStage2Digis"
emtfdigilabel = "simEmtfDigis"
#emtfdigilabel = emtfdigilabel_data


# a label is just a tuple of strings that is initialized just
# like and edm::InputTag
label = ("genParticles")

ROOT.gROOT.SetBatch()        # don't pop up canvases
f = ROOT.TFile(emtfdigilabel+"_PU2016_MC.root", "recreate")
#f = ROOT.TFile(emtfdigilabel+"_Run2016H_v1_281976.root", "recreate")
t = ROOT.TTree("TFHits", "tree title")


# create 1 dimensional float arrays (python's float datatype corresponds to c++ doubles)
# as fill variables
chamber = n.zeros(1, dtype=int)
ring = n.zeros(1, dtype=int)
station = n.zeros(1, dtype=int)
endcap = n.zeros(1, dtype=int)
bx = n.zeros(1, dtype=int)
wg = n.zeros(1, dtype=int)
hs = n.zeros(1, dtype=int)
Is_CSC_hit = n.zeros(1, dtype=int)
quality =n.zeros(1, dtype=int)
pattern = n.zeros(1, dtype=int)
isUsedbyTtrack =n.zeros(1, dtype=bool)
tracknumhits = n.zeros(1, dtype=int)
trackpt = n.zeros(1, dtype=int)
tracketa = n.zeros(1, dtype=float)
trackphi = n.zeros(1, dtype=float)
tracksector = n.zeros(1, dtype=int)
trackhasME1 =n.zeros(1, dtype=bool)
trackhasME2 =n.zeros(1, dtype=bool)
trackhasME3 =n.zeros(1, dtype=bool)
trackhasME4 =n.zeros(1, dtype=bool)




# create the branches and assign the fill-variables to them
t.Branch('chamber', chamber, 'chamber/I')
t.Branch('ring', ring, 'ring/I')
t.Branch('station', station, 'station/I')
t.Branch('endcap', endcap, 'endcap/I')
t.Branch('bx', bx, 'bx/I')
t.Branch('wg', wg, 'wg/I')
t.Branch('hs', hs, 'hs/I')
t.Branch('Is_CSC_hit', Is_CSC_hit, 'Is_CSC_hit/I')
t.Branch('quality', quality, 'quality/I')
t.Branch('isUsedbyTtrack', isUsedbyTtrack, 'isUsedbyTtrack/B')
t.Branch('tracknumhits',tracknumhits,'tracknumhits/I')
t.Branch('trackpt',trackpt,'trackpt/I')
t.Branch('tracketa',tracketa,'tracketa/D')
t.Branch('trackphi',trackphi,'trackphi/D')
t.Branch('tracksector',tracksector,'tracksector/I')
t.Branch('trackhasME1',trackhasME1,'trackhasME1/B')
t.Branch('trackhasME2',trackhasME2,'trackhasME2/B')
t.Branch('trackhasME3',trackhasME3,'trackhasME3/B')
t.Branch('trackhasME4',trackhasME4,'trackhasME4/B')

#t.Branch('eta', eta, 'eta/D')
def checkLCT(hit, alllcts):
    for lct in alllcts:
    	if (lct.BX()==hit.BX() and lct.Wire()==hit.Wire() and lct.Strip()==hit.Strip() and lct.Chamber()==hit.Chamber() and lct.Ring()==hit.Ring() and lct.Station()==hit.Station() and lct.Endcap()==hit.Endcap()):
	    return False
    return True

def initBranches():
    chamber[0] = -1
    ring[0] = -1
    station[0] = -1
    endcap[0] = -9
    bx[0] = -99
    wg[0] = -1
    hs[0] = -1
   # Is_CSC_hit[0] = False
    quality[0] = -1
    tracknumhits[0] = -1
    trackpt[0] = -1
    tracketa[0] = -9
    trackphi[0] = -9
    tracksector[0] = -9
    trackhasME1[0] = False
    trackhasME2[0] = False
    trackhasME3[0] = False
    trackhasME4[0] = False




runEvents = 100000
nevent = 0
# loop over events
for event in events:
    if (runEvents>0 and nevent >= runEvents):
	break
 # use getByLabel, just like in cmsRun
    event.getByLabel(emtfdigilabel, emtfhits)
    event.getByLabel(emtfdigilabel_data, emtfhits_data)
    event.getByLabel(emtfdigilabel, emtftracks)
    event.getByLabel(emtfdigilabel_data, emtftracks_data)
    #event.getByLabel(emtfdigilabel,"CSC", emtfextrahits)
    #event.getByLabel(emtfdigilabel, emtfextratracks)
    print "ievet ",nevent 
    allLCTs = []
    for track in emtftracks.product():
	initBranches()
	#print "endcap ",track.Endcap()," sector ",track.Sector()," bx ",track.BX()," pt ",track.Pt()," eta ",track.Eta()," hits size ",track.NumHits()
	trackpt[0] = track.Pt()
	tracketa[0] = track.Eta()
	#trackphi[0] = track.Phi()
	tracknumhits[0] = track.NumHits()
	tracksector[0] = track.Sector()

	for hit in track.Hits():
	    #print "hit in track ", hit," endcap ",hit.Endcap()," station ",hit.Station()," ring ",hit.Ring()," chamber ", hit.Chamber()," strip ",hit.Strip()," wg ",hit.Wire()," BX ",hit.BX()
	    endcap[0] = hit.Endcap()
	    station[0] = hit.Station()
	    ring[0] = hit.Ring()
	    chamber[0] = hit.Chamber()
	    hs[0] = hit.Strip()
	    wg[0] = hit.Wire()
	    bx[0] = hit.BX()
	    quality[0] = hit.Quality()
	    pattern[0] = hit.Pattern()
	    if checkLCT(hit, allLCTs):
		#print "fill LCT"
		isUsedbyTtrack[0] = True
		t.Fill()
		allLCTs.append(hit)
    #for track in emtftracks_data.product():
	#print "in data, endcap ",track.Endcap()," sector ",track.Sector()," bx ",track.BX()," pt ",track.Pt()," eta ",track.Eta()," hits size ",track.NumHits()
	#for hit in track.Hits():
	    #print "hit in track, endcap ",hit.Endcap()," station ",hit.Station()," ring ",hit.Ring()," chamber ", hit.Chamber()," strip ",hit.Strip()," wg ",hit.Wire()," BX ",hit.BX()
	   
    #for track in emtfextratracks.product():
	#print "extra endcap ",track.Endcap()," sector ",track.Sector()," bx ",track.BX()," pt ",track.Pt()," eta ",track.Eta()," hits size ",track.NumHits()
	#for hit in track.Hits():
	    #print "hit in track, endcap ",hit.Endcap()," station ",hit.Station()," ring ",hit.Ring()," chamber ", hit.Chamber()," strip ",hit.Strip()," wg ",hit.Wire()," BX ",hit.BX()
    #nmatched = len(allLCTs)
    #for hit in emtfhits.product():
    	#print "hit ",hit," endcap ",hit.Endcap()," station ",hit.Station()," ring ",hit.Ring()," chamber ", hit.Chamber()," strip ",hit.Strip()," wg ",hit.Wire()," BX ",hit.BX()
	#if checkLCT(hit, allLCTs):
	    #print "fill LCT"
	   # allLCTs.append(hit)

    #print "print all LCTs, before set "
    #ihit = -1
    #for hit in allLCTs:
        #ihit +=1 
    	#print "hit ",hit, " endcap ",hit.Endcap()," station ",hit.Station()," ring ",hit.Ring()," chamber ", hit.Chamber()," strip ",hit.Strip()," wg ",hit.Wire()," BX ",hit.BX()
    	
    #for hit in emtfhits_data.product():
    	##print "in data, endcap ",hit.Endcap()," station ",hit.Station()," ring ",hit.Ring()," chamber ", hit.Chamber()," strip ",hit.Strip()," wg ",hit.Wire()," BX ",hit.BX()
    #for hit in emtfextrahits.product():
    	#print "extra endcap ",hit.Endcap()," station ",hit.Station()," ring ",hit.Ring()," chamber ", hit.Chamber()," strip ",hit.Strip()," wg ",hit.Wire()," BX ",hit.BX()," eta ",hit.Eta()
    """
    event.getByLabel (mpclct_e_label, mpclct_e)
    print "mpclct_e " , mpclct_e.product()
    mpclct_e_all = mpclct_e.product()
    for encap  in range(1,3):
	for ring in range(1,3):
	    for station in range(1, 5):
		for chamber in range(0,36):
		    #cscid = CSCDetId(encap, station, ring, chamber, 0)
		    lcts = mpclct_e_all.get(CSCDetId(encap, station, ring, chamber, 0))

		    # get the product
		    for lct in lcts: 
			print " lct ",lct
			#bx_e = lct.getBX()
			#wg_e = lct.getKeyWG()
			#hs_e = lct.getKeyStrip()
		#	print "bx_e ",bx_e," wg_e ",wg_e," hs_e ",hs_e
			#t.Fill()
    #not sure how to increase iterator  without using ++ and how to get elements inside a pair
    iterator  = mpclct_e_all.begin()
    print "type ",type(iterator)
    while (iterator != mpclct_e_all.end()):
	lcts = iterator.second
	print "iterator ",iterator, " first ",iterator.first," chamber ",iterator.first.chamber()
	print "lcts ",lcts," type ",type(lcts)
	iterator = iterator.next()
	#print "lct ",lct, " bx ",lct.getBX()," wg ",lct.getKeyWG()," hs ",lct.getKeyStrip()
	#break 
    """
    nevent +=  1

f.Write()
f.Close()
