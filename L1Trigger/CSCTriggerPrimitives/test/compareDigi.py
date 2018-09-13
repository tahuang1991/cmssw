import ROOT
import random
import os
import sys
import numpy as np
import pandas as pd
import array
from math import *
from uncertainties import ufloat
import Useful_func as uf
import matplotlib.pyplot as plt

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetStatW(0.07)
ROOT.gStyle.SetStatH(0.06)

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
    c0.SetBatch(kTRUE);
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
    drawoption = "goffcolz"
    if xBins < 20 and yBins < 20:
        drawoption = "colztextgoff"
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
    if num>0 and den>0:
        #myerr = sqrt( (pow(num,2)*(num+den)) / (pow(den,3)) ) # Poisson not good for small num
        #myerr = (1./den) * sqrt(num*(1.-num/den))
        #tex0 = ROOT.TLatex(0.2,.76,"%s"%("Fraction off-diagonal: " + str(format((num)/(den)*100,'.3f')) + "%"))
        tex0 = ROOT.TLatex(0.2,.76,"Fraction off-diagonal: " + str('{:.3f}'.format(((num)/(den)*100).nominal_value)) + "% +- " + str('{:.3f}'.format(((num)/(den)*100).std_dev)) + "%")
        tex0.SetTextSize(0.03)
        tex0.SetTextFont(62)
        tex0.SetNDC()
        tex0.Draw("samegoff")
        num = ufloat(off_diag_1, sqrt(off_diag_1))
        tex0a = ROOT.TLatex(0.2,.66,"Fraction missing in emul. (zero): " + str('{:.3f}'.format(((num)/(den)*100).nominal_value)) + "% +- " + str('{:.3f}'.format(((num)/(den)*100).std_dev)) + "%")
        tex0a.SetTextSize(0.03)
        tex0a.SetTextFont(62)
        tex0a.SetNDC()
        tex0a.Draw("samegoff")
        num = ufloat(off_diag_m1, sqrt(off_diag_m1))
        tex0b = ROOT.TLatex(0.2,.56,"Fraction different in emul. (not zero): " + str('{:.3f}'.format(((num)/(den)*100).nominal_value)) + "% +- " + str('{:.3f}'.format(((num)/(den)*100).std_dev)) + "%")
        tex0b.SetTextSize(0.03)
        tex0b.SetTextFont(62)
        tex0b.SetNDC()
        tex0b.Draw("samegoff")
        tex1 = ROOT.TLatex(0.2,.86,"%s"%(text))
        tex1.SetTextSize(0.05)
        tex1.SetTextFont(62)
        tex1.SetNDC()
        tex1.Draw("samegoff")
    #c0.SaveAs("%s"%picname+".png")
    c0.SaveAs("%s"%picname+".pdf")
    c0.SaveAs("%s"%picname+".C")

