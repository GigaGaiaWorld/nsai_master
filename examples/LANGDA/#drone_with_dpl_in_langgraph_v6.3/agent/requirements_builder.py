from typing import List, Dict, Tuple
from utils import (
    _ordinal,
    _parse_simple_dictonary,
    _expand_nested_list,
    _langda_list_to_dict,
    _list_to_dict,
)
class RequirementsBuilder:
    """
    build the requirements for langda and lann based on their dictonaries.
    IF you want to expand the terms that langda could use, add them in the LANGDATERMS
    """
    NETWORK_HEADER = "The Information of Networks:"
    LANGDA_HEADER = "The Information for Generating Code of {ordinal} Placeholder"
    REPORT_HEADER = "The {ordinal} Code Block That You Should Analyse:"
    REGENERATE_HEADER = "The {ordinal} Code Block That You Should Regenerate:"

    # LANGDATERMS = [
    #     ("HASH", "Hash tag of code, please use it actually for generation"),
    #     ("LOT", "Tools that you could use"),
    #     ("NET", "Network Requirements"),
    #     ("LLM", "Requirements of Rules"),
    #     ] # FUP term is not used for prompting, so it doesn't show here
    
    LANGDATERMS = [
        ("HASH", "<HASH> Hash tag of code: {HASH} </HASH>"),
        # ("LOT", "Tools that you could use"),
        # ("NET", "Network Requirements"),
        ("LLM", "<LLM> Requirements of Rules: {LLM} </LLM>"),
        ] # FUP term is not used for prompting, so it doesn't show here

    
    @staticmethod
    def build_network_info(net: Dict[str, str]) -> List[str]:
        item_lines = []
        item_lines.append(f"The Information of Network: {net['nn']}")  # head field
        # extend with term descriptions
        item_lines.extend(
            f"For the term: {k}, user says: {v}"
            for k, v in net.items() if k != 'nn'
        )
        item_lines.append("")  # blank line separator
        return item_lines

    @staticmethod
    def build_all_network_info(lann_dicts: List[Dict[str, str]]) -> List[str]:
        if not lann_dicts:
            return []
        lines = [RequirementsBuilder.NETWORK_HEADER]
        for net in lann_dicts:
            item_lines = RequirementsBuilder.build_network_info(net)
            lines.extend(item_lines)
        return lines
 

    @staticmethod
    def build_langda_info(idx:int, langda_dict: Dict[str, str], has_header = True) -> List[str]:
        item_lines = []
        # head = langda_dict.get("HEAD", "").strip()
        ordinal = _ordinal(idx)
        # if has_header:
        #     header = (
        #         RequirementsBuilder.LANGDA_HEADER.format(ordinal=ordinal)
        #         if not head else
        #         f"{RequirementsBuilder.LANGDA_HEADER.format(ordinal=ordinal)}, inside the Parent Predicate: {head}"
        #     )
        #     item_lines.append(header)

        # item_lines.append(RequirementsBuilder.LANGDA_HEADER.format(ordinal=ordinal))
        # for each possible key, append if present
        # !!!! we only use LLM and HASH right now
        item_lines.append("<Langda> Information of {ordinal} Placeholder:".format(ordinal))
        for term, description in (RequirementsBuilder.LANGDATERMS):
            if langda_dict.get(term):
                item_lines.append(description.format(langda_dict[term]))
        item_lines.append("</Langda>")
        return item_lines

    @staticmethod
    def build_all_langda_info(langda_dicts: List[Dict[str, str]]) -> List[dict]:
        lines: List[dict] = []
        for idx, langda in enumerate(langda_dicts, start=1):
            item_lines = RequirementsBuilder.build_langda_info(idx, langda)
            lines.append({langda["HASH"]:item_lines})
        return lines

    @staticmethod
    def build_requirements(lann_dicts: List[dict],langda_dicts: List[dict]) -> Tuple[List[dict],List[str]]:
        if lann_dicts:
            network_infos=RequirementsBuilder.build_all_network_info(lann_dicts)
        else:
            network_infos = []
        langda_infos = RequirementsBuilder.build_all_langda_info(langda_dicts)
        return langda_infos, network_infos


    @staticmethod
    def build_generate_info(langda_reqs:List[dict],lann_reqs:List[str]) -> List[str]:
        generate_info = []
        for langda_item in langda_reqs:
            _, value = _parse_simple_dictonary(langda_item)
            generate_info.extend(value)
        generate_info.extend(_expand_nested_list(lann_reqs))
        return generate_info

    @staticmethod
    def build_report_info(code_list: List[dict], langda_dicts: List[Dict[str, str]]) -> List[str]:
        lines: List[str] = []
        langda_hash_index = _langda_list_to_dict(langda_dicts)

        for idx, code_item in enumerate(code_list, start=1):
            key, value = _parse_simple_dictonary(code_item)
            # if not(key == langda_dict["HASH"]):
            #     raise ValueError(f"build_report_info: Key:{key} does not exist in langda_dicts")
            ordinal = _ordinal(idx)
            lines.append(RequirementsBuilder.REPORT_HEADER.format(ordinal=ordinal))
            if key not in langda_hash_index:
                raise ValueError(f"build_report_info: Key:{key} does not exist in langda_dicts")

            item_lines = RequirementsBuilder.build_langda_info(idx, langda_hash_index[key],has_header=False)
            lines.append(value) # code
            lines.append(item_lines) # requirements
            lines.append("Please make sure the code fits inside the placeholder(Which means it doesn't have to be a 'complete' code).") # 
            lines.append("")
        return _expand_nested_list(lines)

    @staticmethod
    def build_regenerate_info(code_list:List[dict], report_list:List[dict],langda_reqs:List[List[str]],lann_reqs:List[str]) -> Tuple[List[dict], List[str]]:
        """
        args:
            code_list: list of codes
            report_list: list of reports in json form
        return:
            fest_code_list: fest_code_list only contains the 
            regenerate_info:
            regenerate_indices:
        """
        fest_code_list:List[dict] = []
        langda_reqs_dict = _list_to_dict(langda_reqs)
        regenerate_info = _expand_nested_list(lann_reqs)
        for idx, (code_item, report_item) in enumerate(zip(code_list,report_list)):
            ordinal = _ordinal(idx)

            key, value = _parse_simple_dictonary(code_item)
            report_content = report_item[key]
            need_regenerate = str(report_content["Need_regenerate"]).strip('"').strip("'")

            if not report_content: # check if the code and report matches
                raise ValueError(f"build_regenerate_info: key:{key} the report: {report_content}")
            if not key in langda_reqs_dict: # check if the code has corresponding requirements
                raise ValueError(f"build_regenerate_info: key:{key} not in langda_reqs: {langda_reqs}")
            if need_regenerate == 'True' or need_regenerate == 'true':

                fest_code_list.append({key:None})
                regenerate_info.append(RequirementsBuilder.REGENERATE_HEADER.format(ordinal=ordinal))
                regenerate_info.append(f"Requirements:")
                regenerate_info.append(langda_reqs_dict[key])     # It's a list of string
                
                regenerate_info.append(f"Current Code:")
                regenerate_info.append(value)

                regenerate_info.append(f"It's corresponding analysis:")
                regenerate_info.append(report_content["Report"])
                regenerate_info.append("")

            elif need_regenerate == 'False' or need_regenerate == 'false':
                fest_code_list.append(code_item)
            else:
                raise ValueError(f"Need_regenerate has invalid value: {report_content['Need_regenerate']}")
        
        return fest_code_list, _expand_nested_list(regenerate_info)