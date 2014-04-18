#include <L1Trigger/CSCTriggerPrimitives/src/CSCMotherboardME21.h>
#include <FWCore/MessageLogger/interface/MessageLogger.h>
#include <DataFormats/MuonDetId/interface/CSCTriggerNumbering.h>
#include <L1Trigger/CSCCommonTrigger/interface/CSCTriggerGeometry.h>
#include <DataFormats/Math/interface/deltaPhi.h>
#include <DataFormats/Math/interface/normalizedPhi.h>
#include <Geometry/GEMGeometry/interface/GEMGeometry.h>
#include <Geometry/GEMGeometry/interface/GEMEtaPartitionSpecs.h>
#include <iomanip> 

const double CSCMotherboardME21::lut_wg_eta_odd[112][2] = {
{ 0,2.441},{ 1,2.435},{ 2,2.425},{ 3,2.414},{ 4,2.404},{ 5,2.394},{ 6,2.384},{ 7,2.374},
{ 8,2.365},{ 9,2.355},{10,2.346},{11,2.336},{12,2.327},{13,2.317},{14,2.308},{15,2.299},
{16,2.290},{17,2.281},{18,2.273},{19,2.264},{20,2.255},{21,2.247},{22,2.238},{23,2.230},
{24,2.221},{25,2.213},{26,2.205},{27,2.197},{28,2.189},{29,2.181},{30,2.173},{31,2.165},
{32,2.157},{33,2.149},{34,2.142},{35,2.134},{36,2.127},{37,2.119},{38,2.112},{39,2.104},
{40,2.097},{41,2.090},{42,2.083},{43,2.075},{44,2.070},{45,2.059},{46,2.054},{47,2.047},
{48,2.041},{49,2.034},{50,2.027},{51,2.020},{52,2.014},{53,2.007},{54,2.000},{55,1.994},
{56,1.988},{57,1.981},{58,1.975},{59,1.968},{60,1.962},{61,1.956},{62,1.950},{63,1.944},
{64,1.937},{65,1.931},{66,1.924},{67,1.916},{68,1.909},{69,1.902},{70,1.895},{71,1.888},
{72,1.881},{73,1.875},{74,1.868},{75,1.861},{76,1.854},{77,1.848},{78,1.841},{79,1.835},
{80,1.830},{81,1.820},{82,1.815},{83,1.809},{84,1.803},{85,1.796},{86,1.790},{87,1.784},
{88,1.778},{89,1.772},{90,1.766},{91,1.760},{92,1.754},{93,1.748},{94,1.742},{95,1.736},
{96,1.731},{97,1.725},{98,1.719},{99,1.714},{100,1.708},{101,1.702},{102,1.697},{103,1.691},
{104,1.686},{105,1.680},{106,1.675},{107,1.670},{108,1.664},{109,1.659},{110,1.654},{111,1.648},
};

const double CSCMotherboardME21::lut_wg_eta_even[112][2] = {
{ 0,2.412},{ 1,2.405},{ 2,2.395},{ 3,2.385},{ 4,2.375},{ 5,2.365},{ 6,2.355},{ 7,2.345},
{ 8,2.335},{ 9,2.325},{10,2.316},{11,2.306},{12,2.297},{13,2.288},{14,2.279},{15,2.270},
{16,2.261},{17,2.252},{18,2.243},{19,2.234},{20,2.226},{21,2.217},{22,2.209},{23,2.200},
{24,2.192},{25,2.184},{26,2.175},{27,2.167},{28,2.159},{29,2.151},{30,2.143},{31,2.135},
{32,2.128},{33,2.120},{34,2.112},{35,2.105},{36,2.097},{37,2.090},{38,2.082},{39,2.075},
{40,2.068},{41,2.060},{42,2.053},{43,2.046},{44,2.041},{45,2.030},{46,2.025},{47,2.018},
{48,2.011},{49,2.005},{50,1.998},{51,1.991},{52,1.985},{53,1.978},{54,1.971},{55,1.965},
{56,1.958},{57,1.952},{58,1.946},{59,1.939},{60,1.933},{61,1.927},{62,1.921},{63,1.915},
{64,1.909},{65,1.902},{66,1.895},{67,1.887},{68,1.880},{69,1.873},{70,1.866},{71,1.859},
{72,1.853},{73,1.846},{74,1.839},{75,1.832},{76,1.826},{77,1.819},{78,1.812},{79,1.806},
{80,1.801},{81,1.792},{82,1.787},{83,1.780},{84,1.774},{85,1.768},{86,1.762},{87,1.756},
{88,1.750},{89,1.744},{90,1.738},{91,1.732},{92,1.726},{93,1.720},{94,1.714},{95,1.708},
{96,1.702},{97,1.697},{98,1.691},{99,1.685},{100,1.680},{101,1.674},{102,1.669},{103,1.663},
{104,1.658},{105,1.652},{106,1.647},{107,1.642},{108,1.636},{109,1.631},{110,1.626},{111,1.621},
};

