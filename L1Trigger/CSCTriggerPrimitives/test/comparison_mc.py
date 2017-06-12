from ROOT import *
import sys
sys.argv.append( '-b' )
import ROOT
ROOT.gROOT.SetBatch(1)
import os
#ROOT.gErrorIgnoreLevel=1001

cscstations = [ [0,0], 
                [1,1], [1,2], [1,3],
                [2,1], [2,2],
                [3,1], [3,2],
                [4,1], [4,2],]
csclabel = {
    1 : {
        0 : {
            0 : ["pAll", 'All CSCs'] 
            },
        1 : {
            1 : ["pME11","ME+1/1"],
            2 : ["pME12","ME+1/2"],
            3 : ["pME13","ME+1/3"],
            #4 : ["pME1a","ME+1/1a"]
            },
        2 : {
            1 : ["pME21","ME+2/1"],
            2 : ["pME22","ME+2/2"]
            },
        3 : {
            1 : ["pME31","ME+3/1"],
            2 : ["pME32","ME+3/2"]
            },
        4 : {
            1 : ["pME41","ME+4/1"],
            2 : ["pME42","ME+4/2"]
            },
        },
    2 : {
        0 : {
            0 : ["mAll","All CSCs"]
            },
        1 : {
            1 : ["mME1b","ME-1/1b"],
            2 : ["mME12","ME-1/2"],
            3 : ["mME13","ME-1/3"],
            4 : ["mME1a","ME-1/1a"],
            },
        2 : {
            1 : ["mME21","ME-2/1"],
            2 : ["mME22","ME-2/2"]
            },
        3 : {
            1 : ["mME31","ME-3/1"],
            2 : ["mME32","ME-3/2"]
            },
        4 : {
            1 : ["mME41","ME-4/1"],
            2 : ["mME42","ME-4/2"]
            },
        },
    }
gROOT.SetBatch(1)
gStyle.SetStatStyle(0)
gStyle.SetOptStat("nemr")

ch = TChain("Events")
#filedir = "/eos/uscms/store/user/tahuang/SingleMuon_Run2MC_GEN_SIM_DIGI_L1_DIGI2RAW/L1REPACK_RAW2DIGI_0919/160920_153918/0000/"
filedir = "/eos/uscms/store/user/tahuang/SingleMuon_Run2MC_GEN_SIM_DIGI_L1_DIGI2RAW/SingleMuonPt100_MC_GEN_SIM_DIGI_L1_DIGI2RAW_updatetimeBitForBxZero/161103_024426/0000/"
#fc = TFileCollection("dum")
#fc.Add("/eos/uscms/store/user/lpcgem/SingleMuonPt100_MC/SingleMuonPt100_MC_L1REPACK_DIGI2RAW_v2/160811_011552/0000/*.root")
#fc.Add("SingleMuPt100_cfi_DIGIL1_10k_NewDigiBunchOffsets_v1.root")
#fc.Add("output_l1_2016B_doublemuon_272936_batch_20k_1.root")
#fc.Add("/eos/uscms/store/user/tahuang/SingleMuon/SingleMuon_2016G_v1_278819/160915_235753/0000/*.root")
#fc.Add("/eos/uscms/store/user/tahuang/SingleMuon_Run2MC_GEN_SIM_DIGI_L1_DIGI2RAW/SingleMuonPt100_MC_GEN_SIM_DIGI_L1_DIGI2RAW/160916_001033/0000/*root")
#fc.Add("/eos/uscms/store/user/tahuang/SingleMuon/SingleMuon_2016G_v1_278820/160916_164507/0000/*root")
#fc.Add("/eos/uscms/store/user/tahuang/SingleMuon_Run2MC_GEN_SIM_DIGI_L1_DIGI2RAW/L1REPACK_RAW2DIGI_0919/160920_153918/0000/out_ReL1*.root")
#fc.Add("/eos/uscms/store/user/tahuang/SingleMuon_Run2MC_GEN_SIM_DIGI_L1_DIGI2RAW_2015stage1/SingleMuonPt100_MC_GEN_SIM_DIGI_L1_DIGI2RAW_2015stage1/161031_200959/0000/*root")
#fc.Add("/eos/uscms/store/user/tahuang/SingleMuon_Run2MC_GEN_SIM_DIGI_L1_DIGI2RAW_2015stage1/SingleMuonPt100_MC_GEN_SIM_DIGI_L1_DIGI2RAW_2015stage1/161101_164141/0000/*root")
#fc.Add("/eos/uscms/store/user/tahuang/SingleMuon_Run2MC_GEN_SIM_DIGI_L1_DIGI2RAW/SingleMuonPt100_MC_GEN_SIM_DIGI_L1_DIGI2RAW_keepRaw/160919_154255/0000/*root")
#fc.Add("/eos/uscms/store/user/tahuang/SingleMuon_Run2MC_GEN_SIM_DIGI_L1_DIGI2RAW/SingleMuonPt100_MC_GEN_SIM_DIGI_L1_DIGI2RAW_updatetimeBitForBxZero/161103_024426/0000/*root")
#SingleMuPt100_cfi_L1REPACK_RAW2DIGI_10k_Baseline_backup.root
#print fc
#fc.Print()
#ch.AddFileInfoList(fc.GetList())
def getChain(filedir, chain):
    if os.path.isdir(filedir):
    	ls = os.listdir(filedir)
    	for x in ls:
	     if not(x.endswith(".root")):
	     #print "x.endswith(.root) ", x.endswith(".root")
		continue
	     x = filedir[:]+x
    	     if os.path.isdir(x):
		continue
	     chain.Add(x)
    elif os.path.isfile(filedir):
	chain.Add(filedir)
    else:
	print " it is not file or dir ", filedir
    return chain

