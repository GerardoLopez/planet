[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GerardoLopez/planet/master)

One way to explore the mock-up is by clicking on the Binder icon above to lunch an Binder hosted Jupyter notebook, this make take a while since the conda en
vironment I used is a bit bulky and include lots of libraries, plus hang tight please! Once the Notebook has launch just navigate to the ```planet``` folder and then click in the ```planet.ipynb``` file.

The easiest wat to run the code is by doing it locally, you need a Linux box, then please:
* Download conda
  * ```wget https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh```
    * Install conda ```bash ./Anaconda3-5.1.0-Linux-x86_64.sh```
* Clone this repo
  * ```git clone https://github.com/GerardoLopez/planet```
* Create a conda environment using the provided ```environment.yml```
  * ```conda env create -f environment.yml```
* Now you can run the code
  * ```cd planet```
  * ```jupyter notebook```
    * Click in the ```planet.ipynb``` file and follow the instructions

