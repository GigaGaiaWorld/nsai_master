from typing import List, Dict, Tuple
from utils import (
    _ordinal,
    _parse_simple_dictonary,
    _expand_nested_list,
    _parse_simple_dictonary,
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

    LANGDATERMS = [("LOT", "Tools that you could use"),
                   ("NET", "Network Requirements"),
                   ("LLM", "Requirements of Rules"),
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
    def build_langda_info(idx:int, langda_dict: Dict[str, str]) -> List[str]:
        item_lines = []
        head = langda_dict.get("HEAD", "").strip()
        ordinal = _ordinal(idx)
        header = (
            RequirementsBuilder.LANGDA_HEADER.format(ordinal=ordinal)
            if not head else
            f"{RequirementsBuilder.LANGDA_HEADER.format(ordinal=ordinal)}, inside the Parent Predicate: {head}"
        )
        item_lines.append(header)
        # for each possible key, append if present
        for term, descrip in (RequirementsBuilder.LANGDATERMS):
            if langda_dict.get(term):
                item_lines.append(f"{descrip}: {langda_dict[term].strip()}")
        item_lines.append("")
        return item_lines

    @staticmethod
    def build_all_langda_info(langda_dicts: List[Dict[str, str]]) -> List[str]:
        lines: List[str] = []
        for idx, langda in enumerate(langda_dicts, start=1):
            item_lines = RequirementsBuilder.build_langda_info(idx, langda)
            lines.append(item_lines)
        return lines


    @staticmethod
    def build_requirements(lann_dicts: List[dict],langda_dicts: List[dict]) -> Tuple[List[str],List[str]]:
        if lann_dicts:
            network_infos=RequirementsBuilder.build_all_network_info(lann_dicts)
        else:
            network_infos = []
        langda_infos = RequirementsBuilder.build_all_langda_info(langda_dicts)
        return network_infos, langda_infos, 


    @staticmethod
    def build_generate_info(langda_reqs:List[str],lann_reqs:List[str]) -> List[str]:
        generate_info = _expand_nested_list(langda_reqs)
        generate_info.extend(_expand_nested_list(lann_reqs))
        return generate_info

    @staticmethod
    def build_report_info(code_list: List[dict]) -> List[str]:
        lines: List[str] = []
        for idx, code_item in enumerate(code_list):
            key, value = _parse_simple_dictonary(code_item)
            ordinal = _ordinal(idx)
            lines.append(RequirementsBuilder.REPORT_HEADER.format(ordinal=ordinal))
            lines.append(value)
            lines.append("")
        return lines

    @staticmethod
    def build_regenerate_info(code_list:List[dict], report_list:List[dict],langda_reqs:List[str],lann_reqs:List[str]) -> Tuple[List[dict], List[str]]:
        """
        args:
            code_list: list of codes
            report_list: list of reports in json form
        return:
            fest_code_list: 
            regenerate_info:
            regenerate_indices:
        """
        fest_code_list:List[dict] = []
        regenerate_info = _expand_nested_list(lann_reqs)
        for idx, (code_item, report, req) in enumerate(zip(code_list,report_list,langda_reqs)):
            ordinal = _ordinal(idx)
            key, value = _parse_simple_dictonary(code_item)

            if report["Need_regenerate"] == "True":
                fest_code_list.append({key:None})
                regenerate_info.append(RequirementsBuilder.REGENERATE_HEADER.format(ordinal=ordinal))
                regenerate_info.append(f"Requirements:")
                regenerate_info.append(req)
                regenerate_info.append(f"Current Code:")
                regenerate_info.append(value)
                regenerate_info.append(f"It's corresponding analysis:")
                regenerate_info.append(report["Report"])
                regenerate_info.append("")

            else:
                fest_code_list.append(code_item)
        
        return fest_code_list, regenerate_info