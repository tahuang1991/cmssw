import ROOT
import random
import os
import sys
import numpy as np
import array
from math import *
from uncertainties import ufloat

ROOT.gROOT.SetBatch(0)
ROOT.gStyle.SetStatW(0.07)
ROOT.gStyle.SetStatH(0.06)

#ROOT.gStyle.SetOptStat(111110)

#ROOT.gStyle.SetErrorX(0)
#ROOT.gStyle.SetErrorY(0)

ROOT.gStyle.SetTitleStyle(0)
ROOT.gStyle.SetTitleAlign(13) ## coord in top left
ROOT.gStyle.SetTitleX(0.)
ROOT.gStyle.SetTitleY(1.)
ROOT.gStyle.SetTitleW(1)
ROOT.gStyle.SetTitleH(0.058)
ROOT.gStyle.SetTitleBorderSize(0)

ROOT.gStyle.SetPadLeftMargin(0.126)
ROOT.gStyle.SetPadRightMargin(0.10)
ROOT.gStyle.SetPadTopMargin(0.06)
ROOT.gStyle.SetPadBottomMargin(0.13)

ROOT.gStyle.SetMarkerStyle(1)


xmin=0
xmax=60
xbins=30
BINM=22
offsetLUT = {}
#binLow = [0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,12.0,14.0,16.0,18.0,20.0,24.0,28.0,32.0,36.0,42.0,50.0,60.0]
binLow = [0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,12.0,14.0,16.0,18.0,20.0,24.0,28.0,32.0,36.0,42.0,50.0]
ptbins = np.asarray(binLow)
	
def gethist1D(chain, den, todraw, x_bins):
	
    xBins = int(x_bins[1:-1].split(',')[0])
    xminBin = float(x_bins[1:-1].split(',')[1])
    xmaxBin = float(x_bins[1:-1].split(',')[2])
    h1 = ROOT.TH1F("h1","h1",xBins,xminBin,xmaxBin)
    chain.Draw("fabs(%s) >> h1"%todraw,den)
    #print "gethist1D, den ",den
    #h1.Print("ALL")
    return h1
		



