mkdir lib
cp requirements.txt ./lib
cd lib
pip3 install -r requirements.txt --target=$PWD
