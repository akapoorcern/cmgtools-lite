from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.tools.tfTool import TFTool
import os 
from copy import deepcopy

class CP5Node_DNN(Module):
    def __init__(self, variations=[], doSystJEC=False, fillInputs=False):
        self.outVars = []
        self._MVAs   = [] 
        fillInputs = True
        varorder = ["lep1_conePt","lep2_conePt","lep1_eta","lep2_eta","lep1_phi","lep2_phi"]
        cats_2lss = ['predictions_ttH','predictions_Rest','predictions_ttW','predictions_tHQ','predictions_ttH_odd']

        if fillInputs:
            self.outVars.extend(varorder+['nEvent'])
            self.inputHelper = self.getVarsForVariation('')
            self.inputHelper['nEvent'] = lambda ev : ev.event

        self.systsJEC = {0:"",\
                         1:"_jesTotalCorrUp"  , -1:"_jesTotalCorrDown",\
                         2:"_jesTotalUnCorrUp", -2: "_jesTotalUnCorrDown",\
                         3:"_jerUp", -3: "_jerDown",\
                     } if doSystJEC else {0:""}
        
        if len(variations): 
            self.systsJEC = {0:""}
            print("self.systsJEC")
            for i,var in enumerate(variations):
                self.systsJEC[i+1]   ="_%sUp"%var
                self.systsJEC[-(i+1)]="_%sDown"%var


        for var in self.systsJEC:
            print("Test above_MVA append")
            self._MVAs.append( TFTool('CP5Node%s'%self.systsJEC[var], os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/tf_model_IHEP.pb',
                               self.getVarsForVariation(self.systsJEC[var]), cats_2lss, varorder))
            print("Test below_MVA append")
            self.outVars.extend( ['CP5Node%s_'%self.systsJEC[var] + x for x in cats_2lss])
            
        print("Test above vars_2lss_unclUp")
        vars_2lss_unclUp = deepcopy(self.getVarsForVariation(''))
        self.outVars.extend( ['CP5Node_unclUp_' + x for x in cats_2lss])

        vars_2lss_unclDown = deepcopy(self.getVarsForVariation(''))
        self.outVars.extend( ['CP5Node_unclDown_' + x for x in cats_2lss])

        worker_2lss_unclUp        = TFTool('CP5Node_unclUp', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/tf_model_IHEP.pb',
                                           vars_2lss_unclUp, cats_2lss, varorder)
        worker_2lss_unclDown      = TFTool('CP5Node_unclDown', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/tf_model_IHEP.pb',
                                           vars_2lss_unclDown, cats_2lss, varorder)
        
        self._MVAs.extend( [worker_2lss_unclUp, worker_2lss_unclDown])

        

    def getVarsForVariation(self, var ): 
        print("getVarsForVariation")
        return { 
            "lep1_conePt"      : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])], 
            "lep2_conePt"      : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[1])],
            "lep1_eta"         : lambda ev : ev.LepGood_eta[int(ev.iLepFO_Recl[0])] if ev.nLepFO_Recl >= 1 else 0,
            "lep2_eta"         : lambda ev : ev.LepGood_eta[int(ev.iLepFO_Recl[1])] if ev.nLepFO_Recl >= 2 else -9,
            "lep1_phi"         : lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else -9,
            "lep2_phi"         : lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else -9,
        }


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print("beginfile")
        print(self.outVars)
        declareOutput(self, wrappedOutputTree, self.outVars)
        
    def analyze(self,event):
        
        myvars = [event.iLepFO_Recl[0],event.iLepFO_Recl[1],event.iLepFO_Recl[2]]
        ret = []
        if self.inputHelper:
            for var in self.inputHelper:
                ret.append( (var, self.inputHelper[var](event)))
        for worker in self._MVAs:
            name = worker.name
            if ( not hasattr(event,"nJet25_jerUp_Recl") and not hasattr(event, "nJet25_jesBBEC1_yearDown_Recl")) and ('_jes' in name or  '_jer' in name or '_uncl' in name): continue # using jer bc components wont change
            ret.extend( [(x,y) for x,y in worker(event).iteritems()])
        writeOutput(self, dict(ret))
        
        return True
