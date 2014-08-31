#!/bin/bash

cd ${HOME}/
cp /export/home/extras/mipsx/hello.s ${HOME}/
export PATH=/export/home/extras/mipsx/:$PATH
python /export/home/extras/mipsx/mipsx.py
