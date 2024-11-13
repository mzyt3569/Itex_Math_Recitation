import json
import re
from pylatexenc.latexwalker import LatexWalker, LatexMacroNode, LatexGroupNode, LatexCharsNode, LatexEnvironmentNode, LatexMathNode
from modules.utils import find_index,find_first
from collections import deque
import copy

inequal_operator = ["<",">",r"\leq",r"\geq","≥","≤"]
left_operator = ['[','{','(']
right_operator = [']','}',')']

close_operator = [',',':','ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ', '①', '②', '③', '④', '⑤']

left_operator_with_bs = [r'\(',r'\(',r'\['] # this have to match with re, i think it doesn't need.
right_operator_with_bs = [r'\\\)',r'\\\}',r'\\\]',r'\\\s*right\)',r'\\\s*right\}',r'\\\s*right\]'] # this have to match with re
close_operator_with_bs = [r'\\begin\s*\{cases\}',r'\\end\s*\{cases\}',r'\\mid',r'\\\\',r'\\quad',r'\?',r'\\text\{([^}]*)\}']

def search_left(sliced_string: str) -> str:
    ret, cnt = "", [0,0,0]
    for idx in range(len(sliced_string),0,-1):
        c = sliced_string[idx-1] #현재 문자열 체크.

        if c in right_operator:
            cnt[right_operator.index(c)] += 1
            ret = c + ret
        elif c in left_operator:
            cnt[left_operator.index(c)] -= 1
            if cnt[left_operator.index(c)] < 0: break
            ret = c + ret
        elif c in close_operator or (ord('가') <= ord(c) <= ord('힣') and sum(cnt) == 0):
            break
        elif find_first(sliced_string[:idx],close_operator_with_bs,True) != -1:
            break
        elif c == '.' and idx-1 != 0 and not (ord('0') <= ord(sliced_string[idx-2]) <= ord('9')):
            break
        else:
            ret = c + ret
        
    return ret

def search_right(entire_string,op_idx,indices):
    #input : 전체 식, 현재 부등호, 다른 부등호들의 시작 위치
    #output : 현재 부등호의 오른쪽 부분, 사용된 배열, 같은 레벨의 부등호 개수

    ret = ""
    used = []
    cnt = [0,0,0] #소괄호, 중괄호, 대괄호 쓰는 용도
    op_cnt = 1

    for idx in range(op_idx[1],len(entire_string)):
        c = entire_string[idx] # 현재 체크할 문자입니다.
        if c in left_operator:
            cnt[left_operator.index(c)] += 1
            ret += c
        elif c in right_operator:
            cnt[right_operator.index(c)] -= 1
            if cnt[right_operator.index(c)] < 0: break
            ret += c
        elif (chk := find_first(entire_string[idx:],right_operator_with_bs)) != -1:
            chk %= 3
            cnt[chk] -= 1
            if cnt[chk] < 0: break
            ret += c
        elif c in close_operator or (ord('가') <= ord(c) <= ord('힣') and sum(cnt) == 0):
            break
        elif find_first(entire_string[idx:],close_operator_with_bs) != -1:
            break
        else:
            ret += c

        if idx in indices and sum(cnt) == 0:
            used.append(indices.index(idx))
            op_cnt += 1
    return ret,used,op_cnt

def replace_pure(pure: dict, non_pure: list[str]) -> None:
    first = len(pure) # 처음에 pure의 길이가 얼마였는가?
    pattern = r"^\[INEQUAL\s+\d+\]$" # 매칭 패턴

    new_non_pure = []
    for idx,l in enumerate(non_pure):
        np_inequal = l[0]
        for key,value in pure.items(): np_inequal = np_inequal.replace(value,key)
        non_pure[idx][0] = np_inequal

    for (np_inequal,cnt) in non_pure:
        if re.fullmatch(pattern, np_inequal):
            continue
        elif cnt == len(find_index(np_inequal,inequal_operator)):
            pure[f"[INEQUAL {len(pure) + 1}]"] = np_inequal.strip()
        else:
            new_non_pure.append([np_inequal,cnt])

    non_pure = new_non_pure
    if first != len(pure): replace_pure(pure,non_pure)

