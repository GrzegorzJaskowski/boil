class Task:
    def __init__(self, name, duration, dependencies=None):
        self.name = name
        self.duration = duration
        self.dependencies = dependencies or []
        self.earliest_start = 0
        self.earliest_finish = 0
        self.latest_start = float('inf')
        self.latest_finish = float('inf')

class CPM:
    def __init__(self, tasks):
        self.tasks = {task.name: task for task in tasks}

    def calculate_earliest_times(self):
        for task in self.tasks.values():
            if not task.dependencies:
                task.earliest_start = 0
            else:
                task.earliest_start = max(
                    self.tasks[dep].earliest_finish for dep in task.dependencies
                )
            task.earliest_finish = task.earliest_start + task.duration

    def calculate_latest_times(self, project_duration):
        for task in reversed(list(self.tasks.values())):
            if task.earliest_finish == project_duration:
                task.latest_finish = project_duration
            else:
                successors = self.get_successors(task.name)
                if successors:
                    task.latest_finish = min(
                        self.tasks[successor].latest_start for successor in successors
                    )
                else:
                    # No successors; use earliest finish as the latest finish
                    task.latest_finish = task.earliest_finish
            task.latest_start = task.latest_finish - task.duration

    def get_successors(self, task_name):
        return [t.name for t in self.tasks.values() if task_name in t.dependencies]

    def find_critical_path(self):
        critical_path = []
        for task in self.tasks.values():
            if task.earliest_start == task.latest_start:
                critical_path.append(task.name)
        return critical_path

    def run(self):
        self.calculate_earliest_times()
        project_duration = max(task.earliest_finish for task in self.tasks.values())
        self.calculate_latest_times(project_duration)
        critical_path = self.find_critical_path()

        return {
            'tasks': {
                task.name: {
                    'ES': task.earliest_start,
                    'EF': task.earliest_finish,
                    'LS': task.latest_start,
                    'LF': task.latest_finish,
                } for task in self.tasks.values()
            },
            'critical_path': critical_path,
            'project_duration': project_duration,
        }

if __name__ == "__main__":
    # print("Enter tasks (name, duration, dependencies) or type 'done' to finish input:")

    A = Task('A', 3)
    B = Task('B', 5)
    C = Task('C', 2, ['A'])
    D = Task('D', 4, ['B'])
    E = Task('E', 3, ['B'])
    F = Task('F', 2, ['C','D'])
    G = Task('G', 4, ['E'])
    H = Task('H', 3, ['F','G'])
    I = Task('I', 2, ['H'])
    tasks = [
        A, B, C, D, E, F, G, H, I
    ]

    # while True:
    #     user_input = input("Task (format: name duration dep1,dep2,...): ")
    #     if user_input.lower() == 'done':
    #         break

    #     parts = user_input.split()
    #     name = parts[0]
    #     duration = int(parts[1])
    #     dependencies = parts[2].split(',') if len(parts) > 2 else []
    #     tasks.append(Task(name, duration, dependencies))

    cpm = CPM(tasks)
    results = cpm.run()

    print("\nTask Details:")
    for task_name, times in results['tasks'].items():
        print(f"Task {task_name}: ES={times['ES']}, EF={times['EF']}, LS={times['LS']}, LF={times['LF']}")

    print("\nCritical Path:", " -> ".join(results['critical_path']))
    print("Project Duration:", results['project_duration'])