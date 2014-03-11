//-----------------------------------------------------------------------------
//
//   Class: CSCMotherboardME11
//
//   Description:
//    Extended CSCMotherboard for ME11 to handle ME1a and ME1b separately
//
//   Author List: Vadim Khotilovich 12 May 2009
//
//-----------------------------------------------------------------------------

#include <L1Trigger/CSCTriggerPrimitives/src/CSCMotherboardME11.h>
//#include <Utilities/Timing/interface/TimingReport.h>
#include <FWCore/MessageLogger/interface/MessageLogger.h>
#include <DataFormats/MuonDetId/interface/CSCTriggerNumbering.h>
#include <Geometry/GEMGeometry/interface/GEMGeometry.h>
#include <Geometry/GEMGeometry/interface/GEMEtaPartitionSpecs.h>
#include <L1Trigger/CSCCommonTrigger/interface/CSCTriggerGeometry.h>
#include <DataFormats/Math/interface/deltaPhi.h>
#include <DataFormats/Math/interface/normalizedPhi.h>
#include <cmath>
#include <tuple>

// LUT for which ME1/1 wire group can cross which ME1/a halfstrip
// 1st index: WG number
// 2nd index: inclusive HS range
const int CSCMotherboardME11::lut_wg_vs_hs_me1a[48][2] = {
{0, 95},{0, 95},{0, 95},{0, 95},{0, 95},
{0, 95},{0, 95},{0, 95},{0, 95},{0, 95},
{0, 95},{0, 95},{0, 77},{0, 61},{0, 39},
{0, 22},{-1,-1},{-1,-1},{-1,-1},{-1,-1},
{-1,-1},{-1,-1},{-1,-1},{-1,-1},{-1,-1},
{-1,-1},{-1,-1},{-1,-1},{-1,-1},{-1,-1},
{-1,-1},{-1,-1},{-1,-1},{-1,-1},{-1,-1},
{-1,-1},{-1,-1},{-1,-1},{-1,-1},{-1,-1},
{-1,-1},{-1,-1},{-1,-1},{-1,-1},{-1,-1},
{-1,-1},{-1,-1},{-1,-1} };
// a modified LUT for ganged ME1a
const int CSCMotherboardME11::lut_wg_vs_hs_me1ag[48][2] = {
{0, 31},{0, 31},{0, 31},{0, 31},{0, 31},
{0, 31},{0, 31},{0, 31},{0, 31},{0, 31},
{0, 31},{0, 31},{0, 31},{0, 31},{0, 31},
{0, 22},{-1,-1},{-1,-1},{-1,-1},{-1,-1},
{-1,-1},{-1,-1},{-1,-1},{-1,-1},{-1,-1},
{-1,-1},{-1,-1},{-1,-1},{-1,-1},{-1,-1},
{-1,-1},{-1,-1},{-1,-1},{-1,-1},{-1,-1},
{-1,-1},{-1,-1},{-1,-1},{-1,-1},{-1,-1},
{-1,-1},{-1,-1},{-1,-1},{-1,-1},{-1,-1},
{-1,-1},{-1,-1},{-1,-1} };

// LUT for which ME1/1 wire group can cross which ME1/b halfstrip
// 1st index: WG number
// 2nd index: inclusive HS range
const int CSCMotherboardME11::lut_wg_vs_hs_me1b[48][2] = {
{-1,-1},{-1,-1},{-1,-1},{-1,-1},{-1,-1},
{-1,-1},{-1,-1},{-1,-1},{-1,-1},{-1,-1},
{100, 127},{73, 127},{47, 127},{22, 127},{0, 127},
{0, 127},{0, 127},{0, 127},{0, 127},{0, 127},
{0, 127},{0, 127},{0, 127},{0, 127},{0, 127},
{0, 127},{0, 127},{0, 127},{0, 127},{0, 127},
{0, 127},{0, 127},{0, 127},{0, 127},{0, 127},
{0, 127},{0, 127},{0, 127},{0, 127},{0, 127},
{0, 127},{0, 127},{0, 127},{0, 127},{0, 105},
{0, 93},{0, 78},{0, 63} };

// LUT with bending angles of the GEM-CSC high efficiency patterns (98%)
// 1st index: pt value = {5,10,15,20,30,40}
// 2nd index: bending angle for odd numbered chambers
// 3rd index: bending angle for even numbered chambers
const double CSCMotherboardME11::lut_pt_vs_dphi_gemcsc[7][3] = {
//  {3.,  0.02974150, 0.01970300},
  {5.,  0.02203511, 0.00930056},
  {6 ,  0.0182579 , 0.00790009},
  {10., 0.01066000, 0.00483286},
  {15., 0.00722795, 0.00363230},
  {20., 0.00562598, 0.00304878},
  {30., 0.00416544, 0.00253782},
  {40., 0.00342827, 0.00230833} };

const double CSCMotherboardME11::lut_wg_etaMin_etaMax_odd[48][3] = {
{0, 2.44005, 2.44688},
{1, 2.38863, 2.45035},
{2, 2.32742, 2.43077},
{3, 2.30064, 2.40389},
{4, 2.2746, 2.37775},
{5, 2.24925, 2.35231},
{6, 2.22458, 2.32754},
{7, 2.20054, 2.30339},
{8, 2.1771, 2.27985},
{9, 2.15425, 2.25689},
{10, 2.13194, 2.23447},
{11, 2.11016, 2.21258},
{12, 2.08889, 2.19119},
{13, 2.06809, 2.17028},
{14, 2.04777, 2.14984},
{15, 2.02788, 2.12983},
{16, 2.00843, 2.11025},
{17, 1.98938, 2.09108},
{18, 1.97073, 2.0723},
{19, 1.95246, 2.0539},
{20, 1.93456, 2.03587},
{21, 1.91701, 2.01818},
{22, 1.8998, 2.00084},
{23, 1.88293, 1.98382},
{24, 1.86637, 1.96712},
{25, 1.85012, 1.95073},
{26, 1.83417, 1.93463},
{27, 1.8185, 1.91882},
{28, 1.80312, 1.90329},
{29, 1.788, 1.88803},
{30, 1.77315, 1.87302},
{31, 1.75855, 1.85827},
{32, 1.74421, 1.84377},
{33, 1.7301, 1.8295},
{34, 1.71622, 1.81547},
{35, 1.70257, 1.80166},
{36, 1.68914, 1.78807},
{37, 1.67592, 1.77469},
{38, 1.66292, 1.76151},
{39, 1.65011, 1.74854},
{40, 1.63751, 1.73577},
{41, 1.62509, 1.72319},
{42, 1.61287, 1.71079},
{43, 1.60082, 1.69857},
{44, 1.59924, 1.68654},
{45, 1.6006, 1.67467},
{46, 1.60151, 1.66297},
{47, 1.60198, 1.65144} };

const double CSCMotherboardME11::lut_wg_etaMin_etaMax_even[48][3] = {
{0, 2.3917, 2.39853},
{1, 2.34037, 2.40199},
{2, 2.27928, 2.38244},
{3, 2.25254, 2.35561},
{4, 2.22655, 2.32951},
{5, 2.20127, 2.30412},
{6, 2.17665, 2.27939},
{7, 2.15267, 2.25529},
{8, 2.12929, 2.2318},
{9, 2.1065, 2.20889},
{10, 2.08425, 2.18652},
{11, 2.06253, 2.16468},
{12, 2.04132, 2.14334},
{13, 2.0206, 2.12249},
{14, 2.00033, 2.1021},
{15, 1.98052, 2.08215},
{16, 1.96113, 2.06262},
{17, 1.94215, 2.04351},
{18, 1.92357, 2.02479},
{19, 1.90538, 2.00645},
{20, 1.88755, 1.98847},
{21, 1.87007, 1.97085},
{22, 1.85294, 1.95357},
{23, 1.83614, 1.93662},
{24, 1.81965, 1.91998},
{25, 1.80348, 1.90365},
{26, 1.78761, 1.88762},
{27, 1.77202, 1.87187},
{28, 1.75672, 1.85641},
{29, 1.74168, 1.84121},
{30, 1.72691, 1.82628},
{31, 1.7124, 1.8116},
{32, 1.69813, 1.79716},
{33, 1.68411, 1.78297},
{34, 1.67032, 1.769},
{35, 1.65675, 1.75526},
{36, 1.64341, 1.74174},
{37, 1.63028, 1.72844},
{38, 1.61736, 1.71534},
{39, 1.60465, 1.70245},
{40, 1.59213, 1.68975},
{41, 1.57981, 1.67724},
{42, 1.56767, 1.66492},
{43, 1.55572, 1.65278},
{44, 1.55414, 1.64082},
{45, 1.55549, 1.62903},
{46, 1.5564, 1.61742},
{47, 1.55686, 1.60596} };

