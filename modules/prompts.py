latex2kor_sys = """
당신은 LateX로 쓰인 수식을 한국어로 번역하는 역할을 수행해야 합니다. LaTeX에 영어나 기호가 포함되지 않게 모두 한국어로 바꾸어주세요.
숫자 역시 한국어로 음독해야합니다. 예를 들어, '12'는 '십이'로 번역되어야 합니다.
LaTeX의 중간에 [FRAC X]와 [INEQUAL X]의 키워드가 들어있을 수 있습니다. 여기서 X는 숫자를 의미합니다.
[FRAC X]는 어떤 분수를 나타내며, [INEQUAL X]는 어떤 부등식을 나타냅니다. 
이들은 절대 한국어로 음독하지 말고 그대로 두어야 합니다. 읽을 때는 각각 분수나 부등식이 들어있다고 가정하고 자연스럽게 읽으십시오.
특히 부등식을 나타내는 [INEQUAL X]는, 부등식이 문맥에 따라 읽는 법이 달라질 수 있으므로, 유의하여 주십시오.
"""

latex2kor_usr1 = """
\\begin{cases} x+2 & ([INEQUAL 1]) \\\\ x-4 & ([INEQUAL 2]) \\end{cases}
"""
latex2kor_ass1 = """
[INEQUAL 1]일 때 엑스 더하기 이, [INEQUAL 2]일 때 엑스 빼기 사
"""

latex2kor_usr2 = """
[FRAC 1] = x^2 + 2x + 2 + 10^3 + 10^{e\\sin x}
"""
latex2kor_ass2 = """
[FRAC 1]은 엑스제곱 더하기 이엑스 더하기 이 더하기 십의 세제곱 더하기 십의 이사인엑스제곱
"""

latex2kor_usr3 = """
[FRAC 1]\\int_{0}^{[FRAC 2]y}f(x)dx
"""
latex2kor_ass3 = """
[FRAC 1] 적분 영에서 [FRAC 2]까지 에프엑스 디엑스
"""

latex2kor_usr4 = """
\\overline{AC} = \\overline{BD}
"""
latex2kor_ass4 = """
선분 에이씨는 선분 비디
"""

latex2kor_usr5 = """
V(\\overline{X}) = P([INEQUAL 1])
"""
latex2kor_ass5 = """
브이 엑스 바는 [INEQUAL 1]일 때 피
"""

latex2kor_usr6 = """
Q(x) = \\{1, 2, 3, \\cdots, x\\}
"""
latex2kor_ass6 = """
큐엑스는 집합 일, 이, 삼, 점점점, 엑스
"""

latex2kor_shot = [
    {"role" : "system", "content" : latex2kor_sys},
    {"role" : "user", "content" : latex2kor_usr1},
    {"role" : "assistant", "content" : latex2kor_ass1},
    {"role" : "user", "content" : latex2kor_usr2},
    {"role" : "assistant", "content" : latex2kor_ass2},
    {"role" : "user", "content" : latex2kor_usr3},
    {"role" : "assistant", "content" : latex2kor_ass3},
    {"role" : "user", "content" : latex2kor_usr4},
    {"role" : "assistant", "content" : latex2kor_ass4},
    {"role" : "user", "content" : latex2kor_usr5},
    {"role" : "assistant", "content" : latex2kor_ass5},
    {"role" : "user", "content" : latex2kor_usr6},
    {"role" : "assistant", "content" : latex2kor_ass6}
]

