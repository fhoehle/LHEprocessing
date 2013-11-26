import ROOT,re,numpy
def makeTLorentzVecOfGenEventInfo(idx,vecParts):
  return ROOT.TLorentzVector(vecParts[idx].x[0],vecParts[idx].x[1],vecParts[idx].x[2],vecParts[idx].x[3])
def makeTLorentzVecBareLheEvent(idx,vecParts):
  return ROOT.TLorentzVector(vecParts[idx][6],vecParts[idx][7],vecParts[idx][8],vecParts[idx][9])

######
def lheEvents(fileNames):
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
          yield generateLHEevent(convertedLHE(content))
      if eventblock:
          content += line
  raise StopIteration
def convertedLHE(bareLHEEvent):
  return (re.sub('#.*\n','',bareLHEEvent,re.S).strip('<event>\n|<event/>\n')).replace('\t','  ').split('\n')
def generateLHEevent(converted): 
  lheEvent = myLHEevent()
  
  lheEvent.eventSettings = [ float(v) for v in converted.pop(0).split()]
  for partCand in converted:
    tmpPart= numpy.fromstring(partCand,sep=' ')
    part=myParticle(pdgId=int(tmpPart[0]),px=float(tmpPart[6]),py=float(tmpPart[7]),pz=float(tmpPart[8]),E=float(tmpPart[9]))
    lheEvent.parts.append(part)
  return lheEvent
class myParticle(object):
  def __init__(self,px=0,py=0,pz=0,E=0,pdgId=0):
    self.px=px
    self.py=py
    self.pz=pz
    self.E=E
    self.pdgId=pdgId
  def SetPxPyPzE(self,px,py,pz,E,pdgId=0):
    self.px=px
    self.py=py
    self.pz=pz
    self.E=E
    self.pdgId=pdgId
  def getTLoretzVec(self):
    return ROOT.TLorentzVector(self.px,self.py,self.pz,self.E)
class myLHEevent (object):
  def __init__(self):
    self.eventSettings = None
    self.parts=[]
class ttbarLheEvent(object):
  def addPart(self,label,part):
    self.__dict__[label]=part
###################
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

