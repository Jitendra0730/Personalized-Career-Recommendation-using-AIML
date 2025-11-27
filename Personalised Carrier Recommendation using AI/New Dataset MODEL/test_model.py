import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sentence_transformers import SentenceTransformer

def categorize_salary(salary):
    if salary <= 50000:
        return 'Low'
    elif salary <= 80000:
        return 'Medium'
    else:
        return 'High'

def load_dataset():
    data = pd.read_csv(r"C:\Users\metro\Desktop\UDP 7th Sem\Personalised Carrier Recommendation using AI\New Dataset MODEL\New Dataset\job_recommendation_dataset.csv")
    data = data.dropna()
    data['Salary'] = pd.to_numeric(data['Salary'], errors='coerce')
    print(f"Initial dataset size: {len(data)} rows")
    data = data[~data['Job Title'].str.lower().isin(['make'])]
    data = data.drop_duplicates(subset=['Job Title', 'Industry', 'Required Skills'])
    data['Salary Category'] = data['Salary'].apply(categorize_salary)
    data = data.reset_index(drop=True)
    print(f"Cleaned dataset size: {len(data)} rows")
    return data

def preprocess_data(data):
    categorical_cols = ['Experience Level', 'Industry', 'Location', 'Salary Category']
    numerical_cols = ['Salary']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols),
            ('num', StandardScaler(), numerical_cols)
        ])
    
    X = preprocessor.fit_transform(data)
    return X, preprocessor, data

def generate_text_embeddings(data, user_input):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    job_texts = data['Job Title'] + " " + data['Industry'] + " " + data['Required Skills']
    job_embeddings = model.encode(job_texts.tolist(), show_progress_bar=False)
    
    user_text = f"{user_input['interests']} {user_input['skills']} {user_input['profession']}"
    user_embedding = model.encode([user_text], show_progress_bar=False)
    
    text_similarities = cosine_similarity(user_embedding, job_embeddings)[0]
    
    print(f"Text similarity stats: min={text_similarities.min():.4f}, max={text_similarities.max():.4f}, mean={text_similarities.mean():.4f}")
    
    top_indices = np.argsort(text_similarities)[-10:]
    print("\nTop 10 jobs by text similarity (for debugging):")
    for idx in top_indices:
        print(f"Job: {data.iloc[idx]['Job Title']}, Industry: {data.iloc[idx]['Industry']}, Similarity: {text_similarities[idx]:.4f}")
    
    return text_similarities

def create_suitability_labels(data, user_input, text_similarities):
    if len(text_similarities) != len(data):
        raise ValueError(f"Mismatch: text_similarities ({len(text_similarities)}) and data ({len(data)}) have different lengths")
    
    labels = []
    profession_keywords = ['engineer', 'developer', 'programmer', 'scientist', 'teacher', 'educator', 'administrator']
    user_salary_category = categorize_salary(user_input['expected_salary'])
    
    for idx, row in data.iterrows():
        title_match = any(keyword in row['Job Title'].lower() for keyword in profession_keywords)
        
        text_match = text_similarities[idx] > 0.4
        salary_match = row['Salary Category'] == user_salary_category
        exp_match = (
            (row['Experience Level'] == 'Entry Level' and user_input['experience'] <= 2) or
            (row['Experience Level'] == 'Mid Level' and 2 < user_input['experience'] <= 5) or
            (row['Experience Level'] == 'Senior Level' and user_input['experience'] > 5)
        )
        
        if text_match and title_match and (salary_match or exp_match):
            labels.append(1)
        else:
            labels.append(0)
    
        if title_match and row['Industry'] not in [user_input['interests'], 'Software'] and labels[-1] == 1:
            print(f"Warning: Mismatched industry for {row['Job Title']}: Expected {user_input['interests']} or Software, got {row['Industry']}")
    
    if sum(labels) == 0:
        top_indices = np.argsort(text_similarities)[-5:]  # Increased to top 5 for robustness
        for idx in top_indices:
            if any(keyword in data.iloc[idx]['Job Title'].lower() for keyword in profession_keywords):
                labels[idx] = 1
    
    print(f"Label distribution: {sum(labels)} suitable, {len(labels) - sum(labels)} unsuitable")
    return np.array(labels)