CSCMotherboardME11::CSCMotherboardME11(unsigned endcap, unsigned station,
			       unsigned sector, unsigned subsector,
			       unsigned chamber,
			       const edm::ParameterSet& conf) :
		CSCMotherboard(endcap, station, sector, subsector, chamber, conf)
{
  edm::ParameterSet commonParams = conf.getParameter<edm::ParameterSet>("commonParam");

  // special configuration parameters for ME11 treatment
  smartME1aME1b = commonParams.getUntrackedParameter<bool>("smartME1aME1b", true);
  disableME1a = commonParams.getUntrackedParameter<bool>("disableME1a", false);
  gangedME1a = commonParams.getUntrackedParameter<bool>("gangedME1a", false);

  if (!isSLHC) edm::LogError("L1CSCTPEmulatorConfigError")
    << "+++ Upgrade CSCMotherboardME11 constructed while isSLHC is not set! +++\n";
  if (!smartME1aME1b) edm::LogError("L1CSCTPEmulatorConfigError")
    << "+++ Upgrade CSCMotherboardME11 constructed while smartME1aME1b is not set! +++\n";

  edm::ParameterSet alctParams = conf.getParameter<edm::ParameterSet>("alctSLHC");
  edm::ParameterSet clctParams = conf.getParameter<edm::ParameterSet>("clctSLHC");
  edm::ParameterSet tmbParams = conf.getParameter<edm::ParameterSet>("tmbSLHC");

  clct1a = new CSCCathodeLCTProcessor(endcap, station, sector, subsector, chamber, clctParams, commonParams, tmbParams);
  clct1a->setRing(4);

  match_earliest_alct_me11_only = tmbParams.getUntrackedParameter<bool>("matchEarliestAlctME11Only",true);
  match_earliest_clct_me11_only = tmbParams.getUntrackedParameter<bool>("matchEarliestClctME11Only",true);

  // if true: use regular CLCT-to-ALCT matching in TMB
  // if false: do ALCT-to-CLCT matching
  clct_to_alct = tmbParams.getUntrackedParameter<bool>("clctToAlct",true);

  // whether to not reuse CLCTs that were used by previous matching ALCTs
  // in ALCT-to-CLCT algorithm
  drop_used_clcts = tmbParams.getUntrackedParameter<bool>("tmbDropUsedClcts",true);

  tmb_cross_bx_algo = tmbParams.getUntrackedParameter<unsigned int>("tmbCrossBxAlgorithm");

  // maximum lcts per BX in ME11: 2, 3, 4 or 999
  max_me11_lcts = tmbParams.getUntrackedParameter<unsigned int>("maxME11LCTs",4);

  pref[0] = match_trig_window_size/2;
  for (unsigned int m=2; m<match_trig_window_size; m+=2)
  {
    pref[m-1] = pref[0] - m/2;
    pref[m]   = pref[0] + m/2;
  }

  //----------------------------------------------------------------------------------------//

  //       G E M  -  C S C   I N T E G R A T E D   L O C A L   A L G O R I T H M

  //----------------------------------------------------------------------------------------//

  // masterswitch
  runGEMCSCILT_ = tmbParams.getUntrackedParameter<bool>("runGEMCSCILT", false);

  /// Do GEM matching?
  do_gem_matching = tmbParams.getUntrackedParameter<bool>("doGemMatching", false);
  
  /// GEM matching dphi and deta
  gem_match_delta_phi_odd = tmbParams.getUntrackedParameter<double>("gemMatchDeltaPhiOdd", 0.0055);
  gem_match_delta_phi_even = tmbParams.getUntrackedParameter<double>("gemMatchDeltaPhiEven", 0.0031);
  gem_match_delta_eta = tmbParams.getUntrackedParameter<double>("gemMatchDeltaEta", 0.08);

  /// delta BX for GEM pads matching
  gem_match_delta_bx = tmbParams.getUntrackedParameter<int>("gemMatchDeltaBX", 1);

  /// min eta of LCT for which we require GEM match (we don't throw out LCTs below this min eta)
  gem_match_min_eta = tmbParams.getUntrackedParameter<double>("gemMatchMinEta", 1.62);

  /// whether to throw out GEM-fiducial LCTs that have no gem match
  gem_clear_nomatch_lcts = tmbParams.getUntrackedParameter<bool>("gemClearNomatchLCTs", true);

  // central bx for LCT is 6 for simulation
  lct_central_bx = tmbParams.getUntrackedParameter<int>("lctCentralBX", 6);

  // debug gem matching
  debug_gem_matching = tmbParams.getUntrackedParameter<bool>("debugGemMatching", false);

  // print available pads
  print_available_pads = tmbParams.getUntrackedParameter<bool>("printAvailablePads", false);

  // max delta BX for copad 
  maxPadDeltaBX_ = tmbParams.getUntrackedParameter<int>("maxPadDeltaBX",1);

  // drop low quality stubs if they don't have GEMs
  dropLowQualityCLCTsNoGEMs_ = tmbParams.getUntrackedParameter<bool>("dropLowQualityCLCTsNoGEMs",false);

  // drop low quality stubs if they don't have GEMs
  dropLowQualityALCTsNoGEMs_ = tmbParams.getUntrackedParameter<bool>("dropLowQualityALCTsNoGEMs",false);

  // use only the central BX for GEM matching
  centralBXonlyGEM_ = tmbParams.getUntrackedParameter<bool>("centralBXonlyGEM",false);
  
  // build LCT from ALCT and GEM
  buildLCTfromALCTandGEM_ME1b_ = tmbParams.getUntrackedParameter<bool>("buildLCTfromALCTandGEMinME1b",false);
  buildLCTfromALCTandGEM_overlap_ = tmbParams.getUntrackedParameter<bool>("buildLCTfromALCTandGEMinOverlap",false);

  // build LCT from CLCT and GEM
  buildLCTfromCLCTandGEM_ME1b_ = tmbParams.getUntrackedParameter<bool>("buildLCTfromCLCTandGEMinME1b",false);
  buildLCTfromCLCTandGEM_overlap_ = tmbParams.getUntrackedParameter<bool>("buildLCTfromALCTandGEMinOverlap",false);

  // LCT ghostbusting
  doLCTGhostBustingWithGEMs_ = tmbParams.getUntrackedParameter<bool>("doLCTGhostBustingWithGEMs",false);

  // correct LCT timing with GEMs
  correctLCTtimingWithGEM_ = tmbParams.getUntrackedParameter<bool>("correctLCTtimingWithGEM",false);

  // use "old" or "new" dataformat for integrated LCTs?
  useOldLCTDataFormatALCTGEM_ = tmbParams.getUntrackedParameter<bool>("useOldLCTDataFormatALCTGEM",true);
  useOldLCTDataFormatCLCTGEM_ = tmbParams.getUntrackedParameter<bool>("useOldLCTDataFormatCLCTGEM",true);
}


CSCMotherboardME11::CSCMotherboardME11() : CSCMotherboard()
{
  // Constructor used only for testing.

  clct1a = new CSCCathodeLCTProcessor();
  clct1a->setRing(4);

  pref[0] = match_trig_window_size/2;
  for (unsigned int m=2; m<match_trig_window_size; m+=2)
  {
    pref[m-1] = pref[0] - m/2;
    pref[m]   = pref[0] + m/2;
  }
}


CSCMotherboardME11::~CSCMotherboardME11()
{
  if (clct1a) delete clct1a;
}


void CSCMotherboardME11::clear()
{
  CSCMotherboard::clear();
  if (clct1a) clct1a->clear();
  for (int bx = 0; bx < MAX_LCT_BINS; bx++)
  {
    //firstLCT1a[bx].clear();
    //secondLCT1a[bx].clear();
    for (unsigned int mbx = 0; mbx < match_trig_window_size; mbx++)
      for (int i=0;i<2;i++)
      {
        allLCTs1b[bx][mbx][i].clear();
        allLCTs1a[bx][mbx][i].clear();
      }
  }
}

// Set configuration parameters obtained via EventSetup mechanism.
void CSCMotherboardME11::setConfigParameters(const CSCDBL1TPParameters* conf)
{
  alct->setConfigParameters(conf);
  clct->setConfigParameters(conf);
  clct1a->setConfigParameters(conf);
  // No config. parameters in DB for the TMB itself yet.
}