def draw2Dplots_1(ch, xaxis, yaxis, x_bins, y_bins, xtitle, ytitle,cuts, text, picname):

    xBins = int(x_bins[1:-1].split(',')[0])
    xminBin = float(x_bins[1:-1].split(',')[1])
    xmaxBin = float(x_bins[1:-1].split(',')[2])
    yBins = int(y_bins[1:-1].split(',')[0])
    yminBin = float(y_bins[1:-1].split(',')[1])
    ymaxBin = float(y_bins[1:-1].split(',')[2])

    todrawb0 = "%s"%yaxis+":"+"%s>>b0"%xaxis
    
    c0 = ROOT.TCanvas("c0","c0")
    c0.SetGridx()
    c0.SetGridy()
    c0.SetTickx()
    c0.SetTicky()
    b0 = ROOT.TH2F("b0","b0",xBins,xminBin,xmaxBin,yBins,yminBin,ymaxBin)
    b0.SetTitle("#scale[1.4]{#font[61]{CMS}} #font[52]{preliminary}"+"  "*15+"2018, RunD")
    #b0.SetTitle("%s Vs %s,%s"%(ytitle0, xtitle, st_title)) 
    #b1.SetTitleFont(62)
    b0.SetTitleSize(0.05)
    b0.GetXaxis().SetTitle("%s"%xtitle)
    b0.GetYaxis().SetTitle("%s"%ytitle)
    b0.GetXaxis().SetTitleSize(.05)
    b0.GetYaxis().SetTitleSize(.05)
    #b1.SetMaximum(30)
    b0.SetStats(0)
    print "todraw ",todrawb0, " cut ",cuts
    #hasxy = "&& fabs(%s)>0 && fabs(%s)>0"%(xaxis, yaxis0)
    drawoption = "colz"
    if xBins < 20 and yBins < 20:
        drawoption = "colztext"
    ch.Draw(todrawb0, cuts, drawoption)
    diag, off_diag_1, off_diag_m1 = 0., 0., 0.
    for iX in range(1, xBins):
        for iY in range(1, yBins):
            binCont = b0.GetBinContent(iX, iY)
            if binCont > 0:
                if( abs(iX-iY)<=1 ):
                    diag += binCont
                elif( abs(iX-iY)>1 and (iX==1 or iY==1) ):
                    off_diag_1 += binCont
                else:
                    off_diag_m1 += binCont
    num = ufloat(off_diag_m1+off_diag_1, sqrt(off_diag_m1+off_diag_1))
    den = ufloat(diag+off_diag_1+off_diag_m1, sqrt(diag+off_diag_1+off_diag_m1))
    #myerr = sqrt( (pow(num,2)*(num+den)) / (pow(den,3)) ) # Poisson not good for small num
    #myerr = (1./den) * sqrt(num*(1.-num/den))
    tex0 = ROOT.TLatex(0.2,.76,"%s"%("Fraction off-diagonal: " + str(format((num)/(den)*100,'.3f')) + "%"))
    tex0.SetTextSize(0.03)
    tex0.SetTextFont(62)
    tex0.SetNDC()
    tex0.Draw("same")
    num = ufloat(off_diag_1, sqrt(off_diag_1))
    #myerr = (1./den) * sqrt(num*(1.-num/den))
    tex0a = ROOT.TLatex(0.2,.66,"%s"%("Fraction off-diagonal (zeros): " + str(format((num)/(den)*100,'.3f')) + "%"))
    tex0a.SetTextSize(0.03)
    tex0a.SetTextFont(62)
    tex0a.SetNDC()
    tex0a.Draw("same")
    num = ufloat(off_diag_m1, sqrt(off_diag_m1))
    #myerr = (1./den) * sqrt(num*(1.-num/den))
    tex0b = ROOT.TLatex(0.2,.56,"%s"%("Fraction off-diagonal (not zeros): " + str(format((num)/(den)*100,'.3f')) + "%"))
    tex0b.SetTextSize(0.03)
    tex0b.SetTextFont(62)
    tex0b.SetNDC()
    tex0b.Draw("same")
    tex1 = ROOT.TLatex(0.2,.86,"%s"%(text))
    tex1.SetTextSize(0.05)
    tex1.SetTextFont(62)
    tex1.SetNDC()
    tex1.Draw("same")
    #c0.SaveAs("%s"%picname+".png")
    c0.SaveAs("%s"%picname+".pdf")
    c0.SaveAs("%s"%picname+".C")

def draw1D_compare(filelist, chname, h_names, nbin, bimMin, binMax, cuts, text, picname):

    c0 = ROOT.TCanvas("c0","c0")
    c0.SetGridx()
    c0.SetGridy()
    c0.SetTickx()
    c0.SetTicky()
    chs = [ROOT.TChain("lctreader/"+chname), ROOT.TChain("lctreader/"+chname)]
    chs[0].Add(filelist[0])
    chs[1].Add(filelist[1])

    for nH, this_h in enumerate(h_names):
        h0 = ROOT.TH1F("h0", 'h0', nbin[nH], bimMin[nH], binMax[nH])
        chs[0].Draw(this_h+"_data>>h0",cuts)
        h1 = ROOT.TH1F("h1", 'h1', nbin[nH], bimMin[nH], binMax[nH])
        chs[0].Draw(this_h+"_emul>>h1", cuts)
        h2 = ROOT.TH1F("h2", 'h2', nbin[nH], bimMin[nH], binMax[nH])
        chs[1].Draw(this_h+"_emul>>h2", cuts)
        if h0 > h1 and h0 > h2:
            h_max = h0.GetMaximum()
        elif h1 > h0 and h1 > h2:
            h_max = h1.GetMaximum()
        elif h2 > h0 and h2 > h1:
            h_max = h2.GetMaximum()
        h0.Draw()
        h0.GetXaxis().SetTitle(this_h)
        h0.SetTitle("")
        h0.GetYaxis().SetLimits(h0.GetMinimum(), h_max*(1.1))
        h1.Draw("same")
        h1.SetLineColor(ROOT.kRed)
        h2.Draw("same")
        h2.SetLineColor(ROOT.kGreen+2)
        tex = ROOT.TLatex(0.2,.86,"%s"%(text))
        tex.SetTextSize(0.05)
        tex.SetTextFont(62)
        tex.SetNDC()
        tex.Draw("same")
        legend = ROOT.TLegend(0.65,0.8,0.85,0.9)
        legend.SetFillColor(ROOT.kWhite)
        legend.AddEntry(h0, "SHLC ON, data", "l")
        legend.AddEntry(h1, "SLHC ON, emul", "l")
        legend.AddEntry(h2, "SLHC OFF, emul", "l")
        legend.Draw("same")
        c0.SaveAs("%s"%picname + this_h + ".pdf")

