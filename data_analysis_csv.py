"""
  Accuracy historic:
  1. 0.5459183673469388
  2. 0.5459183673469388
  3. Waiting...
"""

import pandas as pd;
import seaborn as sns;
import math;
import matplotlib.pyplot as plt;

sns.set_style("white");
plt.figure(figsize=(10, 10));

data = pd.read_csv('diabetes_dataset.csv')

# Informações Gerais do dataframe
# data.info()

# Informações ausentes para cada coluna
# emptyColumns = data.isnull().sum();
# print(emptyColumns)

def dropOutliers(data, columnName):
  percentile25, percentile75 = np.percentile(data[columnName], [25, 75]);
  # IQR = Q3 − Q1 (intervalo interquartil).
  iqr = percentile75 - percentile25;
  print(iqr);

  lower = percentile25 - (1.5 * iqr);
  upper = percentile75 + (1.5 * iqr);

  dataWithoutOutliers = data[
    (data[columnName] >= lower) &
    (data[columnName] <= upper)
  ];

  return dataWithoutOutliers;

def updateNaNColumn(df, columnName, type = 'mean'):
  negativeCases = getPartitionedData(df[columnName], df['Outcome'], 0);
  positiveCases = getPartitionedData(df[columnName], df['Outcome'], 1);

  # insert mean in NaN rows of positive cases:
  df.loc[
    df['Outcome'] == 1,
    columnName
  ] = df.loc[
    df['Outcome'] == 1,
    columnName
  ].fillna(
      getMeanValue(positiveCases) if type == 'mean'
    else 
      getMedianValue(positiveCases)
    );

  # insert mean in NaN rows of negative cases:
  df.loc[
    df['Outcome'] == 0,
    columnName
  ] = df.loc[
    df['Outcome'] == 0,
    columnName
  ].fillna(
      getMeanValue(negativeCases) if type == 'mean'
    else 
      getMedianValue(negativeCases)
  );

def getPartitionedData(column, outcome, delimiter = 0):
  df = pd.DataFrame({ 'data': column, 'label': outcome });
  filteredData = df[df['label'] == delimiter];
  return filteredData['data'];

def getMeanValue(dataFrame):
  return math.floor(dataFrame.mean());

def getMedianValue(dataFrame):
  return math.floor(dataFrame.median());

# Boxplot
def plotBoxPlot(dataFrame):
  plt.boxplot(dataFrame, vert=False);
  plt.show();

# plt.hist(data['BloodPressure']);
# plt.show();

# df = getPartitionedData(data['BloodPressure'], data['Outcome'], 0);
# dfMean = getMeanValue(df);

# feature_cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
# 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'];

# print("Before")
# print(data.head());
# updateNaNColumnWithMean(data, 'SkinThickness');
# updateNaNColumnWithMean(data, 'BloodPressure');
# updateNaNColumnWithMean(data, 'Insulin');
# updateNaNColumnWithMean(data, 'BMI');
# print("After")
# print(data.head());
# print(df);
# print(dfMean);
plotBoxPlot(data);
