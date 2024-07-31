import json
import subprocess
import time
from kattis_client import initialize_kattis_client
from openai_client import get_solution_from_openai
from problem_fetcher import fetch_and_cache_problems, fetch_problem_statements
from solution_manager import save_solution_to_file
from submitter import submit_solution_to_kattis
from utils import load_json, save_json

    # Step 1: Fetch and cache problems
    # Step 2: Fetch problem statements

def process_statements_and_save_solutions():
    # Step 3: Load problem statements and process them
    problem_statements = load_json('problem_statements_cache.json')

    # Dictionary to hold results
    #submission_count = 0

    i = 98

    for problem in problem_statements[i:(i+5)]:

        problem_id = problem['id']
        problem_statement = problem['statement']
        conversation_history = []
        
        # Step 4: Get initial solution from OpenAI API
        solution, conversation_history = get_solution_from_openai(problem_statement, conversation_history=conversation_history) 
    
        if solution:
             # Step 5: Save the solution to a file
            filename = save_solution_to_file(problem_id, solution, "solutions1")

            # Step 6: Submit the solution to Kattis
            try:
                submit_solution_to_kattis(filename, problem_id, 1, problem_statement, conversation_history, i)
            except subprocess.CalledProcessError:
                continue

            i += 1

            #submission_count += 1
            
            # Pause for a minute after every 10 submissions
            #if submission_count % 5 == 0:
                #print("Waiting for 1 minute to avoid hitting submission limits...")

           
if __name__ == "__main__":
    kattis_instance = initialize_kattis_client()
    #print(kattis_instance.problems(*[True]*4).to_df())
    #fetch_and_cache_problems(kattis_instance)
    #fetch_problem_statements(limit=None)
    process_statements_and_save_solutions()
