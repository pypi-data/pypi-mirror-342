#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GraphQL Schema to HttpRunner 测试用例转换工具

该模块是GraphQL Schema到HttpRunner测试用例转换工具的主入口。
处理命令行参数，读取GraphQL Schema文件，协调调用解析器和生成器模块。

主要功能：
1. 解析命令行参数，提供友好的命令行界面
2. 读取GraphQL Schema文件或通过内省查询获取Schema
3. 协调调用SchemaParser解析Schema
4. 协调调用TestCaseGenerator生成测试用例
5. 协调调用QueryGenerator生成查询语句列表
6. 支持通过配置文件批量生成多个项目的测试用例
"""

import argparse
import sys
import os
import csv
import time
import datetime
import yaml

from . import __version__
from .parser import GraphQLSchemaParser
from .generator import HttpRunnerTestCaseGenerator
from .query_generator import GraphQLQueryGenerator
from .introspection import fetch_schema_from_introspection, IntrospectionQueryError
from .utils import backup_queries_file, compare_query_files


def process_single_project(introspection_url=None, schema_file=None, output=None, base_url="http://localhost:8888", 
                         max_depth=2, is_api=False, required=False, is_testcases=True, project_name=None):
    """处理单个项目"""
    schema = None
    
    # 设置默认输出路径
    if output is None:
        if is_testcases:
            if is_api:
                output = 'api'
            else:
                output = 'testcases'
        else:
            # project_name有值时，为批处理模式，否则为单项目模式
            if project_name:
                output = 'query.yaml'
            else:
                output = 'query.yml'
    
    # 从Schema文件中读取
    if schema_file:
        # 检查Schema文件是否存在
        if not os.path.isfile(schema_file):
            print(f"错误：Schema文件 '{schema_file}' 不存在")
            return False
        
        # 读取Schema文件
        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_content = f.read()
        except Exception as e:
            print(f"读取Schema文件时出错: {e}")
            return False
        
        # 解析Schema
        print(f"开始解析GraphQL Schema文件: {schema_file}")
        try:
            parser = GraphQLSchemaParser(schema_content)
            schema = parser.parse()
        except Exception as e:
            print(f"解析Schema文件时出错: {e}")
            return False
    
    # 通过内省查询获取Schema
    elif introspection_url:
        try:
            schema = fetch_schema_from_introspection(introspection_url)
        except IntrospectionQueryError as e:
            print(f"内省查询失败: {e}")
            return False
        except Exception as e:
            print(f"获取Schema时出错: {e}")
            return False
    
    # 生成测试用例
    if is_testcases:
        output_type = "API层" if is_api else "用例层"
        print(f"\n开始生成HttpRunner {output_type}测试用例...")
        try:
            generator = HttpRunnerTestCaseGenerator(schema, base_url, max_depth, required)

            if is_api:
                testcase_count = generator.generate_api_test_cases(output)
                print(f"\n已生成{testcase_count}个API层测试用例到目录: {output}")
            else:
                testcase_count = generator.generate_test_cases(output)
                print(f"\n已生成{testcase_count}个用例层测试用例到目录: {output}")

        except Exception as e:
            print(f"生成测试用例时出错: {e}")
            return False
    
    # 生成查询语句列表
    else:
        print(f"\n开始生成GraphQL查询语句列表...")
        try:
            generator = GraphQLQueryGenerator(schema, max_depth)
            queries = generator.generate_queries(output, base_url)
            query_count = len(queries)
            print(f"\n已生成{query_count}个查询语句到文件: {output}")
        except Exception as e:
            print(f"生成查询语句时出错: {e}")
            return False
    
    print(f"使用的最大查询深度: {max_depth}")
    print(f"使用的基础URL或产品名: {base_url}")
    if is_testcases:
        print(f"是否只包含必选参数：{'是' if required else '否'}")
    
    return True


def batch_generate(config_file, is_testcases=True):
    """批量生成HttpRunner测试用例"""
    
    if not os.path.exists(config_file):
        print(f"错误：配置文件 '{config_file}' 不存在")
        sys.exit(1)
    
    print(f"开始批量生成测试用例，配置文件：{config_file}")
    
    # 读取配置文件
    projects = []
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                projects.append(row)
    except Exception as e:
        print(f"读取配置文件时出错: {e}")
        sys.exit(1)
    
    if not projects:
        print("配置文件中没有发现项目")
        sys.exit(1)
    
    # 设置批模式生成Graphql查询语句时统一聚合在query.yaml
    queries_output = "query.yaml"
    backup_file = None
    
    if not is_testcases and os.path.exists(queries_output):
        # 备份旧的查询语句文件
        backup_file = backup_queries_file(queries_output)
    
    # 批量处理每个项目
    success_count = 0
    failed_count = 0
    for project in projects:
        project_name = project["project_name"]
        introspection_url = project["introspection_url"]
        output = project["output"] if is_testcases else queries_output
        base_url = project["base_url"]
        max_depth = int(project.get("max_depth", 2))
        required = project.get("required", "false").lower() == "true"
        is_api = project.get("api", "false").lower() == "true"
        
        print(f"\n{'='*80}")
        print(f"开始处理项目: {project_name}")
        print(f"内省查询URL: {introspection_url}")
        print(f"基础URL或产品名: {base_url}")
        print(f"最大深度: {max_depth}")
        if is_testcases:
            print(f"生成测试用例类型: {'API层' if is_api else '用例层'}")
            print(f"是否只包含必选参数: {'是' if required else '否'}")
            print(f"输出目录: {output}")
        else:
            print(f"输出文件: {output}")
        
        # 处理单个项目
        start_time = time.time()
        result = process_single_project(
            introspection_url=introspection_url,
            output=output,
            base_url=base_url,
            max_depth=max_depth,
            is_api=is_api,
            required=required,
            is_testcases=is_testcases,
            project_name=project_name
        )
        
        if result:
            success_count += 1
            end_time = time.time()
            print(f"生成完成，耗时: {end_time - start_time:.2f}秒")
        else:
            failed_count += 1
            print(f"生成失败，请稍后重新生成！")
        
    # 输出总结
    print(f"\n{'='*80}")
    print(f"批量生成任务完成")
    print(f"成功处理项目数: {success_count}")
    print(f"失败处理项目数: {failed_count}")
    print(f"总项目数: {len(projects)}")
    # 如果是生成查询语句列表且有备份文件，则生成差异比较报告
    if not is_testcases and backup_file and os.path.exists(queries_output):
        print(f"\n{'='*80}")
        result = compare_query_files(backup_file, queries_output)
        if not result:
            sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='将GraphQL Schema转换为HttpRunner测试用例或查询语句')
    
    # 添加版本信息选项
    parser.add_argument('-V', '--version', action='store_true', help='显示版本信息')
    
    # 添加批处理配置文件选项
    parser.add_argument('-b', '--batch', help='批量处理配置文件路径，如 config.csv')
    
    # 创建互斥组，schema文件和内省查询URL只能二选一
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument('-f', '--schema-file', help='GraphQL Schema文件路径')
    source_group.add_argument('-i', '--introspection-url', help='GraphQL内省查询URL，如http://localhost:9527/graphql')
    
    # 创建互斥组，生成测试用例或查询语句列表
    output_type_group = parser.add_mutually_exclusive_group()
    output_type_group.add_argument('-t', '--testcases', action='store_true', help='生成HttpRunner测试用例')
    output_type_group.add_argument('-q', '--queries', action='store_true', help='生成GraphQL查询语句列表')
    
    parser.add_argument('-o', '--output', default=None, help='输出目录或文件路径，默认根据生成类型自动生成api、testcases、query.yml文件') # 批模式生成Graphql查询语句聚合在query.yaml
    parser.add_argument('-u', '--base-url', default='http://localhost:8888', help='基础URL或产品名，生成用例时作为API基础URL，生成查询语句时作为分组标识')
    parser.add_argument('-d', '--max-depth', type=int, default=2, help='GraphQL查询嵌套的最大深度，默认为2')
    parser.add_argument('--api', action='store_true', help='生成API层测试用例而非用例层测试用例')
    parser.add_argument('--required', action='store_true', help='只包含必选参数，默认情况下包含所有参数')
    
    args = parser.parse_args()
    
    # 如果指定了版本信息选项，显示版本信息后退出
    if args.version:
        print(f"{__version__}")
        return
    
    # 如果指定了批处理配置文件，进入批处理模式
    if args.batch:
        is_testcases = not args.queries  # 默认生成测试用例，除非指定了 -q 选项
        batch_generate(args.batch, is_testcases)
        return
    
    # 检查常规模式下必需的参数
    if not args.schema_file and not args.introspection_url:
        parser.error("必须指定 -f/--schema-file 或 -i/--introspection-url 选项，或者使用 -b/--batch 批处理配置文件")
        
    if not args.testcases and not args.queries:
        parser.error("必须指定 -t/--testcases 或 -q/--queries 选项")
    
    output = args.output
    backup_file = None
    
    # 单项目模式下，如果生成查询语句并且输出文件已存在，则备份旧文件
    if args.queries and os.path.exists(output or 'query.yml'):
        backup_file = backup_queries_file(output or 'query.yml')
    
    # 处理单个项目
    result = process_single_project(
        introspection_url=args.introspection_url,
        schema_file=args.schema_file,
        output=output,
        base_url=args.base_url,
        max_depth=args.max_depth,
        is_api=args.api,
        required=args.required,
        is_testcases=args.testcases
    )
    
    # 如果是生成查询语句列表且有备份文件，则生成差异比较报告
    if result and args.queries and os.path.exists(output or 'query.yml') and backup_file:
        result = compare_query_files(backup_file, output or 'query.yml')
        if not result:
            sys.exit(1)


if __name__ == '__main__':
    main() 