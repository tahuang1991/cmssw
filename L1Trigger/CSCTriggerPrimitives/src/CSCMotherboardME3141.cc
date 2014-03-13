#include <L1Trigger/CSCTriggerPrimitives/src/CSCMotherboardME3141.h>
#include <FWCore/MessageLogger/interface/MessageLogger.h>
#include <DataFormats/MuonDetId/interface/CSCTriggerNumbering.h>
#include <L1Trigger/CSCCommonTrigger/interface/CSCTriggerGeometry.h>
#include <Geometry/RPCGeometry/interface/RPCGeometry.h>

CSCMotherboardME3141::CSCMotherboardME3141(unsigned endcap, unsigned station,
                               unsigned sector, unsigned subsector,
                               unsigned chamber,
                               const edm::ParameterSet& conf) :
  CSCMotherboard(endcap, station, sector, subsector, chamber, conf)
{
  edm::ParameterSet commonParams = conf.getParameter<edm::ParameterSet>("commonParam");
  
  if (!isSLHC) edm::LogError("L1CSCTPEmulatorConfigError")
    << "+++ Upgrade CSCMotherboardME3141 constructed while isSLHC is not set! +++\n";
  
  edm::ParameterSet alctParams = conf.getParameter<edm::ParameterSet>("alctSLHC");
  edm::ParameterSet clctParams = conf.getParameter<edm::ParameterSet>("clctSLHC");
  edm::ParameterSet tmbParams = conf.getParameter<edm::ParameterSet>("tmbSLHC");

  // central bx for LCT is 6 for simulation
  lct_central_bx = tmbParams.getUntrackedParameter<int>("lctCentralBX", 6);

  // upgrade algorithm
  runUpgradeME3141_ = tmbParams.getUntrackedParameter<bool>("runUpgradeME3141",false);
}

CSCMotherboardME3141::~CSCMotherboardME3141() 
{
}


void
CSCMotherboardME3141::run(const CSCWireDigiCollection* wiredc,
			  const CSCComparatorDigiCollection* compdc,
			  const RPCDigiCollection* rpcDigis) 
{
  clear();

  if (!( alct and clct and runUpgradeME3141_))
  {
    if (infoV >= 0) edm::LogError("L1CSCTPEmulatorSetupError")
      << "+++ run() called for non-existing ALCT/CLCT processor! +++ \n";
    return;
  }

  alct->run(wiredc); // run anodeLCT
  clct->run(compdc); // run cathodeLCT

  bool rpcGeometryAvailable(false);
  if (rpc_g != nullptr) {
    if (infoV >= 0) edm::LogInfo("L1CSCTPEmulatorSetupInfo")
      << "+++ run() called for RPC-CSC integrated trigger! +++ \n";
    rpcGeometryAvailable = true;
  }

  if (runUpgradeME3141_ and not rpcGeometryAvailable) {
    if (infoV >= 0) edm::LogError("L1CSCTPEmulatorSetupError")
      << "+++ run() called for RPC-CSC integrated trigger without valid RPC geometry! +++ \n";
    return;
  }

  // retrieve CSCChamber geometry                                                                                                                                       
  //CSCTriggerGeomManager* geo_manager(CSCTriggerGeometry::get());
  //CSCChamber* cscChamber(geo_manager->chamber(theEndcap, theStation, theSector, theSubsector, theTrigChamber));
  //CSCDetId csc_id(cscChamber->id());
  //const CSCLayer* keyLayer(cscChamber->layer(3));
  //const CSCLayerGeometry* keyLayerGeometry(keyLayer->geometry());
}