#    xBins = int(x_bins[1:-1].split(',')[0])
#    xminBin = float(x_bins[1:-1].split(',')[1])
#    xmaxBin = float(x_bins[1:-1].split(',')[2])
##    tfilelist = []
##    for f in filelist:
##        tfilelist.append(ROOT.TFile(f, "READ"))
#    color = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen+2,ROOT.kMagenta+2, ROOT.kCyan+2]
#    maker = [20,21,22,23,33]
#    title = "#scale[1.4]{#font[61]{CMS}} #font[52]{ Simulation preliminary}"+"  "*15
#    hs1 = ROOT.THStack("hs1","%s"%title)
#    hs2 = ROOT.THStack("hs2","%s"%title)
#    legend = ROOT.TLegend(0.15,0.55,0.5,0.7)
#    legend.SetFillColor(ROOT.kWhite)
#    
#    i=0
#    meanlist = []
#    for ch in chs:
#        #tfilelist[i].cd()
#        print "todraw ","%s>>hist%d"%(xaxis_list[i], i)," cut ",cuts[i]
#        hist = ROOT.TH1F("hist%d"%i,"hist%d"%i, xBins, xminBin, xmaxBin)
#        ch.Draw("%s>>hist%d"%(xaxis_list[i], i),cuts[i])
#        ROOT.SetOwnership(hist, False)
#        hist.SetLineColor(color[i])
#        hist.SetLineWidth(2)
#        hist.Sumw2()
#        hs1.Add(hist)
#        hs2.Add(hist.Scale(1.0/hist.Integral()))
#        mean = hist.GetMean()
#        meanlist.append(mean)
#        rms = hist.GetRMS()
#        #legend.AddEntry(hist, "%s, Mean: %.4f, RMS: %.4f"%(legs[i], mean, rms),"l")
#        legend.AddEntry(hist, "%s, Mean: %.4f"%(legs[i], mean),"l")
#        i +=1
#    c0 = ROOT.TCanvas("c0","c0")
#    c0.SetGridx()
#    c0.SetGridy()
#    c0.SetTickx()
#    c0.SetTicky()
#    c0.SetLogy()
#    hs1.SetMinimum(.001)
#    hs1.Draw("nostacke") 
#    hs1.GetHistogram().GetXaxis().SetTitle("%s"%xtitle)
#    hs1.GetHistogram().GetXaxis().SetTitleSize(.05)
#    hs1.GetHistogram().GetYaxis().SetTitle("Normalized to unity")
#    hs1.GetHistogram().GetYaxis().SetTitleSize(.05)
#    legend.Draw("same")
#    tex1 = ROOT.TLatex(0.2,.8,"%s"%(text))
#    tex1.SetTextSize(0.05)
#    tex1.SetTextFont(62)
#    tex1.SetNDC()
#    tex1.Draw("same")
#    c0.SaveAs("%s"%picname+".C")
#    c0.SaveAs("%s"%picname+".pdf")
#    return meanlist
#    """
#    c1 = ROOT.TCanvas("c1","c1")
#    c1.SetGridx()
#    c1.SetGridy()
#    c1.SetTickx()
#    c1.SetTicky()
#    hs2.Draw("nostack") 
#    hs2.GetHistogram().GetXaxis().SetTitle("%s"%xtitle)
#    hs2.GetHistogram().GetYaxis().SetTitle("Normalized to unity")
#    legend.Draw("same")
#    tex1.SetNDC()
#    tex1.Draw("same")
#    c1.SaveAs("%s"%picname+"_normalized.png")
#    c1.SaveAs("%s"%picname+"_normalized.C")
#    """
#######################################################
cscstations = [ [0,0], 
                [1,1], [1,2], [1,3],[1,4],
                [2,1], [2,2],
                [3,1], [3,2],
                [4,1], [4,2],]
