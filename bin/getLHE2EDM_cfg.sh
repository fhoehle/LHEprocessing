#! /bin/bash
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  echo "Usage: `basename $0` [-h] LABEL LHEFILE [CONDITIONS]"
  exit 0
fi
if [ "$#" -le 1 ]; then
  echo "Usage: `basename $0` [-h] LABEL LHEFILE [CONDITIONS]"
  exit 1
fi
if [ "$1" = "" ]; then
  echo "provide label"
  exit 1
fi
label=$1
lheFile=$2
conds="auto:startup"
if [ ! "$3" = "" ]; then
  conds=$3
fi
cmsDriver.py LHE2EDM -s NONE --conditions $conds --pileup NoPileUp --datamix NODATAMIXER --eventcontent RAWSIM --datatier GEN-SIM --filein file:$lheFile --fileout ${label}_LHE2EDM.root --python_filename ${label}_LHE2EDM_cfg.py --no_exec -n -1 --filetype LHE