inequal2kor_sys = """
당신은 부등식을 특정부분으로 나누어서 한국어로 음독하는 역할을 수행합니다. 주어지는 과정을 그대로 따라하세요.
먼저, 부등호를 기준으로 구성요소를 나눕니다.
두번째, 부등호를 제외한 구성요소들을 한국어로 음독합니다. 이때 모든 영어, 숫자 및 기호들은 한국어로 변환되어야 합니다.
세번째, 부등호를 한국어로 번역해가면서 식을 다시 재조립합니다. 이때, 부등호가 여러개 있는 식은 부등호 하나하나가 식이 되도록 읽어야 합니다.
예를 들어보겠습니다. '에이', '\\leq' , '엑스', '\\leq', '비'가 주어졌을 때, 부등호는 총 2개입니다.
따라서, 이 식은 '에이는 엑스보다 작거나 같고, 엑스는 비보다 작거나 같다.'로 읽을 수 있습니다. 
요소의 중간에 [FRAC X]와 [INEQUAL X]의 키워드가 들어있을 수 있습니다. 여기서 X는 숫자를 의미합니다.
[FRAC X]는 어떤 분수를 나타내며, [INEQUAL X]는 어떤 부등식을 나타냅니다. 
이들은 절대 한국어로 음독하지 말고 그대로 두어야 하지만, 취급은 분수 및 부등식으로 하십시오.
특히 부등식을 나타내는 [INEQUAL X]는, 부등식이 문맥에 따라 읽는 법이 달라질 수 있으므로, 유의하여 주십시오.
출력 형식은 다음과 같습니다.

#출력 형식#
Components : 
Translated : 
Merged:
"""

inequal2kor_usr1 = """
-2 \\leq x \\leq [FRAC 2]
"""
inequal2kor_ass1 = """
Components : '-2', '\\leq', 'x', '\\leq', '[FRAC 2]'
Translated : '마이너스 이', '\\leq', '엑스', '\\leq', '[FRAC 2]'
Merged : 마이너스 이는 엑스보다 작거나 같고, 엑스는 [FRAC 2]보다 작거나 같다.
"""
inequal2kor_usr2 = """
1 < A < B < C
"""
inequal2kor_ass2 = """
Components : '-1', '<', 'A', '<', 'B', '<', 'C'
Translated : '마이너스 일', '<', '에이', '<', '비', '<', '씨'
Merged : 마이너스 일은 에이보다 작고, 에이는 비보다 작고, 비는 씨보다 작다.
"""
inequal2kor_usr3 = """
2n - \\sqrt{4n^2 + n} \\geq x > 2n + \\sqrt{4n^2 + n}
"""
inequal2kor_ass3 = """
Components : '2n - \\sqrt{4n^2 + n}', '\\geq', 'x', '>', '2n + \\sqrt{4n^2 + n}'
Translated : '이엔 빼기 루트 사엔제곱 더하기 엔', '\\geq', '엑스', '>', '이엔 더하기 루트 사엔제곱 더하기 엔'
Merged : 이엔 빼기 루트 사엔제곱 더하기 엔은 엑스보다 크거나 같고, 엑스는 이엔 더하기 루트 사엔제곱 더하기 엔보다 크다.
"""
inequal2kor_usr4 = """
P([INEQUAL 1]) \\leq X \\leq P([INEQUAL 2])
"""
inequal2kor_ass4 = """
Components : 'P([INEQUAL 1])', '\\leq', 'X', '\\leq', 'P([INEQUAL 2])'
Translated : '[INEQUAL 1]일 때 피', '\\leq', '엑스', '\\leq', '[INEQUAL 2]일 때 피'
Merged : [INEQUAL 1]일 때 피는 엑스보다 작거나 같고, 엑스는 [INEQUAL 2]일 때 피보다 작거나 같다.
"""

inequal2kor_shot = [
    {"role": "system", "content": inequal2kor_sys},
    {"role": "user", "content": inequal2kor_usr1},
    {"role": "assistant", "content": inequal2kor_ass1},
    {"role": "user", "content": inequal2kor_usr2},
    {"role": "assistant", "content": inequal2kor_ass2},
    {"role": "user", "content": inequal2kor_usr3},
    {"role": "assistant", "content": inequal2kor_ass3},
    {"role": "user", "content": inequal2kor_usr4},
    {"role": "assistant", "content": inequal2kor_ass4}
]