ch = getChain(filedir, ch)
#exit(1)
#file = TFile("SingleMuPt100_cfi_L1REPACK_RAW2DIGI_10k_Baseline_backup.root")
#outputdirectory = "SingleMuon_2016G_v1_278820/"
outputdirectory = "SingleMuon_MC_100k_80X_20161101_updatetimeBitForBxZero/"
#outputdirectory = "SingleMuon_MC_100k_20161102_ReL1/"
tree = ch#.Get("Events")

csccorrelatedlctdigi = {
    0 : ["trknmb", "trknmb",10,0,10],
    1 : ["valid", "valid",20,0,20],
    2 : ["quality", "quality",20,0,20],
    3 : ["keywire", "keywire",150,0,150],
    4 : ["strip", "strip",224,0,224],
    5 : ["pattern", "pattern",16,0,16],
    6 : ["bend", "bend",10,0,10],
    7 : ["bx", "bx",17,-0.5,16.5],
    8 : ["mpclink", "mpclink",5,0,5],
    9 : ["bx0", "bx0",10,0,10],
    10 : ["syncErr", "syncErr",10,0,10],
    11 : ["cscID", "cscID",15,0,15],
    }

cscalctdigi = {
    0 : ["valid_", "valid",10,0,10],
    1 : ["quality_", "quality",20,0,20],
    2 : ["accel_", "accelerator",10,0,10],
    3 : ["patternb_", "patternb",10,0,10],
    4 : ["keywire_", "keywire",150,0,150],
    5 : ["bx_", "bx",13,-0.5,12.5],
    6 : ["trknmb_", "trknmb",10,0,10],
   7 : ["fullbx_", "fullbx",10,0,10],
}

cscclctdigi = {
    0 : ["valid_", "valid",10,0,10],
    1 : ["quality_", "quality",16,0,16],
    2 : ["pattern_", "pattern",20,0,20],
    3 : ["striptype_", "striptype",10,0,10],
    4 : ["bend_", "bend",10,0,10],
    5 : ["cfeb_", "cfeb",10,0,10],
    6 : ["strip_", "strip",32,0,32],
    7 : ["bx_", "bx",13,-0.5,12.5],
    8 : ["trknmb_", "trknmb",10,0,10],
    9 : ["fullbx_", "fullbx",10,0,10],
    10 : ["getKeyStrip()", "keyStrip",224,0,224],
    }

colors = [kRed, kMagenta+2,kBlue, kOrange+2, kPink+1, 28]
legs = ["#splitline{Unpacked from}{EM TrackFinder}","#splitline{Unpacked from}{CSC TrackFinder}","#splitline{Re-emulated from}{unpacked digis}"]
#legs_MC = ["#splitline{simulated}{Trigger Primitives}","#splitline{packer+unpacker}{+Re-Emulation}","#splitline{packer+unpacker}{data path}"]
legs_MC = ["#splitline{simulated}{Trigger Primitives}","#splitline{packer+unpacker}{+Re-Emulation}","#splitline{packer+unpacker}{from EM TrackFinder}"]


def yRanges(nCollections):
    yrange = 1.0-0.1
    ydelta = yrange/nCollections
    ymins = []
    ymaxs = []
    for d in range(0,nCollections):
        ymins.append(1.0-(1+d)*ydelta)
        ymaxs.append(1.0-d*ydelta)
    return ymins, ymaxs

