from models import PriorityEnum


def get_priority_order():
    return {
        PriorityEnum.urgent: 1,
        PriorityEnum.high: 2,
        PriorityEnum.medium: 3,
        PriorityEnum.low: 4
    }


def search_in_tasks(tasks, query):
    query_lower = query.lower()
    return [
        task for task in tasks
        if query_lower in task.title.lower() or query_lower in task.description.lower()
    ]
