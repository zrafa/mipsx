#!/bin/bash

cp /export/home/extras/mipsx/hello.s ${HOME}/ ;
export PATH=/export/home/extras/mipsx/:$PATH ;
cd ${HOME}/ ;
python /export/home/extras/mipsx/mipsx.py