def inequality_parser(latex_string: str) -> tuple[str,dict]:
    modified_string = latex_string 

    indices = find_index(latex_string,inequal_operator) #각 부등호의 시작점과 끝점을 저장하는 리스트를 반환
    
    checker = set() # 이미 추출된 부등식을 체크하기 위함.
    pure = {} # 피연산자들에 부등호가 없음.
    non_pure = [] # 피연산자들에 부등호가 남아있음. e.g) P(X < 2) < 3
    visited = [False]*len(indices) # 부등호 중복확인 체크.

    for idx,op in enumerate(indices):
        if visited[idx] == True: continue # continue if we checked this op already.

        left_side = search_left(latex_string[:op[0]]) # We search left part of inequality.

        right_side,used,op_cnt = search_right(latex_string,op,[num[0] for num in indices])
        # Input : 전체 식, 현재 부등호, 다른 부등호의 시작 위치. 
        # Output : 현재 부등호 기준 오른쪽 파트, 사용된 부등호의 인덱스, 이어져 있는 부등식 개수.

        for num in used: visited[num] = True # 오른쪽을 탐색하는 동안 찾은 부등호는 탐색 표시.

        if left_side.count('|') == 1: left_side = left_side[left_side.find('|')+1:] # 땜빵 : 만약 {x | x < 2} 와 같은 식이면, 조건 앞을 삭제 시킨다.
        inequality = left_side + latex_string[op[0]:op[1]] + right_side # 부등식을 조합한다.

        if len(find_index(inequality,inequal_operator)) == op_cnt:
            # 만약 자신 하위의 부등식이 없다면
            if inequality not in checker:
                pure[f"[INEQUAL {len(pure) + 1}]"] = inequality.strip()
                checker.add(inequality)
        else:
            if inequality not in checker:
            # 자신 하위의 부등식이 있다면
                non_pure.append([inequality,op_cnt])
                checker.add(inequality)
    
    replace_pure(pure,non_pure)
    for key,value in pure.items():
        modified_string = modified_string.replace(value,key)
    return modified_string,pure

def inequality_extractor(json_dict: dict) -> dict:
    # this function iterates all latex itmes, and if there exist inequalities, than make inequal_list inside the latex.
    ret = {}

    for latex_idx,latex_val in json_dict.items():
        if latex_idx == "Question" or latex_idx == 'File': continue # We do not care about question and file name.
        modified_str,inequal_dict = inequality_parser(latex_val)

        dict_val = {"Origin" : modified_str}
        if inequal_dict: dict_val["Inequal_list"] = inequal_dict # if inequalities are exist, make list.
        ret[latex_idx] = dict_val

    return ret

################################################################

idx = 1

