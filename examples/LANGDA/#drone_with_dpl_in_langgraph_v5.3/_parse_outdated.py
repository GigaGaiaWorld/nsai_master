import re
from typing import List, Tuple

# ================================== PART ONE =================================== #
# ================================= PARSE LANGDA ================================= #
def find_langda_position_in_letter(text) -> List[tuple]:
    origin_text = text

    # Lists that contain contents:
    bracket_stack, langda_positions = [], []
    # Status Parameters:
    in_langda, in_quotes, is_escaped = False, False, False
    in_comment, in_multiline_comment = False, False
    langda_start = -1

    i = 0 # Iterate all single letter in text:
    try:
        while i < len(origin_text):
            # ----------------------- check comment ----------------------- #
            # Check if in the single line comment:
            if origin_text[i] == '%' and not in_quotes:
                in_comment = True
                i += 1
                continue
            # if break line, quit comment
            if origin_text[i] == '\n' and in_comment:
                in_comment = False
                i += 1
                continue
            
            # Check if in the mulitline comment:
            if origin_text[i] == '/*' and not in_quotes:
                in_multiline_comment = True
                i += 1
                continue
            # if break line, quit comment
            if origin_text[i] == '*/' and in_comment:
                in_multiline_comment = False
                i += 1
                continue
            

            # If IN THE COMMENT, SKIP:
            if in_comment or in_multiline_comment:
                i += 1
                continue

            # ----------------------- check langda ----------------------- #
            if origin_text[i:i+7] == 'langda(' and i+7 < len(origin_text):
                in_langda = True
                langda_start = i
                bracket_stack.append("depth")
                i += 7

            elif in_langda: # find new langda, if not in a langda predicate
                if origin_text[i] == '"' and not is_escaped: 
                    in_quotes = not in_quotes
                # This actually implements a simple state machine that keeps track of whether or not we are in the escape state:
                is_escaped = origin_text[i] == '\\' and not is_escaped

                if not in_quotes:
                    if origin_text[i] == '(':
                        bracket_stack.append("depth")
                    elif origin_text[i] == ')':
                        bracket_stack.pop()
                    if not bracket_stack:
                        langda_positions.append((langda_start, i+1))
                        in_langda = False
            
            i += 1
        
    except Exception as e:
        print(f"Error at find_langda_position_in_letter: {e}")
        
    # print(langda_positions)
    return langda_positions

def find_langda_position_in_line(text) -> List[tuple]:
    pass


def find_predicates_and_add_slot_in_line(text:str, slot:str="% {{NET}} {{LLM}}") -> List[tuple]:
    """
    find the predicate that contains langda, and add a line before the line that contains slot like: {{NET}}, {{LLM}}
    """
    lines = text.split('\n')
    current_predicate_start, current_predicate = None, False
    has_langda, langda_count = False, 0
    head_name = None

    predicate_position_list = []
    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()
        
        # skip comment and empty line
        if not line or line.startswith('%'):
            idx += 1
            continue
        
        # First, check the stand alone langda predicates
        pattern_single = r'langda\((.*?)\)\.'
        langda_match = re.match(pattern_single, line)
        if langda_match and not current_predicate:
            # 
            predicate_position_list.append(("none", [line], 1))  # head, lines, count
            lines.insert(idx, slot)
            idx += 2  # skip 2 line
            continue
        
        # Then, check complicated predicates
        predicate_start = re.match(r'([a-z][a-zA-Z0-9_]*)\((.*?)\)\s*:-', line)
        if predicate_start:  # first line of the predicate
            if current_predicate and has_langda and current_predicate_start is not None and head_name is not None:
                predicate_position_list.append((head_name, lines[current_predicate_start:idx], langda_count))
                lines.insert(current_predicate_start, slot)
                idx += 1
            
            current_predicate = True
            current_predicate_start = idx
            has_langda = False
            langda_count = 0  # 重置langda计数器
            head_name = predicate_start.group(1)
        
        # 
        if current_predicate:
            i = 0
            in_quotes = False
            is_escaped = False
            
            while i < len(line):
                # process "escaped" symbol
                if line[i] == '\\' and not is_escaped:
                    is_escaped = True
                    i += 1
                    continue
                # process "", in quote or out of quote
                if line[i] == '"' and not is_escaped:
                    in_quotes = not in_quotes
                elif not in_quotes and line[i:i+7] == "langda(" and (i == 0 or not line[i-1].isalnum()):
                    has_langda = True
                    langda_count += 1
                
                is_escaped = False
                i += 1

        # does the complicated predicate end
        if current_predicate and line.endswith('.'):
            if has_langda and head_name is not None:
                predicate_lines = lines[current_predicate_start:idx+1]  # +1 to include the current line
                predicate_position_list.append((head_name, predicate_lines, langda_count))
                lines.insert(current_predicate_start, slot)
                idx += 1
            
            # reset predicate analysis state
            current_predicate = False
            current_predicate_start = None
            has_langda = False
            langda_count = 0
            head_name = None
        
        idx += 1
    
    # process the last unprocessed predicate
    if current_predicate and has_langda and current_predicate_start is not None and head_name is not None:
        predicate_lines = lines[current_predicate_start:] 
        predicate_position_list.append((head_name, predicate_lines, langda_count))
        lines.insert(current_predicate_start, slot)
    
    return lines, predicate_position_list


