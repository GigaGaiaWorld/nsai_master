import re
import json
import uuid
import hashlib
from problog.program import PrologString, Clause, AnnotatedDisjunction, Term
from typing import Literal, List, Union, Tuple, Dict, Any
from langgraph.graph import END, StateGraph
from state import BasicState, Mode
from config import paths

def _langda_list_to_dict(langda_dicts):
    """
    Just turn [{},{},...] to {"hash1":{},"hash2":{},...}
    """
    langda_hash_index = {}
    for langda_item in langda_dicts:
        if "HASH" in langda_item:
            langda_hash_index[langda_item["HASH"]] = langda_item
    return langda_hash_index

def _expand_nested_list(lists, max_depth=10, current_depth=0):
    """
    Expand nested list to a flat list.
    Includes depth detection to prevent infinite recursion.
    """
    if current_depth > max_depth:
        raise RecursionError(f"Maximum recursion depth {max_depth} exceeded!")

    flat_list = []
    for item in lists:
        if isinstance(item, list):
            nested_items = _expand_nested_list(item, max_depth, current_depth + 1)
            flat_list.extend(nested_items)
        else:
            flat_list.append(item)
    return flat_list


def _list_to_dict(listdict:List[dict]):
    dictdict:Dict[str,Any] = {}
    for dict in listdict:
        key, value = _parse_simple_dictonary(dict)
        dictdict[key] = value
    return dictdict

def _parse_simple_dictonary(code_item:dict) -> Tuple[str, Any]:
    """
    parse the dictonary only has one item, form like: {"hash":Any content here}
    """
    key, value = next(iter(code_item.items()))
    return key, value

def _compute_short_md5(len:int, content:Union[str,dict], upper:bool = False) -> str:
    """
    Computes a short MD5 hash of the given content with specified length.
    Converts to uppercase if upper=True.
    """
    if isinstance(content, dict):
        hash_str = hashlib.md5(json.dumps(content).encode('utf-8')).hexdigest()[:len]
    elif isinstance(content, str):
        hash_str = hashlib.md5(content.encode('utf-8')).hexdigest()[:len]
    else:
        raise TypeError("_compute_short_md5: the input should be string or dictonary")
    return hash_str.upper() if upper else hash_str


def _compute_random_md5(len:int, upper:bool = False) -> str:
    """
    Generates a random MD5-style hash string by taking a UUID and slicing the hex.
    Converts to uppercase if upper=True.
    """
    hash_str = uuid.uuid4().hex[:len].upper()
    return hash_str.upper() if upper else hash_str


def _ordinal(n:int) -> str:
    """
    Simple function to convert an int number to an ordinal
    args:
        n: input number
    """
    # from int number generate ordinal: 1st,2nd,3rd,4th,5th,...
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix

def _draw_mermaid_png(graph:StateGraph, graph_str:str):
    """
    well, it will not give you the mermaid_png because of the restrict of api,
    But it will generate a mmd file, you can generate png yourself from https://mermaid.live/edit
    args:
        graph: current StateGraph
        graph_str: name of the graph, only used for creating filename
    """
    graph_mermaid = graph.get_graph().draw_mermaid()
    paths.save_as_file(graph_mermaid,"mermaid", graph_str)

def _replace_placeholder(template:str, replacement_list:Union[List[str],List[dict]], placeholder="{{LANGDA}}") -> str:
    """
    args:
        template: template with placeholders
        replacement_list: the list of content that will fit into the placeholder.
        placeholder: default as {{LANGDA}}
        - if the value is None, the corresponding placeholder remains unchanged. 
        - valid input forms: List[str] or List[dict]
    """
    replace_str_list = []
    if all(isinstance(item, dict) for item in replacement_list):
        for item in replacement_list:
            # value = item["Code"]
            _, value = next(iter(item.items()))
            replace_str_list.append(value)
    else:
        replace_str_list = replacement_list

    segments = template.split(placeholder)
    # segments[0] + (N times [replacement or placeholder] + segments[1..])
    result = segments[0]
    # Traversal:
    for i, seg in enumerate(segments[1:]):
        if i < len(replace_str_list) and replace_str_list[i] is not None:
            result += replace_str_list[i]
        else:
            result += placeholder
        result += seg
    return result


