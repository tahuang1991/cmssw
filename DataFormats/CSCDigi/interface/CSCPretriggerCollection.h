#ifndef CSCPretrigger_CSCPretriggerCollection_h
#define CSCPretrigger_CSCPretriggerCollection_h

/** \class CSCPretriggerCollection
 *
 *  For CLCT trigger primitives
 *  \author N. Terentiev - CMU
 *
*/

#include "DataFormats/MuonDetId/interface/CSCDetId.h"
#include "DataFormats/MuonData/interface/MuonDigiCollection.h"
#include "DataFormats/CSCDigi/interface/CSCPretrigger.h"
//#include "CSCPretrigger.h"

typedef MuonDigiCollection<CSCDetId, CSCPretrigger> CSCPretriggerCollection;

#endif