chambernames = ["all",
		"ME1/b","ME1/2","ME1/3","ME1/a",
		"ME2/1","ME2/2",
		"ME3/1","ME3/2",
		"ME4/1","ME4/2",]
allvars = ["quality","bend","pattern","key_WG","key_hs", "bx", "totStubs", "trknmb"]
xbinsall = ["(17,-1.5,15.5)","(3,-1.5,1.5)","(13,-1.5,11.5)","(122,-1.5,120.5)","(227,-1.5,225.5)", "(17,-1.5,15.5)", "(7, -0.5, 6.5)", "(4,-1.5, 2.5)"]
bx_bins = "(16, 0.5,16.5)"


xtitle = "timing of LCTs, BX"
xaxis = "bx"
xaxis_list = [xaxis, xaxis]

def compareDataAndEmulation(rootfiles, outputdir):
    if len(rootfiles)==1 :
        rootfile = rootfiles[0]
        for chname in ['alcttree','clcttree','lcttree']:
            obj = chname[:-4]
            ch = ROOT.TChain("lctreader/"+chname)
            ch.Add(rootfile)
            for ivar, var in enumerate(allvars):
                x_bins = xbinsall[ivar]
                xaxis = var+"_data"; yaxis = var+"_emul"
                xtitle = obj+","+var +", Data"
                ytitle = obj+","+var +", Re-emulation"
                if var == "bx":
                    yaxis = "bx_corr_emul"
                    ytitle = obj+",converted bx"+", Re-emulation"
                    if chname == 'alcttree':
                        x_bins = "(10, -1.5, 8.5)"
                    elif chname == 'clcttree':
                        x_bins = "(6, -1.5, 4.5)"
                    elif chname == "lcttree":
                        x_bins = "(4, -1.5, 2.5)"

                if var == "quality" and (chname == 'alcttree' or chname == 'clcttree'):
                    x_bins = "(8,-1.5, 6.5)"
                text = "Data Vs Re-emulation"
                #print "text ",text," xaxis ",xaxis," yaxis ",yaxis," cuts ",cuts
                picname = os.path.join(outputdir, obj+"_"+var+"_data_reemulation")
                cuts = "(bx_corr_emul>=0 || bx_data>=0) && !(station==1 && (ring==1 || ring==4))"
                draw2Dplots_1(ch, xaxis, yaxis, x_bins, x_bins, xtitle, ytitle, cuts, text, picname+"_noMEpm11")
                cuts = "(bx_corr_emul>=0 || bx_data>=0) && (endcap==1 && station==1 && (ring==1 || ring==4) && chamber==9)"
                draw2Dplots_1(ch, xaxis, yaxis, x_bins, x_bins, xtitle, ytitle, cuts, text, picname+"_ME119")
                cuts = "(bx_corr_emul>=0 || bx_data>=0) && (endcap==1 && station==1 && (ring==1 || ring==4) && chamber!=9)"
                draw2Dplots_1(ch, xaxis, yaxis, x_bins, x_bins, xtitle, ytitle, cuts, text, picname+"_ME11no9")
                for ichambertype in range(1, len(cscstations)):
                    chambername = chambernames[ichambertype]
                    st = cscstations[ichambertype][0]
                    ring = cscstations[ichambertype][1]
                    if ring == 4:
                        continue
                    picname = os.path.join(outputdir, obj+"_"+var+"_data_reemulation_st%d_ring%d"%(st, ring))
                    if ichambertype == 1:
                        chambername = "ME1/1"
                        #for k in range(1, 37):
                        #    text_pme11 = "Data Vs Re-emulation, p"+chambername+", chamber%d"%k
                        #    picname_pme11 = os.path.join(outputdir, obj+"_"+var+"_data_reemulation_st%d_ring%d_chamber%d_endcap1"%(st, ring, k))
                        #    cuts_pme11 = cuts+" && "+cuts_ch+" && chamber ==%d && endcap==1"%k
                        #    draw2Dplots_1(ch, xaxis, yaxis, x_bins, x_bins, xtitle, ytitle, cuts_pme11, text_pme11, picname_pme11)
                        #    text_mme11 = "Data Vs Re-emulation, m"+chambername+", chamber%d"%k
                        #    picname_mme11 = os.path.join(outputdir, obj+"_"+var+"_data_reemulation_st%d_ring%d_chamber%d_endcap2"%(st, ring, k))
                        #    cuts_mme11 = cuts+" && "+cuts_ch+" && chamber ==%d && endcap==2"%k
                        #    draw2Dplots_1(ch, xaxis, yaxis, x_bins, x_bins, xtitle, ytitle, cuts_mme11, text_mme11, picname_mme11)
                    text = "Data Vs Re-emulation, "+chambername
                    cuts = "(bx_corr_emul>=0 || bx_data>=0)"
                    cuts_ch = "station == %d && ring ==%d "%(st, ring)
                    draw2Dplots_1(ch, xaxis, yaxis, x_bins, x_bins, xtitle, ytitle,cuts+" && "+cuts_ch, text, picname)
    if len(rootfiles)==2 :
        for chname in ['alcttree','clcttree','lcttree']:
            obj = chname[:-4]
            #!for ivar, var in enumerate(allvars):
            #!    x_bins = xbinsall[ivar]
            #!    xaxis = var
            #!    xtitle = obj + "," + var
            #!    if var == "bx":
            #!        if chname == 'alcttree':
            #!            x_bins = "(10, -1.5, 8.5)"
            #!        elif chname == 'clcttree':
            #!            x_bins = "(6, -1.5, 4.5)"
            #!        elif chname == "lcttree":
            #!            x_bins = "(4, -1.5, 2.5)"

            #!    if var == "quality" and (chname == 'alcttree' or chname == 'clcttree'):
            #!        x_bins = "(8,-1.5, 6.5)"
            picname = os.path.join(outputdir, obj + "_")
            h_names = ['totStubs','nStub','quality','bend','bx','fullbx','key_WG','key_hs']
            nbin    = [7,  9,  10,   7,  25, 17, 81, 251]
            bimMin  = [-1.5,-4.5, -1.5,  -3.5, -12.5, -8.5 , -1, -1]
            binMax  = [5.5,  4.5,  8.5,   3.5,  12.5,  8.5,  80,  250]
            cuts = "(bx_corr_emul>=0 || bx_data>=0) && !(station==1 && (ring==1 || ring==4))"
            text = obj + ', ' + 'noME+-1/1'
            draw1D_compare(rootfiles, chname, h_names, nbin, bimMin, binMax, cuts, text, picname+"noMEpm11")
            cuts = "(bx_corr_emul>=0 || bx_data>=0) && (endcap==1 && station==1 && (ring==1 || ring==4) && chamber==9)"
            text = obj + ', ' + 'ME1/1/9'
            draw1D_compare(rootfiles, chname, h_names, nbin, bimMin, binMax, cuts, text, picname+"ME119")
            cuts = "(bx_corr_emul>=0 || bx_data>=0) && (endcap==1 && station==1 && (ring==1 || ring==4) && chamber!=9)"
            text = obj + ', ' + 'ME1/1/no9'
            draw1D_compare(rootfiles, chname, h_names, nbin, bimMin, binMax, cuts, text, picname+"ME11no9")
