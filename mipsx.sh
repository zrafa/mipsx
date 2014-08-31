#!/bin/bash

ssh 10.0.15.130 -X "
cp /export/home/extras/mipsx/hello.s ${HOME}/ ;
export PATH=/export/home/extras/mipsx/:$PATH ;
cd ${HOME}/ ;
python /export/home/extras/mipsx/mipsx.py" 
