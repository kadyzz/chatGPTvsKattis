import json
import requests
from bs4 import BeautifulSoup, Tag

def fetch_and_cache_problems(kattis_instance):
    problems = kattis_instance.problems(*[True]*4)
    with open('problems_cache.json', 'w') as f:
        json.dump(problems, f, indent=4)

def fetch_problem_statements(limit):
    with open('problems_cache.json', 'r') as f:
        problems = json.load(f)
    
    problems = problems[:limit]
    problem_statements = []

    for problem in problems:
        problem_id = problem['id']
        problem_link = problem['link']
        response = requests.get(problem_link)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        problem_statement_div = soup.find('div', {'class': 'problembody'})
        if problem_statement_div:
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
        
        problem_statements.append({
            "id": problem_id,
            "name": problem['name'],
            "statement": problem_statement
        })
    
    with open('problem_statements_cache.json', 'w') as f:
        json.dump(problem_statements, f, indent=4)