#                text = "Data"
#                picname = os.path.join(outputdir, obj+"_"+var+"_data_reemulation")
#                cuts = "(bx_corr_emul>=0 || bx_data>=0) && !((endcap==1 || endcap==2 ) && station==1 && (ring==1 || ring==4))"
#                draw2Dplots_1(ch, xaxis, yaxis, x_bins, x_bins, xtitle, ytitle, cuts, text, picname+"_noME11")
#                cuts = "(bx_corr_emul>=0 || bx_data>=0) && (endcap==1 && station==1 && (ring==1 || ring==4) && chamber==9)"
#                draw2Dplots_1(ch, xaxis, yaxis, x_bins, x_bins, xtitle, ytitle, cuts, text, picname+"_ME119")
#                cuts = "(bx_corr_emul>=0 || bx_data>=0) && (endcap==1 && station==1 && (ring==1 || ring==4) && chamber!=9)"
#                draw2Dplots_1(ch, xaxis, yaxis, x_bins, x_bins, xtitle, ytitle, cuts, text, picname+"_ME11no9")
#                for ichambertype in range(1, len(cscstations)):
#                    chambername = chambernames[ichambertype]
#                    st = cscstations[ichambertype][0]
#                    ring = cscstations[ichambertype][1]
#                    if ring == 4:
#                        continue
#                    picname = os.path.join(outputdir, obj+"_"+var+"_data_reemulation_st%d_ring%d"%(st, ring))
#                    if ichambertype == 1:
#                        chambername = "ME1/1"
#                        #for k in range(1, 37):
#                        #    text_pme11 = "Data Vs Re-emulation, p"+chambername+", chamber%d"%k
#                        #    picname_pme11 = os.path.join(outputdir, obj+"_"+var+"_data_reemulation_st%d_ring%d_chamber%d_endcap1"%(st, ring, k))
#                        #    cuts_pme11 = cuts+" && "+cuts_ch+" && chamber ==%d && endcap==1"%k
#                        #    draw2Dplots_1(ch, xaxis, yaxis, x_bins, x_bins, xtitle, ytitle, cuts_pme11, text_pme11, picname_pme11)
#                        #    text_mme11 = "Data Vs Re-emulation, m"+chambername+", chamber%d"%k
#                        #    picname_mme11 = os.path.join(outputdir, obj+"_"+var+"_data_reemulation_st%d_ring%d_chamber%d_endcap2"%(st, ring, k))
#                        #    cuts_mme11 = cuts+" && "+cuts_ch+" && chamber ==%d && endcap==2"%k
#                        #    draw2Dplots_1(ch, xaxis, yaxis, x_bins, x_bins, xtitle, ytitle, cuts_mme11, text_mme11, picname_mme11)
#                    text = "Data Vs Re-emulation, "+chambername
#                    cuts = "(bx_corr_emul>=0 || bx_data>=0)"
#                    cuts_ch = "station == %d && ring ==%d "%(st, ring)
#                    draw2Dplots_1(ch, xaxis, yaxis, x_bins, x_bins, xtitle, ytitle,cuts+" && "+cuts_ch, text, picname)

