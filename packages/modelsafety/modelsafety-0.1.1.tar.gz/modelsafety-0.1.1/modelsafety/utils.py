"""
ModelSafety SDK 工具函数
"""

import os
import json
import csv
from typing import Dict, List, Any, Optional, Tuple


def save_questions_to_json(questions: List[Dict], filename: str) -> str:
    """
    保存题目到JSON文件
    
    Args:
        questions: 题目列表
        filename: 文件名
        
    Returns:
        保存的文件路径
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    return os.path.abspath(filename)


def save_questions_to_csv(questions: List[Dict], filename: str) -> str:
    """
    保存题目到CSV文件
    
    Args:
        questions: 题目列表
        filename: 文件名
        
    Returns:
        保存的文件路径
    """
    # 确定所有可能的字段
    all_fields = set()
    for question in questions:
        all_fields.update(question.keys())
    
    # 整理字段顺序，常见字段放前面
    priority_fields = ["ID", "id", "题型", "问题", "prompt", "选项", "options", "答案", "answer"]
    fields = []
    
    # 先添加优先字段（如果存在）
    for field in priority_fields:
        if field in all_fields:
            fields.append(field)
            all_fields.remove(field)
    
    # 添加剩余字段
    fields.extend(sorted(all_fields))
    
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for question in questions:
            writer.writerow(question)
    
    return os.path.abspath(filename)


def save_report_to_file(report_content: bytes, filename: str) -> str:
    """
    保存报告到文件
    
    Args:
        report_content: 报告内容
        filename: 文件名
        
    Returns:
        保存的文件路径
    """
    with open(filename, "wb") as f:
        f.write(report_content)
    return os.path.abspath(filename)


def load_questions_from_json(filename: str) -> List[Dict]:
    """
    从JSON文件加载题目
    
    Args:
        filename: 文件名
        
    Returns:
        题目列表
    """
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def load_questions_from_csv(filename: str) -> List[Dict]:
    """
    从CSV文件加载题目
    
    Args:
        filename: 文件名
        
    Returns:
        题目列表
    """
    questions = []
    with open(filename, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            questions.append(dict(row))
    
    return questions


def format_model_responses(
    model_outputs: List[str], 
    questions: List[Dict],
    model_name: str = "default"
) -> List[Dict]:
    """
    格式化模型输出为API所需的响应格式
    
    Args:
        model_outputs: 模型输出文本列表
        questions: 原题目列表，用于获取question_id
        model_name: 模型名称
        
    Returns:
        格式化后的响应列表
    """
    responses = []
    for i, output in enumerate(model_outputs):
        if i >= len(questions):
            break
        
        question_id = questions[i].get("ID") or questions[i].get("id") or f"q{i+1}"
        responses.append({
            "question_id": question_id,
            "model": model_name,
            "response": output
        })
    
    return responses 