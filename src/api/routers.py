from api.students import router as router_students
from api.groups import router as router_groups
all_routers = [
    router_groups,
    router_students,
]