def compareSegments(collections, legs, alldigis, endcap, station, ring, variable, text):
 
    nCollections = len(collections)
    ymins, ymaxs = yRanges(nCollections)
    
    
    var = csccorrelatedlctdigi[variable][0]
    varstr = csccorrelatedlctdigi[variable][1]
    varnbin = csccorrelatedlctdigi[variable][2]
    varminbin = csccorrelatedlctdigi[variable][3]
    varmaxbin = csccorrelatedlctdigi[variable][4]
    


    c = TCanvas("c","c",800,600)
    c.cd()

    def addCollection(collection, index):
        #collection_substring = collection[len('CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_'):] + "_" + varstr + "_" + csclabel[endcap][station][ring][0] 
        collection_substring = collection + "_" + varstr + "_" + csclabel[endcap][station][ring][0] 
        hist = TH1D(collection_substring,"CSC Segments " + varstr + " " + 
                   csclabel[endcap][station][ring][1] + "; " + varstr + "; Normalized to Unity",varnbin,varminbin,varmaxbin)
	if index==2:
    		#var = csccorrelatedlctdigi[variable][0]+"-2"
    		var = csccorrelatedlctdigi[variable][0]
	else:
    		var = csccorrelatedlctdigi[variable][0]+"_"
	print "index ",index," var ",var
        if station==0 and ring==0:
            tree.Draw(collection + ".obj.data_.second." + var + ">>" + hist.GetName(),
                      collection + ".obj.data_.first.endcap() == %d && "%(endcap)+
			collection + ".obj.data_.second.isValid()")
        else:
            tree.Draw(collection + ".obj.data_.second." + var + ">>" + hist.GetName(),
                      collection + ".obj.data_.first.endcap() == %d && "%(endcap) +
                      collection + ".obj.data_.first.station()==%d && "%(station) + 
                      collection + ".obj.data_.first.ring()==%d && "%(ring) +
			collection + ".obj.data_.second.isValid()")
            
        hist.SetLineColor(colors[index])
	hist.SetLineWidth(2)
        
        
        if varstr is 'bx':
            if hist.GetEntries()!=0:
                print '%s |'%collection, csclabel[endcap][station][ring][1], '|', hist.GetBinContent(6)/hist.GetEntries(), '|', hist.GetBinContent(7)/hist.GetEntries(), '|', hist.GetBinContent(8)/hist.GetEntries(), '|' ,hist.GetEntries(),'|',hist.Integral()
	    else:
	    	print '%s has 0 entry '%collection
  
        if index==0:
            hist.Draw()
        else:
            hist.Draw("sames")
        gPad.Update()
        hist_st = hist.FindObject("stats");
        hist_st.SetY1NDC(ymins[index]);
        hist_st.SetY2NDC(ymaxs[index])
        hist_st.SetTextColor(colors[index]);
        SetOwnership(hist, False)
        SetOwnership(hist_st, False)
        return hist, hist_st

    def plotCollection(hist, stats, index):
	hist.Scale(1.0/hist.Integral())
	hist.GetYaxis().SetNdivisions(520)
	hist.Draw("same")
        #if index==0: hist.Draw()
        #else:        hist.Draw("sames")
        #stats.Draw("same")
    ## add the$i histograms and the stat boxes
    hists = []
    stats = []

    for i in range(0,nCollections):
        hist, stat = addCollection(collections[i],i)
        hists.append(hist)
        stats.append(stat)
    c.Clear()
    if  endcap == 1:
	cap = "Positive Endcap, "+ csclabel[endcap][station][ring][1]
    else:
	cap = "Negative Endcap, "+ csclabel[endcap][station][ring][1]
    print "endcap ",endcap," cap ",cap
    hs = THStack("hslct"," %s distribution,%s"%(varstr,cap))
    legend = TLegend(0.70,0.6,.850,0.85)
    legend.SetFillColor(ROOT.kWhite)
    legend.SetTextFont(42)
    for i in range(0,nCollections):
	hists[i].SetStats(0)
	hists[i].SetLineStyle(i/2)
	hs.Add(hists[i])
	leg = collections[i].split('_')[1]
	legend.AddEntry(hists[i],"%s"%legs[i],"l")
	#legend.AddEntry(hists[i],"%s"%legs[i],"l")
    hs.Draw("nostack")
    hs.GetHistogram().GetXaxis().SetTitle(varstr)
    legend.Draw("same")
    tex = TLatex(.3,.2,"#splitline{%s}{%s}"%(cap, text));
    tex.SetNDC();
    tex.SetTextSize(.05);
    tex.SetTextFont(62);
    tex.Draw("same");
    c.SetGridx() 
    c.SetGridy() 
    c.SetTickx() 
    c.SetTicky() 
    c.SetLogy()
    c.SaveAs(outputdirectory  + "comparison_all_" + varstr + "_" + csclabel[endcap][station][ring][0] + "_logy_20161102.png")
    c.SaveAs(outputdirectory  + "comparison_all_" + varstr + "_" + csclabel[endcap][station][ring][0] + "_logy_20161102.C")

    c1 = TCanvas("c1","c1",800,600)
    c1.cd()

    b1 = TH1D("b1","b1",varnbin,varminbin,varmaxbin)
    b1.GetYaxis().SetRangeUser(0.01,2)
    b1.GetYaxis().SetTitleOffset(1.2)
    b1.GetYaxis().SetNdivisions(520)
    b1.GetYaxis().SetTitle("Normalized to unity")
    b1.GetXaxis().SetTitle(varstr)
    b1.GetXaxis().SetTitleSize(0.045)
    b1.SetTitle("LCT %s distribution, %s"%(varstr,cap))
    b1.SetTitleSize(.05)
    b1.SetStats(0)
    b1.Draw() 
    for i in range(0,nCollections):
	hists[i].SetStats(0)
        plotCollection(hists[i], stats[i], i)
    legend.Draw("same")
    tex.Draw("same");
    c1.SetGridx() 
    c1.SetGridy() 
    c1.SetTickx() 
    c1.SetTicky() 
    c1.SetLogy()
    c1.SaveAs(outputdirectory  + "MC_comparison_all_" + varstr + "_" + csclabel[endcap][station][ring][0] + "_logy_Normalized_20161102.png")
    c1.SaveAs(outputdirectory  + "MC_comparison_all_" + varstr + "_" + csclabel[endcap][station][ring][0] + "_logy_Normalized_20161102.C")
    

    
