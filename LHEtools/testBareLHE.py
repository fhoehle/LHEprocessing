import ROOT,re,numpy,math
from MyUtilities.MyFunctions.CosTheta1Theta2SpinCorrlation_cfi import CosTheta1Theta2
from MyUtilities.MyFunctions.MyHistFunctions_cfi import MyHistManager
ROOT.gROOT.SetBatch(1)
def makeTLorentzVec(idx,vecParts):
  return ROOT.TLorentzVector(vecParts[idx][6],vecParts[idx][7],vecParts[idx][8],vecParts[idx][9])
def events(fileNames):
  eventblock = False
  content = ""
  for filename in fileNames:
    for line in open(filename):
      if "<event>" in line:
          eventblock = True
          content = ""
      elif "</event>" in line:
          eventblock = False
          content += line
          yield content
      if eventblock:
          content += line 
  raise StopIteration
maxEvents=-1 #4000000
files=["/net/scratch_cms/institut_3b/hoehle/LHEFiles/MCatNLO_5217/ttbar_mcatnlo_7TeV_cteq6m_00.lhe","/net/scratch_cms/institut_3b/hoehle/LHEFiles/MCatNLO_5217/ttbar_mcatnlo_7TeV_cteq6m_01.lhe","/net/scratch_cms/institut_3b/hoehle/LHEFiles/MCatNLO_5217/ttbar_mcatnlo_7TeV_cteq6m_02.lhe","/net/scratch_cms/institut_3b/hoehle/LHEFiles/MCatNLO_5217/ttbar_mcatnlo_7TeV_cteq6m_03.lhe"]
cosTheta1Theta2 = ROOT.TH2D("cosTheta1Theta2","cosTheta1Theta2",10,-1.0,1.0,10,-1.0,1.0)
h1_topPt = ROOT.TH1D("h1_topPt","h1_topPt",200,0,400)
h1_topEnergy = ROOT.TH1D("h1_topEnergy", "h1_topEnergy",200,0,800)
h1_lepPt = ROOT.TH1D("h1_lepPt","h1_lepPt",200,0,400)
h1_lepEnergy = ROOT.TH1D("h1_lepEnergy","h1_lepEnergy",250,0,500)
h1_ptTopPair = ROOT.TH1D("h1_ptTopPair","h1_ptTopPair",200,0,200)
h1_mcSigns = ROOT.TH1D("h1_mcSigns","h1_mcSigns",500,250,250)
h1_usedMcSigns = ROOT.TH1D("h1_usedMcSigns","h1_mcSigns",500,250,250)
myHists=MyHistManager("testingBareLHE_SpinCorrelations",True)
##
for i,bareLheEvent in enumerate(events(files)):
  if maxEvents > 0 and i >= maxEvents:
    break
  if i%1000 == 0:
    print "processing: ",i
  convertedLHE = (re.sub('#.*\n','',bareLheEvent,re.S).strip('<event>\n|<event/>\n')).replace('\t','  ').split('\n')
  lheEvent = []
  firstTopIdx = -1
  for partCand in convertedLHE:
    lheEvent.append(numpy.fromstring(partCand,sep=' '))
  #search beginning of tops
  for j,partCand in enumerate(lheEvent):
    if math.fabs(partCand[0]) == 6 and firstTopIdx == -1: firstTopIdx = j
  top1Idx = firstTopIdx+0; b1Idx=firstTopIdx+2; W1Idx = firstTopIdx + 3; lep1Idx = firstTopIdx+6; nu1Idx = firstTopIdx+7
  top2Idx = firstTopIdx + 1; b2Idx = firstTopIdx+4; W2Idx = firstTopIdx+5; lep2Idx = firstTopIdx + 8; nu2Idx = firstTopIdx+9
  #print lheEvent[top1Idx]," ",lheEvent[top2Idx] 
  mcSign = lheEvent[0][2]/math.fabs(lheEvent[0][2])
  h1_mcSigns.Fill(mcSign)
  if  11 < math.fabs(lheEvent[lep1Idx][0]) <= 15 and 11 < math.fabs(lheEvent[lep2Idx][0]) <= 15: # dileptonic events will pass
    h1_usedMcSigns.Fill(mcSign)
    top1Vec = makeTLorentzVec(top1Idx,lheEvent); top2Vec = makeTLorentzVec(top2Idx,lheEvent); lep1Vec =makeTLorentzVec(lep1Idx,lheEvent); lep2Vec = makeTLorentzVec(lep2Idx, lheEvent)
    #print "lep1 ",lheEvent[lep1Idx][0]," ",lheEvent[lep2Idx][0]," top1 ",lheEvent[top1Idx][0]," top2 ",lheEvent[top2Idx][0]
    cosT1T2=CosTheta1Theta2(lep1Vec,lep2Vec,top1Vec,top2Vec)
    #print "event ",i," cosTheta1 ",cosT1T2[0]," cosTheta1 ",cosT1T2[1]," mcSign ",mcSign," top1Pt ",top1Vec.Pt()," top1E ",top1Vec.Energy()," top2Pt ",top2Vec.Pt()," top2E ",top2Vec.Energy()," lep1Pt ",lep1Vec.Pt()," lep1E ",lep1Vec.Energy()," lep2Pt ",lep2Vec.Pt()," lep2E ",lep2Vec.Energy()  
    cosTheta1Theta2.Fill(cosT1T2[0],cosT1T2[1],mcSign)
    h1_topPt.Fill(top1Vec.Pt(),mcSign);h1_topPt.Fill(top2Vec.Pt(),mcSign)
    h1_topEnergy.Fill(top1Vec.Energy(),mcSign);h1_topEnergy.Fill(top2Vec.Energy(),mcSign)
    h1_lepPt.Fill(lep1Vec.Pt(),mcSign);h1_lepPt.Fill(lep2Vec.Pt(),mcSign)
    h1_lepEnergy.Fill(lep1Vec.Energy(),mcSign);h1_lepEnergy.Fill(lep2Vec.Energy(),mcSign)
    h1_ptTopPair.Fill((top1Vec+top2Vec).Pt(),mcSign)
  #print "i ",i
myHists.saveHist(cosTheta1Theta2,"COLZ")
myHists.saveHist(h1_topPt,"h")
myHists.saveHist(h1_topEnergy,"h")
myHists.saveHist(h1_lepPt,"h")
myHists.saveHist(h1_lepEnergy,"h")
myHists.saveHist(h1_ptTopPair,"h")
myHists.saveHist(h1_usedMcSigns,"h")
myHists.saveHist(h1_mcSigns,"h")
myHists.done()
fitT1T2 = ROOT.TF2("fitT1T2","[0]/4.0*(1-[1]*x*y+[2]*x+[3]*y)")
cosTheta1Theta2.Sumw2(); cosTheta1Theta2.Fit(fitT1T2.GetName(),"N")