void CSCMotherboardME11::run(const CSCWireDigiCollection* wiredc,
                             const CSCComparatorDigiCollection* compdc,
                             const GEMCSCPadDigiCollection* gemPads)
{
  clear();
  
  if (!( alct and clct and  clct1a and smartME1aME1b))
  {
    if (infoV >= 0) edm::LogError("L1CSCTPEmulatorSetupError")
      << "+++ run() called for non-existing ALCT/CLCT processor! +++ \n";
    return;
  }

  alctV = alct->run(wiredc); // run anodeLCT
  clctV1b = clct->run(compdc); // run cathodeLCT in ME1/b
  clctV1a = clct1a->run(compdc); // run cathodeLCT in ME1/a

  bool gemGeometryAvailable(false);
  if (gem_g != nullptr) {
    if (infoV >= 0) edm::LogInfo("L1CSCTPEmulatorSetupInfo")
      << "+++ run() called for GEM-CSC integrated trigger! +++ \n";
    gemGeometryAvailable = true;
  }

  //int n_clct_a=0, n_clct_b=0;
  //if (clct1a->bestCLCT[6].isValid() and clct1a->bestCLCT[6].getBX()==6) n_clct_a++;
  //if (clct1a->secondCLCT[6].isValid() and clct1a->secondCLCT[6].getBX()==6) n_clct_a++;

  int used_alct_mask[20], used_alct_mask_1a[20];
  int used_clct_mask[20], used_clct_mask_1a[20];
  for (int b=0;b<20;b++)
    used_alct_mask[b] = used_alct_mask_1a[b] = used_clct_mask[b] = used_clct_mask_1a[b] = 0;

  // retrieve CSCChamber geometry                                                                                                                                       
  CSCTriggerGeomManager* geo_manager(CSCTriggerGeometry::get());
  CSCChamber* cscChamber(geo_manager->chamber(theEndcap, theStation, theSector, theSubsector, theTrigChamber));
  const CSCLayer* keyLayer(cscChamber->layer(3));
  const CSCLayerGeometry* keyLayerGeometry(keyLayer->geometry());
  auto csc_id(cscChamber->id());
  const bool isEven(csc_id%2==0);
  const int region((theEndcap == 1) ? 1: -1);
  GEMDetId gem_id(region, 1, theStation, 1, csc_id.chamber(), 0);
  const GEMChamber* gemChamber = gem_g->chamber(gem_id);

  // LUT<roll,<etaMin,etaMax> >    
  bool constructPadLUT(true);
  if (constructPadLUT){
    createGEMPadLUT(isEven);
    bool debug(false);
    if (debug){
      if (gemPadToEtaLimits_.size())
        for(auto p : gemPadToEtaLimits_) {
          std::cout << "pad "<< p.first << " min eta " << (p.second).first << " max eta " << (p.second).second << std::endl;
        }
    }
  }

  // loop on all wiregroups to create a LUT <WG,rollMin,rollMax>
  bool constructWGLUT(true);
  if (constructWGLUT){
    cscWgToGemRoll_.clear();
    int numberOfWG(keyLayerGeometry->numberOfWireGroups());
    for (int i = 0; i< numberOfWG; ++i){
      auto etaMin(isEven ? lut_wg_etaMin_etaMax_even[i][1] : lut_wg_etaMin_etaMax_odd[i][1]); 
      auto etaMax(isEven ? lut_wg_etaMin_etaMax_even[i][2] : lut_wg_etaMin_etaMax_odd[i][2]); 
      cscWgToGemRoll_[i] = std::make_pair(assignGEMRoll(etaMin), assignGEMRoll(etaMax));
    }
    bool debug(false);
    if (debug){
      for(auto p : cscWgToGemRoll_) {
        std::cout << "WG "<< p.first << " GEM pads " << (p.second).first << " " << (p.second).second << std::endl;
      }
    }
  }

  bool constructGEMPadCSCHSLUT(true);
  if (constructGEMPadCSCHSLUT){
    gemPadToCscHs_.clear();
    // pick any roll
    auto randRoll(gemChamber->etaPartition(2));
    const int nGEMPads(randRoll->npads());
    for (int i = 0; i< nGEMPads; ++i){
      const LocalPoint lpGEM(randRoll->centreOfPad(i));
      const GlobalPoint gp(randRoll->toGlobal(lpGEM));
      const LocalPoint lpCSC(keyLayer->toLocal(gp));
      const float strip(keyLayerGeometry->strip(lpCSC));
      gemPadToCscHs_[i] = (int) (strip - 0.25)/0.5;
    }
    bool debug(false);
    if (debug){
      std::cout << "detId " << csc_id << std::endl;
      for(auto p : gemPadToCscHs_) {
        std::cout << "GEM Pad "<< p.first << " CSC HS " << p.second << std::endl;
      }
    }
  }
  
  bool constructCSCHSGEMPadLUT(true);
  if (constructCSCHSGEMPadLUT){
    cscHsToGemPad_.clear();
    // pick any roll
    auto randRoll(gemChamber->etaPartition(2));
    auto nStrips((keyLayerGeometry->numberOfStrips()));
    for (float i = 0; i< nStrips; i = i+0.5){
      const LocalPoint lpCSC(keyLayerGeometry->topology()->localPosition(i));
      const GlobalPoint gp(keyLayer->toGlobal(lpCSC));
      const LocalPoint lpGEM(randRoll->toLocal(gp));
      const int HS(i/0.5);
      const bool edge(HS < 5 or HS > 123);
      const float pad(edge ? -99 : randRoll->pad(lpGEM));
      cscHsToGemPad_[int(i/0.5)] = std::make_pair(std::floor(pad),std::ceil(pad));
    }
    bool debug(false);
    if (debug){
      std::cout << "detId " << csc_id << std::endl;
      for(auto p : cscHsToGemPad_) {
        std::cout << "CSC HS "<< p.first << " GEM Pad low " << (p.second).first << " GEM Pad high " << (p.second).second << std::endl;
      }
    }
  }

  // build coincidence pads
  std::auto_ptr<GEMCSCPadDigiCollection> pCoPads(new GEMCSCPadDigiCollection());
  bool buildGEMCSCCoPads = do_gem_matching;
  if (buildGEMCSCCoPads){
    buildCoincidencePads(gemPads, *pCoPads);
  }

  // retrieve pads and copads in a certain BX window for this CSC 
  bool wrapPads = do_gem_matching;
  if (wrapPads){
    pads_.clear();
    coPads_.clear();
    retrieveGEMPads(gemPads, gem_id);
    retrieveGEMPads(pCoPads.get(), gem_id, true);
    //collectGEMPads(gemPads, pCoPads.get(), schDetId); 
  }

  const bool hasPads(pads_.size()!=0);
  const bool hasCoPads(hasPads and coPads_.size()!=0);

  // CLCT-centric CLCT-to-ALCT matching
  if (clct_to_alct) for (int bx_clct = 0; bx_clct < CSCCathodeLCTProcessor::MAX_CLCT_BINS; bx_clct++) {

    // matching in ME1b
    if (clct->bestCLCT[bx_clct].isValid()) {
      int bx_alct_start = bx_clct - match_trig_window_size/2;
      int bx_alct_stop  = bx_clct + match_trig_window_size/2;

      if (print_available_pads){ 
        std::cout << "========================================================================" << std::endl;
        std::cout << "Attempt to reconstruct LCT stubs in ME1/b chamber: " << cscChamber->id() << std::endl;
        std::cout << "------------------------------------------------------------------------" << std::endl;
        std::cout << "+++ Best CLCT Details: ";
        clct->bestCLCT[bx_clct].print();
        std::cout << "+++ Second CLCT Details: ";
        clct->secondCLCT[bx_clct].print();
        
        printGEMTriggerPads(bx_alct_start, bx_alct_stop);      
        printGEMTriggerPads(bx_alct_start, bx_alct_stop, true);      
        
        std::cout << "------------------------------------------------------------------------" << std::endl;
        std::cout << "CLCT-ALCT matching procedure in bx range: [" << bx_alct_start << "," << bx_alct_start << "]" << std::endl;
        std::cout << "------------------------------------------------------------------------" << std::endl;
      }
      
      // matching in ME1b
      int nSuccesFulMatches = 0;
      int nSuccesFulGEMMatches = 0;
      for (int bx_alct = bx_alct_start; bx_alct <= bx_alct_stop; bx_alct++) {
        if (bx_alct < 0 or bx_alct >= CSCAnodeLCTProcessor::MAX_ALCT_BINS) continue;
        if (drop_used_alcts and used_alct_mask[bx_alct]) continue;
        
        if (alct->bestALCT[bx_alct].isValid()) {
          // need extra GEM pad for low quality stubs
          const int quality(alct->bestALCT[bx_alct].getQuality());
          
          if (dropLowQualityALCTsNoGEMs_ and (quality < 4) and hasPads){
            // pick the pad that corresponds 
            std::pair<unsigned int, const GEMCSCPadDigi*> my_pad;
            for (auto p : pads_[bx_alct]){
              if (GEMDetId(p.first).chamber() == csc_id.chamber()){
                // for the time being, just the first copad in the super chamber
                my_pad = p;
                break;
              }
            }
            if (!my_pad.second){
              if (print_available_pads) std::cout << "Warning: low quality ALCT without matching GEM trigger pad" << std::endl;
              continue;
            }
            else
              if (print_available_pads) std::cout << "INFO: low quality ALCT with matching GEM trigger pad" << std::endl;
          }
          
          ++nSuccesFulMatches;
          
          if (infoV > 1) LogTrace("CSCMotherboard")
            << "Successful CLCT-ALCT match in ME1b: bx_clct = " << bx_clct
            << "; match window: [" << bx_alct_start << "; " << bx_alct_stop
            << "]; bx_alct = " << bx_alct;
          int mbx = bx_alct_stop - bx_alct;
          correlateLCTs(alct->bestALCT[bx_alct], alct->secondALCT[bx_alct],
                        clct->bestCLCT[bx_clct], clct->secondCLCT[bx_clct],
                        allLCTs1b[bx_alct][mbx][0], allLCTs1b[bx_alct][mbx][1], ME1B);
          if (allLCTs1b[bx_alct][mbx][0].isValid()) {
            used_alct_mask[bx_alct] += 1;
            if (match_earliest_alct_me11_only) break;
          }
        }
        else {
          if (print_available_pads) std::cout << "++Not a valid ALCT in BX: " << bx_alct << std::endl;
          // at this point we don't hav a valid ALCT...
          if (!hasCoPads) continue;
          // ... but we do have a copad! Try to make an LCT from a CLCT and GEM
          if (!buildLCTfromCLCTandGEM_ME1b_) continue;
          // need a function to get the best copad for a CLCT/ALCT
          // now it simply gets the first one in the list 
          ++nSuccesFulGEMMatches;
          // check if there are any gem copads 
          auto coPadsInBx(coPads_[bx_clct]);
          if (coPadsInBx.size()==0){
            if (print_available_pads) std::cout << "No GEM CoPads for this CLCT BX" << std::endl;
            continue;
          }
          auto firstCoPadInBx((coPadsInBx.at(0)).second);
          correlateLCTsGEM(clct->bestCLCT[bx_clct], clct->secondCLCT[bx_clct],
                           *firstCoPadInBx, allLCTs1b[6][0][0], allLCTs1b[6][0][1]);
          
          if (print_available_pads) 
            std::cout << "Successful CLCT-GEM CoPad match in ME1b: bx_clct = " << bx_clct << std::endl << std::endl;
        }
        if (print_available_pads) 
          std::cout << "------------------------------------------------------------------------" << std::endl << std::endl;
      }
    if (nSuccesFulMatches>1){
      if (print_available_pads) std::cout << "Too many successful CLCT-ALCT matches in ME1b: " << nSuccesFulMatches
                                          << ", CSCDetId " << cscChamber->id()
                                          << ", bx_clct = " << bx_clct
                                          << "; match window: [" << bx_alct_start << "; " << bx_alct_stop << "]" << std::endl;
    }
    else if (nSuccesFulMatches==1){
      if (print_available_pads) std::cout << "1 successful CLCT-ALCT match in ME1b: " 
                                          << " CSCDetId " << cscChamber->id()
                                          << ", bx_clct = " << bx_clct
                                          << "; match window: [" << bx_alct_start << "; " << bx_alct_stop << "]" << std::endl;
    }
    else {
      if (print_available_pads) std::cout << "Unsuccessful CLCT-ALCT match in ME1b: " 
                                          << "CSCDetId " << cscChamber->id()
                                          << ", bx_clct = " << bx_clct
                                          << "; match window: [" << bx_alct_start << "; " << bx_alct_stop << "]" << std::endl;
    }
    
    // Do not report CLCT-only LCT for ME1b
    }
    // matching in ME1a
    if (clct1a->bestCLCT[bx_clct].isValid())
      {
        int bx_alct_start = bx_clct - match_trig_window_size/2;
        int bx_alct_stop  = bx_clct + match_trig_window_size/2;
        for (int bx_alct = bx_alct_start; bx_alct <= bx_alct_stop; bx_alct++)
          {
            if (bx_alct < 0 or bx_alct >= CSCAnodeLCTProcessor::MAX_ALCT_BINS) continue;
            if (drop_used_alcts and used_alct_mask_1a[bx_alct]) continue;
            if (alct->bestALCT[bx_alct].isValid())
              {
                if (infoV > 1) LogTrace("CSCMotherboard")
                  << "Successful CLCT-ALCT match in ME1a: bx_clct = " << bx_clct
                  << "; match window: [" << bx_alct_start << "; " << bx_alct_stop
                  << "]; bx_alct = " << bx_alct;
                int mbx = bx_alct_stop - bx_alct;
                correlateLCTs(alct->bestALCT[bx_alct], alct->secondALCT[bx_alct],
                              clct1a->bestCLCT[bx_clct], clct1a->secondCLCT[bx_clct],
                              allLCTs1a[bx_alct][mbx][0], allLCTs1a[bx_alct][mbx][1], ME1A);
                if (allLCTs1a[bx_alct][mbx][0].isValid())
                  {
                    used_alct_mask_1a[bx_alct] += 1;
                    if (match_earliest_alct_me11_only) break;
                  }
              }
            //  	else {
            // 	  if (print_available_pads) std::cout << "++Not a valid ALCT in BX: " << bx_alct << std::endl;
            // 	  // at this point we don't hav a valid ALCT...
            //  	  if (!hasCoPads) continue;
            // 	  // ... but we do have a copad! Try to make an LCT from a ALCT and GEM
            // 	  if (!buildLCTfromCLCTandGEM_) continue;
            // 	  // need a function to get the best copad for a CLCT/ALCT
            // 	  // now it simply gets the first one in the list 
            // 	  // check if there are any gem copads 
            // 	  auto coPadsInBx(coPads_[bx_alct]);
            // 	  if (coPadsInBx.size()==0){
            // 	    if (print_available_pads) std::cout << "No GEM CoPads for this ALCT BX" << std::endl;
            // 	    continue;
            // 	  }
            // 	  auto firstCoPadInBx((coPadsInBx.at(0)).second);
            // 	  GEMDetId detId(((coPadsInBx.at(0)).first));
            //  	  int rollN(detId.roll());
            //  	  if (isPadInOverlap(rollN)) {
            // 	    correlateLCTsGEM(clct->bestCLCT[bx_clct], clct->secondCLCT[bx_clct],
            // 			     *firstCoPadInBx, allLCTs1a[6][0][0], allLCTs1a[6][0][1]);
            // 	    ++nSuccesFulGEMMatches;
            //  	  }
            // 	  if (print_available_pads) 
            // 	    std::cout << "Successful ALCT-GEM CoPad match in Me1a: bx_clct = " << bx_clct << std::endl << std::endl;
            // 	}
          }
        // Do not report CLCT-only LCT for ME1b
      }
    // Do not attempt to make ALCT-only LCT for ME1b
  } // end of CLCT-centric matching
  
  //  bool foundCLCT(false);
  
  // ALCT-centric ALCT-to-CLCT matching
  else for (int bx_alct = 0; bx_alct < CSCAnodeLCTProcessor::MAX_ALCT_BINS; bx_alct++)
  {
    if (alct->bestALCT[bx_alct].isValid())
    {
      int bx_clct_start = bx_alct - match_trig_window_size/2;
      int bx_clct_stop  = bx_alct + match_trig_window_size/2;

      if (print_available_pads){ 
        std::cout << "========================================================================" << std::endl;
        std::cout << "ALCT-CLCT matching in ME1/1 chamber: " << cscChamber->id() << std::endl;
        std::cout << "------------------------------------------------------------------------" << std::endl;
       std::cout << "+++ Best ALCT Details: ";
        alct->bestALCT[bx_alct].print();
        std::cout << "+++ Second ALCT Details: ";
        alct->secondALCT[bx_alct].print();
        
        printGEMTriggerPads(bx_clct_start, bx_clct_stop);      
        printGEMTriggerPads(bx_clct_start, bx_clct_stop, true);      
        
        std::cout << "------------------------------------------------------------------------" << std::endl;
        std::cout << "Attempt ALCT-CLCT matching in ME1/b in bx range: [" << bx_clct_start << "," << bx_clct_stop << "]" << std::endl;
      }
      
      // matching in ME1b
      int nSuccesFulMatches = 0;
      int nSuccesFulGEMMatches = 0;
      for (int bx_clct = bx_clct_start; bx_clct <= bx_clct_stop; bx_clct++)
      {
        if (bx_clct < 0 or bx_clct >= CSCCathodeLCTProcessor::MAX_CLCT_BINS) continue;
        if (drop_used_clcts and used_clct_mask[bx_clct]) continue;
        if (clct->bestCLCT[bx_clct].isValid())
        {
          const int quality(clct->bestCLCT[bx_clct].getQuality());
          const int lowQ(quality < 4);
          if (print_available_pads) std::cout << "++Valid CLCT in BX: " << bx_clct << std::endl;
//           if (print_available_pads) {
//             std::cout << "CASE A1" << bx_clct << std::endl;
//             if (hasPads) std::cout << "CASE A2" << bx_clct << std::endl;
//             if (hasPads and lowQ) std::cout << "CASE A3" << bx_clct << std::endl;
// //             if (hasPads and lowQ and matchingGEMPad(clct->bestCLCT[bx_clct], alct->bestALCT[bx_alct], pads_[bx_alct], coPads_[bx_alct])) std::cout << "CASE A4" << bx_clct << std::endl;
// //             if (hasPads and lowQ and !matchingGEMPad(clct->bestCLCT[bx_clct], alct->bestALCT[bx_alct], pads_[bx_alct], coPads_[bx_alct])) std::cout << "CASE A5" << bx_clct << std::endl;
//             if (hasCoPads) std::cout << "CASE A5" << bx_clct << std::endl;
//             if (hasCoPads and lowQ) std::cout << "CASE A6" << bx_clct << std::endl;
//           }
          if (dropLowQualityCLCTsNoGEMs_ and lowQ and hasPads){
            // pick the pad that corresponds 
            auto matchingPads(matchingGEMPads(clct->bestCLCT[bx_clct], pads_[bx_clct], false));
            int nFound(matchingPads.size());
            const bool clctInEdge(clct->bestCLCT[bx_clct].getKeyStrip() < 5 or clct->bestCLCT[bx_clct].getKeyStrip() > 123);
            if (clctInEdge){
              if (print_available_pads) std::cout << "\tInfo: low quality CLCT in CSC chamber edge, don't care about GEM pads" << std::endl;
            }
            else {
              if (nFound != 0){
                if (print_available_pads) std::cout << "\tInfo: low quality CLCT with " << nFound << " matching GEM trigger pads" << std::endl;
              }
              else {
                if (print_available_pads) std::cout << "\tWarning: low quality CLCT without matching GEM trigger pad" << std::endl;
                continue;
              }
            }
          }
          
          const bool checkIncorrectTiming(false);
          if (checkIncorrectTiming and hasCoPads){
            std::pair<unsigned int, const GEMCSCPadDigi*> my_copad;
            for (auto p : coPads_[bx_clct]){
              if (GEMDetId(p.first).chamber() == csc_id.chamber()){
                my_copad = p;
                break;
              }
            }
            std::cout << "Copad BX " << my_copad.second->bx() << std::endl;
            std::cout << "CLCT BX " << bx_clct << std::endl;
            if (my_copad.second and my_copad.second->bx() != bx_clct){
              std::cout << "CLCT BX is different from CoPad BX" << std::endl;
            }
          }
          
          ++nSuccesFulMatches;
          //	    if (infoV > 1) LogTrace("CSCMotherboard")
          int mbx = bx_clct-bx_clct_start;
          correlateLCTs(alct->bestALCT[bx_alct], alct->secondALCT[bx_alct],
                        clct->bestCLCT[bx_clct], clct->secondCLCT[bx_clct],
                        allLCTs1b[bx_alct][mbx][0], allLCTs1b[bx_alct][mbx][1], ME1B, pads_[bx_clct], coPads_[bx_clct]);
          if (print_available_pads) {
            std::cout << "Successful ALCT-CLCT match in ME1b: bx_alct = " << bx_alct
                      << "; match window: [" << bx_clct_start << "; " << bx_clct_stop
                      << "]; bx_clct = " << bx_clct << std::endl;
            std::cout << "+++ Best CLCT Details: ";
            clct->bestCLCT[bx_clct].print();
            std::cout << "+++ Second CLCT Details: ";
            clct->secondCLCT[bx_clct].print();
          }
          
          if (allLCTs1b[bx_alct][mbx][0].isValid()) {
            used_clct_mask[bx_clct] += 1;
            if (match_earliest_clct_me11_only) break;
          }
        }
        else {
          if (print_available_pads) std::cout << "++Not a valid CLCT in BX: " << bx_clct << std::endl;
          if (not buildLCTfromALCTandGEM_ME1b_) continue;
          if (not hasCoPads) continue;
          
          // find the best matching copad - first one 
          try {
            auto copads(matchingGEMPads(alct->bestALCT[bx_alct], coPads_[bx_clct]));             
            if (print_available_pads) std::cout << "\t++Number of matching GEM CoPads in BX " << bx_alct << " : "<< copads.size() << std::endl;
            
            ++nSuccesFulGEMMatches;            
            correlateLCTsGEM(alct->bestALCT[bx_alct], alct->secondALCT[bx_alct],
                             *(copads.at(0)).second, allLCTs1b[bx_alct][0][0], allLCTs1b[bx_alct][0][1]);
            
            if (allLCTs1b[bx_alct][0][0].isValid()) {
              if (match_earliest_clct_me11_only) break;
            }
            if (print_available_pads) 
              std::cout << "Successful ALCT-GEM CoPad match in ME1b: bx_alct = " << bx_alct << std::endl << std::endl;
          }
          catch (const std::out_of_range& oor) {
            if (print_available_pads) std::cout << "\t++No valid GEM CoPads in BX: " << bx_alct << std::endl;
            continue;
          }
        }
        if (print_available_pads) 
          std::cout << "------------------------------------------------------------------------" << std::endl << std::endl;
      }
      if (print_available_pads) {
        std::cout << "========================================================================" << std::endl;
        std::cout << "Summary: " << std::endl;
        if (nSuccesFulMatches>1)
          std::cout << "Too many successful ALCT-CLCT matches in ME1b: " << nSuccesFulMatches
                    << ", CSCDetId " << cscChamber->id()
                    << ", bx_alct = " << bx_alct
                    << "; match window: [" << bx_clct_start << "; " << bx_clct_stop << "]" << std::endl;
        else if (nSuccesFulMatches==1)
          std::cout << "1 successful ALCT-CLCT match in ME1b: " 
                    << " CSCDetId " << cscChamber->id()
                    << ", bx_alct = " << bx_alct
                    << "; match window: [" << bx_clct_start << "; " << bx_clct_stop << "]" << std::endl;
        else if (nSuccesFulGEMMatches==1)
          std::cout << "1 successful ALCT-GEM match in ME1b: " 
                    << " CSCDetId " << cscChamber->id()
                    << ", bx_alct = " << bx_alct
                    << "; match window: [" << bx_clct_start << "; " << bx_clct_stop << "]" << std::endl;
        else 
          std::cout << "Unsuccessful ALCT-CLCT match in ME1b: " 
                    << "CSCDetId " << cscChamber->id()
                    << ", bx_alct = " << bx_alct
                    << "; match window: [" << bx_clct_start << "; " << bx_clct_stop << "]" << std::endl;
      }
      
      if (print_available_pads) {
        std::cout << "------------------------------------------------------------------------" << std::endl;
        std::cout << "Attempt ALCT-CLCT matching in ME1/a in bx range: [" << bx_clct_start << "," << bx_clct_stop << "]" << std::endl;
      }

      // matching in ME1a
      nSuccesFulMatches = 0;
      nSuccesFulGEMMatches = 0;
      for (int bx_clct = bx_clct_start; bx_clct <= bx_clct_stop; bx_clct++)
      {
        if (bx_clct < 0 or bx_clct >= CSCCathodeLCTProcessor::MAX_CLCT_BINS) continue;
        if (drop_used_clcts and used_clct_mask_1a[bx_clct]) continue;
        if (clct1a->bestCLCT[bx_clct].isValid())
          {
            ++nSuccesFulMatches;
            if (infoV > 1) LogTrace("CSCMotherboard")
              << "Successful ALCT-CLCT match in ME1a: bx_alct = " << bx_alct
              << "; match window: [" << bx_clct_start << "; " << bx_clct_stop
              << "]; bx_clct = " << bx_clct << std::endl;
            if (infoV > 1) LogTrace("CSCMotherboard")
              << "Successful ALCT-CLCT match in ME1a: bx_alct = " << bx_alct
              << "; match window: [" << bx_clct_start << "; " << bx_clct_stop
              << "]; bx_clct = " << bx_clct;
            int mbx = bx_clct-bx_clct_start;
            correlateLCTs(alct->bestALCT[bx_alct], alct->secondALCT[bx_alct],
                          clct1a->bestCLCT[bx_clct], clct1a->secondCLCT[bx_clct],
                          allLCTs1a[bx_alct][mbx][0], allLCTs1a[bx_alct][mbx][1], ME1A);
            if (allLCTs1a[bx_alct][mbx][0].isValid()){
              used_clct_mask_1a[bx_clct] += 1;
              if (match_earliest_clct_me11_only) break;
            }
          }
        else {
          if (print_available_pads) std::cout << "++Not a valid CLCT in BX: " << bx_clct << std::endl;
          if (buildLCTfromALCTandGEM_overlap_) continue;
          // Try to build an ME1/a LCT out of an ALCT and a GEM Co-Pad in the overlap region
          if (10 > alct->bestALCT[bx_alct].getKeyWG() or alct->bestALCT[bx_alct].getKeyWG() > 15) continue;
          if (!hasCoPads) continue;
          
          // find the best matching copad - first one 
          try {
            auto copads(matchingGEMPads(alct->bestALCT[bx_alct], coPads_[bx_clct]));             
            if (print_available_pads) std::cout << "++Number of matching GEM CoPads in BX " << bx_alct << " : "<< copads.size() << std::endl;
            
            ++nSuccesFulGEMMatches;            
            correlateLCTsGEM(alct->bestALCT[bx_alct], alct->secondALCT[bx_alct],
                             *(copads.at(0)).second, allLCTs1a[bx_alct][0][0], allLCTs1a[bx_alct][0][1]);
            if (allLCTs1a[bx_alct][0][0].isValid()) {
              if (match_earliest_clct_me11_only) break;
            }
            if (print_available_pads) 
              std::cout << "Successful ALCT-GEM CoPad match in ME1a: bx_alct = " << bx_alct << std::endl << std::endl;
          }
          catch (const std::out_of_range& oor) {
            if (print_available_pads) std::cout << "\t++No valid GEM CoPads in BX: " << bx_alct << std::endl;
            continue;
          }
        }
      }
      if (print_available_pads) {
        std::cout << "========================================================================" << std::endl;
        std::cout << "Summary: " << std::endl;
        if (nSuccesFulMatches>1)
          std::cout << "Too many successful ALCT-CLCT matches in ME1a: " << nSuccesFulMatches
                    << ", CSCDetId " << cscChamber->id()
                    << ", bx_alct = " << bx_alct
                    << "; match window: [" << bx_clct_start << "; " << bx_clct_stop << "]" << std::endl;
        else if (nSuccesFulMatches==1)
          std::cout << "1 successful ALCT-CLCT match in ME1a: " 
                    << " CSCDetId " << cscChamber->id()
                    << ", bx_alct = " << bx_alct
                    << "; match window: [" << bx_clct_start << "; " << bx_clct_stop << "]" << std::endl;
        else if (nSuccesFulGEMMatches==1)
          std::cout << "1 successful ALCT-GEM match in ME1a: " 
                    << " CSCDetId " << cscChamber->id()
                    << ", bx_alct = " << bx_alct
                    << "; match window: [" << bx_clct_start << "; " << bx_clct_stop << "]" << std::endl;
        else 
          std::cout << "Unsuccessful ALCT-CLCT match in ME1a: " 
                    << "CSCDetId " << cscChamber->id()
                    << ", bx_alct = " << bx_alct
                    << "; match window: [" << bx_clct_start << "; " << bx_clct_stop << "]" << std::endl;
      }
    }
  } // end of ALCT-centric matching

  // possibly use some discrimination from GEMs
  if (gemGeometryAvailable and do_gem_matching) matchGEMPads();

  // reduction of nLCTs per each BX
  for (int bx = 0; bx < MAX_LCT_BINS; bx++)
  {
    // counting
    unsigned int n1a=0, n1b=0;
    for (unsigned int mbx = 0; mbx < match_trig_window_size; mbx++)
      for (int i=0;i<2;i++)
      {
        int cbx = bx + mbx - match_trig_window_size/2;
        if (allLCTs1b[bx][mbx][i].isValid())
        {
          n1b++;
          if (infoV > 0) LogDebug("CSCMotherboard") << "1b LCT"<<i+1<<" "<<bx<<"/"<<cbx<<": "<<allLCTs1b[bx][mbx][i];
        }
        if (allLCTs1a[bx][mbx][i].isValid())
        {
          n1a++;
          if (infoV > 0) LogDebug("CSCMotherboard") << "1a LCT"<<i+1<<" "<<bx<<"/"<<cbx<<": "<<allLCTs1a[bx][mbx][i];
        }
      }
    if (infoV > 0 and n1a+n1b>0) LogDebug("CSCMotherboard") <<"bx "<<bx<<" nLCT:"<<n1a<<" "<<n1b<<" "<<n1a+n1b;

    // some simple cross-bx sorting algorithms
    if (tmb_cross_bx_algo == 1 and (n1a>2 or n1b>2) )
    {
      n1a=0, n1b=0;
      for (unsigned int mbx = 0; mbx < match_trig_window_size; mbx++)
        for (int i=0;i<2;i++)
        {
          if (allLCTs1b[bx][pref[mbx]][i].isValid())
          {
            n1b++;
            if (n1b>2) allLCTs1b[bx][pref[mbx]][i].clear();
          }
          if (allLCTs1a[bx][pref[mbx]][i].isValid())
          {
            n1a++;
            if (n1a>2) allLCTs1a[bx][pref[mbx]][i].clear();
          }
        }

      if (infoV > 0) LogDebug("CSCMotherboard") <<"After x-bx sorting:";
      n1a=0, n1b=0;
      for (unsigned int mbx = 0; mbx < match_trig_window_size; mbx++)
        for (int i=0;i<2;i++)
        {
          int cbx = bx + mbx - match_trig_window_size/2;
          if (allLCTs1b[bx][mbx][i].isValid())
          {
            n1b++;
            if (infoV > 0) LogDebug("CSCMotherboard") << "1b LCT"<<i+1<<" "<<bx<<"/"<<cbx<<": "<<allLCTs1b[bx][mbx][i];
          }
          if (allLCTs1a[bx][mbx][i].isValid())
          {
            n1a++;
            if (infoV > 0) LogDebug("CSCMotherboard") << "1a LCT"<<i+1<<" "<<bx<<"/"<<cbx<<": "<<allLCTs1a[bx][mbx][i];
          }
        }
      if (infoV > 0 and n1a+n1b>0) LogDebug("CSCMotherboard") <<"bx "<<bx<<" nnLCT:"<<n1a<<" "<<n1b<<" "<<n1a+n1b;
    } // x-bx sorting

    // Maximum 2 per whole ME11 per BX case:
    // (supposedly, now we should have max 2 per bx in each 1a and 1b)
    if ( n1a+n1b > max_me11_lcts )
    {
      // do it simple so far: take all low eta 1/b stubs
      unsigned int nLCT=n1b;
      n1a=0;
      // right now nLCT<=2; cut 1a if necessary
      for (unsigned int mbx=0; mbx<match_trig_window_size; mbx++)
        for (int i=0;i<2;i++)
          if (allLCTs1a[bx][mbx][i].isValid()) {
            nLCT++;
            if (nLCT>max_me11_lcts) allLCTs1a[bx][mbx][i].clear();
            else n1a++;
          }
      if (infoV > 0 and nLCT>0) LogDebug("CSCMotherboard") <<"bx "<<bx<<" nnnLCT:"<<n1a<<" "<<n1b<<" "<<n1a+n1b;
    }
  }// reduction per bx

//   if (infoV > 1) LogTrace("CSCMotherboardME11")<<"clct_count E:"<<theEndcap<<"S:"<<theStation<<"R:"<<1<<"C:"
// 					       <<CSCTriggerNumbering::chamberFromTriggerLabels(theSector,theSubsector, theStation, theTrigChamber)
// 					       <<"  a "<<n_clct_a<<"  b "<<n_clct_b<<"  ab "<<n_clct_a+n_clct_b;
}

