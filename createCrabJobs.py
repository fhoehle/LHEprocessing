import os,sys
sys.path.append(os.getenv('CMSSW_BASE')+os.path.sep+'MyCMSSWAnalysisTools')
sys.path.append(os.getenv('CMSSW_BASE')+'/MyCMSSWAnalysisTools/Tools')
import tools as myTools
import CrabTools
## lhes
pathToLhes= "/user/hoehle/tmpLHE"
gridFolderName = "TTbar-whizard"
publishName = "TTbar-whizard_LHE2EDM"
mainFolder="TestLHE2EDM"
LHEs = {
    "tta0":{"pathToLhes":pathToLhes,"gridFolderName":gridFolderName,"publishName":publishName}
}
lheCrab = {}
timeSt = myTools.getTimeStamp()

crabJobFolder = "/user/hoehle/Test"
cmsDriverCommand="cmsDriver.py  LHEtoEDM --conditions auto:mc -s NONE --eventcontent RAWSIM --datatier GEN --no_exec "
addCommands = {"--filein":("file:",".lhef"),"--python_filename":("TTbar-whizard_LHE2EDM_","cfg.py"),"--fileout":("TTbar-whizard_","LHE2EDM.root") }
def commandArgPostfix(cmd,l):
  return addCommands[cmd][0]+l+addCommands[cmd][1]
#####
for label in LHEs.keys():
  lheCrab[label] = {}
  crabDir = crabJobFolder.rstrip('/')+os.path.sep+label
  os.makedirs(crabDir)
  command = "cd "+crabDir+" && "+cmsDriverCommand+" ".join([k+" "+commandArgPostfix(k,label)+" " for k in addCommands.keys()])
  print command
  subPro = myTools.executeCommandSameEnv(command)
  subPro.wait()
  print(subPro.communicate()[0])
  lheCrab[label]["crabDir"] = crabDir
  lheCrab[label]["crabCfg"] = {}; crabCfg = lheCrab[label]["crabCfg"]
  crabCfg["CMSSW"] = {}
  crabCfg["CMSSW"]["pset"] = crabDir+os.path.sep+commandArgPostfix("--python_filename",label)
  lheCrab[label]["output_file"] = commandArgPostfix("--python_filename",label)
  crabCfg["USER"]={}
  crabCfg["USER"]["user_remote_dir"] = mainFolder.rstrip('/')+os.path.sep+ LHEs[label]["gridFolderName"]+"_"+label+"_"+timeSt
  crabCfg["USER"]["additional_input_files"] =  LHEs[label]["pathToLhes"].rstrip('/')+os.path.sep+label+".lhef"
  crabCfg["USER"]["publish_data_name"] =  LHEs[label]["publishName"]+"_"+label
  crabCfg["CMSSW"]["generator"]="lhe"
  crabCfg["CMSSW"]["number_of_jobs"]=1
  crabCfg["CMSSW"]["total_number_of_events"]=100000000
  crabCfg["USER"]["publish_data"]=1
  crabCfg["USER"]["dbs_url_for_publication"]="https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet"
##########
for l,cJ in lheCrab.iteritems():
    crabJob = CrabTools.crabProcess(l,"none","none",cJ["crabDir"],timeSt,mainFolder)
    crabJob.setCrabDir()
    crabJob.createCrabDir()
    crabCfg = crabJob.createCrabCfg(cJ["crabCfg"])
    print crabCfg    
 
#    crabP.createCrabCfg()
#    if sampDict.has_key("crabConfig"):
##      for k1 in sampDict["crabConfig"].keys():
##        for k2 in sampDict["crabConfig"][k1].keys():
##          crabP.crabCfg[k1][k2]=sampDict["crabConfig"][k1][k2]
##    crabP.crabCfg["CMSSW"]["total_number_of_events"]=1000000
##    crabP.crabCfg["CMSSW"]["number_of_jobs"]= 100
##    crabCfgFilename = crabP.createCrabDir()
    crabJob.writeCrabCfg()
    crabJob.executeCrabCommand("-create",debug = True)
##    CrabTools.saveCrabProp(crabP,options["outputPath"]+"/"+postfix+"_"+timeStamp+"_CrabCfg.json")
##    crabP.executeCrabCommand("-submit",debug = True)