CSCMotherboardME21::CSCMotherboardME21(unsigned endcap, unsigned station,
                               unsigned sector, unsigned subsector,
                               unsigned chamber,
                               const edm::ParameterSet& conf) :
  CSCMotherboard(endcap, station, sector, subsector, chamber, conf)
{
  edm::ParameterSet commonParams = conf.getParameter<edm::ParameterSet>("commonParam");
  
  if (!isSLHC) edm::LogError("L1CSCTPEmulatorConfigError")
    << "+++ Upgrade CSCMotherboardME21 constructed while isSLHC is not set! +++\n";
  
  edm::ParameterSet alctParams = conf.getParameter<edm::ParameterSet>("alctSLHC");
  edm::ParameterSet clctParams = conf.getParameter<edm::ParameterSet>("clctSLHC");
  edm::ParameterSet tmbParams = conf.getParameter<edm::ParameterSet>("tmbSLHC");
  edm::ParameterSet me21tmbParams = tmbParams.getParameter<edm::ParameterSet>("me21ILT");

  // central bx for LCT is 6 for simulation
  lct_central_bx = tmbParams.getUntrackedParameter<int>("lctCentralBX", 6);

  // whether to not reuse CLCTs that were used by previous matching ALCTs
  // in ALCT-to-CLCT algorithm
  drop_used_clcts = tmbParams.getUntrackedParameter<bool>("tmbDropUsedClcts",true);

  //----------------------------------------------------------------------------------------//

  //       G E M  -  C S C   I N T E G R A T E D   L O C A L   A L G O R I T H M

  //----------------------------------------------------------------------------------------//

  // masterswitch
  runME21ILT_ = me21tmbParams.getUntrackedParameter<bool>("runME21ILT",false);

  max_me21_lcts = me21tmbParams.getUntrackedParameter<unsigned int>("maxme21lcts", 2);
  /// Do GEM matching?
  do_gem_matching = me21tmbParams.getUntrackedParameter<bool>("doGemMatching", false);
  
  /// GEM matching dphi and deta
  gem_match_delta_phi = me21tmbParams.getUntrackedParameter<double>("gemMatchDeltaPhiOdd", 0.0055);
  gem_match_delta_eta = me21tmbParams.getUntrackedParameter<double>("gemMatchDeltaEta", 0.08);

  /// delta BX for GEM pads matching
  gem_match_delta_bx = me21tmbParams.getUntrackedParameter<int>("gemMatchDeltaBX", 1);

  /// min eta of LCT for which we require GEM match (we don't throw out LCTs below this min eta)
  gem_match_min_eta = me21tmbParams.getUntrackedParameter<double>("gemMatchMinEta", 1.62);

  /// whether to throw out GEM-fiducial LCTs that have no gem match
  gem_clear_nomatch_lcts = me21tmbParams.getUntrackedParameter<bool>("gemClearNomatchLCTs", false);

  // central bx for LCT is 6 for simulation
  lct_central_bx = me21tmbParams.getUntrackedParameter<int>("lctCentralBX", 6);

  // debug gem matching
  debug_gem_matching = me21tmbParams.getUntrackedParameter<bool>("debugGemMatching", false);

  // print available pads
  print_available_pads = me21tmbParams.getUntrackedParameter<bool>("printAvailablePads", false);

  //  deltas used to construct GEM coincidence pads
  maxDeltaBXInCoPad_ = me21tmbParams.getUntrackedParameter<int>("maxDeltaBXInCoPad",1);
  maxDeltaRollInCoPad_ = me21tmbParams.getUntrackedParameter<int>("maxDeltaRollInCoPad",0);
  maxDeltaPadInCoPad_ = me21tmbParams.getUntrackedParameter<int>("maxDeltaPadInCoPad",0);

  //  deltas used to match to GEM pads
  maxDeltaBXPad_ = me21tmbParams.getUntrackedParameter<int>("maxDeltaBXPad",1);
  maxDeltaRollPad_ = me21tmbParams.getUntrackedParameter<int>("maxDeltaRollPad",0);
  maxDeltaPadPad_ = me21tmbParams.getUntrackedParameter<int>("maxDeltaPadPad",0);

  //  deltas used to match to GEM coincidence pads
  maxDeltaBXCoPad_ = me21tmbParams.getUntrackedParameter<int>("maxDeltaBXCoPad",1);
  maxDeltaRollCoPad_ = me21tmbParams.getUntrackedParameter<int>("maxDeltaRollCoPad",0);
  maxDeltaPadCoPad_ = me21tmbParams.getUntrackedParameter<int>("maxDeltaPadCoPad",0);

  // drop low quality stubs if they don't have GEMs
  dropLowQualityCLCTsNoGEMs_ = me21tmbParams.getUntrackedParameter<bool>("dropLowQualityCLCTsNoGEMs",false);
  dropLowQualityALCTsNoGEMs_ = me21tmbParams.getUntrackedParameter<bool>("dropLowQualityALCTsNoGEMs",false);

  // use only the central BX for GEM matching
  centralBXonlyGEM_ = me21tmbParams.getUntrackedParameter<bool>("centralBXonlyGEM",false);
  
  useOldLCTDataFormatALCTGEM_ = me21tmbParams.getUntrackedParameter<bool>("useOldLCTDataFormatALCTGEM",true);
  match_earliest_clct_me21_only_ = me21tmbParams.getUntrackedParameter<bool>("match_earliest_clct_me21_only",false);
  // build LCT from ALCT and GEM
  buildLCTfromALCTandGEM_ME21_ = me21tmbParams.getUntrackedParameter<bool>("buildLCTfromALCTandGEM",false);
  buildLCTfromCLCTandGEM_ME21_ = me21tmbParams.getUntrackedParameter<bool>("buildLCTfromCLCTandGEM",false);
}

CSCMotherboardME21::~CSCMotherboardME21() 
{
}

void CSCMotherboardME21::setConfigParameters(const CSCDBL1TPParameters* conf)
{
  alct->setConfigParameters(conf);
  clct->setConfigParameters(conf);
  // No config. parameters in DB for the TMB itself yet.
}

void CSCMotherboardME21::clear()
{
  CSCMotherboard::clear();

  for (int bx = 0; bx < MAX_LCT_BINS; bx++)
  {
    for (unsigned int mbx = 0; mbx < match_trig_window_size; mbx++)
      for (int i=0;i<2;i++)
        allLCTs[bx][mbx][i].clear();
  }
  cscWgToGemRollShort_.clear();
  cscWgToGemRollLong_.clear();
  gemPadToCscHs_.clear();
  cscHsToGemPad_.clear();
  padsShort_.clear();
  padsLong_.clear();
  coPadsShort_.clear();
  coPadsLong_.clear();
}