def compareLCTs(collections, legs, text, endcap, station, ring, variable):

    nCollections = len(collections)
    ymins, ymaxs = yRanges(nCollections)

    var = csccorrelatedlctdigi[variable][0]
    varstr = csccorrelatedlctdigi[variable][1]
    varnbin = csccorrelatedlctdigi[variable][2]
    varminbin = csccorrelatedlctdigi[variable][3]
    varmaxbin = csccorrelatedlctdigi[variable][4]

    extraCut = "strip >= 0"
    realRing = ring
    
    if station==1 and ring==1:
        extraCut = "strip < 128"

    if station==1 and ring==4:
        extraCut = "strip >= 128"
        realRing = 1

    c = TCanvas("c","c",800,600)
    c.cd()

    def addCollection(collection, index):
        collection_substring = collection[len('CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_'):] + "_" + varstr + "_" + csclabel[endcap][station][ring][0] 
        hist = TH1D(collection_substring,"CSC LCT " + varstr + " " + 
                   csclabel[endcap][station][ring][1] + "; " + varstr + "; Normalized to Unity",varnbin,varminbin,varmaxbin)
	if index==2:
    		#var = csccorrelatedlctdigi[variable][0]+"-2"
    		var = csccorrelatedlctdigi[variable][0]
	else:
    		var = csccorrelatedlctdigi[variable][0]
	print "index ",index," var ",var
        if station==0 and realRing==0:
            tree.Draw(collection + ".obj.data_.second." + var + ">>" + hist.GetName(),
                      collection + ".obj.data_.first.endcap() == %d && "%(endcap)+
			collection + ".obj.data_.second.isValid()")
        else:
            tree.Draw(collection + ".obj.data_.second." + var + ">>" + hist.GetName(),
                      collection + ".obj.data_.first.endcap() == %d && "%(endcap) +
                      collection + ".obj.data_.first.station()==%d && "%(station) + 
                      collection + ".obj.data_.first.ring()==%d && "%(realRing) +
                      collection + ".obj.data_.second." + extraCut+" && "+
			collection + ".obj.data_.second.isValid()")
            
        hist.SetLineColor(colors[index])
	hist.SetLineWidth(2)
        
        
        if varstr is 'bx':
            if hist.GetEntries()!=0:
                print '%s |'%collection, csclabel[endcap][station][ring][1], '|', hist.GetBinContent(6)/hist.GetEntries(), '|', hist.GetBinContent(7)/hist.GetEntries(), '|', hist.GetBinContent(8)/hist.GetEntries(), '|' ,hist.GetEntries(),'|',hist.Integral()
	    else:
	    	print '%s has 0 entry '%collection
  
        if index==0:
            hist.Draw()
        else:
            hist.Draw("sames")
        gPad.Update()
        hist_st = hist.FindObject("stats");
        hist_st.SetY1NDC(ymins[index]);
        hist_st.SetY2NDC(ymaxs[index])
        hist_st.SetTextColor(colors[index]);
        SetOwnership(hist, False)
        SetOwnership(hist_st, False)
        return hist, hist_st

    def plotCollection(hist, stats, index):
	hist.Scale(1.0/hist.Integral())
	hist.GetYaxis().SetNdivisions(520)
	hist.Draw("same")
        #if index==0: hist.Draw()
        #else:        hist.Draw("sames")
        #stats.Draw("same")
    ## add the$i histograms and the stat boxes
    hists = []
    stats = []

    for i in range(0,nCollections):
        hist, stat = addCollection(collections[i],i)
        hists.append(hist)
        stats.append(stat)
    c.Clear()
    if  endcap == 1:
	cap = "Positive Endcap, "+ csclabel[endcap][station][ring][1]
    else:
	cap = "Negative Endcap, "+ csclabel[endcap][station][ring][1]
    print "endcap ",endcap," cap ",cap
    hs = THStack("hslct","LCT %s distribution,%s"%(varstr,cap))
    legend = TLegend(0.65,0.5,1.0,0.9)
    legend.SetFillColor(ROOT.kWhite)
    legend.SetTextFont(42)
    for i in range(0,nCollections):
	hists[i].SetStats(0)
	hs.Add(hists[i])
	leg = collections[i].split('_')[1]
	legend.AddEntry(hists[i],"%s"%legs[i],"l")
	#legend.AddEntry(hists[i],"%s"%legs[i],"l")
    hs.Draw("nostack")
    hs.GetHistogram().GetXaxis().SetTitle(varstr)
    legend.Draw("same")
    tex = TLatex(.3,.2,"#splitline{%s}{%s}"%(cap,text));
    tex.SetNDC();
    tex.SetTextSize(.05);
    tex.SetTextFont(62);
    tex.Draw("same");
    c.SetGridx() 
    c.SetGridy() 
    c.SetTickx() 
    c.SetTicky() 
    c.SetLogy()
    c.SaveAs(outputdirectory  + "comparison_lct_" + varstr + "_" + csclabel[endcap][station][ring][0] + "_logy_20161102.png")
    c.SaveAs(outputdirectory  + "comparison_lct_" + varstr + "_" + csclabel[endcap][station][ring][0] + "_logy_20161102.C")

    c1 = TCanvas("c1","c1",800,600)
    c1.cd()

    b1 = TH1D("b1","b1",varnbin,varminbin,varmaxbin)
    b1.GetYaxis().SetRangeUser(0.01,2)
    b1.GetYaxis().SetTitleOffset(1.2)
    b1.GetYaxis().SetNdivisions(520)
    b1.GetYaxis().SetTitle("Normalized to unity")
    b1.GetXaxis().SetTitle(varstr)
    b1.GetXaxis().SetTitleSize(0.045)
    b1.SetTitle("LCT %s distribution, %s"%(varstr,cap))
    b1.SetTitleSize(.05)
    b1.SetStats(0)
    b1.Draw() 
    for i in range(0,nCollections):
	hists[i].SetStats(0)
        plotCollection(hists[i], stats[i], i)
    legend.Draw("same")
    tex.Draw("same");
    c1.SetGridx() 
    c1.SetGridy() 
    c1.SetTickx() 
    c1.SetTicky() 
    c1.SetLogy()
    c1.SaveAs(outputdirectory  + "MC_comparison_lct_" + varstr + "_" + csclabel[endcap][station][ring][0] + "_logy_Normalized_20161102.png")
    c1.SaveAs(outputdirectory  + "MC_comparison_lct_" + varstr + "_" + csclabel[endcap][station][ring][0] + "_logy_Normalized_20161102.C")
    