def get_user_input():
    print("Welcome to the Personalized Career Recommendation System!")
    interests = input("Enter your interests (e.g., technology, healthcare, education): ").lower().strip()
    skills = input("Enter your skills (e.g., programming, data analysis, teaching): ").lower().strip()
    profession = input("Enter your preferred profession (e.g., engineer, teacher, scientist): ").lower().strip()
    try:
        expected_salary = float(input("Enter your expected salary : "))
    except ValueError:
        expected_salary = 0.0
        print("Invalid salary input. Defaulting to 0.")
    try:
        experience = float(input("Enter your experience (years): "))
    except ValueError:
        experience = 0.0
        print("Invalid experience input. Defaulting to 0.")
    
    return {
        'interests': interests,
        'skills': skills,
        'profession': profession,
        'expected_salary': expected_salary,
        'experience': experience
    }

def create_user_profile(user_input, preprocessor, data):
    user_data = pd.DataFrame({
        'Experience Level': ['Entry Level' if user_input['experience'] <= 2 else 'Mid Level' if user_input['experience'] <= 5 else 'Senior Level'],
        'Industry': [data['Industry'].mode()[0]],
        'Location': [data['Location'].mode()[0]],
        'Salary Category': [categorize_salary(user_input['expected_salary'])],
        'Salary': [user_input['expected_salary']]
    })
    return preprocessor.transform(user_data)

def recommend_jobs(user_input, user_vector, X, data, preprocessor, text_similarities, top_n=5):
    labels = create_suitability_labels(data, user_input, text_similarities)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, labels)
    
    try:
        suitability_probs = clf.predict_proba(X)[:, 1]
    except IndexError:
        print("Warning: Only one class predicted. Falling back to text similarity.")
        suitability_probs = text_similarities
    
    user_salary_category = categorize_salary(user_input['expected_salary'])
    suitable_indices = np.where(
        (suitability_probs > 0.5) & 
        (data['Salary Category'] == user_salary_category)
    )[0]
    if len(suitable_indices) < top_n:
        print("Few suitable jobs found. Including high text-similarity jobs.")
        top_text_indices = np.argsort(text_similarities)[-top_n:]
        suitable_indices = np.unique(np.concatenate([suitable_indices, top_text_indices]))
    
    X_suitable = X[suitable_indices]
    similarities = cosine_similarity(user_vector, X_suitable)
    
    combined_scores = 0.5 * similarities[0] + 0.5 * text_similarities[suitable_indices]
    combined_scores = np.clip(combined_scores, 0, 1)
    
    top_indices = suitable_indices[combined_scores.argsort()[-top_n:][::-1]]
    recommendations = data.iloc[top_indices][['Job Title', 'Company', 'Location', 'Experience Level', 'Salary', 'Salary Category', 'Industry', 'Required Skills']]
    
    return recommendations, combined_scores[combined_scores.argsort()[-top_n:][::-1]], text_similarities[top_indices]

# Main function
def main():
    data = load_dataset()
    X, preprocessor, data = preprocess_data(data)
    
    user_input = get_user_input()
    
    text_similarities = generate_text_embeddings(data, user_input)
    
    user_vector = create_user_profile(user_input, preprocessor, data)
    
    recommendations, scores, text_scores = recommend_jobs(user_input, user_vector, X, data, preprocessor, text_similarities)
    
    print("\nTop Career Recommendations:")
    for idx, row in recommendations.iterrows():
        print(f"\nJob Title: {row['Job Title']}")
        print(f"Company: {row['Company']}")
        print(f"Location: {row['Location']}")
        print(f"Experience Level: {row['Experience Level']}")
        print(f"Salary Category: {row['Salary Category']}")
        print(f"Industry: {row['Industry']}")
        print(f"Required Skills: {row['Required Skills']}")
        print(f"Combined Similarity Score: {scores[list(recommendations.index).index(idx)]:.4f}")
        print(f"Text Similarity Score: {text_scores[list(recommendations.index).index(idx)]:.4f}")

if __name__ == "__main__":
    main()