def parse_langda_to_dicts(text:str, langda_positions:List[tuple]):
    result_text = text
    result_dict_list = []
    
    for (start, end) in langda_positions:
        # Extract langda content
        langda_predicates = result_text[start:end]
        pattern = r'langda\s*\(\s*([\s\S]*)\s*\)$'
        try:
            # ======================Part1: store terms in a list====================== #
            match = re.search(pattern, langda_predicates)
            if not match:
                print(f"No match found for pattern in: {langda_predicates}")
                result_dict_list.append({})
                continue

            langda_content = match.group(1)
            # Split into terms
            term_list = []
            term_start, i = 0, 0
            in_quotes, is_escaped = False, False

            while i < len(langda_content):
                # Handle quotes and escaping (with a state machine)
                if langda_content[i] == '"' and not is_escaped:
                    in_quotes = not in_quotes
                is_escaped = langda_content[i] == '\\' and not is_escaped
                
                # seperate into terms
                if not in_quotes and (langda_content[i] == ',' or i == len(langda_content) - 1): # consider the ")" case
                    end_idx = i if langda_content[i] == ',' else i + 1
                    term = langda_content[term_start:end_idx].strip()

                    term_list.append(term)
                    term_start = i + 1
                
                i += 1
            
            # ===================Part2: parse each term as key,value pair=================== #
            # parse each term into a dict element
            result_dict = {}
            for term in term_list:
                j, value_start = 0, 0
                has_value, in_quotes_term, is_escaped_term = False, False, False
                
                # find the key-value separator: ":"
                while j < len(term):
                    # if term[j] == '"' and not is_escaped_term:
                    #     in_quotes_term = not in_quotes_term
                    # is_escaped_term = term[j] == '\\' and not is_escaped_term
                    
                    if term[j] == ':' and not in_quotes_term:
                        value_start = j + 1
                        has_value = True
                        break
                    j += 1
                
                # extract key and value
                if has_value:
                    current_key = term[0:j].strip()
                    value = term[value_start:].strip()
                    
                    # remove quotes 
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    
                    result_dict[current_key] = value
                else:
                    # in case there's no value, just a key
                    current_key = term.strip()
                    result_dict[current_key] = "Unknown"
            # {'X': 'Return', 'T': 'None_value', 'LLM': "there's a high building at: (100,200)", 
            # 'NET': '[mnist_net1(0,1), mnist_net2(2,3)]'}
            result_dict_list.append(result_dict) # 
        except Exception as e:
            print(f"Error at parse_langda_to_dicts: {e}")
    return result_dict_list