void
CSCMotherboardME21::run(const CSCWireDigiCollection* wiredc,
                    const CSCComparatorDigiCollection* compdc,
                    const GEMCSCPadDigiCollection* gemPads) 
{
  clear();

  if (!( alct and clct and runME21ILT_))
  {
    if (infoV >= 0) edm::LogError("L1CSCTPEmulatorSetupError")
      << "+++ run() called for non-existing ALCT/CLCT processor! +++ \n";
    return;
  }

  alct->run(wiredc); // run anodeLCT
  clct->run(compdc); // run cathodeLCT

  bool gemGeometryAvailable(false);
  if (gem_g != nullptr) {
    if (infoV >= 0) edm::LogInfo("L1CSCTPEmulatorSetupInfo")
      << "+++ run() called for GEM-CSC integrated trigger! +++ \n";
    gemGeometryAvailable = true;
  }

  // retrieve CSCChamber geometry                                                                                                                                       
  CSCTriggerGeomManager* geo_manager(CSCTriggerGeometry::get());
  const CSCChamber* cscChamber(geo_manager->chamber(theEndcap, theStation, theSector, theSubsector, theTrigChamber));
  const CSCDetId csc_id(cscChamber->id());

  if (runME21ILT_){
    
    // check for GE2/1 geometry
    if ((not gemGeometryAvailable) or (gemGeometryAvailable and (gem_g->stations()).size()==2)) {
      if (infoV >= 0) edm::LogError("L1CSCTPEmulatorSetupError")
        << "+++ run() called for GEM-CSC integrated trigger without valid GE21 geometry! +++ \n";
      return;
    }

    // trigger geometry
    const CSCLayer* keyLayer(cscChamber->layer(3));
    const CSCLayerGeometry* keyLayerGeometry(keyLayer->geometry());

    const bool isEven(csc_id.chamber()%2==0);
    const int region((theEndcap == 1) ? 1: -1);
    const GEMDetId gem_id_short(region, 1, 2, 1, csc_id.chamber(), 0);
    const GEMDetId gem_id_long(region, 1, 3, 1, csc_id.chamber(), 0);
    //    const GEMChamber* gemChamberShort(gem_g->chamber(gem_id_short));
    const GEMChamber* gemChamberLong(gem_g->chamber(gem_id_long));
    
    // LUT<roll,<etaMin,etaMax> >    
    gemPadToEtaLimitsShort_ = createGEMPadLUT(false);
    gemPadToEtaLimitsLong_ = createGEMPadLUT(true);

    bool debug(false);
    if (debug){
      if (gemPadToEtaLimitsShort_.size())
        for(auto p : gemPadToEtaLimitsShort_) {
          std::cout << "pad "<< p.first << " min eta " << (p.second).first << " max eta " << (p.second).second << std::endl;
        }
      if (gemPadToEtaLimitsLong_.size())
        for(auto p : gemPadToEtaLimitsLong_) {
          std::cout << "pad "<< p.first << " min eta " << (p.second).first << " max eta " << (p.second).second << std::endl;
        }
    }
    
    // loop on all wiregroups to create a LUT <WG,roll>
    const int numberOfWG(keyLayerGeometry->numberOfWireGroups());
    for (int i = 0; i< numberOfWG; ++i){
      auto eta(isEven ? lut_wg_eta_even[i][1] : lut_wg_eta_odd[i][1]); 
      cscWgToGemRollShort_[i] = assignGEMRoll(eta, true);
      cscWgToGemRollLong_[i] = assignGEMRoll(eta, false);
    }
    debug = false;
    if (debug){
	std::cout << "CSC DetId" << csc_id <<"  cscWgToGemRoll LUT "<< std::endl;
      for(auto p : cscWgToGemRollShort_) {
        std::cout << "WG "<< p.first << " GEM Rolls " << p.second << std::endl;
      }
      for(auto p : cscWgToGemRollLong_) {
        std::cout << "WG "<< p.first << " GEM Rolls " << p.second << std::endl;
      }

   }

    auto randRoll(gemChamberLong->etaPartition(2));
    auto nStrips(keyLayerGeometry->numberOfStrips());
    for (float i = 0; i< nStrips; i = i+0.5){
      const LocalPoint lpCSC(keyLayerGeometry->topology()->localPosition(i));
      const GlobalPoint gp(keyLayer->toGlobal(lpCSC));
      const LocalPoint lpGEM(randRoll->toLocal(gp));
      const int HS(i/0.5);
      const float pad(randRoll->pad(lpGEM));
      // HS are wrapped-around
      cscHsToGemPad_[HS] = std::make_pair(std::floor(pad),std::ceil(pad));
    }
    debug = false;
    if (debug){
      std::cout << "detId " << csc_id <<"   cscHsToGemPad LUT" << std::endl;
      for(auto p : cscHsToGemPad_) {
        std::cout << "CSC HS "<< p.first << " GEM Pad low " << (p.second).first << " GEM Pad high " << (p.second).second << std::endl;
      }
    }

    // pick any roll (from short or long superchamber)
    const int nGEMPads(randRoll->npads());
    for (int i = 0; i< nGEMPads; ++i){
      const LocalPoint lpGEM(randRoll->centreOfPad(i));
      const GlobalPoint gp(randRoll->toGlobal(lpGEM));
      const LocalPoint lpCSC(keyLayer->toLocal(gp));
      const float strip(keyLayerGeometry->strip(lpCSC));
      // HS are wrapped-around
      gemPadToCscHs_[i] = (int) (strip - 0.25)/0.5;
    }
    debug = false;
    if (debug){
      std::cout << "detId " << csc_id <<"  gemPadToCscHs LUT " <<std::endl;
      for(auto p : gemPadToCscHs_) {
        std::cout << "GEM Pad "<< p.first << " CSC HS : " << p.second << std::endl;
      }
    }
    
    // build coincidence pads
    std::auto_ptr<GEMCSCPadDigiCollection> pCoPads(new GEMCSCPadDigiCollection());
    buildCoincidencePads(gemPads, *pCoPads);
    
    // retrieve pads and copads in a certain BX window for this CSC 
    padsShort_ = retrieveGEMPads(gemPads, gem_id_short);
    padsLong_ = retrieveGEMPads(gemPads, gem_id_long);
    coPadsShort_ = retrieveGEMPads(pCoPads.get(), gem_id_short, true);
    coPadsLong_ = retrieveGEMPads(pCoPads.get(), gem_id_long, true); 
  }

//  return;

//  const bool hasPads(padsShort_.size()!=0 or padsLong_.size()!=0);
//  const bool hasCoPads(coPadsShort_.size()!=0 or coPadsLong_.size()!=0);
  const bool hasPads(padsLong_.size()!=0);
  const bool hasCoPads(coPadsLong_.size()!=0);

  int used_clct_mask[20];
  for (int c=0;c<20;++c) used_clct_mask[c]=0;

  // ALCT centric matching
  for (int bx_alct = 0; bx_alct < CSCAnodeLCTProcessor::MAX_ALCT_BINS; bx_alct++)
  {
    if (!alct->bestALCT[bx_alct].isValid()) continue;
    
      const int bx_clct_start(bx_alct - match_trig_window_size/2);
      const int bx_clct_stop(bx_alct + match_trig_window_size/2);
      const int bx_gem_start(bx_alct - maxDeltaBXCoPad_);
      const int bx_gem_stop(bx_alct + maxDeltaBXCoPad_);

      if (print_available_pads){ 
        std::cout << "========================================================================" << std::endl;
        std::cout << "ALCT-CLCT matching in ME2/1 chamber: " << cscChamber->id() << std::endl;
        std::cout << "------------------------------------------------------------------------" << std::endl;
        std::cout << "+++ Best ALCT Details: ";
        alct->bestALCT[bx_alct].print();
        std::cout << "+++ Second ALCT Details: ";
        alct->secondALCT[bx_alct].print();
        
      //  printGEMTriggerPads(bx_clct_start, bx_clct_stop, true);      
      //  printGEMTriggerPads(bx_clct_start, bx_clct_stop, true, true);      
        printGEMTriggerPads(bx_clct_start, bx_clct_stop, false);      
        printGEMTriggerPads(bx_clct_start, bx_clct_stop, false, true);      
        
        std::cout << "------------------------------------------------------------------------" << std::endl;
        std::cout << "Attempt ALCT-CLCT matching in ME2/1 in bx range: [" << bx_clct_start << "," << bx_clct_stop << "]" << std::endl;
      }
      
      // ALCT-to-CLCT matching
      int nSuccesFulMatches = 0;
      for (int bx_clct = bx_clct_start; bx_clct <= bx_clct_stop; bx_clct++)
      {
        if (bx_clct < 0 or bx_clct >= CSCCathodeLCTProcessor::MAX_CLCT_BINS) continue;
        if (drop_used_clcts and used_clct_mask[bx_clct]) continue;
        if (!clct->bestCLCT[bx_clct].isValid())  continue;
        int quality = clct->bestCLCT[bx_clct].getQuality(); 
	  //	  const int quality(clct->bestCLCT[bx_clct].getQuality());
          if (print_available_pads) std::cout << "++Valid ME21 CLCT: " << clct->bestCLCT[bx_clct] << std::endl;

	  	  if (runME21ILT_ and dropLowQualityCLCTsNoGEMs_ and quality < 4 and hasPads){
	               // pick the pad that corresponds 
	               auto matchingPads_long(matchingGEMPads(clct->bestCLCT[bx_clct], padsLong_[bx_clct], false, false));
	               //auto matchingPads_short(matchingGEMPads(clct->bestCLCT[bx_clct], padsShort_[bx_clct], true, false));
	              // int nFound(matchingPads_long.size()!=0 ? matchingPads_long.size() : matchingPads_short.size());
	              int nFound(matchingPads_long.size());
		       const bool clctInEdge(clct->bestCLCT[bx_clct].getKeyStrip() < 5 or clct->bestCLCT[bx_clct].getKeyStrip() > 155);
	               if (clctInEdge){
	                 if (print_available_pads) 
			     std::cout << "\tInfo: low quality CLCT in CSC chamber edge, don't care about GEM pads" << std::endl;
	   	    }
	               else {
	                 if (nFound != 0){
	                   if (print_available_pads) std::cout << "\tInfo: low quality CLCT with " << nFound 
			                                        << " matching GEM trigger pads" << std::endl;
	                 }
	                 else {
	                  if (print_available_pads) std::cout << "\tWarning: low quality CLCT without matching GEM trigger pad" << std::endl;
	                  continue;
	                }
	               }
	             }
          
          ++nSuccesFulMatches;
          //	    if (infoV > 1) LogTrace("CSCMotherboard")
	  int mbx = bx_clct-bx_clct_start;
          correlateLCTs(alct->bestALCT[bx_alct], alct->secondALCT[bx_alct],
                        clct->bestCLCT[bx_clct], clct->secondCLCT[bx_clct],
			allLCTs[bx_alct][mbx][0], allLCTs[bx_alct][mbx][1]);
	  if (print_available_pads) {
	    std::cout << "Successful ALCT-CLCT match in ME21: bx_alct = " << bx_alct
		      << "; match window: [" << bx_clct_start << "; " << bx_clct_stop
		      << "]; bx_clct = " << bx_clct << std::endl;
	    std::cout << "+++ Best CLCT Details: ";
	    clct->bestCLCT[bx_clct].print();
	    std::cout << "+++ Second CLCT Details: ";
	    clct->secondCLCT[bx_clct].print();
	  }
          
//           if (allLCTs[bx_alct][mbx][0].isValid()) {
//             used_clct_mask[bx_clct] += 1;
//             if (match_earliest_clct_me21_only) break;
//	       std::cout << "Valid LCT" << allLCTs[bx_alct][mbx][0] << std::endl;
//           }
        } // end of CLCT loop

      // ALCT-to-GEM matching
      int nSuccesFulGEMMatches = 0;
      if (runME21ILT_ and nSuccesFulMatches==0 and buildLCTfromALCTandGEM_ME21_){
        if (print_available_pads) std::cout << "++No valid ALCT-CLCT matches in ME21" << std::endl;
        for (int bx_gem = bx_gem_start; bx_gem <= bx_gem_stop; bx_gem++) {
          if (not hasCoPads) continue;
          // find the best matching copad - first one 
          try {
            auto copads_long(matchingGEMPads(alct->bestALCT[bx_alct], coPadsLong_[bx_gem],false,true));             
           // auto copads_short(matchingGEMPads(alct->bestALCT[bx_alct], coPadsShort_[bx_gem],true,true));             
	   // int nFound(copads_long.size()!=0 ? copads_long.size() : copads_short.size());
	      int nFound(copads_long.size());
	    if (nFound == 0) continue;
	     // auto copads(copads_long.size()!=0 ? copads_long : copads_short);
            if (print_available_pads) std::cout << "\t++Number of matching GEM CoPads in BX " << bx_alct << " : "<< copads_long.size() << std::endl;
            ++nSuccesFulGEMMatches;           
	    int mbx = bx_gem-bx_gem_start; 
            correlateLCTsGEM(alct->bestALCT[bx_alct], alct->secondALCT[bx_alct],
                             *(copads_long.at(0)).second, allLCTs[bx_alct][mbx][0], allLCTs[bx_alct][mbx][1]);
            if (allLCTs[bx_alct][mbx][0].isValid()) {
              if (match_earliest_clct_me21_only_) break;
            }
            if (print_available_pads) 
              std::cout << "Successful ALCT-GEM CoPad match in ME21: bx_alct = " << bx_alct << std::endl << std::endl;
          }
          catch (const std::out_of_range& oor) {
            if (print_available_pads) std::cout << "\t++No valid GEM CoPads in BX: " << bx_alct << std::endl;
            continue;
          }
          if (print_available_pads) 
            std::cout << "------------------------------------------------------------------------" << std::endl << std::endl;
        }
      }

      if (print_available_pads) {
        std::cout << "========================================================================" << std::endl;
        std::cout << "Summary: " << std::endl;
        if (nSuccesFulMatches>1)
          std::cout << "Too many successful ALCT-CLCT matches in ME21: " << nSuccesFulMatches
                    << ", CSCDetId " << cscChamber->id()
                    << ", bx_alct = " << bx_alct
                    << "; match window: [" << bx_clct_start << "; " << bx_clct_stop << "]" << std::endl;
        else if (nSuccesFulMatches==1)
          std::cout << "1 successful ALCT-CLCT match in ME21: " 
                    << " CSCDetId " << cscChamber->id()
                    << ", bx_alct = " << bx_alct
                    << "; match window: [" << bx_clct_start << "; " << bx_clct_stop << "]" << std::endl;
        else if (nSuccesFulGEMMatches==1)
          std::cout << "1 successful ALCT-GEM match in ME21: " 
                    << " CSCDetId " << cscChamber->id()
                    << ", bx_alct = " << bx_alct
                    << "; match window: [" << bx_clct_start << "; " << bx_clct_stop << "]" << std::endl;
        else 
          std::cout << "Unsuccessful ALCT-CLCT match in ME21: " 
                    << "CSCDetId " << cscChamber->id()
                    << ", bx_alct = " << bx_alct
                    << "; match window: [" << bx_clct_start << "; " << bx_clct_stop << "]" << std::endl;

        std::cout << "------------------------------------------------------------------------" << std::endl;
        std::cout << "Attempt ALCT-CLCT matching in ME2/1 in bx range: [" << bx_clct_start << "," << bx_clct_stop << "]" << std::endl;
      }
      
      }// end of ALCT loop

    // possibly use some discrimination from GEMs
  if (gemGeometryAvailable and runME21ILT_ and do_gem_matching)  matchGEMPads();

   // count initial LCTs
  if (print_available_pads){
    std::cout << "========================================================================" << std::endl;
    std::cout << "Counting the LCTs" << std::endl;
    std::cout << "========================================================================" << std::endl;
  }

  for (int bx = 0; bx < MAX_LCT_BINS; bx++) 
    for (unsigned int mbx = 0; mbx < match_trig_window_size; mbx++)
      for (int i=0;i<2;i++)
        if (allLCTs[bx][mbx][i].isValid())
	    std::cout << " LCT  "<< allLCTs[bx][mbx][i] << std::endl;

  std::vector<CSCCorrelatedLCTDigi> lcts;
  lcts =  readoutLCTs();
  bool first = true;
  unsigned int nlct=0;
  for (auto p : lcts )
  {
          if (print_available_pads and first){
            std::cout << "========================================================================" << std::endl;
            std::cout << "Counting the final LCTs" << std::endl;
            std::cout << "========================================================================" << std::endl;
            first = false;
	//    std::cout << "tmb_cross_bx_algo: " << tmb_cross_bx_algo << std::endl;
	    
	  }
          nlct++;
          if (print_available_pads)
            std::cout << " LCT "<<nlct<<"  " << p <<std::endl;
  }
    
}

      /*
	int bx_alct_matched = 0;
  for (int bx_clct = 0; bx_clct < CSCCathodeLCTProcessor::MAX_CLCT_BINS; bx_clct++) {
    if (clct->bestCLCT[bx_clct].isValid()) {
      bool is_matched = false;
      int bx_alct_start = bx_clct - match_trig_window_size/2;
      int bx_alct_stop  = bx_clct + match_trig_window_size/2;
      
      for (int bx_alct = bx_alct_start; bx_alct <= bx_alct_stop; bx_alct++) {
        if (bx_alct < 0 || bx_alct >= CSCAnodeLCTProcessor::MAX_ALCT_BINS) continue;
        // default: do not reuse ALCTs that were used with previous CLCTs
        if (drop_used_alcts && used_alct_mask[bx_alct]) continue;
        if (alct->bestALCT[bx_alct].isValid()) {
          if (infoV > 1) LogTrace("CSCMotherboardME21")
            << "Successful ALCT-CLCT match: bx_clct = " << bx_clct
            << "; match window: [" << bx_alct_start << "; " << bx_alct_stop
            << "]; bx_alct = " << bx_alct;
          correlateLCTs(alct->bestALCT[bx_alct], alct->secondALCT[bx_alct],
                        clct->bestCLCT[bx_clct], clct->secondCLCT[bx_clct]);
          used_alct_mask[bx_alct] += 1;
          is_matched = true;
          bx_alct_matched = bx_alct;
          break;
        }
      }
      // No ALCT within the match time interval found: report CLCT-only LCT
      // (use dummy ALCTs).
      if (!is_matched) {
        if (infoV > 1) LogTrace("CSCMotherboardME21")
          << "Unsuccessful ALCT-CLCT match (CLCT only): bx_clct = "
          << bx_clct << "; match window: [" << bx_alct_start
          << "; " << bx_alct_stop << "]";
        correlateLCTs(alct->bestALCT[bx_clct], alct->secondALCT[bx_clct],
                      clct->bestCLCT[bx_clct], clct->secondCLCT[bx_clct]);
      }
    }
    // No valid CLCTs; attempt to make ALCT-only LCT.  Use only ALCTs
    // which have zeroth chance to be matched at later cathode times.
    // (I am not entirely sure this perfectly matches the firmware logic.)
    // Use dummy CLCTs.
    else {
      int bx_alct = bx_clct - match_trig_window_size/2;
      if (bx_alct >= 0 && bx_alct > bx_alct_matched) {
        if (alct->bestALCT[bx_alct].isValid()) {
          if (infoV > 1) LogTrace("CSCMotherboardME21")
            << "Unsuccessful ALCT-CLCT match (ALCT only): bx_alct = "
            << bx_alct;
          correlateLCTs(alct->bestALCT[bx_alct], alct->secondALCT[bx_alct],
                        clct->bestCLCT[bx_clct], clct->secondCLCT[bx_clct]);
          }
      }
    }
  }

  if (infoV > 0) {
    for (int bx = 0; bx < MAX_LCT_BINS; bx++) {
      if (firstLCT[bx].isValid())
        LogDebug("CSCMotherboardME21") << firstLCT[bx];
      if (secondLCT[bx].isValid())
        LogDebug("CSCMotherboardME21") << secondLCT[bx];
    }
      */
      

