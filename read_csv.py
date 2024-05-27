import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_csv("./output_data/synthetic.csv")
profile = ProfileReport(df, title="Profiling Report")
profile.to_file("your_report.html")