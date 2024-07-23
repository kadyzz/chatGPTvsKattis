import os
import json
import requests
from bs4 import BeautifulSoup, Tag
from autokattis import Kattis

# Initialize Kattis instance with your credentials
username = os.getenv("KATTIS_USERNAME")
token = os.getenv("KATTIS_TOKEN")
kattis_instance = Kattis(username, token)
api_key = os.getenv("OPENAI_API_KEY")

# Fetch all problems and store them in a JSON file
def fetch_and_cache_problems():
    problems = kattis_instance.problems(*[True]*4)
    
    # Save problems to a JSON file
    with open('problems_cache.json', 'w') as f:
        json.dump(problems, f, indent=4)

# Fetch problem statements and store them in a JSON file
def fetch_problem_statements(limit=10):
    with open('problems_cache.json', 'r') as f:
        problems = json.load(f)
    
    # Limit to the first 10 problems
    problems = problems[:limit]
    
    problem_statements = []

    for problem in problems:
        problem_id = problem['id']
        problem_link = problem['link']
        
        # Fetch the problem page
        response = requests.get(problem_link)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        
        # Attempt to extract the problem statement
        problem_statement_div = soup.find('div', {'class': 'problembody'})
        if problem_statement_div:
            # Extract text content from the problem statement, handling <tt> and <br> tags
            problem_statement = []
            for element in problem_statement_div.descendants:
                if isinstance(element, Tag):
                    if element.name == 'tt':
                        problem_statement.append('\n' + element.get_text() + '\n')
                    elif element.name == 'br':
                        problem_statement.append('\n')
                else:
                    problem_statement.append(element.strip())
            problem_statement = ' '.join(problem_statement).replace('\n ', '\n').replace(' \n', '\n')
        else:
            problem_statement = 'Problem statement not found.'
        
        # Add problem details and statement to the list
        problem_statements.append({
            "id": problem_id,
            "name": problem['name'],
            "statement": problem_statement
        })
    
    # Save problem statements to a JSON file
    with open('problem_statements_cache.json', 'w') as f:
        json.dump(problem_statements, f, indent=4)

# Send problem statement to OpenAI API and get the solution
def get_solution_from_openai(problem_statement):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are an assistant that helps with programming problems."},
            {"role": "user", "content": f"Solve the following problem:\n{problem_statement}"}
        ],
        "max_tokens": 1500,
        "temperature": 0.5
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None

# Process problem statements and save solutions
def process_statements_and_save_solutions():
    with open('problem_statements_cache.json', 'r') as f:
        problem_statements = json.load(f)
    
    solutions = []

    for problem in problem_statements:
        problem_id = problem['id']
        problem_name = problem['name']
        problem_statement = problem['statement']
        
        # Get solution from OpenAI API
        solution = get_solution_from_openai(problem_statement)
        
        # Add problem details and solution to the list
        solutions.append({
            "id": problem_id,
            "name": problem_name,
            "statement": problem_statement,
            "solution": solution
        })
    
    # Save solutions to a JSON file
    with open('problem_solutions_cache.json', 'w') as f:
        json.dump(solutions, f, indent=4)

# Run the functions to fetch and cache problems and their statements
fetch_and_cache_problems()
fetch_problem_statements(limit=10)
process_statements_and_save_solutions()

