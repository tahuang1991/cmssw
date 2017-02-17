#ifndef FlatRandomPtAndDxyGunProducer_H
#define FlatRandomPtAndDxyGunProducer_H

/** \class FlatRandomPtAndDxyGunProducer
 *
 * Generates single particle gun in HepMC format
 * The d0 is taken by convention equal to dxy
 ***************************************/

#include "IOMC/ParticleGuns/interface/BaseFlatGunProducer.h"
#include "CLHEP/Random/RandGauss.h"

namespace edm
{

    class FlatRandomPtAndDxyGunProducer : public BaseFlatGunProducer
    {

    public:
        FlatRandomPtAndDxyGunProducer(const ParameterSet & pset);
        virtual ~FlatRandomPtAndDxyGunProducer();

        virtual void produce(Event & e, const EventSetup& es) override;

    private:

        // data members

        double            fMinPt   ;
        double            fMaxPt   ;
	//double            LzMin_   ;
        double            LzWidth_   ;
        double            dxyMin_   ;
        double            dxyMax_   ;

	CLHEP::RandGauss *fRandomGaussGenerator;

    };
}

#endif