# ================================= FINAL PARSER ================================= #
def langda_parser(text:str) -> Tuple[List[dict],str]:
    """
    result_dict_list:'Langda': 'langda(X, T)', 'X': 'Return', 'T': 'None_value', 
                     'LLM': "there's a high building at: (100,200)", 'NET': '[mnist_net1(0,1), mnist_net2(2,3)]',
    result_text: only replace the langda(...) with a clear form
    """
    offset = 0
    result_text = text
    # langda_list = []
    try:

        langda_positions:list = find_langda_position_in_letter(text)

        if not langda_positions:
            print("no langda predicate found...")
            return text
        
        result_dict_list = parse_langda_to_dicts(text,langda_positions)

        if not result_dict_list:
            raise KeyError("could not get the dictonary list!") # maybe KeyError is not so suitable here

        for (start, end), langda_dict in zip(langda_positions, result_dict_list):
            # put key back to langda predicate in forms of langda(X,Y,T,...)
            filtered_keys = [key for key in langda_dict.keys() if key != "NET" and key != "LLM"]
            langda_new_predicate = f"langda({','.join([k.strip() for k in filtered_keys])})"
            langda_dict["Langda"] = langda_new_predicate

            # consider the effect of offset
            adjusted_start = start + offset
            adjusted_end = end + offset
            result_text = result_text[:adjusted_start] + langda_new_predicate + result_text[adjusted_end:]
            # new offset!
            offset += len(langda_new_predicate) - (end - start)
    except SyntaxError as e:
        print(f"capture error while reconstruct the langda predicate: {e}")
    return result_dict_list, result_text # , langda_list



# =================================== PART TWO ==================================== #
# ================================= PARSE NETWORK ================================= #
def parse_networks(network_str:str) -> Tuple[List[Tuple[str, Tuple[int, ...]]], str]:
    network_str = network_str.strip('[]')
    pattern = r'(\w+)\(([\d,]+)\)'
    matches = re.findall(pattern, network_str)

    network_list = []
    for name, params in matches:
        # 将参数字符串拆分并转换为整数元组
        param_tuple = tuple(map(int, params.split(',')))
        network_list.append([name, param_tuple])
    return network_list

def define_event_with_network(net_list: List[Tuple[str, list]]) -> list:
    # 最多支持15个网络
    global_input_names = ['X', 'Y', 'Z', 'A', 'B', 'C', 'I', 'J', 'K', 'M', 'N', 'P', 'Q', 'R', 'S', 'U']
    global_output_names = [f"ID{i}" for i in range(1, 16)]
    print("net_list",len(net_list))
    input_names = global_input_names[:len(net_list)]
    output_names = global_output_names[:len(net_list)]

    event_string_list = []
    net_name_list = []
    if not net_list:
        return ""
    # 添加 NN 谓词的注释
    event_string_list.append("% NN Predicates:")
    for item_list in net_list:
        for item in item_list:
            name = item[0]
            labels = item[1]
            labels_str = ', '.join(map(str, labels))
            event_string_list.append(f"nn({name}, [X], Y, [{labels_str}]) :: {name}(X, Y).")
            net_name_list.append(name)  # 将网络名称添加到列表中

    # 添加事件谓词的注释
    event_string_list.append("\n% Event Predicate:")
    event_string_list.append(f"event({', '.join(output_names)}, T) :-")
    event_string_list.append(f"    happenAt({', '.join(input_names)}, T),")

    # 添加网络调用
    for i, (input_name, output_name, net_name) in enumerate(zip(input_names, output_names, net_name_list)):
        if i < len(net_list) - 1:
            event_string_list.append(f"    {net_name}({input_name}, {output_name}),")
        else:
            event_string_list.append(f"    {net_name}({input_name}, {output_name}).")

    return event_string_list

# ============================== PARSE ALL NETWORKS ============================== #
def parse_all_networks(network_str_list:List[str]) -> str:
    """
    parse_networks: only parse network of single langda predicate
    define_event_with_network: define event and nn predicate, return a line list
    """
    all_network_list = []
    if not network_str_list:
        return []
    net_event_str = "\n% ---------------------------- Network and Event Predicates ---------------------------- %\n"
    for network_str in network_str_list:
        if not network_str:
            all_network_list.append(None)
        else:
            all_network_list.append(parse_networks(network_str))
    event_string_list = define_event_with_network(all_network_list)

    return net_event_str+"\n".join(event_string_list)+"\n"



