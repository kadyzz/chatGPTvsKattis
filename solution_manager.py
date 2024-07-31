import os

def save_solution_to_file(problem_id, solution, directory):
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filename = os.path.join(directory, f'{problem_id}.py')
    with open(filename, 'w') as f:
        f.write(solution)
    return filename  
