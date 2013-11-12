import ROOT
def makeTLorentzVec(idx,vecParts):
  return ROOT.TLorentzVector(vecParts[idx].x[0],vecParts[idx].x[1],vecParts[idx].x[2],vecParts[idx].x[3])
######
def readLHEevent(hepupParts):
  vecs = hepupParts.PUP
  firstTopIdx = -1
  pdgIds = hepupParts.IDUP
  vecs = hepupParts.PUP
  if len(pdgIds) != len(vecs): print "event corrupted"; return None
  for i,(vec,pdgId) in enumerate(zip(vecs,pdgIds)):
    if math.fabs(pdgId.numerator) == 6 and firstTopIdx == -1: firstTopIdx = i
    break
  top1Idx = firstTopIdx+0; b1Idx=firstTopIdx+2; W1Idx = firstTopIdx + 3; lep1Idx = firstTopIdx+6; nu1Idx = firstTopIdx+7 
  top2Idx = firstTopIdx + 1; b2Idx = firstTopIdx+4; W2Idx = firstTopIdx+5; lep2Idx = firstTopIdx + 8; nu2Idx = firstTopIdx+9
  if 11 <= math.fabs(pdgIds[lep1Idx]) <= 15 and 11 <= math.fabs(pdgIds[lep2Idx]) <= 15:
    #print "its dileptonic"
    return {"top1" : makeTLorentzVec(top1Idx,vecs),"top2" : makeTLorentzVec(top2Idx,vecs), "lep1": makeTLorentzVec(lep1Idx,vecs), "lep2": makeTLorentzVec(lep2Idx, vecs)}