void CSCMotherboardME11::runNewAlgorithm(const CSCWireDigiCollection* wiredc,
					 const CSCComparatorDigiCollection* compdc,
					 const GEMCSCPadDigiCollection* gemPads)
{
}


std::vector<CSCCorrelatedLCTDigi> CSCMotherboardME11::readoutLCTs1a()
{
  return readoutLCTs(ME1A);
}


std::vector<CSCCorrelatedLCTDigi> CSCMotherboardME11::readoutLCTs1b()
{
  return readoutLCTs(ME1B);
}


// Returns vector of read-out correlated LCTs, if any.  Starts with
// the vector of all found LCTs and selects the ones in the read-out
// time window.
std::vector<CSCCorrelatedLCTDigi> CSCMotherboardME11::readoutLCTs(int me1ab)
{
  std::vector<CSCCorrelatedLCTDigi> tmpV;

  // The start time of the L1A*LCT coincidence window should be related
  // to the fifo_pretrig parameter, but I am not completely sure how.
  // Just choose it such that the window is centered at bx=7.  This may
  // need further tweaking if the value of tmb_l1a_window_size changes.
  //static int early_tbins = 4;
  // The number of LCT bins in the read-out is given by the
  // tmb_l1a_window_size parameter, forced to be odd
  static int lct_bins   = 
    (tmb_l1a_window_size % 2 == 0) ? tmb_l1a_window_size + 1 : tmb_l1a_window_size;
  static int late_tbins = early_tbins + lct_bins;


  // Start from the vector of all found correlated LCTs and select
  // those within the LCT*L1A coincidence window.
  int bx_readout = -1;
  std::vector<CSCCorrelatedLCTDigi> all_lcts;
  if (me1ab == ME1A) all_lcts = getLCTs1a();
  if (me1ab == ME1B) all_lcts = getLCTs1b();
  std::vector <CSCCorrelatedLCTDigi>::const_iterator plct = all_lcts.begin();
  for (; plct != all_lcts.end(); plct++)
  {
    if (!plct->isValid()) continue;

    int bx = (*plct).getBX();
    // Skip LCTs found too early relative to L1Accept.
    if (bx <= early_tbins) continue;

    // Skip LCTs found too late relative to L1Accept.
    if (bx > late_tbins) continue;

    // If (readout_earliest_2) take only LCTs in the earliest bx in the read-out window:
    // in digi->raw step, LCTs have to be packed into the TMB header, and
    // currently there is room just for two.
    if (readout_earliest_2 and (bx_readout == -1 or bx == bx_readout) )
    {
      tmpV.push_back(*plct);
      if (bx_readout == -1) bx_readout = bx;
    }
    else tmpV.push_back(*plct);
  }
  return tmpV;
}