frac2kor_sys = """
당신은 분수를 나누어서 한국어로 음독하는 역할을 수행합니다. 주어지는 과정을 그대로 따라하세요.
먼저, 분자와 분모를 식에서 분리해냅니다. 앞의 중괄호에 있는 것이 분자, 뒤의 중괄호에 있는 것이 분모입니다. 이때 분자가 앞, 분모가 뒤에 있도록 배치하십시오.
두번째, 분모와 분자의 자리를 바꿉니다. 이때, 순서는 분모가 앞, 분자가 뒤가 됩니다.
세번째, 분리한 분자와 분모를 한국어로 음독합니다. 이때 모든 영어, 숫자 및 기호들은 한국어로 변환되어야 합니다.
네번째, 두 요소 사이에 " 분의 " 라는 문자를 넣습니다. 
예를 들어보겠습니다. \\frac{x+1}{x+2}에서 분자는 x+1, 분모는 x+2입니다. 
따라서 첫번째 단계 후에는 'x+1', 'x+2'가 될 것입니다.
두번째 단계에서는 자리를 바꾸므로, 'x+2', 'x+1'가 될 것이며, 세번째 단계를 거치면 '엑스 더하기 이', '엑스 더하기 일'이 될 것입니다.
마지막으로, 두 요소 사이에 " 분의 "를 넣어서 엑스 더하기 이 분의 엑스 더하기 일로 읽어서, 출력하면 됩니다.
요소의 중간에 [FRAC X]와 [INEQUAL X]의 키워드가 들어있을 수 있습니다. 여기서 X는 숫자를 의미합니다.
[FRAC X]는 어떤 분수를 나타내며, [INEQUAL X]는 어떤 부등식을 나타냅니다. 
이들은 절대 한국어로 음독하지 말고 그대로 두어야 하며, 음독할 때 취급은 분수 및 부등식으로 하십시오.
특히 부등식을 나타내는 [INEQUAL X]는, 부등식이 문맥에 따라 읽는 법이 달라질 수 있으므로, 유의하여 주십시오.
출력 형식은 다음과 같습니다.

#출력 형식#
Original : 
Components : 
Rearranged : 
Translated : 
Merged:
"""

frac2kor_usr1 = r"""
\frac{743}{234}
"""
frac2kor_ass1 = """
Original : '\\frac{743}{234}'
Components : '743', '234'
Rearranged : '234', '743
Translated : '이백삼십사', '칠백사십삼'
Merged : 이백삼십사 분의 칠백사십삼
"""
frac2kor_usr2 = r"""
\frac{8z^6}{x^c y^9}
"""
frac2kor_ass2 = """
Original : '\\frac{8z^6}{x^c y^9}'
Components : '8z^6', 'x^c y^9'
Rearranged : 'x^c y^9', '8z^6'
Translated : '엑스씨제곱 와이구제곱', '팔제트육제곱'
Merged : 엑스씨제곱 와이구제곱 분의 팔제트육제곱
"""
frac2kor_usr3 = r"""
\frac{[FRAC 2]}{32}
"""
frac2kor_ass3 = """\
Origianl : '\\frac{[FRAC 2]}{32}'
Components : '[FRAC 2]', '32'
Rearranged : '32', '[FRAC 2]'
Translated : '삼십이', '[FRAC 2]'
Merged : 삼십이 분의 [FRAC 2]
"""
frac2kor_usr4 = r"""
\frac{P([INEQUAL 1])}{6}
"""
frac2kor_ass4 = """
Original : '\\frac{P([INEQUAL 1])}{6}'
Components : 'P([INEQUAL 1])', '\\overline{CS}'
Rearranged : '\\overline{CS}', 'P([INEQUAL 1])'
Translated : '선분 씨에스', '[INEQUAL 1]일 때 피' 
Merged : 선분 씨에스 분의 [INEQUAL 1]일 때 피
"""

frac2kor_shot = [
    {"role": "system", "content": frac2kor_sys},
    {"role": "user", "content": frac2kor_usr1},
    {"role": "assistant", "content": frac2kor_ass1},
    {"role": "user", "content": frac2kor_usr2},
    {"role": "assistant", "content": frac2kor_ass2},
    {"role": "user", "content": frac2kor_usr3},
    {"role": "assistant", "content": frac2kor_ass3},
    {"role": "user", "content": frac2kor_usr4},
    {"role": "assistant", "content": frac2kor_ass4}
]

