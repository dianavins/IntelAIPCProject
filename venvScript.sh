# in terminal: chmod +x setup_environment.sh

# create and activate environment for the Intel NUC project
conda create -n intel-NUC-project python=3.8
conda init
conda activate intel-NUC-project

# Install dependencies
conda install pytorch torchvision torchaudio cpuonly -c pytorch
pip install transformers datasets
pip install optimum
