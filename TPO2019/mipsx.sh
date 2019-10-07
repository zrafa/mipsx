#!/bin/bash

# ssh 10.0.15.49 -X "
# ssh 10.0.2.31 -C -X "
cp /export/home/extras/mipsx/hello.s ${HOME}/ 
export PATH=/export/home/extras/mipsx/:$PATH 
cd ${HOME}/ 
python /export/home/extras/mipsx/mipsx.py
#python /export/home/extras/mipsx/mipsx.py" 
