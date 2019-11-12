import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# load an FXD csv into a dataframe for a particular person and visualization type
def load_FXD(person, visualization):
    cols = ["fix_number", "timestamp", "duration", "gazepoint_x", "gazepoint_y"]
    path = Path.cwd() / "data" / person
    FXD = pd.read_csv(path / f"{person}.{visualization}FXD.txt", sep="\t", names = cols, header=None)
    return FXD

# return search to process ratio (saccade duration sum / fixation duration sum)
def search_to_process_ratio(FXD):
    FXD["saccade_dur"]= FXD["timestamp"].diff()
    return FXD["saccade_dur"].sum() / FXD["duration"].sum()

# return both s to p and fixation duration average
def information_processing_metrics(FXD):
    fixation_duration_mean = FXD["duration"].mean()
    s_to_p_ratio = search_to_process_ratio(FXD)
    return fixation_duration_mean, s_to_p_ratio

# add fixation duration mean and search to process ratio to additional data
def add_metrics_to_data(main):
    for index, row in main.iterrows():
        person = row["ID"]
        visualization = "graph" if row["Visualization"] == 1 else "tree"
        FXD = load_FXD(person, visualization)
        fixation_duration_mean, s_to_p_ratio = information_processing_metrics(FXD)
        main.loc[index, "fixation_duration_mean"] = fixation_duration_mean
        main.loc[index, "s_to_p_ratio"] = s_to_p_ratio
    return main

# load additional data into dataframe, and add metrics
def load_additional_data():
    path = Path.cwd() / "Additional Participant Data.csv"
    additional_data = pd.read_csv(path, sep=",")
    additional_data = add_metrics_to_data(additional_data)
    return additional_data

main = load_additional_data()

fig = px.parallel_coordinates(main, color="Visualization", 
    labels={"Ontologies": "Ontologies", 
    "Visualization": "Visualization", "Task_Success": "Task Success", 
    "Time_On_Task": "Time on Task", "fixation_duration_mean": "Fixation Duration Mean", 
    "s_to_p_ratio": "Search-to-Process Ratio", }, 
    color_continuous_scale=px.colors.diverging.Tealrose,
                             color_continuous_midpoint=2)
fig.show()