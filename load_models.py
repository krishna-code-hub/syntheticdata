from ydata_synthetic.synthesizers.regular import RegularSynthesizer
from datetime import datetime

print(datetime.now())

#########################################################
#    Loading and sampling from a trained synthesizer    #
#########################################################
synth = RegularSynthesizer.load(path='./models/employee.pkl')

#Sampling the data
data_sample = synth.sample(100000)

data_sample.to_csv("./output_data/synthetic.csv", index=False)

print(datetime.now())