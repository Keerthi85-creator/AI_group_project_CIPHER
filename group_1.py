# -*- coding: utf-8 -*-
"""finalFILE.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yrsQp8rswFSV-xLyI2W1TDmmRNvYHAhy
"""

#harshitha-links
def google_search(query):
    listt = []
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")
    for j in search(query, tld="co.in", num=10, stop=10, pause=2):
        print(j)



#harshitha-para
from googlesearch import search
import requests
from bs4 import BeautifulSoup

def get_info_from_google(query, num_results=3):
    def extract_relevant_text(soup):
        relevant_text = []
        for element in soup.find_all(['p']):
            text = element.get_text(separator=' ', strip=True)
            if text:
                relevant_text.append(text)
        return ' '.join(relevant_text)

    try:
        relevant_information = []
        search_results = search(query, num=num_results, stop=num_results)
        for url in search_results:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            relevant_text = extract_relevant_text(soup)
            if relevant_text:
                relevant_information.append(relevant_text)
        return relevant_information
    except Exception as e:
        print("Error:", e)
        return []

#harshitha-library
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from googlesearch import search

def relevant_data_from_links(query):
    def get_web_page_text(url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = ' '.join([p.get_text() for p in soup.find_all('p')])
            return text
        except Exception as e:
            print(f"Error fetching content from {url}: {e}")
            return None

    def top_links(query):
        listt = []
        try:
            for j in search(query, tld="co.in", num=10, stop=10, pause=2):
                listt.append(j)
        except ImportError:
            print("No module named 'google' found")
        return listt

    # Get top links from Google search
    links = top_links(query)

    # Get text content from each link
    link_texts = [get_web_page_text(link) for link in links if get_web_page_text(link) is not None]

    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit-transform the documents
    tfidf_matrix = vectorizer.fit_transform(link_texts)

    # Transform the query
    query_vector = vectorizer.transform([query])

    # Calculate cosine similarity between query and documents
    similarities = cosine_similarity(query_vector, tfidf_matrix)

    # Sort indices based on similarity scores
    sorted_indices = similarities.argsort()[0][::-1]

    # Retrieve relevant data from the most similar document
    relevant_index = sorted_indices[0]
    relevant_link = links[relevant_index]
    relevant_text = link_texts[relevant_index]

    return relevant_link, relevant_text





#Harshada
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def train_and_predict_logistic_regression(data_file, feature_values):
    # Load the dataset
    data = pd.read_csv(data_file)

    # Keep only relevant columns
    data = data[['no_of_weekend_nights', 'no_of_week_nights', 'lead_time', 'arrival_month', 'avg_price_per_room', 'no_of_special_requests', 'arrival_date', 'booking_status']]

    # Convert 'arrival_date' to datetime and extract day
    data['arrival_date'] = pd.to_datetime(data['arrival_date']).dt.day

    # Define feature weights
    feature_weights = {
        'no_of_weekend_nights': 0.15,
        'no_of_week_nights': 0.2,
        'lead_time': 0.1,
        'arrival_month': 0.05,
        'avg_price_per_room': 0.15,
        'no_of_special_requests': 0.05,
        'arrival_date': 0.3
    }

    # Calculate score for each reservation
    data['reservation_score'] = (
        data['no_of_weekend_nights'] * feature_weights['no_of_weekend_nights'] +
        data['no_of_week_nights'] * feature_weights['no_of_week_nights'] +
        data['lead_time'] * feature_weights['lead_time'] +
        data['arrival_month'] * feature_weights['arrival_month'] +
        data['avg_price_per_room'] * feature_weights['avg_price_per_room'] +
        data['no_of_special_requests'] * feature_weights['no_of_special_requests'] +
        data['arrival_date'] * feature_weights['arrival_date']
    )

    # Predict reservation based on score threshold
    threshold = 0.5  # Define a threshold for reservation prediction
    data['predicted_reservation'] = (data['reservation_score'] >= threshold).astype(int)

    # Splitting the data into features and target variable
    X = data.drop(columns=['booking_status', 'predicted_reservation', 'arrival_month'])  # Drop 'arrival_month' from features
    y = data['booking_status']

    # Splitting the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Model training
    model = LogisticRegression()
    model.fit(X_train_scaled, y_train)

    # Model evaluation
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print('Accuracy:', accuracy)

    # Predict booking status for the input feature values
    scaled_features = scaler.transform([feature_values])
    predicted_booking_status = model.predict(scaled_features)
    print('Predicted booking status:', 'Booked' if predicted_booking_status == 1 else 'Not booked')

    return model, scaler, accuracy
'''
# Example usage:
new_features = [2, 3, 50, 8, 200, 1, 15]  # Example feature values for a reservation
trained_logistic_regression_model, scaler, accuracy = train_and_predict_logistic_regression('Hotel_Reservations.csv', new_features)
'''





##soumya-cg
import nltk
from nltk.chat.util import Chat, reflections
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression, LinearRegression
import pandas as pd
def predict_placement_and_salary(input_data):
    # Load the data
    data = pd.read_csv("combined_dataset.csv")

    # Encode categorical variables
    label_encoders = {}
    for col in ['college_name', 'stream', 'degree', 'gender']:
        label_encoders[col] = LabelEncoder()
        data[col] = label_encoders[col].fit_transform(data[col])

    # Scale the input features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data[['years_of_experience', 'college_name', 'stream', 'degree', 'age', 'gender']])

    # Split the data into features and target variables
    X_train = X_scaled
    y_train_placement = data['placement_status']
    y_train_salary = data['salary']

    # Train the logistic regression model for placement status
    model_placement = LogisticRegression(max_iter=1000)
    model_placement.fit(X_train, y_train_placement)

    # Train the linear regression model for salary
    model_salary = LinearRegression()
    model_salary.fit(X_train, y_train_salary)

    # Encode the input data
    input_data_encoded = {}
    for col in ['college_name', 'stream', 'degree', 'gender']:
        input_data_encoded[col] = label_encoders[col].transform([input_data[col]])[0]
    input_data_encoded['years_of_experience'] = input_data['years_of_experience']
    input_data_encoded['age'] = input_data['age']

    # Scale the input features
    X_input = scaler.transform([list(input_data_encoded.values())])

    # Make predictions on the input data for placement status and salary
    placement_status = model_placement.predict(X_input)[0]
    salary = model_salary.predict(X_input)[0]

    return placement_status, salary




#keerthi
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier

def predict_weather(input_data, k):
    # Load the dataset
    df = pd.read_csv("seattle-weather.csv.xls")

    # Label encode the 'weather' column
    lc = LabelEncoder()
    df["weather"] = lc.fit_transform(df["weather"])

    # Drop the 'date' column
    df = df.drop(["date"], axis=1)

    # Prepare the data
    x = ((df.loc[:, df.columns!="weather"]).astype(int)).values
    y = df["weather"].values

    # Split the data into train and test sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=2)

    # Initialize classifiers
    knn = KNeighborsClassifier(n_neighbors=k)
    svm = SVC()
    gbc = GradientBoostingClassifier()

    # Train the classifiers
    knn.fit(x_train, y_train)
    svm.fit(x_train, y_train)
    gbc.fit(x_train, y_train)

    # Get accuracies
    knn_accuracy = knn.score(x_test, y_test) * 100
    svm_accuracy = svm.score(x_test, y_test) * 100
    gbc_accuracy = gbc.score(x_test, y_test) * 100

    # Make prediction
    ot = gbc.predict(input_data)

    # Decode the prediction
    weather_labels = lc.inverse_transform([0, 1, 2, 3, 4])
    predicted_weather = weather_labels[ot[0]]

    # Print the output
    print("Predicted Weather:", predicted_weather)
    print("KNN Accuracy (k={}): {:.2f}%".format(k, knn_accuracy))
    print("SVM Accuracy: {:.2f}%".format(svm_accuracy))
    print("Gradient Boosting Accuracy: {:.2f}%".format(gbc_accuracy))

     # Different k values to test





# Example usage:

#harshitha

import nltk
from nltk.chat.util import Chat, reflections
import webbrowser  # For opening URLs
import requests    # For fetching stock data
from bs4 import BeautifulSoup  # For web scraping

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Define some patterns and responses
patterns = [
    (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
    (r'how are you?', ['I\'m good, thank you!', 'I\'m doing well, thanks for asking.']),
    (r'what is your name?', ['You can call me CIPHER.', 'I go by the name CIPHER.']),
    (r'(.*) your name?', ['You can call me CIPHER.', 'I go by the name CIPHER.']),
    (r'marks', ['Sure, please provide your 10th marks, 12th marks, and CGPA separated by commas.']),
    (r'searches|google|links', ['Sure, what would you like to search for?']),
    (r'stock', ['Sure, which stock would you like to check?']),
]
'''
query = input("You: ")
google_search(query)
print("******************************")
relevant_link, relevant_text = relevant_data_from_links(query)
print("Relevant Link:", relevant_link)
print("Relevant Text:", relevant_text[:2000])
print("******************************")

relevant_info = get_info_from_google(query)
for info in relevant_info:
  print(info)
'''

'''
m=input("mode:")
if m=="links":
  query = input("You: ")
  google_search(query)
  print("******************************")
elif m=="library":
  query = input("You: ")
  relevant_link, relevant_text = relevant_data_from_links(query)
  print("Relevant Link:", relevant_link)
  print("Relevant Text:", relevant_text[:2000])
  print("******************************")
else:
  query = input("You: ")
  relevant_info = get_info_from_google(query)
  for info in relevant_info:
    print(info)
'''

'''
query = input("You: ")
while query !="quit":


  m=input("mode:")
  if m=="links":
    google_search(query)
    print("******************************")
  elif m=="library":
    relevant_link, relevant_text = relevant_data_from_links(query)
    print("Relevant Link:", relevant_link)
    print("Relevant Text:", relevant_text[:2000])
    print("******************************")
  else:
    relevant_info = get_info_from_google(query)
    for info in relevant_info:
      print(info)
  query = input("You: Enter the word you want to search for")
'''
word = "HI"
while True:
    user_input=input("what do you want to do:")
    if any(word in user_input.lower() for word in ['quit', 'stop']):
      print("Goodbye!!")
      break

    elif any(word in user_input.lower() for word in ['search', 'google']):
        query = input("You: Enter the word you want to search for ")
        m=input("mode:")
        if any(word in m.lower() for word in ['links', 'link','website','websites']):
          google_search(query)
          print("******************************")
        elif m=="library" or  m=='scientific data':
          relevant_link, relevant_text = relevant_data_from_links(query)
          print("Relevant Link:", relevant_link)
          print("Relevant Text:", relevant_text[:2000])
          print("******************************")
        else:
          relevant_info = get_info_from_google(query)
          for info in relevant_info:
              print(info)

    elif any(word in user_input.lower() for word in ['weather', 'sky', 'rain','summer','hot','temperature']):
          print("Enter the values of precipitation seattle")
          a= float(input("You: "))
          print("Enter the values of Maximum Temperature in seattle")
          b=float(input("You:"))
          print("Enter the values of Minimum Temperature in seattle")
          c=float(input("You:"))
          print("Enter the values of wind speed in seattle")
          d=float(input("You:"))
          input_data=[[a,b,c,d]]
          k=int(input("number of neighbours: "))
          predict_weather(input_data,k)


    elif any(word in user_input.lower() for word in ['marks', 'placed', 'pass', 'selected', 'job_prediction', 'salary_prediction']):
          print("Enter your years_of_experience")
          a = float(input("You: "))
          print("Enter your college_name")
          b = input("You: ")
          print("Enter your stream")
          c = input("You: ")
          print("Enter your degree")
          d = input("You: ")
          print("Enter your age")
          e = float(input("You: "))
          print("Enter your gender")
          f = input("You: ")

            # Create a dictionary with input data
          input_data = {'years_of_experience': a,
                          'college_name': b,
                          'stream': c,
                          'degree': d,
                          'age': e,
                          'gender': f}

            # Predict placement status and salary
          placement_status, salary = predict_placement_and_salary(input_data)
          print(f'Predicted Salary: {salary}')

    elif any(word in user_input.lower() for word in ['book', 'reservations','tickets','hotel','booking']):
          print("Enter the no of weekend nights")
          a=float(input("You"))
          print("Enter the no of week nights")
          b=float(input("You "))
          print("Enter the  lead time")
          c=float(input("You "))
          print("Enter the arrival month")
          d=float(input("You "))
          print("Enter the avg price per room")
          e=float(input("You "))
          print("Enter the no of special requests")
          f=float(input("You "))
          print("Enter the  arrival date")
          g=float(input("You "))

          new_features = [a,b,c,d,e,f,g]
          trained_logistic_regression_model, scaler, accuracy = train_and_predict_logistic_regression('Hotel_Reservations.csv', new_features)

    else:
            print("Dont know")