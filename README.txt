An AI-powered dashboard for automated nasalance analysis and speech resonance classification.
This project helps in identifying speech resonance disorders such as Hyponasal, Normal, and Hypernasal speech using Machine Learning techniques.
Features
Speech resonance classification
Severity prediction (Mild / Moderate / Severe)
Interactive dashboard visualization
Machine Learning based prediction system
Language-wise normative comparison
Z-score based analysis
User-friendly interface for clinical interpretation
Technologies Used
Python
Machine Learning
Logistic Regression
Pandas
NumPy
Scikit-learn
Streamlit / Flask (update based on your project)
Matplotlib / Seaborn (if used)
Project Objective
The main objective of this project is to automate the interpretation of nasalance measures for assisting in speech disorder diagnosis. The system compares patient nasalance values with normative speech data and predicts resonance abnormalities.
Dataset Information
The project uses nasalance-related features such as:
Nasalance Mean
Age
Gender
Language
The model analyzes these features to classify resonance conditions.
Machine Learning Model
Final Model Used
Logistic Regression
Model Accuracy
Accuracy: 80.5%
Other Models Evaluated
Decision Tree
Random Forest
Gradient Boosting
KNN
SVM
Project Structure:
Nasalance_AI_Dashboard/
│
├── data/
├── models/
├── app.py
├── requirements.txt
├── README.md
└── assets/

Output
The system predicts:
Resonance Type
Hyponasal
Normal
Hypernasal
Severity Level
Mild
Moderate
Severe
Future Enhancements
Real-time voice analysis
Audio file upload support
Deep Learning integration
Cloud deployment
Multi-language support
Clinical report generation
