import pandas as pd
import re
import datetime
import random

# display the full contents of a column
pd.set_option('display.max_colwidth', None)

# load CSV data
df = pd.read_csv('jeopardy.csv')

# remove hashtag to investigate data contents
#print(df.info())
#print(df.head())

# Data Cleaning

# clean up column names: add underscores and lowercase to allow dot notation
df.rename(columns={
  'Show Number': 'show_number',
  ' Air Date': 'air_date',
  ' Round': 'round',
  ' Category': 'category',
  ' Value': 'value',
  ' Question': 'question',
  ' Answer': 'answer'},
  inplace=True)

# fix value column to be straight floats with no $'s commas or "None"
df.value = df.value.apply(lambda x: float(x.strip('$').replace(',', '')) if x != 'None' else 0)

# change air_date column in datetime format instead of string
df.air_date = df.air_date.apply(lambda x: pd.to_datetime(x))

# remove hypertext reference from question column
df.question = df.question.apply(lambda x: re.sub(re.compile('<.*?>'), '', x))

# change category and answer columns in lowercase for further easy search
df.category = df.category.apply(lambda x: x.lower())
df.answer = df.answer.apply(lambda x: str(x).lower())

# Data Analyzing

# filter dataset to only include rows with questions that contain all words in the user inputted list
def word_filter(dataset, words):
    filter = lambda x: all(word.lower() in x.lower() for word in words)
    return dataset.loc[dataset.question.apply(filter)]

# remove hashtags to test word_filter function
#words1 = ['King', 'England']
#print(word_filter(df, words1))

# find the average difficulty of rounds based on value column
mean_difficulty = df.groupby('round').value.mean().reset_index()
# remove hashtags to observe mean_difficulty
#print(mean_difficulty)

# calculate average value of filtered dataset
def average_value(dataset, words):
  filtered_dataset = word_filter(dataset, words)
  return filtered_dataset.value.mean()

# remove hashtags to test average_value function
#words2 = ['King']
#print(average_value(df, words2))

# calculate unique answers counts in filtered dataset
def unique_answers(dataset, words):
  filtered_dataset = word_filter(dataset, words)
  return filtered_dataset.answer.value_counts().reset_index()

# remove hashtags to test unique_answers function
#words3 = ['King']
#print(unique_answers(df, words3))

# compare computer use in 90s vs 2000s
filtered_by_computer = word_filter(df, ['Computer'])
filtered_by_computer_90s = filtered_by_computer[(filtered_by_computer.air_date > datetime.datetime(1990, 1, 1)) & (filtered_by_computer.air_date < datetime.datetime(1999, 12, 31))]
filtered_by_computer_00s = filtered_by_computer[(filtered_by_computer.air_date > datetime.datetime(2000, 1, 1)) & (filtered_by_computer.air_date < datetime.datetime (2009, 12, 31))]

# remove hashtags to see how computer use has changed
#print('Computer use has changed from {} in 90s to {} in 00s.'.format(str(len(filtered_by_computer_90s)), str(len(filtered_by_computer_00s))))

# Jeopardy Game!

def play_game(dataset):
  yes_or_no = "yes"
  correct = 0
  incorrect = 0

  while (yes_or_no == "yes"):
    random_index = random.randint(0, 216930)
    question = dataset.question.iloc[random_index]
    answer = dataset.answer.iloc[random_index]
    print(question)
    user_input = input('And your answer is: ')

    if user_input.lower() == answer.lower():
      print('Good job! You got it right!')
      correct += 1
      score = "Correct: " + str(correct) + ' vs Incorrect: ' + str(incorrect)
      print('Current Score: ' + score)
      yes_or_no = input('Want to continue? (yes/no): ' )
    else:
      print('Oops. You missed! The correct answer was: ' + answer)
      incorrect += 1
      score = "Correct: " + str(correct) + ' vs Incorrect: ' + str(incorrect)
      print('Current Score: ' + score)
      yes_or_no = input('Want to continue? (yes/no): ' )
  return 'Final Score: ' + score

# Let's play Jeopardy!
play_game(df)