def draw1D_compare(filelist, chname, h_names, nbin, bimMin, binMax, cuts, text, picname, check):

    c0 = ROOT.TCanvas("c0","c0")
    c0.SetGridx()
    c0.SetGridy()
    c0.SetTickx()
    c0.SetTicky()
    chs = [ROOT.TChain("lctreader/"+chname), ROOT.TChain("lctreader/"+chname)]
    chs[0].Add(filelist[0])
    chs[1].Add(filelist[1])

    print 'With the selection ', str(cuts)
    print "  Size in data in '", chname,"' is (in NEW/OLD emulator):", str(chs[0].GetEntries(cuts)),  str(chs[1].GetEntries(cuts))
    if chs[0].GetEntries(cuts) != chs[1].GetEntries(cuts):
        print ' ---- WARNING: DATA in NEW & OLD emulator have different sizes ----'
    for nH, this_h in enumerate(h_names):
        if check != "nocheck" and this_h in check and chname in check:
            print "Checking for differences..."
            for VartoCheck in ['quality','bx','fullbx','key_WG','key_hs']:
                Myindex = h_names.index(VartoCheck)
                h_diff_d1_e0 = ROOT.TH1F("h_diff_d1_e0", 'h_diff_d1_e0', nbin[Myindex], bimMin[Myindex], binMax[Myindex])
                diff_cuts = cuts + " & ( nStub_data==1 & nStub_emul==0 )"
                chs[0].Draw(VartoCheck+"_data>>h_diff_d1_e0", diff_cuts, '')
                h_diff_d1_e0.Draw('h')
                h_diff_d1_e0.GetXaxis().SetTitle(VartoCheck+"_data"); h_diff_d1_e0.SetTitle("")
                c0.SaveAs("%s"%picname + "_DIFF_D1E0_" + VartoCheck + ".pdf")

                h_diff_d2_e1 = ROOT.TH1F("h_diff_d2_e1", 'h_diff_d2_e1', nbin[Myindex], bimMin[Myindex], binMax[Myindex])
                diff_cuts = cuts + " & ( nStub_data==2 & nStub_emul==1 )"
                chs[0].Draw(VartoCheck+"_data>>h_diff_d2_e1", diff_cuts, '')
                h_diff_d2_e1.Draw('h')
                h_diff_d2_e1.GetXaxis().SetTitle(VartoCheck+"_data"); h_diff_d2_e1.SetTitle("")
                c0.SaveAs("%s"%picname + "_DIFF_D2E1_" + VartoCheck + ".pdf")

                h_diff_d1_e2 = ROOT.TH1F("h_diff_d1_e2", 'h_diff_d1_e2', nbin[Myindex], bimMin[Myindex], binMax[Myindex])
                diff_cuts = cuts + " & ( nStub_data==1 & nStub_emul==2 )"
                chs[0].Draw(VartoCheck+"_data>>h_diff_d1_e2", diff_cuts, '')
                h_diff_d1_e2.Draw('h')
                h_diff_d1_e2.GetXaxis().SetTitle(VartoCheck+"_data"); h_diff_d1_e2.SetTitle("")
                c0.SaveAs("%s"%picname + "_DIFF_D1E2_" + VartoCheck + ".pdf")
                del h_diff_d1_e0
                del h_diff_d2_e1
                del h_diff_d1_e2
        h0 = ROOT.TH1F("h0", 'h0_'+str(this_h) + '_' + str(chname) + '_' + str(text), nbin[nH], bimMin[nH], binMax[nH])
        chs[0].Draw(this_h+"_data>>h0",cuts,'')
        h1 = ROOT.TH1F("h1", 'h1_'+str(this_h) + '_' + str(chname) + '_' + str(text), nbin[nH], bimMin[nH], binMax[nH])
        chs[0].Draw(this_h+"_emul>>h1", cuts,'')
        h2 = ROOT.TH1F("h2", 'h2_'+str(this_h) + '_' + str(chname) + '_' + str(text), nbin[nH], bimMin[nH], binMax[nH])
        chs[1].Draw(this_h+"_emul>>h2", cuts,'')
        if h0 > h1 and h0 > h2:
            h_max = h0.GetMaximum()
        elif h1 > h0 and h1 > h2:
            h_max = h1.GetMaximum()
        elif h2 > h0 and h2 > h1:
            h_max = h2.GetMaximum()
        if h0.Integral() > 0:
            h0.Scale( 1./h0.Integral() )
        h0.Draw('h')
        h0.GetXaxis().SetTitle(this_h)
        h0.SetTitle("")
        h0.GetYaxis().SetLimits(h0.GetMinimum(), h_max*(1.1))
        if h1.Integral() > 0:
            h1.Scale( 1./h1.Integral() )
        h1.Draw("hsame")
        h1.SetLineColor(ROOT.kRed)
        if h2.Integral() > 0:
            h2.Scale( 1./h2.Integral() )
        h2.Draw("hsame")
        h2.SetLineColor(ROOT.kGreen+2)
        tex = ROOT.TLatex(0.2,.86,"%s"%(text))
        tex.SetTextSize(0.05)
        tex.SetTextFont(62)
        tex.SetNDC()
        tex.Draw("same")
        x1, y1, x2, y2 = 0.65, 0.8, 0.85, 0.9
        if this_h == 'quality':
           x1, y1, x2, y2 = 0.65, 0.4, 0.85, 0.5
        legend = ROOT.TLegend(x1,y1,x2,y2)
        legend.SetFillColor(ROOT.kWhite)
        legend.AddEntry(h0, "DATA", "l")
        legend.AddEntry(h1, "NEW emulatoatorr", "l")
        legend.AddEntry(h2, "STD emulator", "l")
        legend.Draw("same")
        c0.SaveAs("%s"%picname + this_h + ".pdf")
        del h0
        del h1
        del h2

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
                picname = os.path.join(outputdir, obj+"_"+var+"_data_reemulation")
                cuts = "(bx_corr_emul>=0 || bx_data>=0) && !(station==1 && (ring==1 || ring==4))"
                draw2Dplots_1(ch, xaxis, yaxis, x_bins, x_bins, xtitle, ytitle, cuts, text, picname+"_noMEpm11")
                cuts = "(bx_corr_emul>=0 || bx_data>=0) && (endcap==1 && station==1 && (ring==1 || ring==4) && chamber==9)"
                draw2Dplots_1(ch, xaxis, yaxis, x_bins, x_bins, xtitle, ytitle, cuts, text, picname+"_ME119")
                cuts = "(bx_corr_emul>=0 || bx_data>=0) && (station==1 && (ring==1 || ring==4) && (chamber!=9 && chamber!=11))"
                draw2Dplots_1(ch, xaxis, yaxis, x_bins, x_bins, xtitle, ytitle, cuts, text, picname+"_ME11no911")
                for ichambertype in range(1, len(cscstations)):
                    chambername = chambernames[ichambertype]
                    st = cscstations[ichambertype][0]
                    ring = cscstations[ichambertype][1]
                    if ring == 4:
                        continue
                    picname = os.path.join(outputdir, obj+"_"+var+"_data_reemulation_st%d_ring%d"%(st, ring))
                    if ichambertype == 1:
                        chambername = "ME1/1"
                    text = "Data Vs Re-emulation, "+chambername
                    cuts = "(bx_corr_emul>=0 || bx_data>=0)"
                    cuts_ch = "station == %d && ring ==%d "%(st, ring)
                    draw2Dplots_1(ch, xaxis, yaxis, x_bins, x_bins, xtitle, ytitle,cuts+" && "+cuts_ch, text, picname)
    if len(rootfiles)==2 :
        for chname in ['alcttree','clcttree','lcttree']:
            obj = chname[:-4]
            picname = os.path.join(outputdir, obj + "_")
            h_names = ['nStub','quality','bx','fullbx','key_WG','key_hs']
            nbin    = [9,    10,   25, 17, 81, 251]
            bimMin  = [-4.5, -1.5, -12.5, -8.5 , -1, -1]
            binMax  = [4.5,  8.5,  12.5,  8.5,  80,  250]
            cuts = "(bx_corr_emul>=0 || bx_data>=0) && !(station==1 && (ring==1 || ring==4))"
            text = obj + ', ' + 'noME+-1/1'
            draw1D_compare(rootfiles, chname, h_names, nbin, bimMin, binMax, cuts, text, picname+"noMEpm11","nocheck")
            cuts = "(bx_corr_emul>=0 || bx_data>=0) && (endcap==1 && station==1 && (ring==1 || ring==4) && chamber==9)"
            text = obj + ', ' + 'ME1/1/9'
            draw1D_compare(rootfiles, chname, h_names, nbin, bimMin, binMax, cuts, text, picname+"ME119","check_clcttree_nStub") 
            cuts = "(bx_corr_emul>=0 || bx_data>=0) && (station==1 && (ring==1 || ring==4) && (chamber!=9 && chamber!=11))"
            text = obj + ', ' + 'ME1/1/no911'
            draw1D_compare(rootfiles, chname, h_names, nbin, bimMin, binMax, cuts, text, picname+"ME11no911","nocheck")

