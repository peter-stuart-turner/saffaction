import pandas as pd

df = pd.read_excel('mindmap-v3.xlsx', sheet_name='solutions')

def find_category(i, row):
    if pd.isna(row['Problem']) or pd.isnull(row['Ideas']):
        for i in range(i,0,-1):
            if not pd.isna(df.iloc[i]['Problem']):
                return df.iloc[i]['Problem']
    else:
        return row['Problem']

def find_problem(df, i):
    row = df.iloc[i]
    if pd.isna(row['Ideas']) or pd.isnull(row['Ideas']):
        for i in range(i,0,-1):
            if not pd.isna(df.iloc[i]['Ideas']):
                return df.iloc[i]['Ideas']
    else:
        return row['Ideas']

def find_problems_for_category(df, category_name):
    problems = []
    for i, row in df.iterrows():
        if row['Problem']==category_name:
            if find_problem(df, i) not in problems:
                problems.append(find_problem(df, i))
    return problems

def find_solutions_for_problem(df, problem):
    solutions = []
    for i, row in df.iterrows():
        if find_problem(df, i) == problem:
            if not pd.isna(row['Entity(s)']):
                if row['Entity(s)'] not in solutions:
                    solutions.append(row['Entity(s)'])
    return solutions

def find_problem_category_links(df, entries, problem_category):
    links = []
    problems = find_problems_for_category(df, problem_category)
    for p in entries['problems']:
        if p.get('text') in problems:
            links.append(p.get('id'))
    return links

def find_problem_links(df, entries, problem):
    links = []
    solutions = find_solutions_for_problem(df, problem)
    for s in entries.get('solutions'):
        if s.get('text') in solutions:
            links.append(s.get('id'))
    return links


def create_entries(df):
    problem_categories = []
    problems = []
    solutions = []
    for pc in df['Problem'].unique():
        if not pd.isna(pc) and not pd.isnull(pc):
            problem_categories.append(pc)

    for i, row in df.iterrows():
        if not pd.isna(row['Ideas']) and not pd.isnull(row['Ideas']):
            if row['Ideas'] not in problems:
                problems.append(row['Ideas'])
        else:
            if find_problem(df, i) not in problems:
                problems.append(find_problem(df, i))
    for i, row in df.iterrows():
        if not pd.isna(row['Entity(s)']) and not pd.isnull(row['Entity(s)']):
            if row['Entity(s)'] not in solutions:
                solutions.append(row['Entity(s)'])
            else:
                # TODO
                pass
    data = {
        'problem_categories': [],
        'problems': [],
        'solutions': []
    }
    i = 0
    for pc in problem_categories:
        data['problem_categories'].append({
            'id': i,
            'links': [],
            'weight': 1,
            'text': pc
        })
        i += 1
    for p in problems:
        data['problems'].append({
            'id': i,
            'links': [],
            'weight': 1,
            'text': p
        })
        i += 1
    for s in solutions:
        data['solutions'].append({
            'id': i,
            'links': [],
            'weight': 1,
            'text': s
        })
        i += 1
    for pc in data.get('problem_categories'):
        pc['links'] = find_problem_category_links(df, data, pc.get('text'))
    for p in data.get('problems'):
        p['links'] = find_problem_links(df, data, p.get('text'))
    return data


data = create_entries(df)

with open("./data.js", 'a') as file:
    file.truncate(0)
    file.write(f'const json_input =\n {data}\nexport default json_input;')
