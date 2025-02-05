from api.admin_teachers import router_teachers as router_admin_teachers
from api.admin_subjects import router as router_admin_subjects
from api.admin_groups import router as router_admin_groups
from api.admin_students import router_admin_students
from api.students import router as router_students
from api.teachers import router as router_teachers
from api.files import router as router_files


all_routers = [
    router_admin_subjects,
    router_admin_groups,
    router_admin_students,
    router_admin_teachers,
    router_students,
    router_teachers,
    router_files,
]
