import re
from typing import List, Tuple, Dict
from enum import Enum

class PredicateState(Enum):
    """Enum class defines predicate state"""
    NONE = "NONE" # Not in langda predicate
    BODY = "BODY" # In the langda predicate body
    END  = "END." # At the end of the langda predicate

class Parser(object):
    """Parsing Prolog code, especially parsers for langda and lann predicates

    Attributes:
        text (str): original input text
        result_text (str): processed text result
        lann_dicts (List[dict]): parsed lann predicate list
        langda_dicts (List[dict]): parsed langda predicate list
    """
    def __init__(self, text):
        self.text:str = text
        self.result_text:str = ""
        self.lann_dicts:List[dict] = []
        self.langda_dicts:List[dict] = []


    # =============================== CODE FOR PARSING ORIGINAL CODE =============================== #
    def _find_original_line(self,original_text: str, compressed_line: str) -> str:
        """
        Find the line in the original text that corresponds to the compressed line, preserving the original spaces

        Args:
            original_text: original text
            compressed_line: compressed line

        Returns:
            The original line found, or an empty string if not found

        """
        original_lines = original_text.split('\n')
        # compare with removing spaces
        compressed_line_no_spaces = compressed_line.strip()
        for orig_line in original_lines:
            if re.sub(r' +', ' ', orig_line.strip()) == compressed_line_no_spaces:
            # if orig_line.strip().replace(' ', '') == compressed_line_no_spaces:
                return orig_line
        return ""  # could not find...

    def _map_state(self,state:bool):
        return PredicateState.BODY.value if state else PredicateState.NONE.value

    def get_dense_code_with_comments(self) -> List[Tuple[str, str, str]]:
        """
        process the code line by line and store code and comment separately,
        return with [(code_block, comment_block, in_langda),...] form

        Args:
            text: The original unprocessed text in string
        It calls the function: self._find_original_line(), and self._map_state()
        Returns:
            a List, each element is a Tuple of ("pure code block", "pure comment block", "in_langda")

        in_langda indicates if the code block belongs to a langda predicate, 
        it has three states: "BODY":contains langda, "NONE":has no langda, "END.":at the end of a langda
        """
        print("getting codes with comments...")
        # ----------------------- initialization ----------------------- #
        original_text = self.text  # 
        # ----------------------- normalize the code form ----------------------- #
        text = re.sub(r' +', ' ', self.text) # remove extra spaces from code only
        # text = re.sub(r' +', '', text) # remove extra spaces from code only
        lines = text.split('\n')
        dense_code_with_comments = []

        # State Parameters
        in_quotes = False
        in_multiline_comment = False
        is_escaped = False
        current_comment = ""
        code_segment = ""
        # ----------------------- langda tracking parameters ----------------------- #
        in_langda = False
        bracket_stack = []
        main_bracket_stack = []
        idl = 0  # index of line
        while idl < len(lines):
            line = lines[idl].strip()   # cleaned line
            
            if not line:  # skip empty line
                idl += 1
                continue
            
            code_line_st = 0    # the first code char in line
            code_line_nd = None # the last code char in line
            idc = 0             # index of character
            
            # Flag to track if this line contains langda predicate

            while idc < len(line):
                # ------------------------------PART1------------------------------ #
                # ------------------------- check langda -------------------------- #
                if not in_quotes and not in_multiline_comment:
                    if line[idc] == '(':
                        main_bracket_stack.append("depth")
                    elif line[idc] == ')' and main_bracket_stack:
                        main_bracket_stack.pop()
                    # <<<====================== EXTENDABLE AREA =========================>>> #
                    # ========================= EXTENDABLE: LANGDA ========================= #
                    # Check for langda predicate start
                    if (idc <= len(line) - 7 and line[idc:idc+7] == 'langda(') and not in_langda:
                        in_langda = True
                        bracket_stack.append("depth")
                        
                        # If there's code before langda, we cut it as non-langda code in a single block
                        if code_line_st < idc:
                            code_segment = line[code_line_st:idc]
                            dense_code_with_comments.append((code_segment, "", PredicateState.NONE.value))
                        
                        code_line_st = idc
                        idc += 7
                        continue
                    # ========================= EXTENDABLE: LANN =========================== #
                    # Check for lann predicate start
                    elif (idc <= len(line) - 5 and line[idc:idc+5] == 'lann(') and not in_langda:
                        in_langda = True
                        bracket_stack.append("depth")
                        
                        # If there's code before langda, we cut it as non-langda code in a single block
                        if code_line_st < idc:
                            code_segment = line[code_line_st:idc]
                            dense_code_with_comments.append((code_segment, "", PredicateState.NONE.value))
                        
                        code_line_st = idc
                        idc += 5
                        continue
                    # ========================= EXTENDABLE: ??? ============================ #
                    # The new extend logic for detect other predicates could be inserted here!
                    # ......
                    # <<<====================== EXTENDABLE AREA =========================>>> #

                    # Tracking bracket matching for langda
                    elif in_langda:
                        if line[idc] == '(' and not in_quotes:
                            bracket_stack.append("depth")
                        elif line[idc] == ')' and not in_quotes:
                            bracket_stack.pop()
                            
                            # If bracket stack is empty, we've reached the end of langda
                            if not bracket_stack:
                                in_langda = False
                                
                                # Add the langda code segment
                                code_line_nd = idc
                                code_segment = line[code_line_st:code_line_nd+1]

                                # ------------ check comment in remain line ------------- #
                                # ------------ there's a problem: when the pattern is not unique, it will cause some error.
                                comment_segment = "" # give a default value, prevent from none value error
                                original_line = self._find_original_line(original_text, line)

                                if original_line:
                                        comment_match = re.search(r'"\)\s*%', original_line) # find the pattern: ") + optional spaces + %                                
                                        if comment_match:
                                            comment_pos = original_line.find('%', comment_match.start())
                                            if comment_pos != -1:
                                                # print("comment_pos",code_line_nd,comment_pos)
                                                comment_segment = original_line[comment_pos:]
                                                dense_code_with_comments.append((code_segment, comment_segment, PredicateState.END.value)) # At the end of a langda, we use "END"!!!
                                                

                                dense_code_with_comments.append((code_segment, "", PredicateState.END.value)) # At the end of a langda, we use "END"!!!

                                # Set the start for any following non-langda code
                                code_line_st = idc + 1
                                code_line_nd = None
                                # if comment_segment:
                                #     break
                # ------------------------------PART2------------------------------ #
                # ------------------------- check comment ------------------------- #
                if not in_quotes:

                    ### 1.Single Line Comment -------------------------------- #
                    if line[idc] == '%' and not in_multiline_comment:
                        code_line_nd = idc
                        if code_line_st < code_line_nd: # ignore empty line
                            code_segment = line[code_line_st:code_line_nd]
                            # find comment in the original uncompressed lines
                            original_line = self._find_original_line(original_text, line)
                            if original_line:
                                comment_segment = original_line[original_line.find('%'):]
                            else:
                                comment_segment = line[idc:]  # store the comments

                            dense_code_with_comments.append((code_segment, comment_segment, self._map_state(in_langda)))
                        else:
                            # the whole block is a comment (why I do not say "line", because there's code_line_st)
                            original_line = self._find_original_line(original_text, line)
                            if original_line:
                                comment = original_line[original_line.find('%'):]
                            else:
                                comment = line[idc:]

                            dense_code_with_comments.append(("", comment, self._map_state(in_langda)))

                            # it will cause problem: the full line comment will add to the previous predicate by fault!!!
                            # if len(dense_code_with_comments) > 0:
                            #     # add the comment together with the previous code
                            #     # we use is_langda_flag to seperate it from is_langda
                            #     last_code, last_comment, is_langda_flag = dense_code_with_comments[-1]
                            #     dense_code_with_comments[-1] = (last_code, last_comment + " " + comment, is_langda_flag)
                            # else:
                            #     # If the whole block is a comment, 
                            #     dense_code_with_comments.append(("", comment, self._map_state(in_langda)))
                        break

                    ### 2.Start of Multiline Comment -------------------------------- #
                    if idc < len(line) - 1 and line[idc:idc+2] == '/*':
                        in_multiline_comment = True
                        code_line_nd = idc
                        
                        # find comment in the original uncompressed lines
                        original_line = self._find_original_line(original_text, line)
                        if original_line:
                            comment_part = original_line[original_line.find('/*'):]
                        else:
                            comment_part = line[idc:]
                            
                        if code_line_st < code_line_nd:  # ignore empty line
                            code_segment = line[code_line_st:code_line_nd]
                            dense_code_with_comments.append((code_segment, "", self._map_state(in_langda)))
                            current_comment = comment_part  # gather multiline comments 
                        else:
                            current_comment = comment_part  # the whole line is in comment
                        idc += 2
                        continue

                    ### 3.End of Multiline Comment -------------------------------- #
                    elif idc < len(line) - 1 and line[idc:idc+2] == '*/':
                        in_multiline_comment = False
                        # find comment in the original uncompressed lines
                        original_line = self._find_original_line(original_text, line)
                        if original_line:
                            end_comment_part = original_line[:original_line.find('*/')+2]
                            current_comment += "\n" + end_comment_part  # add the comment
                        else:
                            current_comment += "\n" + line[:idc+2]  # add */ to the comment
                        
                        # add the comment together with the previous code
                        if len(dense_code_with_comments) > 0:
                            # we use is_langda_flag to seperate it from is_langda
                            last_code, last_comment, is_langda_flag = dense_code_with_comments[-1]
                            if last_comment:
                                dense_code_with_comments[-1] = (last_code, last_comment + "\n" + current_comment, is_langda_flag)
                            else:
                                dense_code_with_comments[-1] = (last_code, current_comment, is_langda_flag)
                        else:
                            # if there's no code before it
                            dense_code_with_comments.append(("", current_comment, self._map_state(in_langda)))
                        
                        current_comment = ""  # reset comment
                        idc += 2
                        code_line_st = idc
                        continue

                    ### 4.Continuely processing -------------------------------- #
                    elif in_multiline_comment:
                        # gather multiline comments
                        if idc == 0:  # whole line
                            # ...
                            original_line = self._find_original_line(original_text, line)
                            if original_line:
                                current_comment += "\n" + original_line
                            else:
                                current_comment += "\n" + line
                            break  # jump!
                        idc += 1
                        continue

                    # ----------------------------PART3---------------------------- #
                    # ---------- line change after a parent predicate end --------- #

                    # elif line[idc:idc+1] == ').':
                    #     """
                    #     似乎被上面代码“挡”掉了, 完全没发挥作用
                    #     """
                    #     # print("End State OF PREDICATE OR LANGDA:", in_langda, code_segment)
                    #     code_line_nd = idc
                    #     if code_line_st < code_line_nd:  # ignore empty line
                    #         code_segment = line[code_line_st:code_line_nd]
                    #         dense_code_with_comments.append((code_segment, "", self._map_state(in_langda)))
                    #         if idc+2 <len(line): code_line_st = idc+2
                    elif line[idc] == '.' and not main_bracket_stack:
                        # print("End State OF PREDICATE OR LANGDA:", in_langda, code_segment)
                        code_line_nd = idc
                        code_segment = line[code_line_st:code_line_nd+1]
                        dense_code_with_comments.append((code_segment, "", self._map_state(in_langda)))
                        if idc+1 <len(line): 
                            code_line_st = idc+1
                            code_line_nd = None

                # ------------------------------PART4------------------------------ #
                # --------------- process quotes and escape symbols --------------- #
                # Escaped state check
                if line[idc] == '\\' and not is_escaped:
                    is_escaped = True
                    idc += 1
                    continue
                
                # Quoted state check
                if line[idc] == '"' and not is_escaped:
                    in_quotes = not in_quotes

                # -----%---- # new char # -----%---- #
                is_escaped = False
                idc += 1

            # ------------------------------PART5------------------------------ #
            # --------- ---------- process end of the line -------------------- #
            # Reach the end of the line, if there is code and it is not in a multi-line comment, add it to the pure code
            if not in_multiline_comment and code_line_st < len(line) and code_line_nd is None: # ignore empty line
                code_segment = line[code_line_st:]
                dense_code_with_comments.append((code_segment, "", self._map_state(in_langda)))

            # -----%---- # new line # -----%---- #
            idl += 1

        # print 4 test
        print("===================dense_code_with_comments==================\n")
        for code, comment, is_langda in dense_code_with_comments:
                print(f"LANGDA:{is_langda}||CODE:{code}|      COMMENT: {comment}")
        print("=============================================================\n")
        return dense_code_with_comments # [(code,comment,is_langda),...]


    # =============================== CODE FOR PARSING LAGNDA AND LANN =============================== #
    def _parse_lann_or_langda_content_to_dicts(self,content) -> dict:
        """
        Parse content in LANN or LANGDA format into a dictionary.
        
        Args:
            content: String content to parse, typically obtained from match.group(1)
            
        Returns:
            A dictionary where each key-value pair represents a parsed term
        """
        result_dict = {}
        term_start = 0
        
        # State variables
        in_quotes = False
        is_escaped = False
        in_brackets = 0
        current_part = ""  # Initialize current_part
        
        # ======================Part1: store terms in a list====================== #
        idc = 0  # index of content character
        while idc < len(content):
            # Handle quotes and escaping (with a state machine)
            if content[idc] == '"' and not is_escaped:
                in_quotes = not in_quotes
                
            elif content[idc] == '[' and not in_quotes:
                in_brackets += 1
                current_part += content[idc]
            elif content[idc] == ']' and not in_quotes:
                in_brackets -= 1
                current_part += content[idc]
                
            # Update escape state
            is_escaped = content[idc] == '\\' and not is_escaped
            
            # Separate into terms, when: not in quotes, not in bracket, and current char is ","
            if not in_quotes and in_brackets == 0 and (content[idc] == ',' or idc == len(content) - 1):
                end_idx = idc if content[idc] == ',' else idc + 1
                if not term_start < end_idx:
                    raise ValueError("Term not found, please check the definition of langda and lann.")
                term = content[term_start:end_idx].strip()
                
                # =================== Part2: find keys and value pairs =============== #
                idt = 0  # index of term character
                has_value = False  # Initialize has_value
                
                while idt < len(term):
                    if term[idt] == ':':
                        value_start = idt + 1
                        has_value = True
                        break
                        
                    idt += 1
                    
                # =================== Part3: parse each term as key,value pair =============== #
                # extract key and value
                if has_value:
                    key = term[0:idt].strip()
                    value = term[value_start:].strip()
                    
                    # # remove quotes 
                    # if value.startswith('"') and value.endswith('"'):
                    #     value = value[1:-1]
                    
                    result_dict[key] = value
                else:
                    # in case there's no value, just a key
                    key = term.strip()
                    result_dict[key] = ""
                    
                term_start = idc + 1  # next term...
                
            idc += 1
            
        if not result_dict:
            raise ValueError("Langda information not found, forgot to define langda parameters?")
            
        return result_dict


    def replace_langda_and_lann_terms(self,text_list:List[Tuple[str, str, str]]) -> Tuple[List[str],List[dict],List[dict]]:
        """
        Replace langda and lann predicates in the given text list.
        And store informations in dictonary
        Args:
            text_list: List of tuples (code, comment, predicate_status)
                    where predicate_status can be "NONE", "BODY", or "END."
        It calls the function: self._parse_lann_or_langda_content_to_dicts()
        Returns:
            Tuple of (modified text list, lann_dicts, langda_dicts)
        """
        print("processing langda and lann terms...")
        # Initialize outputs
        text_list_copy = text_list.copy()  # Create a copy to avoid modifying the original
        lann_dicts:List[dict] = []
        langda_dicts:List[dict] = []
        result_text_list = []

        # State variables
        single_langda = []
        single_lann = []
        single_comment = []
        in_langda = False
        in_lann = False

        predicate_head = ""
        predicate_end = None

        idl = 0
        while idl < len(text_list_copy):
            current_item:Tuple[str,str,str] = text_list_copy[idl]
            if len(current_item) != 3:
                raise ValueError(f"Warning: Position {idl} has a uncorrect form: {current_item}")
                
            (code, comment, predicate_status) = current_item
            if ":-" in code:
                predicate_head, _, _ = code.strip().partition(":-")

            if code and "." == code[-1]:
                predicate_end = True
                if code == ".":
                    idl += 1
                    continue # ignore the pure "." line

            has_langda = code.startswith("langda(")
            has_lann = code.startswith("lann(")
            # -------------------- #           PART1            # -------------------- #
            # -------------------- Process single lann predicates -------------------- #
            # Start of lann predicate
            if has_lann and not in_lann:
                in_lann = True
                lann_start = idl    # mark the start of lann predicate
                single_lann = []
                single_comment = []
                if not idl + 1 < len(text_list_copy):
                    raise ValueError("The code is incomplete, please check your lann predicates.")

            # -------------------- #            PART2             # -------------------- #
            # -------------------- Process single langda predicates -------------------- #
            # Start of langda predicate
            if has_langda and not in_langda:
                langda_head = predicate_head
                in_langda = True
                single_langda = []
                single_comment = []


            if in_lann:
                # Middle of lann predicate
                if predicate_status == PredicateState.BODY.value:
                    single_lann.append(code)
                    single_comment.append(comment)

                # End of lann predicate
                elif predicate_status == PredicateState.END.value:
                    # Add the current segment
                    single_lann.append(code)
                    single_comment.append(comment)
                    # Create the full lann term and its dict representation
                    full_lann_term = "".join(single_lann)
                    full_lann_content = full_lann_term[5:-1]
                    lann_dict = self._parse_lann_or_langda_content_to_dicts(full_lann_content)
                    lann_dicts.append(lann_dict)

                    # -------------------- # REPLACE # -------------------- #
                    # Replace the original segments with our processed version:
                    # nn(net_name,[X],Y,[1,2,3])::digit(X,Y).
                    nn_term = f"nn({','.join([k for k in lann_dict.keys()])})"
                    lann_dict['nn'] = nn_term

                    # Filter out empty comments before joining (optional, same as langda)
                    filtered_comments = [c for c in single_comment if c]
                    joined_comments = "\n".join(filtered_comments) + "\n" + nn_term

                    result_text_list.append(joined_comments)

                    # Reset state
                    lann_dict = {}
                    in_lann = False


            elif in_langda:

                # Middle of langda predicate
                if predicate_status == PredicateState.BODY.value:
                    single_langda.append(code)
                    single_comment.append(comment)
                
                # End of langda predicate
                elif predicate_status == PredicateState.END.value:
                    # Add the current segment
                    single_langda.append(code)
                    single_comment.append(comment)
                    
                    # Create the full langda term and its dict representation
                    full_langda_term = " ".join(single_langda)
                    full_langda_content = full_langda_term[7:-1]
                    langda_dict = self._parse_lann_or_langda_content_to_dicts(full_langda_content)
                    langda_dict["HEAD"] = langda_head
                    langda_dicts.append(langda_dict)
                    langda_head = ""
                    # -------------------- # REPLACE # -------------------- #
                    # Replace the original segments with our processed version:
                    # # comment1...
                    # # comment2...
                    #  "\n{{LANGDA}}\n"
                    
                    # Filter out empty comments before joining
                    filtered_comments = [c for c in single_comment if c]
                    joined_comments = "\n".join(filtered_comments) + "{{LANGDA}}"
                    
                    # Replace all items from langda_start to idl with a single item containing our joined comments
                    # text_list_copy[langda_start:idl+1] = [(joined_comments, "", "NONE")]
                    result_text_list.append(joined_comments)
                    # Adjust index to continue after our replacement - always advance by 1
                    # since we replaced with a single item
                    # idl = langda_start
                    
                    # Reset state
                    langda_dict = {}
                    in_langda = False

            else:
                result_text_list.append(code + comment)
            
            if predicate_end:
                predicate_head = ""
                predicate_end = False
            idl += 1
        return result_text_list, lann_dicts, langda_dicts
        # return [item[0] for item in text_list_copy], lann_dicts, langda_dicts