# =============================== TEXTS FOR TESTING =============================== #
full_text_for_parse_test = '''
% =============================== % EXAMPLE % =============================== %
% UAV properties
initial_langda_content[i]ge ~ normal(90, 5).
langda_content[i]ge_cost ~ normal(-0.1, 0.2).
weight ~ normal(0.2, 0.1).

% Weather conditions
1/10::fog; 9/10::clear.

% Visual line of sight
vlos(X) :- 
    fog, distance(X, operator) < 50;
    clear, distance(X, operator) < 100;
    clear, over(X, bay), distance(X, operator) < 400.

langda(ans:"answer",LLM:"nothing").
% langda(X:"answer",LLM).
langda(why:"answer",NET:"[mlp(1,2,3,4,5,6)]").
langda(X).

% Sufficient langda_content[i]ge to return to operator
can_return(X) :- 
    B is initial_langda_content[i]ge, O is langda_content[i]ge_cost,
    D is distance(X, operator), 0 < B + (2 * O * D).

% Permits related to local features
permits(X) :- 
    distance(X, service) < 15; distance(X, primary) < 15;
    distance(X, secondary) < 10; distance(X, tertiary) < 5;
    distance(X, crossing) < 5; distance(X, rail) < 5;
    over(X, park).

valid_drone_flight(X) :- (langda(X:"Return",T,LLM:"there's a high building at: (100,200)",NET:"[mnist_net1(0,1), mnist_net2(2,3)]",), vlos(X));(can_return(X));langda(T:"anstimewer",NET).

coin_win() :-
    langda(X:"return", T:"time", NET:"[mnist_net1(0,1), mnist_net2(2,3)]", 
    LLM:"If the code difference is 2, it returns 1, otherwise it returns 0."), 
    permits(X), langda(X:"return", Y:"fun", Z:"darmstadt", NET:"[position_net(there,here), audio(dog,child,horn)]", 
    LLM:"If the we is 2, 
    and horn is there, we eat banana.").
    
% Definition of a valid mission
landscape(X) :- 
    vlos(X), weight < 25, can_return(X); 
    permits(X), can_return(X).
'''

full_text_for_result_test = """
% =============================== % EXAMPLE % =============================== %
% UAV properties
initial_langda_content[i]ge ~ normal(90, 5).
langda_content[i]ge_cost ~ normal(-0.1, 0.2).
weight ~ normal(0.2, 0.1).

% Weather conditions
1/10::fog; 9/10::clear.

% Visual line of sight
vlos(X) :- 
    fog, distance(X, operator) < 50;
    clear, distance(X, operator) < 100;
    clear, over(X, bay), distance(X, operator) < 400.

langda(ans).
% langda(X:"answer",LLM).
langda(why).
langda(X).

% Sufficient langda_content[i]ge to return to operator
can_return(X) :- 
    B is initial_langda_content[i]ge, O is langda_content[i]ge_cost,
    D is distance(X, operator), 0 < B + (2 * O * D).

% Permits related to local features
permits(X) :- 
    distance(X, service) < 15; distance(X, primary) < 15;
    distance(X, secondary) < 10; distance(X, tertiary) < 5;
    distance(X, crossing) < 5; distance(X, rail) < 5;
    over(X, park).

valid_drone_flight(X) :- (langda(X,T), vlos(X));(can_return(X));langda(T).

coin_win() :-
    langda(X,T), 
    permits(X), langda(X,Y,Z).
    
% Definition of a valid mission
landscape(X) :- 
    vlos(X), weight < 25, can_return(X); 
    permits(X), can_return(X).

"""


if __name__ == "__main__":
    langda_parser(full_text_for_parse_test)
    # parse_networks("[mnist_net1(0,1), mnist_net2(2,3)]")
    # parse_networks("[mlp(1,2,3,4,5,6)]")
    # print(find_predicates_and_add_slot_in_line(full_text_for_result_test))