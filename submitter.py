
import subprocess
import time
import json
from solution_manager import save_solution_to_file
from openai_client import get_solution_from_openai

def load_results(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_results(filename, results):
    with open(filename, 'w') as file:
        json.dump(results, file, indent=4)

def submit_solution_to_kattis(filename, problem_id, attempt, problem_statement, conversation_history, i):
    time.sleep(60) # Pause for a minute before submitting to avoid hitting submission limits
    cmd = f'kattis {filename}'
    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(input=b'y\n')
    
    stderr_output = stderr.decode(errors='replace')
    stdout_output = stdout.decode(errors='replace')

    print(f"stdout: {stdout_output}"  + "\n\n")
    #print(f"{conversation_history}" + "\n\n")

    # Get the last line of the stdout_output to check the result
    last_line = stdout_output.strip().split('\n')[-1]

    print(conversation_history)

    if process.returncode != 0:
        if attempt != 2:
            attempt += 1
            print(f"Attempt {attempt} failed for problem {problem_id} with error: {last_line}. Retrying...")
            feedback = f"The solution was incorrect or caused a runtime error. The last line of the output received was: '{last_line}'. Please provide a corrected solution. Give no explanation or text, only the code."
            revised_solution, new_conversation_history = get_solution_from_openai(problem_statement, feedback, conversation_history)
            if revised_solution:
                new_filename = save_solution_to_file(problem_id, revised_solution, f"solutions{attempt}")
                submit_solution_to_kattis(new_filename, problem_id, attempt, problem_statement, new_conversation_history, i)
        else:
            print(f"Max attempts reached for problem {problem_id}. Moving to the next problem.")
    elif "token" in last_line:
        print(f"max token reached {problem_id}")
    else:
        print(f"Solution submitted successfully for problem {problem_id}")

    results = load_results('kattis_results.json')
    
    # Save the latest response from Kattis to a dictionary
    results[i] = {
        "problem_id": problem_id,
        "result": stdout_output.strip().split('\rTest cases: ')[-1] + "\n\n" + last_line,
        "attempt": attempt
    }

    # Save results after each problem is processed
    save_results('kattis_results.json', results)
