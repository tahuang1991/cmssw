#include "L1Trigger/L1TMuon/src/Phase2/L1TDisplacedMuonPtAssignment.h"
#include "Geometry/GEMGeometry/interface/GEMGeometry.h"
#include "Geometry/RPCGeometry/interface/RPCGeometry.h"
#include "Geometry/DTGeometry/interface/DTGeometry.h"
#include "Geometry/CSCGeometry/interface/CSCGeometry.h"
#include "Geometry/GEMGeometry/interface/ME0Geometry.h"

#include "L1Trigger/L1TMuon/src/Phase2/EndcapTriggerPtAssignmentHelper.h"
#include "L1Trigger/L1TMuon/src/Phase2/BarrelTriggerPtAssignmentHelper.h"

#include "iostream"

using namespace L1TMuon;
using namespace EndcapTriggerPtAssignmentHelper;

L1TDisplacedMuonPtAssignment::L1TDisplacedMuonPtAssignment(const edm::ParameterSet& iConfig)
{
  // assignment_.reset(new L1TMuon::L1TDisplacedMuonPtAssignment(iConfig));

  // std::unique_ptr<EndcapTriggerPtAssignmentHelper> endcapHelper_;
  // std::unique_ptr<BarrelTriggerPtAssignmentHelper> barrelHelper_;
}

L1TDisplacedMuonPtAssignment::~L1TDisplacedMuonPtAssignment()
{
}

void L1TDisplacedMuonPtAssignment::calculatePositionPtBarrel(){}
void L1TDisplacedMuonPtAssignment::calculatePositionPtOverlap(){}
void L1TDisplacedMuonPtAssignment::calculatePositionPtEndcap()
{
  EvenOdd123 parity = EndcapTriggerPtAssignmentHelper::getParity(isEven[0], isEven[1],
                                                                 isEven[2], isEven[3]);

  // ignore invalid cases
  // put a warning message here!
  if (parity == EvenOdd123::Invalid)
    return;

  //ddY123 available and also need to consider whether GE21 is used or not!!!  FIXME
  const float ddY123 = EndcapTriggerPtAssignmentHelper::deltadeltaYcalculation(gp_st_layer3[0], gp_st_layer3[1], gp_st_layer3[2],
										  gp_st_layer3[1].eta(), parity);
  // lowest pT assigned
  positionPt_ = 2.0;

  // walk through the DDY LUT and assign the pT that matches
  const int etaSector = EndcapTriggerPtAssignmentHelper::GetEtaPartition_position(gp_ME[1].eta());
  for (int i=0; i<EndcapTriggerPtAssignmentHelper::NPtbins; i++){
    if (std::fabs(ddY123) <= EndcapTriggerPtAssignmentHelper::PositionPtDDYLUT[i][etaSector][int(parity)])
      positionPt_ = float(EndcapTriggerPtAssignmentHelper::PtBins[i]);
    else
      break;
  }
}

void L1TDisplacedMuonPtAssignment::calculateDirectionPtBarrel()
{
  // check case
  int dt_stub_case = 0;//getBarrelStubCase(has_stub_mb1, has_stub_mb2, has_stub_mb3, has_stub_mb4);

  float barrel_direction_pt;

  switch(dt_stub_case){
  case 0:
    barrel_direction_pt = BarrelTriggerPtAssignmentHelper::getDirectionPt2Stubs(dPhi_barrel_dir_12, "DT1_DT2");
    break;
  case 1:
    barrel_direction_pt = BarrelTriggerPtAssignmentHelper::getDirectionPt2Stubs(dPhi_barrel_dir_13, "DT1_DT3");
    break;
  case 2:
    barrel_direction_pt = BarrelTriggerPtAssignmentHelper::getDirectionPt2Stubs(dPhi_barrel_dir_14, "DT1_DT4");
    break;
  case 3:
    barrel_direction_pt = BarrelTriggerPtAssignmentHelper::getDirectionPt2Stubs(dPhi_barrel_dir_23, "DT2_DT3");
    break;
  case 4:
    barrel_direction_pt = BarrelTriggerPtAssignmentHelper::getDirectionPt2Stubs(dPhi_barrel_dir_24, "DT2_DT4");
    break;
  case 5:
    barrel_direction_pt = BarrelTriggerPtAssignmentHelper::getDirectionPt2Stubs(dPhi_barrel_dir_34, "DT3_DT4");
    break;
  case 6:
    // first dphi is x value, second dphi is y value!!!!
    barrel_direction_pt = BarrelTriggerPtAssignmentHelper::getDirectionPt3or4Stubs(dPhi_barrel_dir_12, dPhi_barrel_dir_13, "DT1_DT2__DT1_DT3");
    break;
  case 7:
    barrel_direction_pt = BarrelTriggerPtAssignmentHelper::getDirectionPt3or4Stubs(dPhi_barrel_dir_12, dPhi_barrel_dir_14, "DT1_DT2__DT1_DT4");
    break;
  case 8:
    barrel_direction_pt = BarrelTriggerPtAssignmentHelper::getDirectionPt3or4Stubs(dPhi_barrel_dir_13, dPhi_barrel_dir_14, "DT1_DT3__DT1_DT4");
    break;
  case 9:
    barrel_direction_pt = BarrelTriggerPtAssignmentHelper::getDirectionPt3or4Stubs(dPhi_barrel_dir_23, dPhi_barrel_dir_24, "DT2_DT3__DT2_DT4");
    break;
  case 10:
    barrel_direction_pt = BarrelTriggerPtAssignmentHelper::getDirectionPt3or4Stubs(dPhi_barrel_dir_14, dPhi_barrel_dir_23, "DT1_DT4__DT2_DT3");
    break;
  default:
    // all else fails; assign lowest possible pT
    barrel_direction_pt = 2;
    break;
  };
  std::cout << barrel_direction_pt << std::endl;
}