def compareALCTs(collections, endcap, station, ring, variable):

    legs = ["Unpacked from CSC data path","Re-emulated from unpacked digis"]
    nCollections = len(collections)
    ymins, ymaxs = yRanges(nCollections)
        
    var = cscalctdigi[variable][0]
    varstr = cscalctdigi[variable][1]
    varnbin = cscalctdigi[variable][2]
    varminbin = cscalctdigi[variable][3]
    varmaxbin = cscalctdigi[variable][4]

    c = TCanvas("c","c",800,600)
    c.cd()

    def addCollection(collection, index):
        collection_substring = collection[len('CSCDetIdCSCALCTDigiMuonDigiCollection_'):] + "_" + varstr + "_" + csclabel[endcap][station][ring][0]
        hist = TH1D(collection_substring,"CSCALCTDigi " + varstr + " " + 
                   csclabel[endcap][station][ring][1] + "; " + varstr + "; Normalized to Unity",varnbin,varminbin,varmaxbin)
	if index==0:
    		var = cscalctdigi[variable][0]+"+5"
	else:
    		var = cscalctdigi[variable][0]
	print "index ",index," var ",var

        if station==0 and ring==0:
            tree.Draw(collection + ".obj.data_.second." + var + ">>" + hist.GetName(),
                      collection + ".obj.data_.first.endcap() == %d && "%(endcap)+
			collection + ".obj.data_.second.isValid()")
        else:
            tree.Draw(collection + ".obj.data_.second." + var + ">>" + hist.GetName(),
                      collection + ".obj.data_.first.endcap() == %d && "%(endcap) +
                      collection + ".obj.data_.first.station()==%d && "%(station) + 
                      collection + ".obj.data_.first.ring()==%d"%(ring)+"&&"+
			 collection + ".obj.data_.second.isValid()")
            
        hist.SetLineColor(colors[index])
	if index ==0:
		hist.SetLineWidth(3)
	else:
		hist.SetLineWidth(2)
	
        if varstr is 'bx':
            if hist.GetEntries()!=0:
                print 'ALCT |', csclabel[endcap][station][ring][1], '|', hist.GetBinContent(6)/hist.GetEntries(), '|', hist.GetBinContent(7)/hist.GetEntries(), '|', hist.GetBinContent(8)/hist.GetEntries(), '|' 
        if index==0:
            hist.Draw()
        else:
            hist.Draw("sames")
        gPad.Update()
        hist_st = hist.FindObject("stats");
        hist_st.SetY1NDC(ymins[index]);
        hist_st.SetY2NDC(ymaxs[index])
        hist_st.SetTextColor(colors[index]);
        SetOwnership(hist, False)
        SetOwnership(hist_st, False)
        return hist, hist_st

    def plotCollection(hist, stats, index):
	hist.Scale(1.0/hist.Integral())
	hist.GetYaxis().SetNdivisions(520)
	hist.Draw("same")
        #if index==0: hist.Draw()
        #else:        hist.Draw("sames")
        #stats.Draw("same")
        
    ## add the histograms and the stat boxes
    hists = []
    stats = []
    for i in range(0,nCollections):
        hist, stat = addCollection(collections[i],i)
        hists.append(hist)
        stats.append(stat)

    c.Clear()
    b1 = TH1D("b1","b1",varnbin,varminbin,varmaxbin)
    b1.GetYaxis().SetRangeUser(0.001,2)
    b1.GetYaxis().SetTitleOffset(1.2)
    b1.GetYaxis().SetNdivisions(520)
    b1.GetYaxis().SetTitle("Normalized to unity")
    b1.GetXaxis().SetTitle(varstr)
    b1.GetXaxis().SetTitleSize(0.045)
    b1.SetTitle("ALCT %s distribution, Data Vs Emulator, Positive Endcap"%varstr)
    b1.SetTitleSize(.05)
    b1.SetStats(0)
    b1.Draw() 
    legend = TLegend(0.4,0.75,0.9,0.9)
    legend.SetFillColor(ROOT.kWhite)
    legend.SetTextFont(42)
    for i in range(0,nCollections):
	hists[i].SetStats(0)
        plotCollection(hists[i], stats[i], i)
	leg = collections[i].split('_')[1]
	legend.AddEntry(hists[i],"%s"%legs[i],"l")
    legend.Draw("same")

    c.SetGridx() 
    c.SetGridy() 
    c.SetTickx() 
    c.SetTicky() 
    c.SetLogy()
    c.SaveAs(outputdirectory  + "comparison_alct_" + varstr + "_" + csclabel[endcap][station][ring][0] + "_logy_Normalized_0912.png")
    c.SaveAs(outputdirectory  + "comparison_alct_" + varstr + "_" + csclabel[endcap][station][ring][0] + "_logy_Normalized_0912.C")


