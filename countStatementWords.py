import json

# Load the problem_statements JSON
with open('problem_statements_cache.json', 'r') as f:
    problem_statements = json.load(f)

# Load the other JSON file
with open('hard_problems.json', 'r') as f:
    results = json.load(f)

# Create a dictionary for quick lookup of problem statements by 'id'
problem_statements_dict = {item['id']: item['statement'] for item in problem_statements}

# Iterate over the results and calculate the word count for the matching statement
for result in results:
    problem_id = result['problem_id']
    if problem_id in problem_statements_dict:
        statement = problem_statements_dict[problem_id]
        word_count = len(statement.split())
        print(f"Problem ID: {problem_id}, Word Count in 'statement': {word_count}")
    else:
        print(f"Problem ID: {problem_id} not found in problem statements")

# Optionally, save the results with word counts back to a file
for result in results:
    problem_id = result['problem_id']
    if problem_id in problem_statements_dict:
        statement = problem_statements_dict[problem_id]
        word_count = len(statement.split())
        result['statement_word_count'] = word_count

with open('results_with_word_count.json', 'w') as f:
    json.dump(results, f, indent=4)
