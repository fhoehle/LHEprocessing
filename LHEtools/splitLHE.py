import re,getopt,sys
opts, args = getopt.getopt(sys.argv[1:], '',['inputFile=','steps=','outputFile=',"maxEvents="])
inputFile=None
steps=-1
outputFile=None
maxEvents=-1
for opt,arg in opts:
 #print opt , " :   " , arg
 if opt in  ("--inputFile"):
  inputFile=arg
 if opt in ("--steps"):
  steps=int(arg)
 if opt in ("--outputFile"):
  outputFile=arg
 if opt in ("--maxEvents"):
  maxEvents=int(arg)
if inputFile == None or steps==-1:
 sys.exit("input settings wrong")
if outputFile==None:
 outputFile=re.match('(.*)\.lhe',str(inputFile)).group(1)+"_"
def events(filename):
  eventblock = False
  content = ""
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
def getHeader(filename):
  content=""
  for line in open(filename):
    #print line
    if "<event>" in line:
        return content
    else:
        content += line

header =  getHeader(inputFile)
#
content=''
numfile=0
for i, event in enumerate(events(inputFile)):
#  if i == int(maxEvents):
#   break
  content+=event
  if i != 0 and (i+1)%steps == 0:
   print "writing file ",outputFile+str(numfile)+".lhe ..."
   outfile=open(outputFile+str(numfile)+".lhe","w")
   outfile.write(header)
   outfile.write(content)
   outfile.write("</LesHouchesEvents>")
   outfile.close()
   content=''
   numfile+=1
   print "done."
  if i == int(maxEvents):
   break

print "finished, created ",numfile," files, each contains ",steps," events" 