// Returns vector of found correlated LCTs, if any.
std::vector<CSCCorrelatedLCTDigi> CSCMotherboardME11::getLCTs1b()
{
  std::vector<CSCCorrelatedLCTDigi> tmpV;

  for (int bx = 0; bx < MAX_LCT_BINS; bx++) 
    for (unsigned int mbx = 0; mbx < match_trig_window_size; mbx++)
      for (int i=0;i<2;i++)
        if (allLCTs1b[bx][mbx][i].isValid()) tmpV.push_back(allLCTs1b[bx][mbx][i]);
  return tmpV;
}

// Returns vector of found correlated LCTs, if any.
std::vector<CSCCorrelatedLCTDigi> CSCMotherboardME11::getLCTs1a()
{
  std::vector<CSCCorrelatedLCTDigi> tmpV;
  
  // disabled ME1a
  if (mpc_block_me1a or disableME1a) return tmpV;

  // Report all LCTs found.
  for (int bx = 0; bx < MAX_LCT_BINS; bx++)
    for (unsigned int mbx = 0; mbx < match_trig_window_size; mbx++) 
      for (int i=0;i<2;i++)
        if (allLCTs1a[bx][mbx][i].isValid())  tmpV.push_back(allLCTs1a[bx][mbx][i]);
  return tmpV;
}


