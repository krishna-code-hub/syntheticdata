# Import the necessary modules
from pmlb import fetch_data
import pandas as pd
from ydata_synthetic.synthesizers.regular import RegularSynthesizer
from ydata_synthetic.synthesizers import ModelParameters, TrainParameters
from datetime import datetime

print(datetime.now())

# Load data
data = pd.read_csv("./input_data/original_employee_data.csv")

num_cols = ['id']
cat_cols = [ 'first_name','last_name','email','gender','ip_address','company Name','Language']

# Define model and training parameters
ctgan_args = ModelParameters(batch_size=300, lr=2e-4, betas=(0.5, 0.9))
train_args = TrainParameters(epochs=20)

# Train the generator model
synth = RegularSynthesizer(modelname='ctgan', model_parameters=ctgan_args)
synth.fit(data=data, train_arguments=train_args, num_cols=num_cols, cat_cols=cat_cols)

#Saving the synthesizer to later generate new events
synth.save(path='./models/employee.pkl')

print(datetime.now())