void CSCMotherboardME21::correlateLCTs(CSCALCTDigi bestALCT,
				   CSCALCTDigi secondALCT,
				   CSCCLCTDigi bestCLCT,
				   CSCCLCTDigi secondCLCT,
				   CSCCorrelatedLCTDigi& lct1,
				   CSCCorrelatedLCTDigi& lct2)
{
  bool anodeBestValid     = bestALCT.isValid();
  bool anodeSecondValid   = secondALCT.isValid();
  bool cathodeBestValid   = bestCLCT.isValid();
  bool cathodeSecondValid = secondCLCT.isValid();

  if (anodeBestValid and !anodeSecondValid)     secondALCT = bestALCT;
  if (!anodeBestValid and anodeSecondValid)     bestALCT   = secondALCT;
  if (cathodeBestValid and !cathodeSecondValid) secondCLCT = bestCLCT;
  if (!cathodeBestValid and cathodeSecondValid) bestCLCT   = secondCLCT;

  // ALCT-CLCT matching conditions are defined by "trig_enable" configuration
  // parameters.
  if ((alct_trig_enable  and bestALCT.isValid()) or
      (clct_trig_enable  and bestCLCT.isValid()) or
      (match_trig_enable and bestALCT.isValid() and bestCLCT.isValid()))
  {
    lct1 = constructLCTs(bestALCT, bestCLCT);
    lct1.setTrknmb(1);
  }

  if (((secondALCT != bestALCT) or (secondCLCT != bestCLCT)) and
      ((alct_trig_enable  and secondALCT.isValid()) or
       (clct_trig_enable  and secondCLCT.isValid()) or
       (match_trig_enable and secondALCT.isValid() and secondCLCT.isValid())))
  {
    lct2 = constructLCTs(secondALCT, secondCLCT);
    lct2.setTrknmb(2);
  }
}

