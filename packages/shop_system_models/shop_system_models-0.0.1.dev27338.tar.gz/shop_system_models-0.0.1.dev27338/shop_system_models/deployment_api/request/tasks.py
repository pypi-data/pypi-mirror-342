from typing import List

from shop_system_models.consts.enums import TaskStatuses
from pydantic import BaseModel


class Task(BaseModel):
    title: str
    assignee_role: List = []
    shop_id: str
    shop_name: str
    submit_url: str = ''
    variables: dict
    element_id: str
    form_json: dict
    job_key: int
    process_id: str
    process_instance_key: int
    process_monitoring_url: str
    deadline: int
    status: TaskStatuses = TaskStatuses.pending

    class Config:
        use_enum_values = True
