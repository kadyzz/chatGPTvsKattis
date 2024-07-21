import os
import openai
import subprocess
from autokattis import Kattis

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Kattis instance
kattis_instance = Kattis(username=os.getenv("KATTIS_USERNAME"), token=os.getenv("KATTIS_TOKEN"))

def get_solution_from_chatgpt(problem_statement):
    prompt = f"Write a Java program to solve the following problem:\n\n{problem_statement}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1500,
    )
    solution = response.choices[0].text.strip()
    return solution

def submit_solution(problem_id, solution_file):
    # Use Kattis CLI to submit the solution
    result = subprocess.run(['kattis', 'submit', solution_file], capture_output=True, text=True)
    return result.stdout

def get_submission_response(submission_id):
    response = kattis_instance.get_submission(submission_id)
    return response['status']

def get_problems_by_difficulty(difficulty):
    problems = kattis_instance.get_problems_by_difficulty(difficulty)
    return problems

# Example usage
difficulty = 'easy'
problems = get_problems_by_difficulty(difficulty)
for problem in problems:
    problem_id = problem['id']
    problem_name = problem['name']
    print(f"Fetching problem: {problem_name} (ID: {problem_id})")
    
    # Get the problem statement
    problem_statement = kattis_instance.get_problem_statement(problem_id)
    
    # Get the solution from ChatGPT
    solution = get_solution_from_chatgpt(problem_statement)
    
    # Save the solution to a file
    solution_file = f"{problem_id}.java"
    with open(solution_file, "w") as f:
        f.write(solution)
    
    # Submit the solution using Kattis CLI
    submission_result = submit_solution(problem_id, solution_file)
    print(f'Submission result for {problem_name}: {submission_result}')
    
    # Parse submission ID from submission result
    # Assuming the result contains a URL with the submission ID
    submission_id = submission_result.split('/')[-1].strip()
    
    # Fetch the submission response
    submission_response = get_submission_response(submission_id)
    print(f'Submission response for {problem_name}: {submission_response}')
