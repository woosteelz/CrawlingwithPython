from indeed import get_jobs as get_indeed_jobs
from stackoverflow import get_jobs as get_so_jobs
from jobkorea import get_jobs as get_jobkorea_jobs
from save import save_to_file

indeed_jobs = get_indeed_jobs()
so_jobs = get_so_jobs()
jobkorea_jobs = get_jobkorea_jobs()
jobkorea_jobs = list(filter(None, jobkorea_jobs))

jobs = indeed_jobs + so_jobs + jobkorea_jobs

save_to_file(jobs)