void L1TDisplacedMuonPtAssignment::calculateDirectionPtOverlap(){}
//Low: eta<2.1, GE11 and GE21 are used 
//high: eta>2.1, GE11 and GE21, ME0 are usd
void L1TDisplacedMuonPtAssignment::calculateDirectionPtEndcap(){
    EvenOdd123 parity = EndcapTriggerPtAssignmentHelper::getParity(isEven[0], isEven[1],//only first two station matters
                                                                 isEven[1], isEven[1]);
    float dPhi_dir_st1_st2 = 99;//add function to calculate dphiM_st1, dphiM_st2
    //dPhi_dir_st1_st2 available, FIXME
    directionPt_ = 2.0;
    int neta = EndcapTriggerPtAssignmentHelper::GetEtaPartition_direction( gp_ME[1].eta() );
    for (int i=0; i<EndcapTriggerPtAssignmentHelper::NPtbins; i++){
	if (std::fabs(dPhi_dir_st1_st2) <= EndcapTriggerPtAssignmentHelper::DirectionbasedLUT[i][neta][int(parity)])
	    directionPt_ = float(EndcapTriggerPtAssignmentHelper::PtBins[i]);
	else
	    break;
    }

}
//void L1TDisplacedMuonPtAssignment::calculateDirectionPtEndcapHigh(){}

void L1TDisplacedMuonPtAssignment::calculateHybridPtBarrel(){}
void L1TDisplacedMuonPtAssignment::calculateHybridPtOverlap(){}
//Low: eta<2.1, GE11 and GE21 are used 
void L1TDisplacedMuonPtAssignment::calculateHybridPtEndcapLow(){
    int neta = EndcapTriggerPtAssignmentHelper::GetEtaPartition_hybrid( gp_ME[1].eta() );
    //ddY123, dPhi_dir_st1_st2 available, FIXME
    float ddY123 = 99;
    float dPhi_dir_st1_st2 = 99;
    hybridPt_ = 2.0;
    if (fabs(ddY123)>=40 or fabs(dPhi_dir_st1_st2)>=1.0){//rejected by hybrid
	return;
    }
    int npar = int(EndcapTriggerPtAssignmentHelper::getParity(isEven[0], isEven[1],
                                                                 isEven[2], isEven[3]));
    //by defualt right now, GE21 is used, FIXME
    for (int i=0; i<EndcapTriggerPtAssignmentHelper::NPtbins; i++){
       if(EndcapTriggerPtAssignmentHelper::ellipse(EndcapTriggerPtAssignmentHelper::HybridLUT[i][neta][npar][0],
						   EndcapTriggerPtAssignmentHelper::HybridLUT[i][neta][npar][1],
						   EndcapTriggerPtAssignmentHelper::HybridLUT[i][neta][npar][2],
						   EndcapTriggerPtAssignmentHelper::HybridLUT[i][neta][npar][3],
						   EndcapTriggerPtAssignmentHelper::HybridLUT[i][neta][npar][4], 
						   ddY123, dPhi_dir_st1_st2) <=1)
	    hybridPt_ = EndcapTriggerPtAssignmentHelper::PtBins[i];
       /*else if(not(useGE21) and EndcapTriggerPtAssignmentHelper::ellipse(EndcapTriggerPtAssignmentHelper::HybridME21CSConly[i][neta][npar][0],
				                            EndcapTriggerPtAssignmentHelper::HybridME21CSConly[i][neta][npar][1],
				                            EndcapTriggerPtAssignmentHelper::HybridME21CSConly[i][neta][npar][2],
				                            EndcapTriggerPtAssignmentHelper::HybridME21CSConly[i][neta][npar][3],
				                            EndcapTriggerPtAssignmentHelper::HybridME21CSConly[i][neta][npar][4], 
							    ddY123, dPhi_dir_st1_st2) <=1)
	    hybrid_pt = EndcapTriggerPtAssignmentHelper::PtBins[i];
	    */
       else//make sure LUT is consitent
	    break;
    }
}
//high: eta>2.1, GE11 and GE21, ME0 are usd
void L1TDisplacedMuonPtAssignment::calculateHybridPtEndcapHigh(){}

int L1TDisplacedMuonPtAssignment::getBarrelStubCase(bool MB1, bool MB2, bool MB3, bool MB4)
{
  if (    MB1 and     MB2 and not MB3 and not MB4) return 0;
  if (    MB1 and not MB2 and     MB3 and not MB4) return 1;
  if (    MB1 and not MB2 and not MB3 and     MB4) return 2;
  if (not MB1 and     MB2 and     MB3 and not MB4) return 3;
  if (not MB1 and     MB2 and not MB3 and     MB4) return 4;
  if (not MB1 and not MB2 and     MB3 and     MB4) return 5;

  if (    MB1 and     MB2 and     MB3 and not MB4) return 6;
  if (    MB1 and     MB2 and not MB3 and     MB4) return 7;
  if (    MB1 and not MB2 and     MB3 and     MB4) return 8;
  if (not MB1 and     MB2 and     MB3 and     MB4) return 9;

  if (MB1 and MB2 and MB3 and MB4) return 10;

  return -1;
}