std::vector<CSCCorrelatedLCTDigi> CSCMotherboardME21::readoutLCTs()
{
    return getLCTs();
 
}


std::vector<CSCCorrelatedLCTDigi> CSCMotherboardME21::getLCTs()
{
    std::vector<CSCCorrelatedLCTDigi> result;
    for (int bx = 0; bx < MAX_LCT_BINS; bx++ )
    {
      std::vector<CSCCorrelatedLCTDigi> tmpV = sortLCTsByQual(bx);
      result.insert(result.end(), tmpV.begin(), tmpV.end());
    }
    return result;
}

//sort LCTs by Quality in each BX
std::vector<CSCCorrelatedLCTDigi> CSCMotherboardME21::sortLCTsByQual(int bx)
 {
  std::vector<CSCCorrelatedLCTDigi> LCTs;
  std::vector<CSCCorrelatedLCTDigi> tmpV;
  tmpV.clear();
  LCTs.clear();
  for (unsigned int mbx = 0; mbx < match_trig_window_size; mbx++) 
      for (int i=0;i<2;i++)
        if (allLCTs[bx][mbx][i].isValid())  
            LCTs.push_back(allLCTs[bx][mbx][i]);
  std::vector<CSCCorrelatedLCTDigi>::iterator plct = LCTs.begin();
  for (; plct != LCTs.end(); plct++)
  {
      if (!plct->isValid()) continue;
      std::vector<CSCCorrelatedLCTDigi>::iterator itlct = tmpV.begin();
      for (; itlct != tmpV.end(); itlct++)
	  if((*itlct).getQuality() < (*plct).getQuality()) break;
    
     if(itlct==tmpV.end()) tmpV.push_back(*plct);
     else tmpV.insert(itlct--, *plct);
          
  }
 // debug 
//  std::cout << "sort LCTs by quality" << std::endl;
  if (tmpV.size()> max_me21_lcts) tmpV.erase(tmpV.begin()+max_me21_lcts, tmpV.end());
    return  tmpV;
 }


