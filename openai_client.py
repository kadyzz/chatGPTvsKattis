import requests
import os

api_key = os.getenv("OPENAI_API_KEY")

def get_solution_from_openai(problem_statement, feedback=None, conversation_history = None):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    messages = [
        {"role": "system", "content": "You are an sofware developer that solves programming problems."},
        {"role": "user", "content": f"Solve the following problem efficiently in Python, take your time. Make sure your solution passes the given sample tests. Don't give any explanations, answer only with the code:\n{problem_statement}"}
    ]

    if conversation_history:
        messages = conversation_history
    
    if feedback:
        messages.append({"role": "user", "content": feedback})
    
    payload = {
        "model": "gpt-4o",
        "messages": messages,
        "max_tokens": 1500,
        "temperature": 0.5
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        solution = result['choices'][0]['message']['content'].strip()
        if solution.startswith("```python"):
            solution = solution[len("```python"):].strip()
        if solution.endswith("```"):
            solution = solution[:-len("```")].strip()
        messages.append({"role": "assistant", "content": solution})
        return solution, messages
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None, messages
