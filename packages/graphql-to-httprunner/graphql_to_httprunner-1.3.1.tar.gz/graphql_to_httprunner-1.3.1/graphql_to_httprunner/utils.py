#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GraphQL Schema to HttpRunner 工具类模块

此模块提供工具函数，主要包括：
1. 查询语句文件备份功能
2. 查询语句文件差异对比与报告生成功能

这些功能主要用于在生成新的GraphQL查询语句时，保留旧版本并生成详细的差异比较报告，
便于用户了解API变更情况，实现API变更的可视化跟踪。
"""

import os
import sys
import shutil
import datetime
import difflib
import yaml


def backup_queries_file(file_path):
    """
    备份查询语句文件
    
    将现有的查询语句文件备份为带时间戳的文件，并删除原文件
    
    Args:
        file_path (str): 需要备份的文件路径
        
    Returns:
        str or None: 备份文件的路径，失败时返回None
    """
    if not os.path.exists(file_path):
        return None
    
    # 分离文件名和扩展名
    file_name, file_ext = os.path.splitext(file_path)
    backup_path = f"{file_name}.bak.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{file_ext}"
    
    try:
        shutil.copy2(file_path, backup_path)
        print(f"备份旧的查询语句文件: {file_path} -> {backup_path}")
        os.remove(file_path)
        print(f"删除旧的查询语句文件: {file_path}")
        return backup_path
    except Exception as e:
        print(f"备份旧查询语句文件时出错: {e}")
        return None


def compare_query_files(old_file, new_file):
    """
    比较新旧查询语句文件的差异并保存差异结果
    
    分析新旧查询语句文件的差异，生成详细的Markdown格式差异报告，
    包括项目级变更、查询级变更以及详细的文本差异
    
    Args:
        old_file (str): 旧查询语句文件路径
        new_file (str): 新查询语句文件路径
        
    Returns:
        bool: 如果存在差异，返回True，否则返回False
    """
    if not os.path.exists(old_file) or not os.path.exists(new_file):
        print(f"无法进行文件对比，旧文件或新文件不存在")
        return False
    
    # 读取旧文件内容
    try:
        with open(old_file, 'r', encoding='utf-8') as f:
            old_content = yaml.safe_load(f)
    except Exception as e:
        print(f"读取旧文件内容时出错: {e}")
        return False
    
    # 读取新文件内容
    try:
        with open(new_file, 'r', encoding='utf-8') as f:
            new_content = yaml.safe_load(f)
    except Exception as e:
        print(f"读取新文件内容时出错: {e}")
        return False
    
    # 分析差异
    diff_result = {
        "added_projects": [],
        "removed_projects": [],
        "modified_projects": {},
        "added_queries": {},
        "removed_queries": {},
        "modified_queries": {},
    }
    
    # 检查项目级差异
    old_projects = set(old_content.keys())
    new_projects = set(new_content.keys())
    
    diff_result["added_projects"] = list(new_projects - old_projects)
    diff_result["removed_projects"] = list(old_projects - new_projects)
    
    # 对于共同存在的项目，检查查询语句差异
    common_projects = old_projects.intersection(new_projects)
    for project in common_projects:
        old_queries = set(old_content[project].keys())
        new_queries = set(new_content[project].keys())
        
        # 检查是否有查询语句差异
        added_queries = new_queries - old_queries
        if added_queries:
            diff_result["added_queries"][project] = list(added_queries)
        
        removed_queries = old_queries - new_queries
        if removed_queries:
            diff_result["removed_queries"][project] = list(removed_queries)
        
        # 检查共同查询语句的内容差异
        common_queries = old_queries.intersection(new_queries)
        modified_queries = []
        
        for query in common_queries:
            if old_content[project][query] != new_content[project][query]:
                modified_queries.append(query)
        
        if modified_queries:
            diff_result["modified_queries"][project] = modified_queries
        
        # 如果项目有任何变化，记录到modified_projects
        if (project in diff_result["added_queries"] or 
            project in diff_result["removed_queries"] or 
            project in diff_result["modified_queries"]):
            diff_result["modified_projects"][project] = {
                "added_queries": diff_result["added_queries"].get(project, []),
                "removed_queries": diff_result["removed_queries"].get(project, []),
                "modified_queries": diff_result["modified_queries"].get(project, [])
            }
    
    # 生成详细的文本差异
    diff_lines = []
    diff_lines.append("# GraphQL查询语句差异报告")
    diff_lines.append(f"# 旧文件: {old_file}")
    diff_lines.append(f"# 新文件: {new_file}")
    diff_lines.append("")
    
    # 添加项目级差异信息
    if diff_result["added_projects"]:
        diff_lines.append("## 新增项目")
        for project in diff_result["added_projects"]:
            diff_lines.append(f"- {project}")
        diff_lines.append("")
    
    if diff_result["removed_projects"]:
        diff_lines.append("## 移除项目")
        for project in diff_result["removed_projects"]:
            diff_lines.append(f"- {project}")
        diff_lines.append("")
    
    # 添加查询语句差异信息
    if diff_result["modified_projects"]:
        diff_lines.append("## 修改项目")
        for project, changes in diff_result["modified_projects"].items():
            diff_lines.append(f"### {project}")
            
            if changes["added_queries"]:
                diff_lines.append("#### 新增查询")
                for query in changes["added_queries"]:
                    diff_lines.append(f"- {query}")
                    diff_lines.append(f"  ```")
                    diff_lines.append(f"  {new_content[project][query]}")
                    diff_lines.append(f"  ```")
            
            if changes["removed_queries"]:
                diff_lines.append("#### 移除查询")
                for query in changes["removed_queries"]:
                    diff_lines.append(f"- {query}")
                    diff_lines.append(f"  ```")
                    diff_lines.append(f"  {old_content[project][query]}")
                    diff_lines.append(f"  ```")
            
            if changes["modified_queries"]:
                diff_lines.append("#### 修改查询")
                for query in changes["modified_queries"]:
                    diff_lines.append(f"- {query}")
                    diff_lines.append(f"  旧:")
                    diff_lines.append(f"  ```")
                    diff_lines.append(f"  {old_content[project][query]}")
                    diff_lines.append(f"  ```")
                    diff_lines.append(f"  新:")
                    diff_lines.append(f"  ```")
                    diff_lines.append(f"  {new_content[project][query]}")
                    diff_lines.append(f"  ```")
                    
                    # 生成详细的文本差异
                    old_lines = old_content[project][query].splitlines()
                    new_lines = new_content[project][query].splitlines()
                    differ = difflib.Differ()
                    diff = list(differ.compare(old_lines, new_lines))
                    if len(diff) > 1:  # 如果有多于一行的差异
                        diff_lines.append(f"  差异详情:")
                        diff_lines.append(f"  ```diff")
                        for line in diff:
                            diff_lines.append(f"  {line}")
                        diff_lines.append(f"  ```")
            
            diff_lines.append("")
    
    # 判断是否存在差异
    has_difference = (diff_result["added_projects"] or 
                     diff_result["removed_projects"] or 
                     diff_result["modified_projects"])
    
    if has_difference:
        # 保存差异结果
        diff_file = f"{new_file}.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.diff.md"
        try:
            with open(diff_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(diff_lines))
            print(f"生成查询语句差异报告: {diff_file}")
        except Exception as e:
            print(f"保存差异报告时出错: {e}")
            return False
        # 输出汇总信息
        print(f"\n新旧查询语句文件差异比较结果:")
        if diff_result["added_projects"]:
            print(f"- 新增项目: {len(diff_result['added_projects'])}")
        if diff_result["removed_projects"]:
            print(f"- 移除项目: {len(diff_result['removed_projects'])}")
        
        modified_count = len(diff_result["modified_projects"])
        if modified_count:
            print(f"- 修改项目: {modified_count}")
            
            added_queries_count = sum(len(queries) for queries in diff_result["added_queries"].values())
            if added_queries_count:
                print(f"  - 新增查询: {added_queries_count}")
            
            removed_queries_count = sum(len(queries) for queries in diff_result["removed_queries"].values())
            if removed_queries_count:
                print(f"  - 移除查询: {removed_queries_count}")
            
            modified_queries_count = sum(len(queries) for queries in diff_result["modified_queries"].values())
            if modified_queries_count:
                print(f"  - 修改查询: {modified_queries_count}")
        
        print("详细差异报告已生成成功！")
        return True
    else:
        print(f"\n查询语句文件比较结果: 没有发现差异！")
        return False