// match GEMpad to ALCT and then build LCT from GEMCopad and ALCT
CSCMotherboardME21::GEMPadsBX CSCMotherboardME21::matchingGEMPads(const CSCALCTDigi& alct, const GEMPadsBX& pads,
       					                	 bool isshort, bool isCopad, bool first)
{
    CSCMotherboardME21::GEMPadsBX result;

  auto cscWgToGemRoll_(isshort ? cscWgToGemRollShort_ : cscWgToGemRollLong_);
  auto alctRoll(cscWgToGemRoll_[alct.getKeyWG()]);

  const bool debug(false);
  if (debug) std::cout << "ALCT keyWG " << alct.getKeyWG() << ", rolls " << alctRoll << std::endl;
  for (auto p: pads){
    auto padRoll(GEMDetId(p.first).roll());
    if (debug) std::cout << "Candidate ALCT: " << padRoll << std::endl;
    //
    if (alctRoll == -99 or alctRoll != padRoll ) continue;  //invalid region
    if (debug) std::cout << "++Matches! " << std::endl;
    result.push_back(p);
    if (first) return result;
  }
  return result;
}

// match GEMpad to ALCT and then build LCT from GEMCopad and ALCT
CSCMotherboardME21::GEMPadsBX CSCMotherboardME21::matchingGEMPads(const CSCCLCTDigi& clct, const GEMPadsBX& pads,
       					                	 bool isshort, bool isCopad, bool first)
{
    CSCMotherboardME21::GEMPadsBX result;

  // fetch the low and high pad edges
  int deltaPad(isCopad ? maxDeltaPadCoPad_ : maxDeltaPadPad_);
  const int lowPad(cscHsToGemPad_[clct.getKeyStrip()].first);
  const int highPad(cscHsToGemPad_[clct.getKeyStrip()].second);
  const bool debug(false);
  if (debug) std::cout << "lowpad " << lowPad << " highpad " << highPad << " delta pad " << deltaPad <<std::endl;
  for (auto p: pads){
    auto padRoll((p.second)->pad());
    if (debug) std::cout << "padRoll " << padRoll << std::endl;
    if (std::abs(lowPad - padRoll) <= deltaPad or std::abs(padRoll - highPad) <= deltaPad){
    if (debug) std::cout << "++Matches! " << std::endl;
      result.push_back(p);
      if (first) return result;
      
    }
  }
    return result;
}

// to mach GEMpad to low quality clct
CSCMotherboardME21::GEMPadsBX CSCMotherboardME21::matchingGEMPads(const CSCCLCTDigi& clct, const CSCALCTDigi& alct, 
	                                                          const GEMPadsBX& pads, 
                                                                  bool isshort, bool isCoPad, bool first)
{
  CSCMotherboardME21::GEMPadsBX result;

  // Fetch all (!) pads matching to ALCTs and CLCTs
  auto padsClct(matchingGEMPads(clct, pads, isshort, isCoPad, false));
  auto padsAlct(matchingGEMPads(alct, pads, isshort, isCoPad, false));

  const bool debug(false);
  if (debug) std::cout << "-----------------------------------------------------------------------"<<std::endl;
  // Check if the pads overlap
  for (auto p : padsAlct){
    if (debug) std::cout<< "Candidate ALCT: " << p.first << " " << *(p.second) << std::endl;
    for (auto q: padsClct){
      if (debug) std::cout<< "++Candidate CLCT: " << q.first << " " << *(q.second) << std::endl;
      // look for exactly the same pads
      if ((p.first != q.first) or GEMCSCPadDigi(*(p.second)) != *(q.second)) continue;
      if (debug) std::cout << "++Matches! " << std::endl;
      result.push_back(p);
      if (first) return result;
    }
  }
 return result;
}


int CSCMotherboardME21::assignGEMRoll(double eta, bool isshort)
{
  int result = -99;
  auto gemPadToEtaLimits_( isshort ? gemPadToEtaLimitsShort_ : gemPadToEtaLimitsLong_);
  for(auto p : gemPadToEtaLimits_) {
    const float minEta((p.second).first);
    const float maxEta((p.second).second);
    if (minEta <= eta and eta <= maxEta) {
      result = p.first;
      break;
    }
  }
  return result;
}

void CSCMotherboardME21::buildCoincidencePads(const GEMCSCPadDigiCollection* out_pads, GEMCSCPadDigiCollection& out_co_pads)
{
  // build coincidences
  for (auto det_range = out_pads->begin(); det_range != out_pads->end(); ++det_range) {
    const GEMDetId& id = (*det_range).first;
    if (id.station() != 3) continue; // comment out if we use short and Long chamber
    
    // all coincidences detIDs will have layer=1
    if (id.layer() != 1) continue;
    
    // find the corresponding id with layer=2
    GEMDetId co_id(id.region(), id.ring(), id.station(), 2, id.chamber(), id.roll());
    
    auto co_pads_range = out_pads->get(co_id);
    // empty range = no possible coincidence pads
    if (co_pads_range.first == co_pads_range.second) continue;
      
    // now let's correlate the pads in two layers of this partition
    const auto& pads_range = (*det_range).second;
    for (auto p = pads_range.first; p != pads_range.second; ++p) {
      for (auto co_p = co_pads_range.first; co_p != co_pads_range.second; ++co_p) {
        // check the match in pad
        if (std::abs(p->pad() - co_p->pad()) > maxDeltaPadInCoPad_) continue;
        // check the match in BX
        if (std::abs(p->bx() - co_p->bx()) > maxDeltaBXInCoPad_ ) continue;
        
        // always use layer1 pad's BX as a copad's BX
        GEMCSCPadDigi co_pad_digi(p->pad(), p->bx());
        out_co_pads.insertDigi(id, co_pad_digi);
      }
    }
  }
}


