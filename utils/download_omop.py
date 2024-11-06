import redivis
import sys

# condition occurence: condition_occurrence:6fn1
# person: person:cdwn
# concept: concept:w5gj

user = redivis.user("demo")
dataset = user.dataset("cms_synthetic_patient_data_omop:ye2v:v2_0")

query = dataset.query("""
    SELECT * FROM condition_occurrence:6fn1
    LIMIT 10000;
""")

# Load table as a dataframe
df = query.to_pandas_dataframe()
# df.head()
print(df)
df.to_csv(sys.argv[1], index = False, sep = '\t')