bool CSCMotherboardME11::doesALCTCrossCLCT(CSCALCTDigi &a, CSCCLCTDigi &c, int me)
{
  if ( !c.isValid() or !a.isValid() ) return false;
  int key_hs = c.getKeyStrip();
  int key_wg = a.getKeyWG();
  if ( me == ME1A )
  {
    if ( !gangedME1a )
    {
      // wrap around ME11 HS number for -z endcap
      if (theEndcap==2) key_hs = 95 - key_hs;
      if ( key_hs >= lut_wg_vs_hs_me1a[key_wg][0] and 
           key_hs <= lut_wg_vs_hs_me1a[key_wg][1]    ) return true;
      return false;
    }
    else
    {
      if (theEndcap==2) key_hs = 31 - key_hs;
      if ( key_hs >= lut_wg_vs_hs_me1ag[key_wg][0] and
           key_hs <= lut_wg_vs_hs_me1ag[key_wg][1]    ) return true;
      return false;
    }
  }
  if ( me == ME1B)
  {
    if (theEndcap==2) key_hs = 127 - key_hs;
    if ( key_hs >= lut_wg_vs_hs_me1b[key_wg][0] and 
         key_hs <= lut_wg_vs_hs_me1b[key_wg][1]      ) return true;
  }
  return false;
}