std::map<int,std::pair<double,double> >
CSCMotherboardME21::createGEMPadLUT(bool isLong)
{
  std::map<int,std::pair<double,double> > result;

  const int st(isLong ? 3 : 2);
  // no distinction between even and odd in GE2/1
  auto chamber(gem_g->chamber(GEMDetId(1,1,st,1,1,0)));
  if (chamber==nullptr) return result;

  for(int i = 1; i<= chamber->nEtaPartitions(); ++i){
    auto roll(chamber->etaPartition(i));
    if (roll==nullptr) continue;
    const float half_striplength(roll->specs()->specificTopology().stripLength()/2.);
    const LocalPoint lp_top(0., half_striplength, 0.);
    const LocalPoint lp_bottom(0., -half_striplength, 0.);
    const GlobalPoint gp_top(roll->toGlobal(lp_top));
    const GlobalPoint gp_bottom(roll->toGlobal(lp_bottom));
    result[i] = std::make_pair(gp_top.eta(), gp_bottom.eta());
  }
  return result;
}

std::map<int, std::vector<std::pair<unsigned int, const GEMCSCPadDigi*> > >
CSCMotherboardME21::retrieveGEMPads(const GEMCSCPadDigiCollection* gemPads, unsigned id, bool iscopad)
{
  int deltaBX(iscopad ? maxDeltaBXCoPad_ : maxDeltaBXPad_);
  GEMPads result;

  auto superChamber(gem_g->superChamber(id));
  for (auto ch : superChamber->chambers()) {
    for (auto roll : ch->etaPartitions()) {
      GEMDetId roll_id(roll->id());
      auto pads_in_det = gemPads->get(roll_id);
      for (auto pad = pads_in_det.first; pad != pads_in_det.second; ++pad) {
        auto id_pad = std::make_pair(roll_id(), &(*pad));
        const int bx_shifted(lct_central_bx + pad->bx());
        for (int bx = bx_shifted - deltaBX;bx <= bx_shifted + deltaBX; ++bx) {
          if (iscopad){
            if(bx != lct_central_bx) continue;
            result[bx].push_back(id_pad);  
          }else{
            result[bx].push_back(id_pad);  
          }
        }
      }
    }
  }
  return result;
}


void CSCMotherboardME21::correlateLCTsGEM(CSCALCTDigi bestALCT, CSCALCTDigi secondALCT,
			                  GEMCSCPadDigi gemPad,
			                  CSCCorrelatedLCTDigi& lct1, CSCCorrelatedLCTDigi& lct2)
{
    
  bool anodeBestValid     = bestALCT.isValid();
  bool anodeSecondValid   = secondALCT.isValid();

  if (anodeBestValid and !anodeSecondValid)     secondALCT = bestALCT;
  if (!anodeBestValid and anodeSecondValid)     bestALCT   = secondALCT;

  if ((alct_trig_enable  and bestALCT.isValid()) or
      (match_trig_enable and bestALCT.isValid()))
  {
    lct1 = constructLCTsGEM(bestALCT, gemPad, useOldLCTDataFormatALCTGEM_);
    lct1.setTrknmb(1);
    lct1.setGEMDPhi(0.0);
  }

  if ((alct_trig_enable  and secondALCT.isValid()) or
      (match_trig_enable and secondALCT.isValid() and secondALCT != bestALCT))
  {
    lct2 = constructLCTsGEM(secondALCT, gemPad, useOldLCTDataFormatALCTGEM_);
    lct2.setTrknmb(2);
    lct2.setGEMDPhi(0.0);
   }
}

CSCCorrelatedLCTDigi CSCMotherboardME21::constructLCTsGEM(const CSCALCTDigi& alct, const GEMCSCPadDigi& gem,
                                                          bool oldDataFormat)
{

    if (oldDataFormat){
    // CLCT pattern number - no pattern
    unsigned int pattern = 0;

    // LCT quality number
    unsigned int quality = 11;
    
    // Bunch crossing
    int bx = alct.getBX();
    
    // get keyStrip from LUT
    int keyStrip = gemPadToCscHs_[gem.pad()];
    // construct correlated LCT; temporarily assign track number of 0.
      return CSCCorrelatedLCTDigi(0, 1, quality, alct.getKeyWG(), keyStrip, pattern, 0, bx, 0, 0, 0, theTrigChamber);
    }
      else return CSCCorrelatedLCTDigi(0,0,0,0,0,0,0,0,0,0,0,0);
    
}


