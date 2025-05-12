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

def _construct_format(this):
    escaped = re.escape(this)
    return rf'"{escaped}"\s*:\s*"([^"]*)"'

def _find_all_blocks(type:Literal["report","code","other"], text:str, ext_mark:str="") -> List[dict]:
    """
    find block with certain patterns in json form.
    Args:
        type: find block in code or in report file, if choose "other", it will use external pattern
        text: the text that needs to search through
        other_pattern: use other patterns
    """
    blocks:List[dict] = []
    if type == "other":
        """
        return with [block,...] form
        """
        pattern = r"```(?:report|[a-z]*)?\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        if not matches:
            pattern = r"```(?:json|[a-z]*)?\n(.*?)```"
            matches = re.findall(pattern, text, re.DOTALL)

        blocks:List[str] = []
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            for code in matches:
                try:
                    m_report = re.search(_construct_format("Report"), code)
                    report_val = m_report.group(1) if m_report else None

                    m_valid = re.search(_construct_format("Valid"), code)
                    valid_val = m_valid.group(1) if m_valid else ""

                    normalized_report_block = report_val.replace("\\n", "\n")
                    blocks.append({ext_mark:{"Report":normalized_report_block,"Valid":valid_val}})

                except ValueError:
                    blocks.append({ext_mark:None})

    elif type == "code":
        """
        return with [{"hash":"code content",...] form
        """

        pattern = r"```(?:prolog|[a-z]*)?\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        if not matches:
            pattern = r"```(?:json|[a-z]*)?\n(.*?)```"
            matches = re.findall(pattern, text, re.DOTALL)

        if matches:
            for code in matches:
            #     try:
            #         block = json.loads(code)
            #         block["Code"] = "% === % LLM Generated Logic Codes % === %\n"+block["Code"]+"\n% === % ========================= % === %"
            #         blocks.append({block["HASH"]:block["Code"]})
            #     except ValueError:
            #         print(f"_find_all_blocks: could not parse the code block of {block}")
            #         blocks.append({block["HASH"]:None})
                try:
                    m_hash = re.search(_construct_format("HASH"), code)
                    # m_hash = re.search(r'"HASH"\s*:\s*"([^"]*)"', code)
                    hash_val = m_hash.group(1) if m_hash else None

                    m_code = re.search(_construct_format("Code"), code)
                    # m_code = re.search(r'"Code"\s*:\s*"([\s\S]*?)"', code)
                    code_block = m_code.group(1) if m_code else ""
                    normalized_code_block = code_block.replace("\\n", "\n")
                    blocks.append({hash_val:normalized_code_block})

                except ValueError as e:
                    print(e)
        else:
            raise ValueError("_find_all_blocks: no match found!")
    elif type == "report":
        """
        return with [{"hash":{"HASH":"hash","Report":"report content","Need_regenerate":"True"}},...] form
        """
        pattern = r"```report\s+(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            for report in matches:
                try:
                    block = json.loads(report)
                    blocks.append({block["HASH"]:block})
                except ValueError:
                    blocks.append({block["HASH"]:None})

    else:
        raise ValueError("you must choose from ['report','code','other']")
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