#rootfileON = "TPEHists_SLHCOn_run321710.root"
rootfileON = "TPEHists_svOn.root"
outputdir1 = "data_reemulation_321710_SLHCOn/"
os.system("mkdir -p "+outputdir1)
#compareDataAndEmulation([rootfileON], outputdir1)

#rootfileOFF = "TPEHists_SLHCOff_run321710.root"
rootfileOFF = "TPEHists_svOff.root"
outputdir2 = "data_reemulation_321710_SLHCOff/"
os.system("mkdir -p "+outputdir2)
#compareDataAndEmulation([rootfileOFF], outputdir2)

outputdir3 = "data_reemulation_321710_SLHCOff_On_1D/"
os.system("mkdir -p "+outputdir3)
compareDataAndEmulation([rootfileON,rootfileOFF], outputdir3)

# Overlap 1D plots
c0 = ROOT.TCanvas("c0","c0")
f_on = ROOT.TFile(rootfileON,"READ")
f_of = ROOT.TFile(rootfileOFF,"READ")
for h1D in ["ALCTs_per_event","ALCTs_per_chamber","ALCTs_per_CSCtype"]:
    f_on.cd()
    ALCTs_per_event_on = f_on.Get("lctreader/"+h1D)
    f_of.cd()
    ALCTs_per_event_of = f_of.Get("lctreader/"+h1D)
    ALCTs_per_event_on.Draw()
    ALCTs_per_event_of.Draw("same")
    c0.SaveAs(outputdir3 + "/" + h1D + ".png")

