# GPLR
This repo provides implementations and hands-on notebooks for generating customer personas using the GPLR algorithm.

## Table of Contents
- [Installation](#installation)
- [Setting Up OpenAI API Key](#setting-up-openai-api-key)
- [GPLR: Notebooks](#gplr-notebooks)
- [LGCN3: Codes](#lgcn3-codes)
- [A_LGCN3: Codes](#a_lgcn3-codes)

## Installation
To set up the environment and install all required packages, follow these steps:
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the following command to install the dependencies:

   ```bash
   python -m venv myenv
   source myenv/bin/activate
   pip install -r requirements.txt

## Setting Up OpenAI API Key
This project requires an API key from OpenAI to access specific functionalities. Please complete the following steps:
1. Create or log into your [OpenAI account](https://platform.openai.com/).
2.	Navigate to the API section and generate a new API key.
3.	Set up your API key as an environment variable to allow the project to access OpenAI’s API:

    ```bash
    export OPENAI_API_KEY='your_api_key_here'
4.	Confirm that the API key is correctly set up by running:

    ```bash
    echo $OPENAI_API_KEY
Ensure this returns the correct key value before proceeding.
## GPLR: Notebooks
In the /src directory, there are two main Jupyter notebooks that you can work with:
1.	**persona_collection.ipynb**
	- This notebook shows how to collect persona labels with LLMs for users and items within the MBA (Market Basket Analysis) dataset.
	- Users can run/modify this notebook to gather persona data for new datasets as needed.
2.	**gplr.ipynb**
	- This is the primary notebook executes the GPLR algorithm to generate customer personas using RevAff, based on a carefully sampled prototype user set.
    - The generated results are saved in JSON format and stored in the /data/gplr_res/ directory.
### Usage
1.	Open the /src directory.
2.	Launch Jupyter Notebook by running:

    ``` bash
    jupyter notebook
3. Open the notebook in the web page.
## LGCN3: Codes
For LGCN3, follow these steps:
1. Go to the `/src/baselines/lgcn3` directory:
   ```bash
   cd /src/baselines/lgcn3
2.	Construct the low-pass graph filter by running the command:
    ```bash
    python3 pretraining/_graph_embeddings_tri.py
3. Start the training process:
    ```bash
    python3 run_exp.py --model 11 --lr 0.001 --lamda 0.005 --layer 1 --batch 40000 --epoch 1000
LGCN3's code is implemented based on the original open-source implementation of the LGCN model from the paper *Low-pass Graph Convolutional Network for Recommendation*.

## A_LGCN3: Codes
For A_LGCN3, follow these steps:
1. Go to the `/src/baselines/lgcn3` directory:
   ```bash
   cd /src/baselines/lgcn3
2.	Construct the low-pass graph filter by running the command:
    ```bash
    python3 pretraining/_graph_embeddings_tri.py
3. Start the training process:
    ```bash
    python3 run_exp.py --model 14 --lr 0.001 --lamda 0.02 --layer 1 --batch 80000 --epoch 1000 --afd_alpha 1e-4