def fraction_parser(latex_string: str) -> tuple[str,dict]:
    latex_list = {} # 분수가 들어갈 예정입니다.
    walker = LatexWalker(latex_string) # pylatexenc가 적절히 먼저 파싱을 하면
    nodes, pos, length = walker.get_latex_nodes() # 우리가 파싱된 node를 가져올 수 있다.
    modified_str = ""

    def traverse_node(node,frac_list):
        global idx
        if isinstance(node,LatexEnvironmentNode):
            # 중요 : 현재 EnvironmentNode에 들어가는 것이 case밖에 없었으므로, 이 방식이 유효함.
            # 만약 matrix가 등장한다면, 이 역시 수정해야 한다.
            ret_str = "\\begin{cases}"
            for env_node in node.nodelist:
                ret_str += traverse_node(env_node,frac_list)
            ret_str += "\\end{cases}"
            return ret_str
        elif isinstance(node,LatexMathNode):
            # 중요 : MathNode역시 역슬래시 괄호류 밖에 없는데, 이 중에서 쓰이는 것이 소괄호 말고는 없었음.
            # 애초에 이러한 Node는 없는게 좋다.
            ret_str = "\\("
            for math_node in node.nodelist:
                ret_str += traverse_node(math_node,frac_list)
            ret_str += "\\)"
            return ret_str
        elif isinstance(node,LatexGroupNode):
            # 중괄호에 둘러쌓인 부분이 단독으로 존재한다면, 이쪽으로 온다.
            ret_str = "{"
            for group_node in node.nodelist:
                ret_str += traverse_node(group_node,frac_list)
            ret_str += "}"
            return ret_str
        elif isinstance(node,LatexMacroNode):
            # 중괄호에 둘러쌓인 부분이 특정 Macro(frac,sqrt)에 종속되어있다면, 이쪽으로 온다.
            if node.macroname == 'frac':
                now = idx
                ret = f"[FRAC {now}]"
                idx += 1
                numerator = node.nodeargd.argnlist[0]
                denominator = node.nodeargd.argnlist[1]
                num_str = traverse_node(numerator,frac_list)[1:-1]
                den_str = traverse_node(denominator,frac_list)[1:-1]
                temp = "\\frac{" + num_str + "}{" + den_str + "}"
                # temp = [num_str,den_str]
                frac_list[now] = temp
                return ret
            elif node.macroname == 'sqrt':
                sqrt_latex = node.nodeargd.argnlist
                ret_str = "\\sqrt"
                for sqrt_node in sqrt_latex:
                    if sqrt_node == None:
                        continue
                    ret_str += traverse_node(sqrt_node,frac_list)
                return ret_str
            else:
                return node.latex_verbatim()
        else:
            return node.latex_verbatim()

    for node in nodes:
        modified_str += traverse_node(node,latex_list) # 만들어진 node를 각각 순회하면서 분수를 찾고, 대체한다.
    return modified_str,dict(sorted(latex_list.items())) # 수정된 Latex와 분수 목록을 반환한다.

def fraction_extractor(json_dict: dict) -> dict:
    ret_dict = {}
    for latex_idx,latex_val in json_dict.items():
        global idx
        idx = 1
        
        modified,listed = fraction_parser(latex_val["Origin"])
        frac_list = {}
        dict_val = {"Origin" : modified}
        frac_list.update(listed)
        if "Inequal_list" in latex_val:
            
            for ie_idx,ie_val in latex_val["Inequal_list"].items():
                ie_mod,ie_list = fraction_parser(ie_val)
                latex_val["Inequal_list"][ie_idx] = ie_mod
                frac_list.update(ie_list)
            dict_val["Inequal_list"] = latex_val["Inequal_list"]

        new_dict = {}
        if frac_list:
            for key3,val3 in frac_list.items():
                new_dict[f"[FRAC {key3}]"] = val3
            dict_val["Frac_list"] = new_dict
        ret_dict[latex_idx] = dict_val
    return ret_dict

################################################################

def parse_latex(seperated_latex: dict) -> tuple[dict,str,str]:
    cp_latex = copy.deepcopy(seperated_latex)

    if cp_latex is None: return None,None,None
    
    Question, File = None, None
    
    if cp_latex["Question"]: Question = cp_latex["Question"]
    if cp_latex["File"]: File = cp_latex["File"]

    inequality_parsed = inequality_extractor(cp_latex) # first, parse inequality.
    inequality_fraction_parsed = fraction_extractor(inequality_parsed) # second, parse fraction.


    # if is_debug:
    #     print("PARSED!!!!!!!!!!!!!!!!!!!!!!!")
    #     print(json.dumps(inequality_fraction_parsed,indent=4,ensure_ascii=False))
    #     print("\n")

    return inequality_fraction_parsed,Question,File