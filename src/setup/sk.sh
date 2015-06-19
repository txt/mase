installingBuildDependencies() {
  sudo apt-get install \
    build-essential python-dev python-setuptools \
    python-numpy python-scipy \
    libatlas-dev libatlas3gf-base
}
BLASandLAPACK() { 
 sudo update-alternatives --set libblas.so.3 \
    /usr/lib/atlas-base/atlas/libblas.so.3
 sudo update-alternatives --set liblapack.so.3 \
    /usr/lib/atlas-base/atlas/liblapack.so.3
}
matplotlib() {
  sudo apt-get install python-matplotlib
}
sklearn() {
  pip install --user  --install-option="--prefix=" -U scikit-learn
}
installingBuildDependencies
BLASandLAPACK
matplotlib
sklearn