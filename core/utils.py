import pandas as pd


class ExcelDataImporter():
    def __init__(self):
        self.df = pd.read_excel('core/mindmap-v3.xlsx', sheet_name='solutions')
        
    def run(self):
        self.data = self.create_entries()

    def write_to_json(self):
        print(self.data)
        with open("./data.js", 'a') as file:
            file.truncate(0)
            file.write(f'const json_input =\n {self.data}\nexport default json_input;')

    def find_category(self, i, row):
        if pd.isna(row['Problem']) or pd.isnull(row['Ideas']):
            for i in range(i,0,-1):
                if not pd.isna(self.df.iloc[i]['Problem']):
                    return self.df.iloc[i]['Problem']
        else:
            return row['Problem']
    
    def find_problem(self, i):
        row =self.df.iloc[i]
        if pd.isna(row['Ideas']) or pd.isnull(row['Ideas']):
            for i in range(i,0,-1):
                if not pd.isna(self.df.iloc[i]['Ideas']):
                    return self.df.iloc[i]['Ideas']
        else:
            return row['Ideas']
    
    def find_problems_for_category(self, category_name):
        problems = []
        for i, row in self.df.iterrows():
            if row['Problem']==category_name:
                if self.find_problem(i) not in problems:
                    problems.append(self.find_problem(i))
        return problems
    
    def find_solutions_for_problem(self, problem):
        solutions = []
        for i, row in self.df.iterrows():
            if self.find_problem(i) == problem:
                if not pd.isna(row['Entity(s)']):
                    if row['Entity(s)'] not in solutions:
                        solutions.append(row['Entity(s)'])
        return solutions
    
    def find_problem_category_links(self, entries, problem_category):
        links = []
        problems = self.find_problems_for_category(problem_category)
        for p in entries['problems']:
            if p.get('text') in problems:
                links.append(p.get('id'))
        return links
    
    def find_problem_links(self, entries, problem):
        links = []
        solutions = self.find_solutions_for_problem(problem)
        for s in entries.get('solutions'):
            if s.get('text') in solutions:
                links.append(s.get('id'))
        return links

    def create_entries(self):
        problem_categories = []
        problems = []
        solutions = []
        for pc in self.df['Problem'].unique():
            if not pd.isna(pc) and not pd.isnull(pc):
                problem_categories.append(pc)
    
        for i, row in self.df.iterrows():
            if not pd.isna(row['Ideas']) and not pd.isnull(row['Ideas']):
                if row['Ideas'] not in problems:
                    problems.append(row['Ideas'])
            else:
                if self.find_problem(i) not in problems:
                    problems.append(self.find_problem(i))
        for i, row in self.df.iterrows():
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
            pc['links'] = self.find_problem_category_links(data, pc.get('text'))
        for p in data.get('problems'):
            p['links'] = self.find_problem_links(data, p.get('text'))
        return data