def _find_all_blocks(type: Literal["report", "code", "other"], text: str, ext_mark: str = "") -> List[dict]:
    """
    修复版的解析函数，正确处理ProbLog代码中的转义序列
    """
    blocks: List[dict] = []
    
    # 根据类型选择正则表达式
    if type == "other" or type == "report":
        pattern = r"```(?:report|[a-z]*)?\n(.*?)```"
    elif type == "code":
        pattern = r"```(?:problog|[a-z]*)?\n(.*?)```"
    else:
        raise ValueError("you must choose from ['report','code','other']")
    
    matches = re.findall(pattern, text, re.DOTALL)
    
    if not matches:
        pattern = r"```(?:json|[a-z]*)?\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
    
    for match in matches:
        match = match.strip()
        
        try:
            # 直接尝试解析JSON
            match_json = json.loads(match)
        except json.JSONDecodeError:
            # 智能处理转义序列
            try:
                # 创建一个映射来临时替换特殊序列
                replacements = {
                    r'\\\\=': '___DOUBLE_BACKSLASH_EQUALS___',
                    r'\\=': '___BACKSLASH_EQUALS___',
                    r'\\n': '___BACKSLASH_N___',
                    '\n': '\\n',  # 将实际的换行符替换为转义的换行符
                }
                
                processed_match = match
                
                # 首先处理实际的换行符
                processed_match = processed_match.replace('\n', '\\n')
                
                # 然后处理其他特殊序列（按长度降序，确保先处理长的）
                for pattern, replacement in sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True):
                    if pattern != '\n':  # 跳过已处理的换行符
                        processed_match = processed_match.replace(pattern, replacement)
                
                # 尝试解析JSON
                match_json = json.loads(processed_match)
                
                # 还原特殊序列
                if isinstance(match_json, dict) and "Code" in match_json:
                    code = match_json["Code"]
                    # 还原顺序也很重要
                    for pattern, replacement in replacements.items():
                        if pattern != '\n':  # 不需要还原换行符
                            code = code.replace(replacement, pattern)
                    match_json["Code"] = code
                
            except json.JSONDecodeError as e:
                print(f"JSON解析失败: {e}")
                print(f"原始内容: {repr(match)}")
                print(f"处理后内容: {repr(processed_match)}")
                continue
        
        # 根据类型处理解析结果
        if type == "other":
            blocks.append({ext_mark: match_json})
        elif type == "code":
            if isinstance(match_json, dict) and "HASH" in match_json and "Code" in match_json:
                blocks.append({match_json["HASH"]: match_json["Code"]})
            else:
                blocks.append({"unknown": f"code: invalid structure - {match_json}"})
        elif type == "report":
            if isinstance(match_json, dict) and "HASH" in match_json:
                blocks.append({match_json["HASH"]: match_json})
            else:
                blocks.append({"unknown": f"report: invalid structure - {match_json}"})
    
    return blocks

def _print_stream(stream):
    for s in stream:
        messages = s["messages"][-1]
        print(f"Stream item type: {type(s)}")
        print(f"Stream item content: {s}")
        if "tool_calls" in s:
            print(f"Tool calls: {s['tool_calls']}")
        if "tool_results" in s:
            print(f"Tool results: {s['tool_results']}")
        
        if isinstance(messages, tuple):
            print(f"Tuple message: {messages}")
        else:
            try:
                print(f"Message content: {messages.content}")
                messages.pretty_print()
            except AttributeError:
                print(f"Cannot pretty print: {messages}")

def _select_mode(state:BasicState, langda_dict):
    keys = set(langda_dict.keys())
    if not "NET" in keys and not "LLM" in keys:
        if len(keys) >= 1:
            state["mode"] = Mode.PURE_PAR
        else:
            raise KeyError("forget to set langda parameter?")

    elif not "NET" in keys and "LLM" in keys:
        if len(keys) > 1:
            state["mode"] = Mode.PARA_LLM
        else:
            state["mode"] = Mode.PURE_LLM

    elif "NET" in keys and not "LLM" in keys:
        if len(keys) > 1:
            state["mode"] = Mode.FULL_LLM  
        else:
            state["mode"] = Mode.PURE_NET

    else:
        if len(keys) > 2:
            state["mode"] = Mode.FULL_LLM  
        else:
            state["mode"] = Mode.ELSE
