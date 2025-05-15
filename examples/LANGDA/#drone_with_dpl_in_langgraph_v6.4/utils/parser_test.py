import re
from enum import Enum
from typing import List, Tuple
from problog.logic import Term, Var, Constant, Clause, AnnotatedDisjunction, And, Or, Not, AggTerm

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
        lann_dicts:List[dict]: a list
        langda_dicts:List[dict]: a list
    """
    def __init__(self):
        self.type_mapping = {
            Term: "term",
            Var: "variable",
            Constant: "constant",
            Clause: "clause",
            AnnotatedDisjunction: "annotated_disjunction",
            And: "conjunction",
            Or: "disjunction",
            Not: "negation",
            AggTerm: "aggregation"
        }
    def _map_state(self,state:bool):
        return PredicateState.BODY.value if state else PredicateState.NONE.value
    
    def get_dense_code_with_comments(self,text) -> List[Tuple[str, str, str]]:
        """
        process the code line by line and store code and comment separately,
        return with [(code_block, comment_block, in_langda),...] form

        args:
            text: The original unprocessed text in string
        It calls the function: self._find_original_line(), and self._map_state()
        returns:
            a List, each element is a Tuple of ("pure code block", "pure comment block", "in_langda")

        in_langda indicates if the code block belongs to a langda predicate, 
        it has three states: "BODY":contains langda, "NONE":has no langda, "END.":at the end of a langda
        """
        print("getting codes with comments...")
        # ----------------------- initialization ----------------------- #
        original_text = text  # 

        # ----------------------- normalize the code form ----------------------- #
        text = re.sub(r' +', ' ', text) # remove extra spaces from code only
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
        main_bracket_stack = []

        idl = 0  # index of line
        while idl < len(lines):
            line = lines[idl]  # cleaned line

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
                        main_bracket_stack.append("depth")
                        
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
                        main_bracket_stack.append("depth")
                        
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
                            main_bracket_stack.append("depth")
                        elif line[idc] == ')' and not in_quotes:
                            main_bracket_stack.pop()
                            
                            # If bracket stack is empty, we've reached the end of langda
                            if not main_bracket_stack:
                                in_langda = False
                                
                                # Add the langda code segment
                                code_line_nd = idc
                                code_segment = line[code_line_st:code_line_nd+1]

                                # ------------ check comment in remain line ------------- #
                                # ------------ there's a problem: when the pattern is not unique, it will cause some error.
                                comment_segment = "" # give a default value, prevent from none value error
                                comment_match = re.search(r'"\)\s*%', code_segment) # find the pattern: ") + optional spaces + %                                
                                if comment_match:
                                    comment_pos = line.find('%', comment_match.start())
                                    if comment_pos != -1:
                                        # print("comment_pos",code_line_nd,comment_pos)
                                        comment_segment = line[comment_pos:]
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
                            comment_segment = line[idc:]  # store the comments
                            dense_code_with_comments.append((code_segment, comment_segment, self._map_state(in_langda)))
                        else:
                            # the whole block is a comment (why I do not say "line", because there's code_line_st)
                            comment = line[idc:]
                            dense_code_with_comments.append(("", comment, self._map_state(in_langda)))
                        break

                    ### 2.Start of Multiline Comment -------------------------------- #
                    if idc < len(line) - 1 and line[idc:idc+2] == '/*':
                        in_multiline_comment = True
                        code_line_nd = idc
                        comment_part = line[idc:]
                        if code_line_st < code_line_nd:  # ignore empty line
                            code_segment = line[code_line_st:code_line_nd]
                            dense_code_with_comments.append((code_segment, "", self._map_state(in_langda)))
                        current_comment = comment_part  # gather multiline comments 
                        idc += 2
                        continue

                    ### 3.End of Multiline Comment -------------------------------- #
                    elif idc < len(line) - 1 and line[idc:idc+2] == '*/':
                        in_multiline_comment = False
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
                            current_comment += "\n" + line
                            break  # jump!
                        idc += 1
                        continue

                    # ----------------------------PART3---------------------------- #
                    # ---------- line change after a parent predicate end --------- #
                    elif line[idc] == '.' and not main_bracket_stack:
                        if idc > 0 and not line[idc-1].isdigit() and (idc == len(line)-1 or not line[idc+1].isdigit()):
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

        return dense_code_with_comments # [(code,comment,is_langda),...]