#rootfileON = "TPEHists_SLHCOn_run321710.root"
rootfileON = "Send_322118_ON/outTOT.root"
outputdir1 = "data_reemulation_322118_SLHCOn/"
#outputdir1 = "data_reemulation_321710_SLHCOn/"
os.system("mkdir -p "+outputdir1)
#compareDataAndEmulation([rootfileON], outputdir1)

#rootfileOFF = "TPEHists_SLHCOff_run321710.root"
rootfileOFF = "Send_322118_OFF/outTOT.root"
outputdir2 = "data_reemulation_322118_SLHCOff/"
#outputdir2 = "data_reemulation_321710_SLHCOff/"
os.system("mkdir -p "+outputdir2)
#compareDataAndEmulation([rootfileOFF], outputdir2)

outputdir3 = "data_reemulation_322118_SLHCOff_On_1D/"
#outputdir3 = "data_reemulation_321710_SLHCOff_On_1D/"
os.system("mkdir -p "+outputdir3)
os.system("mkdir -p "+outputdir3+'/csv/')
compareDataAndEmulation([rootfileON,rootfileOFF], outputdir3)

### Using Pandas
##print "Creating Dataframes"
##treename = 'lctreader/alcttree'
##df_ON_AL = uf.root2panda(rootfileON, treename)
##df_ON_AL.to_csv(outputdir3 + '/csv/df_ON_AL.csv')
##treename = 'lctreader/clcttree'
##df_ON_CL = uf.root2panda(rootfileON, treename)
##df_ON_CL.to_csv(outputdir3 + '/csv/df_ON_CL.csv')
##treename = 'lctreader/lcttree'
##df_ON_CT = uf.root2panda(rootfileON, treename)
##df_ON_CT.to_csv(outputdir3 + '/csv/df_ON_CT.csv')
##treename = 'lctreader/alcttree'
##df_OF_AL = uf.root2panda(rootfileOFF, treename)
##df_OF_AL.to_csv(outputdir3 + '/csv/df_OF_AL.csv')
##treename = 'lctreader/clcttree'
##df_OF_CL = uf.root2panda(rootfileOFF, treename)
##df_OF_CL.to_csv(outputdir3 + '/csv/df_OF_CL.csv')
##treename = 'lctreader/lcttree'
##df_OF_CT = uf.root2panda(rootfileOFF, treename)
##df_OF_CT.to_csv(outputdir3 + '/csv/df_OF_CT.csv')
##print "Creating Dataframes with subset of data"
###print df_ON_CL.columns.values
###['nEvents' 'nRUN' 'nEvent' 'totStubs_data' 'totStubs_emul' 'nStub_data'
### 'nStub_emul' 'chamber' 'ring' 'endcap' 'station' 'chambertype' 'has_data'
### 'has_emul' 'quality_data' 'quality_emul' 'npretrig' 'quality_pretrig'
### 'maxquality_pretrig' 'pattern_data' 'pattern_emul' 'pattern_pretrig'
### 'maxpattern_pretrig' 'bend_data' 'bx_data' 'fullbx_data' 'bend_emul'
### 'bx_emul' 'fullbx_emul' 'bend_pretrig' 'bx_pretrig' 'bx_corr_emul'
### 'key_WG_data' 'key_WG_emul' 'key_hs_data' 'key_hs_emul' 'key_hs_pretrig'
### 'trknmb_data' 'trknmb_emul' 'dphi_data' 'dphi_emul' 'eta_data' 'eta_emul'
### 'phi_data' 'phi_emul']
##
### Select events in CLCT where there is mismatch
##print "Creating Dataframes according to selection"
### Q)  ((df_ON_CL['bx_corr_emul']==0) | (df_ON_CL['bx_data']>=0)) ?
##basic_AL_cutON   = ( (df_ON_AL['bx_corr_emul']==0) | (df_ON_AL['bx_data']>=0) )
##basic_AL_cutOF   = ( (df_OF_AL['bx_corr_emul']==0) | (df_OF_AL['bx_data']>=0) )
##sel_AL_119ON     = ((basic_AL_cutON) & ((df_ON_AL['endcap']==1) & (df_ON_AL['station']==1) & ((df_ON_AL['ring']==1) | (df_ON_AL['ring']==4))) & (df_ON_AL['chamber']==9))
##sel_AL_119OF     = ((basic_AL_cutOF) & ((df_OF_AL['endcap']==1) & (df_OF_AL['station']==1) & ((df_OF_AL['ring']==1) | (df_OF_AL['ring']==4))) & (df_OF_AL['chamber']==9))
##sel_AL_11no911ON = ((basic_AL_cutON) & ((df_ON_AL['station']==1) & ((df_ON_AL['ring']==1) | (df_ON_AL['ring']==4))) & ((df_ON_AL['chamber']!=9) & (df_ON_AL['chamber']!=11) ) )
##sel_AL_11no911OF = ((basic_AL_cutOF) & ((df_OF_AL['station']==1) & ((df_OF_AL['ring']==1) | (df_OF_AL['ring']==4))) & ((df_OF_AL['chamber']!=9) & (df_OF_AL['chamber']!=11) ) )
##sel_AL_no11ON    = ((basic_AL_cutON) & ~((df_ON_AL['station']==1) & ((df_ON_AL['ring']==1) | (df_ON_AL['ring']==4))) )
##sel_AL_no11OF    = ((basic_AL_cutOF) & ~((df_OF_AL['station']==1) & ((df_OF_AL['ring']==1) | (df_OF_AL['ring']==4))) )
##basic_CL_cutON   = ( (df_ON_CL['bx_corr_emul']==0) | (df_ON_CL['bx_data']>=0) )
##basic_CL_cutOF   = ( (df_OF_CL['bx_corr_emul']==0) | (df_OF_CL['bx_data']>=0) )
##sel_CL_119ON     = ((basic_CL_cutON) & ((df_ON_CL['endcap']==1) & (df_ON_CL['station']==1) & ((df_ON_CL['ring']==1) | (df_ON_CL['ring']==4))) & (df_ON_CL['chamber']==9))
##sel_CL_119OF     = ((basic_CL_cutOF) & ((df_OF_CL['endcap']==1) & (df_OF_CL['station']==1) & ((df_OF_CL['ring']==1) | (df_OF_CL['ring']==4))) & (df_OF_CL['chamber']==9))
##sel_CL_11no911ON = ((basic_CL_cutON) & ((df_ON_CL['station']==1) & ((df_ON_CL['ring']==1) | (df_ON_CL['ring']==4))) & ((df_ON_CL['chamber']!=9) & (df_ON_CL['chamber']!=11) ) )
##sel_CL_11no911OF = ((basic_CL_cutOF) & ((df_OF_CL['station']==1) & ((df_OF_CL['ring']==1) | (df_OF_CL['ring']==4))) & ((df_OF_CL['chamber']!=9) & (df_OF_CL['chamber']!=11) ) )
##sel_CL_no11ON    = ((basic_CL_cutON) & ~((df_ON_CL['station']==1) & ((df_ON_CL['ring']==1) | (df_ON_CL['ring']==4))) )
##sel_CL_no11OF    = ((basic_CL_cutOF) & ~((df_OF_CL['station']==1) & ((df_OF_CL['ring']==1) | (df_OF_CL['ring']==4))) )
##basic_CT_cutON   = ( (df_ON_CT['bx_corr_emul']==0) | (df_ON_CT['bx_data']>=0) )
##basic_CT_cutOF   = ( (df_OF_CT['bx_corr_emul']==0) | (df_OF_CT['bx_data']>=0) )
##sel_CT_119ON     = ((basic_CT_cutON) & ((df_ON_CT['endcap']==1) & (df_ON_CT['station']==1) & ((df_ON_CT['ring']==1) | (df_ON_CT['ring']==4))) & (df_ON_CT['chamber']==9))
##sel_CT_119OF     = ((basic_CT_cutOF) & ((df_OF_CT['endcap']==1) & (df_OF_CT['station']==1) & ((df_OF_CT['ring']==1) | (df_OF_CT['ring']==4))) & (df_OF_CT['chamber']==9))
##sel_CT_11no911ON = ((basic_CT_cutON) & ((df_ON_CT['station']==1) & ((df_ON_CT['ring']==1) | (df_ON_CT['ring']==4))) & ((df_ON_CT['chamber']!=9) & (df_ON_CT['chamber']!=11) ) )
##sel_CT_11no911OF = ((basic_CT_cutOF) & ((df_OF_CT['station']==1) & ((df_OF_CT['ring']==1) | (df_OF_CT['ring']==4))) & ((df_OF_CT['chamber']!=9) & (df_OF_CT['chamber']!=11) ) )
##sel_CT_no11ON    = ((basic_CT_cutON) & ~((df_ON_CT['station']==1) & ((df_ON_CT['ring']==1) | (df_ON_CT['ring']==4))) )
##sel_CT_no11OF    = ((basic_CT_cutOF) & ~((df_OF_CT['station']==1) & ((df_OF_CT['ring']==1) | (df_OF_CT['ring']==4))) )
##df_ON_AL119       = df_ON_AL.loc[ sel_AL_119ON ]
##df_OF_AL119       = df_OF_AL.loc[ sel_AL_119OF ]
##df_ON_AL11no911   = df_ON_AL.loc[ sel_AL_11no911ON ]
##df_OF_AL11no911   = df_OF_AL.loc[ sel_AL_11no911OF ]
##df_ON_ALno11      = df_ON_AL.loc[ sel_AL_no11ON ]
##df_OF_ALno11      = df_OF_AL.loc[ sel_AL_no11OF ]
##df_ON_CL119       = df_ON_CL.loc[ sel_CL_119ON ]
##df_OF_CL119       = df_OF_CL.loc[ sel_CL_119OF ]
##df_ON_CL11no911   = df_ON_CL.loc[ sel_CL_11no911ON ]
##df_OF_CL11no911   = df_OF_CL.loc[ sel_CL_11no911OF ]
##df_ON_CLno11      = df_ON_CL.loc[ sel_CL_no11ON ]
##df_OF_CLno11      = df_OF_CL.loc[ sel_CL_no11OF ]
##df_ON_CT119       = df_ON_CT.loc[ sel_CT_119ON ]
##df_OF_CT119       = df_OF_CT.loc[ sel_CT_119OF ]
##df_ON_CT11no911   = df_ON_CT.loc[ sel_CT_11no911ON ]
##df_OF_CT11no911   = df_OF_CT.loc[ sel_CT_11no911OF ]
##df_ON_CTno11      = df_ON_CT.loc[ sel_CT_no11ON ]
##df_OF_CTno11      = df_OF_CT.loc[ sel_CT_no11OF ]
##
### 1D plots
##plt.ioff()
##h_names = ['nStub','quality','bx','fullbx','key_WG','key_hs']
##nbin    = [9,       10,      25,    17,   81, 251]
##bimMin  = [-4.5,    -1.5,   -12.5, -8.5 , -1, -1]
##binMax  = [4.5,     8.5,    12.5,  8.5,  80,  250]
##dfs = [ [df_ON_AL119, df_OF_AL119, df_ON_AL11no911, df_OF_AL11no911, df_ON_ALno11, df_OF_ALno11], \
##        [df_ON_CL119, df_OF_CL119, df_ON_CL11no911, df_OF_CL11no911, df_ON_CLno11, df_OF_CLno11], \
##        [df_ON_CT119, df_OF_CT119, df_ON_CT11no911, df_OF_CT11no911, df_ON_CTno11, df_OF_CTno11] ]
##df_name = ["alct","clct","lct"]
##
##print "1D plots:"
##for df_index, df in enumerate(dfs):
##  if df[0].shape[0] != df[1].shape[0] or df[2].shape[0] != df[3].shape[0] or df[4].shape[0] != df[5].shape[0]:
##    print "---- WARNING NEW/OLD emultor files have different size for data ----",  df[0].shape[0], "-", df[1].shape[0], "/", df[2].shape[0], "-", df[3].shape[0], "/", df[4].shape[0], "-", df[5].shape[0]
##  for index, name in enumerate(h_names):
##    print "  ", name
##    Varname = name + "_data"
##    plt.hist( df[0][Varname], bins=nbin[index], range=(bimMin[index],binMax[index]), edgecolor='blue', label='DATA', fill=False )
##    Varname = name + "_emul"
##    plt.hist( df[0][Varname], bins=nbin[index], range=(bimMin[index],binMax[index]), edgecolor='red', label='NEW emulator', fill=False )
##    plt.hist( df[1][Varname], bins=nbin[index], range=(bimMin[index],binMax[index]), edgecolor='green', label='OLD emulator', fill=False )
##    plt.legend(loc='best')
##    plt.xlabel(name); plt.grid(True)
##    plt.savefig(outputdir3 + "/" + df_name[df_index] + "_ME119" + name + "_pd.pdf")
##    plt.clf()
##    Varname = name + "_data"
##    plt.hist( df[2][Varname], bins=nbin[index], range=(bimMin[index],binMax[index]), edgecolor='blue', label='DATA', fill=False )
##    Varname = name + "_emul"
##    plt.hist( df[2][Varname], bins=nbin[index], range=(bimMin[index],binMax[index]), edgecolor='red', label='NEW emulator', fill=False )
##    plt.hist( df[3][Varname], bins=nbin[index], range=(bimMin[index],binMax[index]), edgecolor='green', label='OLD emulator', fill=False )
##    plt.legend(loc='best')
##    plt.xlabel(name); plt.grid(True)
##    plt.savefig(outputdir3 + "/" + df_name[df_index] + "_ME11no911" + name + "_pd.pdf")
##    plt.clf()
##    Varname = name + "_data"
##    plt.hist( df[4][Varname], bins=nbin[index], range=(bimMin[index],binMax[index]), edgecolor='blue', label='DATA', fill=False )
##    Varname = name + "_emul"
##    plt.hist( df[4][Varname], bins=nbin[index], range=(bimMin[index],binMax[index]), edgecolor='red', label='NEW emulator', fill=False )
##    plt.hist( df[5][Varname], bins=nbin[index], range=(bimMin[index],binMax[index]), edgecolor='green', label='OLD emulator', fill=False )
##    plt.legend(loc='best')
##    plt.xlabel(name); plt.grid(True)
##    plt.savefig(outputdir3 + "/" + df_name[df_index] + "_noMEpm11" + name + "_pd.pdf")
##    plt.clf()
##
### Check the special cases
##print "Studying special cases"
##df_ON_CL119_EMdifDA = df_ON_CL119.loc[ (df_ON_CL119['nStub_data']!=df_ON_CL119['nStub_emul']) ]
##num = float(df_ON_CL119_EMdifDA.shape[0])
##den = (df_ON_CL119.shape[0]+df_ON_CL119_EMdifDA.shape[0])
##print "CLCT: DATA-NEW_EMULATOR differs", "%.2f"%(num/den*100),"% of the times (", "%.2f"%(num), "/", "%.2f"%(den),")"
##df_ON_CL119_EM0_DA1 = df_ON_CL119.loc[ (df_ON_CL119['nStub_data']==1) & (df_ON_CL119['nStub_emul']==0) ]
##num = float(df_ON_CL119_EM0_DA1.shape[0])
##den = (df_ON_CL119.shape[0]+df_ON_CL119_EM0_DA1.shape[0])
##print "CLCT: DATA 1/NEW_EMULATOR 0: ", "%.2f"%(num/den*100),"% of the times (", "%.2f"%(num), "/", "%.2f"%(den),")"
##df_ON_CL119_EM1_DA2 = df_ON_CL119.loc[ (df_ON_CL119['nStub_data']==2) & (df_ON_CL119['nStub_emul']==1) ]
##num = float(df_ON_CL119_EM1_DA2.shape[0])
##den = (df_ON_CL119.shape[0]+df_ON_CL119_EM1_DA2.shape[0])
##print "CLCT: DATA 2/NEW_EMULATOR 1: ", "%.2f"%(num/den*100),"% of the times (", "%.2f"%(num), "/", "%.2f"%(den),")"
##df_ON_CL119_EM2_DA1 = df_ON_CL119.loc[ (df_ON_CL119['nStub_data']==1) & (df_ON_CL119['nStub_emul']==2) ]
##num = float(df_ON_CL119_EM2_DA1.shape[0])
##den = (df_ON_CL119.shape[0]+df_ON_CL119_EM2_DA1.shape[0])
##print "CLCT: DATA 1/NEW_EMULATOR 2: ", "%.2f"%(num/den*100),"% of the times (", "%.2f"%(num), "/", "%.2f"%(den),")"
##
### Focus on df_ON_CL119_EM0_DA1
##plt.hist( df_ON_CL119_EM0_DA1['key_WG_data'], 10, range=(0,50) )
##plt.savefig(outputdir3 + '/NewEM0_Data1_WG_data.png')
##plt.hist( df_ON_CL119_EM0_DA1['bx_data'], 24, range=(-12,12) )
##plt.savefig(outputdir3 + '/NewEM0_Data1_BX_data.png')
##plt.hist( df_ON_CL119_EM0_DA1['fullbx_data'], 16, range=(-8,8) )
##plt.savefig(outputdir3 + '/NewEM0_Data1_BXfull_data.png')
