import ROOT,math
from DataFormats.FWLite import Events, Handle
import getopt,sys,decimal,signal
from MyUtilities.MyFunctions.CosTheta1Theta2SpinCorrlation_cfi import CosTheta1Theta2
from MyUtilities.MyFunctions.MyHistFunctions_cfi import MyHistManager
#
def makeTLorentzVec(idx,vecParts):
  return ROOT.TLorentzVector(vecParts[idx].x[0],vecParts[idx].x[1],vecParts[idx].x[2],vecParts[idx].x[3])
######
ROOT.gROOT.SetBatch()
# Create histograms, etc.
ROOT.gROOT.SetStyle('Plain') # white background
ROOT.gStyle.SetOptStat("emrou"); ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptFit(1)
myHists=MyHistManager("testingLHE",True)
###############
testFileName='dcap://grid-dcap.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/mc/Fall11/TT_TuneZ2_7TeV-mcatnlo/AODSIM/PU_S6_START42_V14B-v1/0001/FE35F649-6F2A-E111-A7F7-00261894392C.root'
cosTheta1Theta2 = ROOT.TH2D("cosTheta1Theta2","cosTheta1Theta2",10,-1.0,1.0,10,-1.0,1.0)
h1_topPt = ROOT.TH1D("h1_topPt","h1_topPt",200,0,400)
h1_topEnergy = ROOT.TH1D("h1_topEnergy", "h1_topEnergy",200,0,800)
h1_lepPt = ROOT.TH1D("h1_lepPt","h1_lepPt",200,0,400)
h1_lepEnergy = ROOT.TH1D("h1_lepEnergy","h1_lepEnergy",250,0,500)
h1_ptTopPair = ROOT.TH1D("h1_ptTopPair","h1_ptTopPair",200,0,200)
events = Events()#testFileName)
#events._filenames.append('dcap://grid-dcap.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/mc/Fall11/TT_TuneZ2_7TeV-mcatnlo/AODSIM/PU_S6_START42_V14B-v1/0001/FA02E2E1-682A-E111-AB7B-003048678B18.root')
prefix='dcap://grid-dcap.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms'
mcatnloFiles = open('mcatnlo_files.txt').readlines()
maxFiles = 200
del events._filenames[-1]
for i,mcFile in enumerate(mcatnloFiles):
  if i == maxFiles: break
  events._filenames.append(prefix+mcFile.strip())
print "files processing ",events._filenames
lheHandle = Handle('LHEEventProduct') ;lheLabel="source"
genEvtInfoHandle =  Handle("GenEventInfoProduct");genEvtInfoLabel = "generator" # using MCweights
for evtNo,event in enumerate(events):
  event.getByLabel(genEvtInfoLabel,genEvtInfoHandle); genEvtInfo = genEvtInfoHandle.product()
  mcWeight = genEvtInfo.weight(); mcSign = mcWeight/abs(mcWeight)
  event.getByLabel(lheLabel,lheHandle);lheHandle.product()
  hepupParts = lheHandle.product().hepeup()
  firstTopIdx = -1
  pdgIds = hepupParts.IDUP
  vecs = hepupParts.PUP
  if len(pdgIds) != len(vecs): print "event corrupted"; continue
  for i,(vec,pdgId) in enumerate(zip(vecs,pdgIds)):
    #print pdgId.numerator,"  px ", vec.x[0]," mass ",vec.x[4], "  energy  ",vec.x[3]
    if math.fabs(pdgId.numerator) == 6 and firstTopIdx == -1: firstTopIdx = i
  #print "next event, "
  #everything relative to firstTopIdx
  top1Idx = firstTopIdx+0; b1Idx=firstTopIdx+2; W1Idx = firstTopIdx + 3; lep1Idx = firstTopIdx+6; nu1Idx = firstTopIdx+7 
  top2Idx = firstTopIdx + 1; b2Idx = firstTopIdx+4; W2Idx = firstTopIdx+5; lep2Idx = firstTopIdx + 8; nu2Idx = firstTopIdx+9
  if 11 <= math.fabs(pdgIds[lep1Idx]) <= 15 and 11 <= math.fabs(pdgIds[lep2Idx]) <= 15:
    #print "its dileptonic"
    top1Vec = makeTLorentzVec(top1Idx,vecs); top2Vec = makeTLorentzVec(top2Idx,vecs); lep1Vec =makeTLorentzVec(lep1Idx,vecs); lep2Vec = makeTLorentzVec(lep2Idx, vecs)
    cosT1T2=CosTheta1Theta2(lep1Vec,lep2Vec,top1Vec,top2Vec)
    #print "thisCosT1T2 "
    cosTheta1Theta2.Fill(cosT1T2[0],cosT1T2[1],mcSign)
    h1_topPt.Fill(top1Vec.Pt(),mcSign);h1_topPt.Fill(top2Vec.Pt(),mcSign)
    h1_topEnergy.Fill(top1Vec.Energy(),mcSign);h1_topEnergy.Fill(top2Vec.Energy(),mcSign)
    h1_lepPt.Fill(lep1Vec.Pt(),mcSign);h1_lepPt.Fill(lep2Vec.Pt(),mcSign)
    h1_lepEnergy.Fill(lep1Vec.Energy(),mcSign);h1_lepEnergy.Fill(lep2Vec.Energy(),mcSign)
    h1_ptTopPair.Fill((top1Vec+top2Vec).Pt(),mcSign)

myHists.saveHist(cosTheta1Theta2,"COLZ")
myHists.saveHist(h1_topPt,"h")
myHists.saveHist(h1_topEnergy,"h")
myHists.saveHist(h1_lepPt,"h")
myHists.saveHist(h1_lepEnergy,"h")
myHists.saveHist(h1_ptTopPair,"h")
myHists.done()
fitT1T2 = ROOT.TF2("fitT1T2","[0]/4.0*(1-[1]*x*y+[2]*x+[3]*y)")
cosTheta1Theta2.Sumw2(); cosTheta1Theta2.Fit(fitT1T2.GetName(),"N")