void CSCMotherboardME11::correlateLCTs(CSCALCTDigi bestALCT,
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


void CSCMotherboardME11::correlateLCTsGEM(CSCALCTDigi bestALCT,
					  CSCALCTDigi secondALCT,
					  GEMCSCPadDigi gemPad,
					  CSCCorrelatedLCTDigi& lct1,
					  CSCCorrelatedLCTDigi& lct2)
{
  bool anodeBestValid     = bestALCT.isValid();
  bool anodeSecondValid   = secondALCT.isValid();

  if (anodeBestValid and !anodeSecondValid)     secondALCT = bestALCT;
  if (!anodeBestValid and anodeSecondValid)     bestALCT   = secondALCT;

  if ((alct_trig_enable  and bestALCT.isValid()) or
      (match_trig_enable and bestALCT.isValid()))
  {
    lct1 = constructLCTsGEM(bestALCT, gemPad);
    lct1.setTrknmb(1);
  }

  if ((alct_trig_enable  and secondALCT.isValid()) or
      (match_trig_enable and secondALCT.isValid() and secondALCT != bestALCT))
    {
    lct2 = constructLCTsGEM(secondALCT, gemPad);
    lct2.setTrknmb(2);
  }
}

void CSCMotherboardME11::correlateLCTsGEM(CSCCLCTDigi bestCLCT,
					  CSCCLCTDigi secondCLCT,
					  GEMCSCPadDigi gemPad,
					  CSCCorrelatedLCTDigi& lct1,
					  CSCCorrelatedLCTDigi& lct2)
{
  bool cathodeBestValid     = bestCLCT.isValid();
  bool cathodeSecondValid   = secondCLCT.isValid();

  if (cathodeBestValid and !cathodeSecondValid)     secondCLCT = bestCLCT;
  if (!cathodeBestValid and cathodeSecondValid)     bestCLCT   = secondCLCT;

  if ((clct_trig_enable  and bestCLCT.isValid()) or
      (match_trig_enable and bestCLCT.isValid()))
  {
    lct1 = constructLCTsGEM(bestCLCT, gemPad);
    lct1.setTrknmb(1);
  }

  if ((clct_trig_enable  and secondCLCT.isValid()) or
       (match_trig_enable and secondCLCT.isValid() and secondCLCT != bestCLCT))
    {
    lct2 = constructLCTsGEM(secondCLCT, gemPad);
    lct2.setTrknmb(2);
  }
}

void CSCMotherboardME11::correlateLCTs(CSCALCTDigi bestALCT,
				       CSCALCTDigi secondALCT,
				       CSCCLCTDigi bestCLCT,
				       CSCCLCTDigi secondCLCT,
				       CSCCorrelatedLCTDigi& lct1,
				       CSCCorrelatedLCTDigi& lct2,
               int me, const GEMPadsBX& pads, const GEMPadsBX& copads)
{
  // assume that always anodeBestValid and cathodeBestValid
  
  if (secondALCT == bestALCT) secondALCT.clear();
  if (secondCLCT == bestCLCT) secondCLCT.clear();

  int ok11 = doesALCTCrossCLCT( bestALCT, bestCLCT, me);
  int ok12 = doesALCTCrossCLCT( bestALCT, secondCLCT, me);
  int ok21 = doesALCTCrossCLCT( secondALCT, bestCLCT, me);
  int ok22 = doesALCTCrossCLCT( secondALCT, secondCLCT, me);
  int code = (ok11<<3) | (ok12<<2) | (ok21<<1) | (ok22);

  int dbg=0;
  int ring = me;
  int chamb= CSCTriggerNumbering::chamberFromTriggerLabels(theSector,theSubsector, theStation, theTrigChamber);
  CSCDetId did(theEndcap, theStation, ring, chamb, 0);
  if (dbg) LogTrace("CSCMotherboardME11")<<"debug correlateLCTs in "<<did<<std::endl
	   <<"ALCT1: "<<bestALCT<<std::endl
	   <<"ALCT2: "<<secondALCT<<std::endl
	   <<"CLCT1: "<<bestCLCT<<std::endl
	   <<"CLCT2: "<<secondCLCT<<std::endl
	   <<"ok 11 12 21 22 code = "<<ok11<<" "<<ok12<<" "<<ok21<<" "<<ok22<<" "<<code<<std::endl;

  if ( code==0 ) return;

  // LUT defines correspondence between possible ok## combinations
  // and resulting lct1 and lct2
  int lut[16][2] = {
          //ok: 11 12 21 22
    {0 ,0 }, // 0  0  0  0
    {22,0 }, // 0  0  0  1
    {21,0 }, // 0  0  1  0
    {21,22}, // 0  0  1  1
    {12,0 }, // 0  1  0  0
    {12,22}, // 0  1  0  1
    {12,21}, // 0  1  1  0
    {12,21}, // 0  1  1  1
    {11,0 }, // 1  0  0  0
    {11,22}, // 1  0  0  1
    {11,21}, // 1  0  1  0
    {11,22}, // 1  0  1  1
    {11,12}, // 1  1  0  0
    {11,22}, // 1  1  0  1
    {11,12}, // 1  1  1  0
    {11,22}, // 1  1  1  1
  };

  if (dbg) LogTrace("CSCMotherboardME11")<<"lut 0 1 = "<<lut[code][0]<<" "<<lut[code][1]<<std::endl;

  // first check the special case (11,22) where we have an ambiguity
  const int nPads(pads.size());
  const int nCoPads(copads.size());
  const bool hasPads(nPads!=0);
  const bool hasCoPads(nCoPads!=0);
  
  if (doLCTGhostBustingWithGEMs_ and (lut[code][0] == 11) and (lut[code][0] == 22) and hasPads and (me==ME1B)){

    if (print_available_pads) std::cout << "++Info: 2 valid ALCTs-CLCTs pairs with trigger pads. Call the GHOSTBUSTERS!!!" << std::endl;    
    // first check if there are any copads
    typedef std::pair<int,int> mypair;
    // for each trigger pad, store (deltaRoll,deltaHS) for 11,22,12 and 21.
    std::vector<std::tuple<mypair,mypair,mypair,mypair>> deltas;
    deltas.clear();

    if (hasCoPads){
      for (auto p : copads) {
        const GEMDetId detId(p.first);
        const int rollN(detId.roll());
        const int padN((p.second)->pad());
        
        auto t11(std::make_pair(deltaRoll(  bestALCT.getKeyWG(), rollN), deltaPad(  bestCLCT.getKeyStrip(), padN)));
        auto t22(std::make_pair(deltaRoll(secondALCT.getKeyWG(), rollN), deltaPad(secondCLCT.getKeyStrip(), padN)));
        auto t12(std::make_pair(deltaRoll(  bestALCT.getKeyWG(), rollN), deltaPad(secondCLCT.getKeyStrip(), padN)));
        auto t21(std::make_pair(deltaRoll(secondALCT.getKeyWG(), rollN), deltaPad(  bestCLCT.getKeyStrip(), padN)));

        deltas.push_back(std::make_tuple(t11,t22,t12,t21));
      }
      if (print_available_pads){
        std::cout << "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " << std::endl;
        std::cout << "Printing (deltaRoll, deltaPad) for each (ALCT,CLCT) pair and for each trigger copad" << std::endl;
        for (unsigned i =0; i < deltas.size(); ++i){
          auto c(deltas.at(i));
          std::cout << "\tCoPad " << i << std::endl;
          std::cout << "\t11: " << "(" << std::get<0>(c).first << "," << std::get<0>(c).second << "); "
                    << "22: "   << "(" << std::get<1>(c).first << "," << std::get<1>(c).second << "); " 
                    << "12: "   << "(" << std::get<2>(c).first << "," << std::get<2>(c).second << "); "
                    << "21: "   << "(" << std::get<3>(c).first << "," << std::get<3>(c).second << ")" << std::endl << std::endl;
        }
        std::cout << "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " << std::endl;
      }
      
      
//      lct1 = constructLCTs(bestALCT, bestCLCT);
//      lct1.setTrknmb(1);
//      lct2 = constructLCTs(secondALCT, secondCLCT);
//      lct2.setTrknmb(2);
  
//      lct1 = constructLCTs(bestALCT, secondCLCT);
//      lct1.setTrknmb(1);
//      lct2 = constructLCTs(secondLCT, bestCLCT);
//      lct2.setTrknmb(2);
      return;
    }

    // if no copads were found, do the same with pads...
    if (hasPads){
      for (auto p : pads) {
        const GEMDetId detId(p.first);
        const int rollN(detId.roll());
        const int padN((p.second)->pad());
        
        auto t11(std::make_pair(deltaRoll(  bestALCT.getKeyWG(), rollN), deltaPad(  bestCLCT.getKeyStrip(), padN)));
        auto t22(std::make_pair(deltaRoll(secondALCT.getKeyWG(), rollN), deltaPad(secondCLCT.getKeyStrip(), padN)));
        auto t12(std::make_pair(deltaRoll(  bestALCT.getKeyWG(), rollN), deltaPad(secondCLCT.getKeyStrip(), padN)));
        auto t21(std::make_pair(deltaRoll(secondALCT.getKeyWG(), rollN), deltaPad(  bestCLCT.getKeyStrip(), padN)));

        deltas.push_back(std::make_tuple(t11,t22,t12,t21));
      }
      if (print_available_pads){
        std::cout << "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " << std::endl;
        std::cout << "Printing (deltaRoll, deltaPad) for each (ALCT,CLCT) pair and for each trigger pad" << std::endl;
        for (unsigned i =0; i < deltas.size(); ++i){
          auto c(deltas.at(i));
          std::cout << "\tPad " << i << std::endl;
          std::cout << "\t11: " << "(" << std::get<0>(c).first << "," << std::get<0>(c).second << "); "
                    << "22: "   << "(" << std::get<1>(c).first << "," << std::get<1>(c).second << "); " 
                    << "12: "   << "(" << std::get<2>(c).first << "," << std::get<2>(c).second << "); "
                    << "21: "   << "(" << std::get<3>(c).first << "," << std::get<3>(c).second << ")" << std::endl << std::endl;
        }
        std::cout << "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " << std::endl;
      }

      return;
    }
  }

  switch (lut[code][0]) {
    case 11:
      lct1 = constructLCTs(bestALCT, bestCLCT);
      break;
    case 12:
      lct1 = constructLCTs(bestALCT, secondCLCT);
      break;
    case 21:
      lct1 = constructLCTs(secondALCT, bestCLCT);
      break;
    case 22:
      lct1 = constructLCTs(secondALCT, secondCLCT);
      break;
    default: return;  
  }
  lct1.setTrknmb(1);

  if (dbg) LogTrace("CSCMotherboardME11")<<"lct1: "<<lct1<<std::endl;
  
  switch (lut[code][1])
  {
    case 12:
      lct2 = constructLCTs(bestALCT, secondCLCT);
      lct2.setTrknmb(2);
      if (dbg) LogTrace("CSCMotherboardME11")<<"lct2: "<<lct2<<std::endl;
      return;
    case 21:
      lct2 = constructLCTs(secondALCT, bestCLCT);
      lct2.setTrknmb(2);
      if (dbg) LogTrace("CSCMotherboardME11")<<"lct2: "<<lct2<<std::endl;
      return;
    case 22:
      lct2 = constructLCTs(secondALCT, secondCLCT);
      lct2.setTrknmb(2);
      if (dbg) LogTrace("CSCMotherboardME11")<<"lct2: "<<lct2<<std::endl;
      return;
    default: return;
  }
  if (dbg) LogTrace("CSCMotherboardME11")<<"out of correlateLCTs"<<std::endl;

  return;
}

void CSCMotherboardME11::matchGEMPads()
{
  using namespace std;

  // check if we have any LCTs at all
  int nlct = 0;
  for (int bx = 0; bx < MAX_LCT_BINS; bx++)
    for (unsigned int mbx = 0; mbx < match_trig_window_size; mbx++)
      for (int i=0;i<2;i++)
      {
        CSCCorrelatedLCTDigi& lct = allLCTs1b[bx][mbx][i];
        if (lct.isValid()) nlct++;
      }
  if (nlct == 0) return;

  // retrieve CSCChamber geometry
  CSCTriggerGeomManager* geo_manager = CSCTriggerGeometry::get();
  CSCChamber* cscChamber = geo_manager->chamber(theEndcap, theStation, theSector, theSubsector, theTrigChamber);

  auto csc_id = cscChamber->id();
  int chamber = csc_id.chamber();
  bool is_odd = chamber & 1;

  if (debug_gem_matching) std::cout<<"++++++++  matchGEMPads "<< csc_id <<" +++++++++ "<<std::endl;

  // "key" layer id is used to calculate global position of stub
  CSCDetId key_id(csc_id.endcap(), csc_id.station(), csc_id.ring(), csc_id.chamber(), CSCConstants::KEY_CLCT_LAYER);

  // check if there are any pads 
  if (pads_.empty()) {
    if (debug_gem_matching) std::cout<<"igotnopads"<<std::endl;
    return;
  }

  // walk over BXs
  for (int bx = 0; bx < MAX_LCT_BINS; ++bx)
  {
    auto in_pads = pads_.find(bx);

    // walk over potential LCTs in this BX
    for (unsigned int mbx = 0; mbx < match_trig_window_size; ++mbx)
      for (int i=0; i<2; ++i)
      {
        CSCCorrelatedLCTDigi& lct = allLCTs1b[bx][mbx][i];
        if (!lct.isValid()) continue;
        if (debug_gem_matching) std::cout<<"LCTbefore "<<bx<<" "<<mbx<<" "<<i<<" "<<lct;

        // use -99 as default value whe we don't know if there could have been a gem match
        lct.setGEMDPhi(-99.);

        // "strip" here is actually a half-strip in geometry's terms
        // note that LCT::getStrip() starts from 0
        float fractional_strip = 0.5 * (lct.getStrip() + 1) - 0.25;
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

        if (in_pads == pads_.end()) // has no potential GEM hits with similar BX -> zap it
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
              ( (  is_odd and std::abs(dphi) <= gem_match_delta_phi_odd ) or
                ( !is_odd and std::abs(dphi) <= gem_match_delta_phi_even ) ) and // within delta_phi
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
	  int oddEven = int(not is_odd) + 1;
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
	  if (debug_gem_matching) std::cout<<"found bend angle "<<abs(min_dphi)<<" "<<lct.getGEMDPhiBits()<<" "<<lut_pt_vs_dphi_gemcsc[iFound][oddEven]<<" "<<iFound << std::endl;
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
  int nlct_after = 0;
  for (int bx = 0; bx < MAX_LCT_BINS; bx++)
    for (unsigned int mbx = 0; mbx < match_trig_window_size; mbx++)
      for (int i=0;i<2;i++)
      {
        if (allLCTs1b[bx][mbx][i].isValid()) nlct_after++;
      }
  if (debug_gem_matching) std::cout<<"before "<<nlct<<"  after "<<nlct_after<<std::endl;
}


void CSCMotherboardME11::buildCoincidencePads(const GEMCSCPadDigiCollection* out_pads,
					      GEMCSCPadDigiCollection& out_co_pads,
					      int deltaPad, int deltaRoll)
{
  // build coincidences
  for (auto det_range = out_pads->begin(); det_range != out_pads->end(); ++det_range) {
    const GEMDetId& id = (*det_range).first;
    
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
	if (std::abs(p->pad() - co_p->pad()) > deltaPad) continue;
	// check the match in BX
	if (std::abs(p->bx() - co_p->bx()) > maxPadDeltaBX_ ) continue;
	
	// always use layer1 pad's BX as a copad's BX
	GEMCSCPadDigi co_pad_digi(p->pad(), p->bx());
	out_co_pads.insertDigi(id, co_pad_digi);
      }
    }
  }
}


void CSCMotherboardME11::createGEMPadLUT(bool isEven)
{
  // all GE1/1 chambers are equal
  if (!gem_g) return;
  int ch(isEven ? 2 : 1);
  auto chamber(gem_g->chamber(GEMDetId(1,1,1,1,ch,0)));
  if (chamber==nullptr) return;

  for(int i = 1; i<= chamber->nEtaPartitions(); ++i){
    auto roll(chamber->etaPartition(i));
    if (roll==nullptr) continue;

    const float half_striplength(roll->specs()->specificTopology().stripLength()/2.);
    const LocalPoint lp_top(0., half_striplength+0.025, 0.);
    const LocalPoint lp_bottom(0., -half_striplength-0.025, 0.);
    const GlobalPoint gp_top(roll->toGlobal(lp_top));
    const GlobalPoint gp_bottom(roll->toGlobal(lp_bottom));
    gemPadToEtaLimits_[i] = std::make_pair(gp_top.eta(), gp_bottom.eta());
  }
}


int CSCMotherboardME11::assignGEMRoll(double eta)
{
  int result = -99;
  for(auto p : gemPadToEtaLimits_) {
    const float minEta((p.second).first);
    const float maxEta((p.second).second);
    // apply some smearing to take into account vertex displacement
    if ((minEta - 0.025) <= eta and eta <= (maxEta + 0.025)) {
      result = p.first;
      break;
    }
  }
  return result;
}


CSCCorrelatedLCTDigi CSCMotherboardME11::constructLCTsGEM(const CSCALCTDigi& alct,
                                                          const GEMCSCPadDigi& gem, bool oldDataFormat) 
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
  else {
    // CLCT pattern number - no pattern
    unsigned int pattern = 0;

    // LCT quality number
    unsigned int quality = 1;
    
    // Bunch crossing
    int bx = alct.getBX();
    
    // get keyStrip from LUT
    int keyStrip = gemPadToCscHs_[gem.pad()];

    // construct correlated LCT; temporarily assign track number of 0.
    return CSCCorrelatedLCTDigi(0, 1, quality, alct.getKeyWG(), keyStrip, pattern, 0, bx, 0, 0, 0, theTrigChamber);
  }
}

