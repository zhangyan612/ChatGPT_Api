conda info --envs

conda create --name huggingface python=3.10

conda activate huggingface

conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia

pip install chardet 

huggingface-cli login

pip install accelerate

install cuda by going to their website