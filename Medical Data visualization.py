import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def medical_data_visualizer(filepath):
  # read in the csv file to a Pandas dataframe
  df = pd.read_csv(filepath)

  # Add an overweight column to the data
  df['overweight'] = (df['weight'] / ((df['height'] / 100)**2)) > 25

  # Normalize the data
  df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
  df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)

  # Convert the data into long format and create a chart
  df_long = pd.melt(
    df,
    id_vars=['cardio'],
    value_vars=['cholesterol', 'gluc', 'alco', 'active', 'smoke'])
  sns.catplot(x='variable', y='value', hue='cardio', kind='bar', data=df_long)
  plt.show()

  # Clean the data
  df = df[(df['ap_lo'] <= df['ap_hi'])
          & (df['height'] >= df['height'].quantile(0.025)) &
          (df['height'] <= df['height'].quantile(0.975)) &
          (df['weight'] >= df['weight'].quantile(0.025)) &
          (df['weight'] <= df['weight'].quantile(0.975))]

  # Create a correlation matrix
  corr = df.corr()
  sns.heatmap(corr, annot=True, cmap='coolwarm', mask=(corr >= 1))
  plt.show()