CSCCorrelatedLCTDigi CSCMotherboardME11::constructLCTsGEM(const CSCCLCTDigi& clct,
                                                          const GEMCSCPadDigi& gem, bool oldDataFormat) 
{
  if (oldDataFormat){
    // CLCT pattern number - no pattern
    unsigned int pattern = encodePatternGEM(clct.getPattern(), clct.getStripType());
    
    // LCT quality number -  dummy quality
    unsigned int quality = 5;//findQualityGEM(alct, gem);
    
    // Bunch crossing: get it from cathode LCT if anode LCT is not there.
    int bx = gem.bx();
    
    // pick a random WG
    int wg();
    
    // construct correlated LCT; temporarily assign track number of 0.
    return CSCCorrelatedLCTDigi(0, 1, quality, 0, 0, pattern, 0, bx, 0, 0, 0, theTrigChamber);
  }
  else {
    // CLCT pattern number - no pattern
    unsigned int pattern = encodePatternGEM(clct.getPattern(), clct.getStripType());
    
    // LCT quality number -  dummy quality
    unsigned int quality = 5;//findQualityGEM(alct, gem);
    
    // Bunch crossing: get it from cathode LCT if anode LCT is not there.
    int bx = gem.bx();
    
    // ALCT WG
    int wg();
    
    // construct correlated LCT; temporarily assign track number of 0.
    return CSCCorrelatedLCTDigi(0, 1, quality, 0, 0, pattern, 0, bx, 0, 0, 0, theTrigChamber);
  }
}

unsigned int CSCMotherboardME11::encodePatternGEM(const int ptn, const int highPt)
{
  return 0;
}

unsigned int CSCMotherboardME11::findQualityGEM(const CSCALCTDigi& aLCT, const GEMCSCPadDigi& gem)
{
  return 0;
}

unsigned int CSCMotherboardME11::findQualityGEM(const CSCCLCTDigi& cLCT, const GEMCSCPadDigi& gem)
{
  return 0;
}
 
void CSCMotherboardME11::printGEMTriggerPads(int bx_start, int bx_stop, bool iscopad)
{
  // pads or copads?
  auto thePads(!iscopad ? pads_ : coPads_); 
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
        if (isPadInOverlap(roll_id.roll())) std::cout << " (in overlap)" << std::endl;
        else std::cout << std::endl;
      }
    }
    else
      break;
  }
}

void CSCMotherboardME11::retrieveGEMPads(const GEMCSCPadDigiCollection* gemPads, unsigned id, bool iscopad)
{
  auto superChamber(gem_g->superChamber(id));
  for (auto ch : superChamber->chambers()) {
    for (auto roll : ch->etaPartitions()) {
      GEMDetId roll_id(roll->id());
      auto pads_in_det = gemPads->get(roll_id);
      for (auto pad = pads_in_det.first; pad != pads_in_det.second; ++pad) {
        auto id_pad = std::make_pair(roll_id(), &(*pad));
        const int bx_shifted(lct_central_bx + pad->bx());
        for (int bx = bx_shifted - gem_match_delta_bx;bx <= bx_shifted + gem_match_delta_bx; ++bx) {
          if (iscopad){
            if(bx != lct_central_bx) continue;
            coPads_[bx].push_back(id_pad);  
          }else{
            pads_[bx].push_back(id_pad);  
          }
        }
      }
    }
  }
}

void CSCMotherboardME11::collectGEMPads(const GEMCSCPadDigiCollection* gemPads, const GEMCSCPadDigiCollection* gemCoPads, unsigned id)
{
  auto superChamber(gem_g->superChamber(id));
  for (auto ch : superChamber->chambers()) {
    for (auto roll : ch->etaPartitions()) {
      GEMDetId roll_id(roll->id());
      /// pads
      auto pads_in_det = gemPads->get(roll_id);
      /// copads
      auto copads_in_det = gemCoPads->get(roll_id);

      for (auto pad = pads_in_det.first; pad != pads_in_det.second; ++pad) {

        
        bool padIsCoPad(false);
        bool firstPadIsCoPad(false);

        if (roll_id.layer()==1){
          // first check for pads in layer 1 if they don't occur in the copad collection
          std::cout << "pad " << *(pad) << "checking for copad " << std::endl;
          for (auto copad = copads_in_det.first; copad != copads_in_det.second; ++copad) {
            std::cout << "\tcopad " << *(copad) << std::endl;
            if (*(copad) == *(pad)){
              std::cout << "\t\tcopad!" << std::endl;
              padIsCoPad = true;
              break;
            }
          }
        }
        else {
          // for pads in 2nd layer, check if pad in 1st layer is there --> copad
          GEMDetId roll_id_1(roll->id().region(), roll->id().ring(), roll->id().station(), 1, roll->id().chamber(), roll->id().roll());
          int bxs[] = {5,6,7}; // take into account timing mismeasurement
          for (auto bx : bxs){
            for (auto p : coPads_[bx]){
              if (roll_id_1 == p.first){
                firstPadIsCoPad = true;
                break;
              }          
            }
          }
        }

        auto id_pad = std::make_pair(roll_id, &(*pad));

        const int bx_shifted(lct_central_bx + pad->bx());
        for (int bx = bx_shifted - gem_match_delta_bx;bx <= bx_shifted + gem_match_delta_bx; ++bx) {
          if (padIsCoPad){
            if(bx != lct_central_bx) continue;
            coPads_[bx].push_back(id_pad);  
          }else{
            if (!firstPadIsCoPad)
              pads_[bx].push_back(id_pad);  
          }
        }
      }
    }
  }
}


bool CSCMotherboardME11::isPadInOverlap(int roll)
{
  for (auto& p : cscWgToGemRoll_) {
    // overlap region are WGs 10-15
    if ((p.first < 10) or (p.first > 15)) continue;
    if (((p.second).first <= roll) and (roll <= (p.second).second)) return true;
  }
  return false;
}


int CSCMotherboardME11::deltaRoll(int wg, int pad)
{
  const auto p(cscWgToGemRoll_[wg]);
  return std::min(std::abs(p.first - pad), std::abs(p.second - pad));
}


int CSCMotherboardME11::deltaPad(int hs, int pad)
{
  const auto p(cscHsToGemPad_[hs]);
  return std::min(std::abs(p.first - pad), std::abs(p.second - pad));
}


CSCMotherboardME11::GEMPadsBX  
CSCMotherboardME11::matchingGEMPads(const CSCCLCTDigi& clct, const GEMPadsBX& pads, bool first)
{
  CSCMotherboardME11::GEMPadsBX result;

  // fetch the low and high pad edges
  const int lowPad(cscHsToGemPad_[clct.getKeyStrip()].first);
  const int highPad(cscHsToGemPad_[clct.getKeyStrip()].second);
  for (auto p: pads){
    auto gPad((p.second)->pad());
    if (lowPad != gPad and gPad != highPad) continue;
    result.push_back(p);
    if (first) return result;
  }
  return result;
}


CSCMotherboardME11::GEMPadsBX 
CSCMotherboardME11::matchingGEMPads(const CSCALCTDigi& alct, const GEMPadsBX& pads, bool first)
{
  CSCMotherboardME11::GEMPadsBX result;
  
  auto alctRoll(cscWgToGemRoll_[alct.getKeyWG()]);
  for (auto p: pads){
    auto padRoll(GEMDetId(p.first).roll());
    if (alctRoll.first == -99 and alctRoll.second == -99) continue;  //invalid region
    else if (alctRoll.first == -99 and padRoll != alctRoll.second) continue; // top of the chamber
    else if (alctRoll.second == -99 and padRoll != alctRoll.first) continue; // bottom of the chamber
    else if ((alctRoll.first != -99 and alctRoll.second != -99) and // center
             (alctRoll.first > padRoll and padRoll > alctRoll.second)) continue;
    result.push_back(p);
    if (first) return result;
  }
  return result;
}


CSCMotherboardME11::GEMPadsBX 
CSCMotherboardME11::matchingGEMPads(const CSCCLCTDigi& clct, const CSCALCTDigi& alct, const GEMPadsBX& pads, bool first)
{
  CSCMotherboardME11::GEMPadsBX result;

  // Fetch the pads matching to ALCTs and CLCTs
  auto padsClct(matchingGEMPads(clct, pads, first));
  auto padsAlct(matchingGEMPads(alct, pads, first));

  // Check if the pads overlap
  for (auto p : padsClct){
    for (auto q: padsAlct){
      // look for exactly the same pads
      if ((p.first == q.first) and (p.second == q.second))
        result.push_back(p);
    }
  }
  return result;
}