# =============================== FINAL PARSER API =============================== #
def integrated_code_parser(text:str) -> Tuple[List[str],List[Dict[str,str]],List[Dict[str,str]]]:
    parser = Parser(text)
    text_list = parser.get_dense_code_with_comments()
    result_text, lann_dicts, langda_dicts = parser.replace_langda_and_lann_terms(text_list)
    return result_text, lann_dicts, langda_dicts


# =============================== TEXTS FOR TESTING =============================== #
full_text_for_parse_test = '''
% =============================== % EXAMPLE % =============================== %
lann(mnist_net1:"decrib net1",[M]:"describe M",N,[0,1,"None"]:"desc someting") :: event1(M,N). % lann(what?)
lann(mnist_net2,[X],Y:"what is Y?",[2,3,"dog","horn"]:"output 2 and 3")    % (what_is_this(X,S):maybe?
:: funfunf(X,Y).     % have fun here)!

lann(mnist_net3,       % net work haha
[R],S:"what whatwhaitsat?",     % X and what Y: this Y! stop, lann(X,Y)
["this","thas","was","isss"]:"outoutoutout")    % (what_e q2wre g wads  cf :: event114(X,Y).
:: digit232(R,S).     % have fun here)!


% UAV properties
% initial_langda_content[i]ge ~ normal(90, 5).
% langda_content[i]ge_cost ~ normal(-0.1, 0.2).
% weight ~ normal(0.2, 0.1).

% Weather conditions
1/10::fog; 9/10::clear.

% Visual line of sight
vlos(X) :- 
    fog, distance(X, operator) < 50;
    clear, distance(X, operator) < 100;
    clear, over(X, bay), distance(X, operator) < 400.

langda(ans:"answer",LLM:"nothing"). % langda(LLM:"this is me").
% langda(X:"answer",LLM). % stop it
langda(why:"answer",NET:"[mlp(1,2,3,4,5,6)]").
langda(X:"answer",llm:"stop"). % why not here?
/*
% Sufficient langda_content[i]ge to return to operator
can_return(X) :- 
    B is initial_langda_content[i]ge, O is langda_content[i]ge_cost,
    D is distance(X, operator), 0 < B + (2 * O * D), langda(LLM:"how about this?")
*/ langda(NET:"[no(1,2,3)]",LLM:"This is crazy")        .       waht_coin(sdaw,A) :- zzz(X;Y),
langda(LLM,NET).

% Permits related to local features
permits(X) :- 
    distance(X, service) < 15; distance(X, primary) < 15;
    distance(X, secondary) < 10; distance(X, tertiary) < 5;
    distance(X, crossing) < 5; distance(X, rail) < 5;
    over(X, park).

valid_drone_flight(X) :- (langda(X:"Return",T,LLM:"there's a high building at: (100,200)",NET:"[mnist_net1(0,1), mnist_net2(2,3)]"), vlos(X));(can_return(X));langda(T:"anstimewer",NET).

coin_win() :-
    % the code need to be clean!
    langda(X:"return", T:"time", NET:"[mnist_net1(0,1), mnist_net2(2,3)]",              % a langda code for new stuff
    Y:"happy",              % why the code is happy?
    TOL:"[mnist_net1(0,1), mnist_net2(2,3)]",              % wewewewewewewe
    LLM:"If the code difference is 2, % it returns 1, otherwise it returns 0.")          % we use deepseek here!
    ,permits(X), langda(X:"return", Y:"fun", Z:"darmstadt", NET:"[position_net(there,here), audio(dog,child,horn)]",     % nothing useful % so quit!
    LLM:"If the we is 2,            % comment end
    and horn is there, we eat banana."). coin_this(X,Y,3) :- langda(X,LLM:"asdasda"),       % comment conisthis

    predicate(sd, X), asd(MMMA)
    . 

% Definition of a valid mission
landscape(X) :- 
    vlos(X), weight < 25, can_return(X); 
    permits(X), can_return(X).

'''


if __name__ == "__main__":
    # code, lann, langda = integrated_code_parser("""ass(as(This:"sss(sasa,asas).")).""")
    code, lann, langda = integrated_code_parser(full_text_for_parse_test)
    print("\n".join(code))