void CSCMotherboardME21::matchGEMPads()
{
  
  using namespace std;

  // check if we have any LCTs at all
  int nlct = 0;
  for (int bx = 0; bx < MAX_LCT_BINS; bx++)
    for (unsigned int mbx = 0; mbx < match_trig_window_size; mbx++)
      for (int i=0;i<2;i++)
      {
        CSCCorrelatedLCTDigi& lct = allLCTs[bx][mbx][i];
        if (lct.isValid()) nlct++;
      }
  if (nlct == 0) return;

  // retrieve CSCChamber geometry
  CSCTriggerGeomManager* geo_manager = CSCTriggerGeometry::get();
  CSCChamber* cscChamber = geo_manager->chamber(theEndcap, theStation, theSector, theSubsector, theTrigChamber);
 // const CSCLayer* keyLayerME21(cscChamber->layer(3));
 // const CSCLayerGeometry* keyLayerGeometryME21(keyLayerME21->geometry());

  const CSCDetId me21Id(cscChamber->id());
//  const int nhalfstrip = keyLayerGeometryME21->numberOfStrips() * 2;

  if (debug_gem_matching) std::cout<<"++++++++  matchGEMPads "<< me21Id <<" +++++++++ "<<std::endl;

  // "key" layer id is used to calculate global position of stub
  CSCDetId key_id(me21Id.endcap(), me21Id.station(), me21Id.ring(), me21Id.chamber(), CSCConstants::KEY_CLCT_LAYER);

  // check if there are any pads 
  if (padsLong_.empty()) {
    if (debug_gem_matching) std::cout<<"igotnopads"<<std::endl;
    return;
  }

  // walk over BXs
  for (int bx = 0; bx < MAX_LCT_BINS; ++bx)
  {
    auto in_pads = padsLong_.find(bx);

    // walk over potential LCTs in this BX
    for (unsigned int mbx = 0; mbx < match_trig_window_size; ++mbx)
      for (int i=0; i<2; ++i)
      {
        CSCCorrelatedLCTDigi& lct = allLCTs[bx][mbx][i];
        if (!lct.isValid() or fabs(lct.getGEMDPhi()) < 0.000001) continue;
        if (debug_gem_matching) std::cout<<"LCTbefore "<<bx<<" "<<mbx<<" "<<i<<" "<<lct;

        // use -99 as default value whe we don't know if there could have been a gem match
        lct.setGEMDPhi(-99.);

        // "strip" here is actually a half-strip in geometry's terms
        // note that LCT::getStrip() starts from 0, flip the halfstrip
         float fractional_strip = 0.5 * (lct.getStrip() + 1) - 0.25;
   //     float fractional_strip = 0.5 * (lct.getStrip() + 1) - 0.25;
        auto layer_geo = cscChamber->layer(CSCConstants::KEY_CLCT_LAYER)->geometry();
        // LCT::getKeyWG() also starts from 0
        float wire = layer_geo->middleWireOfGroup(lct.getKeyWG() + 1);

        LocalPoint csc_intersect = layer_geo->intersectionOfStripAndWire(fractional_strip, wire);
        GlobalPoint csc_gp = csc_g->idToDet(key_id)->surface().toGlobal(csc_intersect);

        // is LCT located in the high efficiency GEM eta range?
        bool gem_fid = ( std::abs(csc_gp.eta()) >= gem_match_min_eta );

        if (debug_gem_matching) std::cout<<" lct eta "<<csc_gp.eta()<<" phi "<<csc_gp.phi()<<std::endl;

        if (!gem_fid)
        {
          if (debug_gem_matching) std::cout<<"    -- lct pass no gem req"<<std::endl;
          continue;
        }

        if (in_pads == padsLong_.end()) // has no potential GEM hits with similar BX -> zap it
        {
          if (gem_clear_nomatch_lcts) lct.clear();
          if (debug_gem_matching) std::cout<<"    -- no gem"<<std::endl;
          continue;
        }
        if (debug_gem_matching) std::cout<<"    -- gem possible"<<std::endl;

        // use 99 ad default value whe we expect there to be a gem match
        lct.setGEMDPhi(99.);
         
        // to consider a GEM pad as "matched" it has to be 
        // within specified delta_eta and delta_phi ranges
        // and if there are multiple ones, only the min|delta_phi| is considered as matched
        bool gem_matched = false;
        //int gem_bx = 99;
        float min_dphi = 99.;
        for (auto& id_pad: in_pads->second)
        {
          GEMDetId gem_id(id_pad.first);
          LocalPoint gem_lp = gem_g->etaPartition(gem_id)->centreOfPad(id_pad.second->pad());
          GlobalPoint gem_gp = gem_g->idToDet(gem_id)->surface().toGlobal(gem_lp);
          float dphi = deltaPhi(csc_gp.phi(), gem_gp.phi());
          float deta = csc_gp.eta() - gem_gp.eta();
          if (debug_gem_matching) std::cout<<"    gem with dphi "<< std::abs(dphi) <<" deta "<< std::abs(deta) <<std::endl;

          if( (              std::abs(deta) <= gem_match_delta_eta        ) and // within delta_eta
               ( std::abs(dphi) <= gem_match_delta_phi )  and // within delta_phi
              ( std::abs(dphi) < std::abs(min_dphi) )                          // minimal delta phi
            )
          {
            gem_matched = true;
            min_dphi = dphi;
            //gem_bx = id_pad.second->bx();
          }
        }
        if (gem_matched)
        {
          if (debug_gem_matching) std::cout<<" GOT MATCHED GEM!"<<std::endl;
          lct.setGEMDPhi(min_dphi);
	  // assing the bit value
	 /* int oddEven = int(not is_odd) + 1;
	  int numberOfBendAngles(sizeof lut_pt_vs_dphi_gemcsc / sizeof *lut_pt_vs_dphi_gemcsc);
	  int iFound = 0;
	  if (abs(min_dphi) < lut_pt_vs_dphi_gemcsc[numberOfBendAngles-1][oddEven]) iFound = numberOfBendAngles;
	  else {
	    for (int i=0; i< numberOfBendAngles-1; ++i) {
	      if (debug_gem_matching) std::cout<<"is_odd "<<is_odd <<" min_dphi "<<abs(min_dphi)<<" bend angle lib "<<i<<" "<<lut_pt_vs_dphi_gemcsc[i][oddEven]<< std::endl;
	      if (abs(min_dphi) < lut_pt_vs_dphi_gemcsc[i][oddEven] and abs(min_dphi) > lut_pt_vs_dphi_gemcsc[i+1][oddEven]) 
		iFound = i+1;
	    }
	  }
	  lct.setGEMDPhiBits(iFound);
	  if (debug_gem_matching) std::cout<<"found bend angle "<<abs(min_dphi)
	      <<" "<<lct.getGEMDPhiBits()<<" "<<lut_pt_vs_dphi_gemcsc[iFound][oddEven]<<" "<<iFound << std::endl;
        */
        }
        else
        {
          if (debug_gem_matching) std::cout<<" no gem match";
          if (gem_clear_nomatch_lcts)
          {
            lct.clear();
            if (debug_gem_matching) std::cout<<" - cleared lct";
          }
          if (debug_gem_matching) std::cout<<std::endl;
        }
        if (debug_gem_matching) std::cout<<"LCTafter "<<bx<<" "<<mbx<<" "<<i<<" "<<lct;
      }
  }

  // final count
  /*int nlct_after = 0;
  for (int bx = 0; bx < MAX_LCT_BINS; bx++)
    for (unsigned int mbx = 0; mbx < match_trig_window_size; mbx++)
      for (int i=0;i<2;i++)
      {
        if (allLCTs[bx][mbx][i].isValid()) nlct_after++;
      }

  if (debug_gem_matching) std::cout<<"before "<<nlct<<"  after "<<nlct_after<<std::endl;
   */
  }

void CSCMotherboardME21::printGEMTriggerPads(int bx_start, int bx_stop, bool isShort, bool iscopad)
{
  // pads or copads?
  auto thePads(!iscopad ? (isShort ? padsShort_ : padsLong_) : (isShort ? coPadsShort_ : coPadsLong_));
  const bool hasPads(thePads.size()!=0);
  
  std::cout << "------------------------------------------------------------------------" << std::endl;
  bool first = true;
  for (int bx = bx_start; bx <= bx_stop; bx++) {
    // print only the pads for the central BX
    if (centralBXonlyGEM_ and bx!=lct_central_bx) continue;
    if (bx!=lct_central_bx and iscopad) continue;
    std::vector<std::pair<unsigned int, const GEMCSCPadDigi*> > in_pads = thePads[bx];
    if (first) {
      if (!iscopad) std::cout << "* GEM trigger pads: " << std::endl;
      else          std::cout << "* GEM trigger coincidence pads: " << std::endl;
    }
    first = false;
    if (!iscopad) std::cout << "N(pads) BX " << bx << " : " << in_pads.size() << std::endl;
    else          std::cout << "N(copads) BX " << bx << " : " << in_pads.size() << std::endl;
    if (hasPads){
      for (auto pad : in_pads){
        auto roll_id(GEMDetId(pad.first));
        std::cout << "\tdetId " << pad.first << " " << roll_id << ", pad = " << pad.second->pad() << ", BX = " << pad.second->bx() + 6;
//         if (isPadInOverlap(roll_id.roll())) std::cout << " (in overlap)" << std::endl;
//         else std::cout << std::endl;
      }
    }
    else
      break;
  }
}


