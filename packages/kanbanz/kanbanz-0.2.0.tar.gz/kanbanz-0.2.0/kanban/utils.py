
import json
import re

def read(text):
    pool_pattern = re.compile(r'## ([\s\S]+?)(?=\n## |\n\n\n|\n\*\*\*)')
    pools = pool_pattern.findall(text)
    # 提取任务列表
    task_pattern = re.compile(r'- \[([x ])\]([\s\S]+?)(?=\n|$)')

    kanban_dict = {}

    for pool in pools:
        # 分割池的名称和内容
        try:
            pool_name, pool_content = pool.split('\n', 1)
            pool_name = pool_name.strip()
        except ValueError:
            pool_name = pool
            pool_content = ""
        
        # 提取任务列表
        tasks = task_pattern.findall(pool_content)
        
        # 将任务整理为字典格式
        task_list = []
        for task in tasks:
            status = task[0].strip()
            status = status or " "
            description = task[1].strip()
            task_list.append({
                "status": status,
                "description": description
            })
        
        kanban_dict[pool_name] = task_list
    return kanban_dict

def write(kanban_dict):
    markdown = ""
    
    for pool_name, tasks in kanban_dict.items():
        # 添加池的标题
        if '完成' in pool_name:
            markdown += f"## {pool_name}\n\n**完成**\n"
        else:
            markdown += f"## {pool_name}\n\n"
        
        # 添加任务列表
        for task in tasks:
            status = task["status"]
            description = task["description"].strip()
            markdown += f"- [{status}] {description}\n"
        
        # 池之间添加空行
        markdown += "\n"
    head = """---

kanban-plugin: board

---
"""
    
    tail = """







%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[false,false,false,false,false,false],"link-date-to-daily-note":true,"tag-sort":[{"tag":""}],"move-tags":false,"lane-width":350,"tag-colors":[]}
```
%%
"""
    return head + markdown.strip() + tail

