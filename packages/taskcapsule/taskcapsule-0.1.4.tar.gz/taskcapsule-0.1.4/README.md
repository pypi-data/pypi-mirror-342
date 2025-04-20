# taskcapsule

A simple framework for running commands in parallel using templated commands and dictionaries of
arguments.

## Example

```python
from taskcapsule import TaskRunner, Task
# Look to see if the host is running WebLogic T3
template = "nmap -oG - -p {port} --script weblogic-t3-info {addr}"
items = [{"addr":"1.2.3.4","port": "7002"}]
my_tasks = []
for i in items:
    kwargs = items
    my_tasks.append(
        Task(
            command=template,
            kwargs=kwargs,
            target_metadata={"uuid": "fedcba09-1234-1111-bcde-1234567890fe"},
            # This is in the output if, and only if, T3 is running
            output_filter="T3",
        )
    )

tr = TaskRunner(tasks=my_tasks)
tr.run()
```

### Output

`python example.py|jq`

```log
INFO:taskcapsule:spawning 1 workers
{
  "command": "nmap -oG - -p 7002 --script weblogic-t3-info 1.2.3.4",
  "kwargs": {
    "addr": "1.2.3.4",
    "port": "7002"
  },
  "return_code": 0,
  "stdout": "# Nmap 7.95 scan initiated Thu Apr 17 09:23:50 2025 as: nmap -oG - -p 7002 --script weblogic-t3-info 1.2.3.4\nHost: 1.2.3.4 ()\tStatus: Up\nHost: 45.60.186.97 ()\tPorts: 7002/open/tcp//afs3-prserver//WebLogic application server 12.2.1.4 (T3 enabled)/\n# Nmap done at Thu Apr 17 09:23:51 2025 -- 1 IP address (1 host up) scanned in 0.70 seconds\n",
  "stderr": "",
  "duration": 0.7490861415863037,
  "success_filter": "T3",
  "target_metadata": {
    "uuid": "fedcba09-1234-1111-bcde-1234567890fe"
  }
}
INFO:task-runner:all tasks completed

```