def compareCLCTs(collections, endcap, station, ring, variable):

    nCollections = len(collections)
    ymins, ymaxs = yRanges(nCollections)
        
    var = cscclctdigi[variable][0]
    varstr = cscclctdigi[variable][1]
    varnbin = cscclctdigi[variable][2]
    varminbin = cscclctdigi[variable][3]
    varmaxbin = cscclctdigi[variable][4]

    c = TCanvas("c","c",800,600)
    c.cd()

    def addCollection(collection, index):
        collection_substring = collection[len('CSCDetIdCSCCLCTDigiMuonDigiCollection_'):] + "_" + varstr + "_" + csclabel[endcap][station][ring][0]
        hist = TH1D(collection_substring,"CSC CLCT " + varstr + " " + 
                   csclabel[endcap][station][ring][1] + "; " + varstr + "; Normalized to unity",varnbin,varminbin,varmaxbin)

        extraCut = "getKeyStrip() >=0"
        realRing = ring

        if station==1 and ring==1:
            extraCut = "getKeyStrip() <128"

        if station==1 and ring==4:
            realRing = 1
            extraCut = "getKeyStrip() >=128"

        if station==0 and realRing==0:
            tree.Draw(collection + ".obj.data_.second." + var + ">>" + hist.GetName(),
                      collection + ".obj.data_.first.endcap() == %d &&"%(endcap)+
			 collection + ".obj.data_.second.isValid()")
        else:
            tree.Draw(collection + ".obj.data_.second." + var + ">>" + hist.GetName(),
                      collection + ".obj.data_.first.endcap() == %d && "%(endcap) +
                      collection + ".obj.data_.first.station()==%d && "%(station) + 
                      collection + ".obj.data_.first.ring()==%d && "%(realRing) +
                      collection + ".obj.data_.second." + extraCut+" && "+
			 collection + ".obj.data_.second.isValid()")
            
        hist.SetLineColor(colors[index])
	hist.SetLineWidth(2)
        if varstr is 'bx':
            if hist.GetEntries()!=0:
                print 'CLCT |', csclabel[endcap][station][ring][1], '|', hist.GetBinContent(6)/hist.GetEntries(), '|', hist.GetBinContent(7)/hist.GetEntries(), '|', hist.GetBinContent(8)/hist.GetEntries(), '|' 
        if index==0:
            hist.Draw()
        else:
            hist.Draw("sames")
        gPad.Update()
        hist_st = hist.FindObject("stats");
        hist_st.SetY1NDC(ymins[index]);
        hist_st.SetY2NDC(ymaxs[index])
        hist_st.SetTextColor(colors[index]);
        SetOwnership(hist, False)
        SetOwnership(hist_st, False)
        return hist, hist_st

    def plotCollection(hist, stats, index):
	hist.Scale(1.0/hist.Integral())
	hist.Draw("same")
        #if index==0: hist.Draw()
        #else:        hist.Draw("sames")
        #stats.Draw("same")
        
    ## add the histograms and the stat boxes
    hists = []
    stats = []
    for i in range(0,nCollections):
        hist, stat = addCollection(collections[i],i)
        hists.append(hist)
        stats.append(stat)

    c.Clear()
    b1 = TH1D("b1","b1",varnbin,varminbin,varmaxbin)
    b1.GetYaxis().SetRangeUser(0.001,2.0)
    b1.GetYaxis().SetTitleOffset(1.2)
    b1.GetYaxis().SetNdivisions(520)
    b1.GetYaxis().SetTitle("Normalized to unity")
    b1.GetXaxis().SetTitle(varstr)
    b1.GetXaxis().SetTitleSize(0.045)
    b1.SetTitle("CLCT %s distribution"%varstr)
    b1.SetStats(0)
    b1.Draw() 
    legend = TLegend(0.6,0.75,0.9,0.9)
    legend.SetFillColor(ROOT.kWhite)
    legend.SetTextFont(42)
    for i in range(0,nCollections):
	hists[i].SetStats(0)
        plotCollection(hists[i], stats[i], i)
	leg = collections[i].split('_')[1]
	legend.AddEntry(hists[i],"%s"%leg,"l")
    legend.Draw("same")

    c.SetGridx() 
    c.SetGridy() 
    c.SetTickx() 
    c.SetTicky() 
    c.SetLogy()
    c.SaveAs(outputdirectory  + "comparison_clct_" + varstr + "_" + csclabel[endcap][station][ring][0] + "_logy_Normalized_0909.png")
    c.SaveAs(outputdirectory  + "comparison_clct_" + varstr + "_" + csclabel[endcap][station][ring][0] + "_logy_Normalized_0909.C")

