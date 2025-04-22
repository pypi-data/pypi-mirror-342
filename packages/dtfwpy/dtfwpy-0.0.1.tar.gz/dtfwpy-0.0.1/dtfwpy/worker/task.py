from celery.schedules import crontab
from datetime import timedelta


class Task:
    _tasks: list[str] = []
    _tasks_routes: dict = {}
    _periodic_tasks: dict = {}

    def _register_task_route(self, route: str):
        self._tasks.append(route)
        return self

    def register(self, route: str, queue: str | None = None):
        self._register_task_route(route=route)
        task_dict = {}
        if queue:
            task_dict['queue'] = queue

        self._tasks_routes[route] = task_dict
        return self

    def register_periodic_task(self, route: str, schedule: crontab | timedelta, queue: str | None = None, *args):
        self.register(route=route, queue=queue)
        self._periodic_tasks[route] = {
            'task': route,
            'schedule': schedule,
            'args': args,
        }
        return self

    def get_tasks(self) -> list[str]:
        return self._tasks

    def get_tasks_routes(self) -> dict:
        return self._tasks_routes

    def get_periodic_tasks(self) -> dict:
        return self._periodic_tasks
