import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

# Load the dataset
data = pd.read_csv('data/data.csv')

# Encode categorical variables
label_encoder = LabelEncoder()
data['Symptom'] = label_encoder.fit_transform(data['Symptom'])
data['Condition'] = label_encoder.fit_transform(data['Condition'])
data['Treatment'] = label_encoder.fit_transform(data['Treatment'])
data['Precaution'] = label_encoder.fit_transform(data['Precaution'])
data['Medicine'] = label_encoder.fit_transform(data['Medicine'])
data['Effectiveness'] = label_encoder.fit_transform(data['Effectiveness'])

# Features and target
X = data[['Symptom']]
y = data['Condition']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, 'model/symptom_condition_model.pkl')