soft_sys = """
당신은 주어진 한국어를 부드럽게 만들어주는 역할을 수행합니다. 주어지는 문자열은 모두 한국어이며, 몇몇 한국어들은 대괄호 안에 있습니다.
이러한 대괄호 안의 문자열들은 제 위치에 잘 찾아갔지만, 앞 뒤의 문장들과 부드럽게 이어지지 않은 상태입니다.
이를 부드럽게 만들어서, 원래 한 문장이었던 것처럼 만들어주세요. 한 문장처럼 만들었다면 대괄호는 지워주세요.
예를 들어, "엑스는 [와이는 칠보다 작거나 같다.]일 때 피보다 크거나 같다."라는 문자열이 있습니다.
이때 같다.일 때는 어색하기 때문에 다음과 같이 바꿀 수 있습니다: "엑스는 와이는 칠보다 작거나 같을 때 피보다 크거나 같다" 
"""
soft_usr1 = """
[엑스는 일보다 작다.]일 때 엑스는 일, [엑스는 이보다 크다.]일 때 에프 엑스는 엑스 더하기 이.
"""
soft_ass1 = """
엑스는 일보다 작을 때 엑스는 일, 엑스는 이보다 클 때 에프 엑스는 엑스 더하기 이.
"""

soft_shot = [
    {"role": "system", "content": soft_sys},
    {"role": "user", "content": soft_usr1},
    {"role": "assistant", "content": soft_ass1}
]

merge_sys = """
당신은 한국어 텍스트를 입력받아, 텍스트를 부드럽게 만들어주는 역할을 수행합니다.
당신에게 주어지는 텍스트는 다음과 같이 생성되었습니다.
먼저, 텍스트에서 수식 부분을 분리합니다. 그리고, 분리한 수식을 한국어로 번역하여 원래 자리에 배치하였습니다.
분리된 라텍스는 텍스트에서 대괄호 사이에 들어가 있으므로 쉽게 구분이 가능합니다. 이들을 앞 뒤의 글자들과 부드럽게 이어지게 만들어서, 원래 한 문장이었던 것처럼 만들어주세요.
예를 들어 보겠습니다. "함수 [와이는 루트 이엑스 더하기 육 빼기 삼]에 대한 다음 설명 중 옳은 것은" 이라는 텍스트에서, [와이는 루트 이엑스 더하기 육 빼기 삼]이 번역된 라텍스라는 것을 알 수 있습니다.
당신이 할 일은, 이러한 라텍스들과 원래 문제 사이의 연결이 어색하지 않게 이를 부드럽게 만들고, 대괄호를 제거하는 것입니다.
어떠한 수식들은 대괄호가 여러번 중첩되어 나타날 수 있습니다. 이때는 안쪽에서 바깥쪽으로 텍스트를 부드럽게 만들면 됩니다.
이 때, 한국어로 된 수식을 다시 변형하지 마십시오. 최종 결과물은 오직 한국어로만 이루어져야 합니다.
"""

merge_shot = [
    {"role": "system", "content": merge_sys},
    {"role": "user", "content": soft_usr1},
    {"role": "assistant", "content": soft_ass1}
]

rag_sys_prompt = """
Context: {context}
Question: {question}
Answer: 당신은 LateX를 한국어로 음독하는 역할을 수행합니다.
위의 Context를 참고하여 Question을 올바르게 한글로 음독해 주세요.
context는 참고만 하고 음독하지 말고, question의 latex(영어 및 수식)만을 한국어로 음독해 주세요.
중간에 [FRAC X] 나 [INEQUAL X]로 되어있는 부분이 존재합니다. 여기서 X는 숫자입니다. 이부분은 한국어로 읽지 말고 그대로 놔두세요.
"""