def compareSegmentsAll(collections, legs, alldigis, text):
    for i in range(7,8):
        for p in cscstations:
            compareSegments(collections, legs, alldigis, 1,p[0],p[1],i, text)
        for p in cscstations:
            compareSegments(collections, legs, alldigis, 2,p[0],p[1],i, text)

def compareLCTsAll(collections, legs, text):
    for i in range(7,8):
        for p in cscstations:
            compareLCTs(collections,legs, text, 1,p[0],p[1],i)
        for p in cscstations:
            compareLCTs(collections,legs, text, 2,p[0],p[1],i)

def compareALCTsAll(collections):
    for i in range(5,6):
        for p in cscstations:
            if p[0]==1 and p[1]==4 : continue
            compareALCTs(collections,1,p[0],p[1],i)
        for p in cscstations:
            if p[0]==1 and p[1]==4 : continue
            compareALCTs(collections,2,p[0],p[1],i)
        
def compareCLCTsAll(collections):
    for i in range(7,8):
        for p in cscstations:
            compareCLCTs(collections,1,p[0],p[1],i)
        for p in cscstations:
            compareCLCTs(collections,2,p[0],p[1],i)
        
lct_collections = [
     #'CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_muonCSCDigis_MuonCSCCorrelatedLCTDigi_RAW2DIGI',
    'CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_emtfStage2Digis__RAW2DIGI',
    'CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_csctfDigis__RAW2DIGI',
    'CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_simCscTriggerPrimitiveDigis__RAW2DIGI',
 
#    'CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_simCscTriggerPrimitiveDigis_MPCSORTED_DIGI2RAW',
    #'CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_unpackCSC_MuonCSCCorrelatedLCTDigi_reL1T',
#    'CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_simCscTriggerPrimitiveDigis__reL1T',
#    'CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_simCscTriggerPrimitiveDigis_MPCSORTED_reL1T',
#    'CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_csctfUnpacker__reL1T',
#    'CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_muonCSCDigis_MuonCSCCorrelatedLCTDigi_reL1T'
]

