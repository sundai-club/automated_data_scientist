# install 
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt 

# run tesla example 
panel serve source_code_tsla.py --port 5005

# run genomics example 
panel serve source_code_genomics.py --port 5006 # must be a new port

# BEFORE YOU RUN: 
    # 1. CORRECT THIS LINE INSIDE THE CODE to point to FULL PATH on your computer
        # genomics
            message=f"Download data from /Users/ai/Documents/sundai/automated-data-scientist/panel/homo_sapiens_genomics.csv and {contents}"
        # tesla 
            message=f"Download data from /Users/ai/Documents/sundai/automated-data-scientist/panel/TSLA.csv and {contents}"
    # 2. make sure you put correct openai api key in OAI_CONFIG_LIST file 



# OTHER THINGS TO NOTE: 
# you must CLOSE the plot in order to proceed with the agent... (as shown in my video)
            # https://www.youtube.com/watch?v=zg4vDLURlPQ


# QUESTIONS YOU CAN USE FROM THE DEMO
    # first question to ask for TESLA demo:  
    #               analyze Tesla stock data and generate a volatility plot.
    # first question to ask for GENOMICS demo:  
    #               analyze this genomic data and plot Distribution of features across chromosomes: Create a stacked bar chart showing the count of different features (e.g., genes, exons, transcripts) for each chromosome (seqname).



# DEMO GENERATED RESULTS:
    # see here 
    # ls groupchat_1025_13Oct_genomic_results/
    # ls groupchat_2000_13Oct_tesla_results/



# source of data 
    # first 1000 rows of this 
    # https://www.kaggle.com/datasets/alfrandom/human-genome-annotation
