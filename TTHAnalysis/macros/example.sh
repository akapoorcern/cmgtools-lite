# year=2016


for year in 2016
do
    for file in TTWToLNu_fxfx #TTH_ctcvcp_new THQ_ctcvcp_new TTJets_SingleLeptonFromT TTJets_DiLepton TTJets_SingleLeptonFromTbar
    do
	python prepareEventVariablesFriendTree.py -t NanoAOD /eos/user/s/sesanche/nanoAOD//NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/ output_${year} -F Friends /eos/user/s/sesanche/nanoAOD//NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/1_recl_allvars//{cname}_Friend.root -I CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules CP5Node -F Friends /eos/user/s/sesanche/nanoAOD//NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/5_BDThtt_reco_new_blah/{cname}_Friend.root -F Friends /eos/user/s/sesanche/nanoAOD//NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/0_jmeUnc_v1/{cname}_Friend.root --name mva2lss -d $file -c 0 -N 1000000000000000 -F Friends /eos/user/s/sesanche/nanoAOD//NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/3_tauCount/{cname}_Friend.root -F Friends /eos/user/s/sesanche/nanoAOD//NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/4_evtVars/{cname}_Friend.root
    done
done
#CP5Node