alct_collections = [
    'CSCDetIdCSCALCTDigiMuonDigiCollection_muonCSCDigis_MuonCSCALCTDigi_RAW2DIGI',
    'CSCDetIdCSCALCTDigiMuonDigiCollection_simCscTriggerPrimitiveDigis__RAW2DIGI',
#    'CSCDetIdCSCALCTDigiMuonDigiCollection_unpackCSC_MuonCSCALCTDigi_reL1T',
#    'CSCDetIdCSCALCTDigiMuonDigiCollection_simCscTriggerPrimitiveDigis__reL1T',
#    'CSCDetIdCSCALCTDigiMuonDigiCollection_muonCSCDigis_MuonCSCALCTDigi_reL1T'
]

clct_collections = [
    'CSCDetIdCSCCLCTDigiMuonDigiCollection_muonCSCDigis_MuonCSCCLCTDigi_RAW2DIGI',
    'CSCDetIdCSCCLCTDigiMuonDigiCollection_simCscTriggerPrimitiveDigis__RAW2DIGI',
#    'CSCDetIdCSCCLCTDigiMuonDigiCollection_unpackCSC_MuonCSCCLCTDigi_reL1T',
#    'CSCDetIdCSCCLCTDigiMuonDigiCollection_simCscTriggerPrimitiveDigis__reL1T',
#    'CSCDetIdCSCCLCTDigiMuonDigiCollection_muonCSCDigis_MuonCSCCLCTDigi_reL1T'
]
 
#compareLCTsAll(lct_collections)
#compareALCTsAll(alct_collections)
#compareCLCTsAll(clct_collections)

lct_collections_mc = [
    'CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_simCscTriggerPrimitiveDigis__DIGI2RAW',
    'CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_simCscTriggerPrimitiveDigis__reL1T',
    'CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_emtfStage2Digis__reL1T',
    #'CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_muonCSCDigis_MuonCSCCorrelatedLCTDigi_reL1T',
]
segments_collections_mc = [
    'CSCDetIdCSCALCTDigiMuonDigiCollection_simCscTriggerPrimitiveDigis__DIGI2RAW',
    'CSCDetIdCSCCLCTDigiMuonDigiCollection_simCscTriggerPrimitiveDigis__DIGI2RAW',
    'CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_simCscTriggerPrimitiveDigis__DIGI2RAW',
]
#compareLCTsAll(lct_collections_mc, legs_MC, "MC")
legs = ["ALCT","CLCT","LCT"]
alldigis = [cscalctdigi,cscclctdigi,csccorrelatedlctdigi]
compareSegmentsAll(segments_collections_mc,legs, alldigis, "MC")

