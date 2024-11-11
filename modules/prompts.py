img2latex_sys = """
###지시###
당신은 수학 문제 이미지에서 텍스트를 추출하는 역할을 수행합니다. 이미지가 제공되면 이미지에 들어있는 텍스트를 그대로 반환해주세요.
이미지의 텍스트의 주 언어는 한국어고, 수식을 포함하고 있습니다. 수식에는 영어가 적혀있을 수 있다는 사실을 명심하세요.
수식은 LaTeX로 표현해주세요. 또한 LaTex가 있는 위치에 LaTex를 두지 말고, 그 위치에 LaTeX가 있었다는 사실만 표시하고 LaTeX는 따로 밑에 적어주세요.
LaTeX는 여러개가 될 수 있으며, LaTeX에는 오직 영어, 숫자, 기호만 들어가야 합니다. 한국어는 LaTeX에 포함되면 안됩니다.
한국어가 LaTeX 중간에 끼여있다면, 이를 \\text{}의 형식으로 LaTex에 끼워넣지 말고, LaTeX를 두 부분으로 쪼개서 출력해주세요.
참조해야 할 유의사항과 출력형식은 아래의 텍스트를 참조하세요.

###유의사항###
1. OCR할 때, 문자의 크기에 주의하여 지수인지 판별하세요.
2. 숫자 위에 점이 존재하는 순환소수에서, 점이 정확히 어디 있는지 판별해 주세요. 점은 \\dot{}으로 표시합니다.
3. 루트가 정확히 어디까지 포함하는 판별해 주세요.
4. 문자 두개 위에 바가 존재하는 경우, 선분으로 판별하세요.
5. 분수의 분모와 분자 위치를 유의하세요.

###출력형식###
문제 : ''
Latex_1 : ''
Latex_2 : ''
Latex_3 : ''
"""

img2latex_usr = "이미지는 다음과 같습니다. 이미지에서 텍스트를 추출해주세요."

img2latex_ass_1 = """
Question : [Latex_1]

Latex_1 : '-0.\\dot{7}x^2 + 0.\\dot{1}0\\dot{4}ix + \\int_{2}^{3}xdx = 0'
"""

img2latex_ass_2 = """
Question : [Latex_1]

Latex_1 : '\\overline{AB}:\\overline{ZF} = 4:(3-x)'
"""

img2latex_ass_3 = """
Question : 23. [출제의도] 중복순열의 수를 계산한다
[Latex_1]

Latex_1 : '_{3}P_{2}+_{3}\\Pi_{2} = 3 \\times 2 + 3^2 = 15'
"""

img2latex_ass_4 = """
Question : [Latex_1]에 [Latex_2]을 대입하면 [Latex_3],[Latex_4]
[Latex_5] [Latex_6] 또는 [Latex_7]
따라서 [Latex_8], [Latex_9]이므로
[Latex_10]
또 [Latex_11]에 [Latex_12]을 대입하면 [Latex_13]이므로
[Latex_14]

Latex_1 : 'y = -x^2 + x + 2'
Latex_2 : 'y = 0'
Latex_3 : '-x^2 + x + 2 = 0'
Latex_4 : 'x^2 - x - 2 = 0'
Latex_5 : '(x + 1)(x - 2) = 0'
Latex_6 : '\\therefore x = -1'
Latex_7 : 'x = 2'
Latex_8 : 'A(-1,0)'
Latex_9 : 'B(2,0)'
Latex_10 : '\\overline{AB}=2-(-1)=3'
Latex_11 : 'y = -x^2 + x + 2'
Latex_12 : 'x = 0'
Latex_13 : 'y = 2'
Latex_14 : 'C(0,2)'
"""

img2latex_ass_5 = """
Question : [Latex_1] ㉠
㉠의 양변에 [Latex_2]을 대입하면 [Latex_3],[Latex_4]
㉠의 양변을 [Latex_5]에 대하여 미분하고 [Latex_6]를 대입하면
[Latex_7]이므로
[Latex_8]

Latex_1 : '\\int_{1}^{x}f(t)dt = x^3 - ax + 1 \\quad \\cdots \\cdots'
Latex_2 : 'x = 1'
Latex_3 : '1 - a + 1 = 0'
Latex_4 : 'a = 2'
Latex_5 : 'x'
Latex_6 : 'a = 2'
Latex_7 : 'f(x) = 3x^2 - 2'
Latex_8 : 'f(2) = 12 - 2 = 10'
"""

latex2json_sys = """
###지시###
당신은 주어진 텍스트를 JSON형태의 문자열로 변환시키는 역할을 수행합니다.
텍스트는 구조화 되어 있으며, 콜론을 기준으로 왼쪽은 Attribute, 오른쪽은 값으로 생각하면 됩니다.
이때, Question과 그 값은 JSON에 포함시키지 마십시오. 또한, 대부분의 값은 LaTeX로 이루어진 수식입니다.
이 파일은 바로 JSON으로 변환될 것입니다. 따라서, 역슬래시 같은 특수문자들을 잘 처리해주세요.
입력형식과 출력형식은 다음과 같습니다.

###입력형식###
Question : ''
Latex_1 : ''
Latex_2 : ''
Latex_3 : ''

###출력형식###
{
    "Latex_1" : "",
    "Latex_2" : "",
    "Latex_3" : ""
}
"""

latex2json_usr1 = """
Question : [Latex_1]에 [Latex_2]을 대입하면 [Latex_3],[Latex_4]
[Latex_5] [Latex_6] 또는 [Latex_7]
따라서 [Latex_8], [Latex_9]이므로

Latex_1 : 'y = -x^2 + x + 2'
Latex_2 : 'y = 0'
Latex_3 : '-x^2 + x + 2 = 0'
Latex_4 : 'x^2 - x - 2 = 0'
Latex_5 : '(x + 1)(x - 2) = 0'
Latex_6 : '\\therefore x = -1'
Latex_7 : 'x = 2'
Latex_8 : 'A(-1,0)'
Latex_9 : 'B(2,0)'
"""
latex2json_ass1 = """
{
    "Latex_1" : "y = -x^2 + x + 2",
    "Latex_2" : "y = 0",
    "Latex_3" : "-x^2 + x + 2 = 0",
    "Latex_4" : "x^2 - x - 2 = 0",
    "Latex_5" : "(x + 1)(x - 2) = 0",
    "Latex_6" : "\\therefore x = -1",
    "Latex_7" : "x = 2",
    "Latex_8" : "A(-1,0)",
    "Latex_9" : "B(2,0)"
}
"""

latex2json_usr2 = """
Question : [Latex_1] ㉠
㉠의 양변에 [Latex_2]을 대입하면 [Latex_3],[Latex_4]
㉠의 양변을 [Latex_5]에 대하여 미분하고 [Latex_6]를 대입하면
[Latex_7]이므로
[Latex_8]

Latex_1 : '\\int_{1}^{x}f(t)dt = x^3 - ax + 1 \\quad \\cdots \\cdots'
Latex_2 : 'x = 1'
Latex_3 : '1 - a + 1 = 0'
Latex_4 : 'a = 2'
Latex_5 : 'x'
Latex_6 : 'a = 2'
Latex_7 : 'f(x) = 3x^2 - 2'
Latex_8 : 'f(2) = 12 - 2 = \\frac{1}{2}'
"""

latex2json_ass2 = """
{
    "Latex_1" : "\\int_{1}^{x}f(t)dt = x^3 - ax + 1 \\quad \\cdots \\cdots",
    "Latex_2" : "x = 1",
    "Latex_3" : "1 - a + 1 = 0",
    "Latex_4" : "a = 2",
    "Latex_5" : "x",
    "Latex_6" : "a = 2",
    "Latex_7" : "f(x) = 3x^2 - 2",
    "Latex_8" : "f(2) = 12 - 2 = \\frac{1}{2}"
}
"""

latex2json_shot = [
    {"role": "system", "content": latex2json_sys},
    {"role": "user", "content": latex2json_usr1},
    {"role": "assistant", "content": latex2json_ass1},
    {"role": "user", "content": latex2json_usr2},
    {"role": "assistant", "content": latex2json_ass2}
]

json2kor_sys = """
###지시사항###
당신은 LaTeX로 적힌 수식을 한국어로 번역하는 역할을 수행합니다. 주어지는 텍스트는 JSON 형식으로 이루어진 문자열입니다.
입력에는 여러 Attribute가 있습니다. 이중에서 오직 Attribute가 "1", "3", "5"로만 이루어진 값만 번역하십시오.
LaTeX는 여러개가 주어질 수 있으며, LaTeX에 영어나 기호가 포함되지 않게 한국어로 음독해야 합니다.
숫자 역시 음독하는데, 숫자는 순우리말 대신 한자기반으로 답해주세요. 예를 들어, 1은 '하나'가 아닌 '일'로 번역되어야 합니다.
LaTeX 중간에 [FRAC 번호]로 적힌 것들이 존재합니다. 이러한 것들은 번역하지 말고 그대로 놔두어야 하며, 읽을 때는 하나의 변수로 취급해서 읽어주세요.
그것과 비슷하게 [INEQUAL 번호]로 적힌 것들이 존재합니다. 이들은 실제로는 부등식을 포함하고 있었기에, 이를 하나의 조건으로 생각해서 부드럽게 읽어주세요.
또한, 번역할 때 기존 구조를 반드시 유지해야 합니다. 밑에는 입력형식이 주어집니다.

###입력형식###
{
    {
        "Latex_1": {
            "1": "",
            "frac_list": [
                {
                    "[FRAC 1]": {
                        "OP": "frac",
                        "1": "",
                        "2": ""
                    }
                },
                {
                    "[FRAC 2]": {
                        "OP": "frac",
                        "1": "",
                        "2": ""
                    }
                },
                {
                    "[FRAC 3]": {
                        "OP": "frac",
                        "1": "",
                        "2": ""
                    }
                }
            ],
            "Inequal_list": [
                {
                    "[INEQUAL 1]": {
                        "1": "",
                        "OP1": "",
                        "3": ""
                    }
                }
            ]
        },
        "Latex_2": {
            "1": ""
        }
    },
}
"""

json2kor_usr1 = """
{
    "Latex_1" : {
        "1" : "\\overline{AB} = \\overline{CD}"
    },
    "Latex_2" : {
        "1" : "[FRAC 1] = x^2 + 2x + 2 + 10^3 + 10^{e\\sin x}",
        "frac_list" : [
            {
                "[FRAC 1]" : {
                    "OP" : "frac",
                    "1" : "y+2",
                    "2" : "x+1"
                }
            }
        ]
    },
    "Latex_3" : {
        "1" : "[INEQUAL 1]",
        "Inequal_list" : [
            {
                "[INEQUAL 1]": {
                    "1": "1",
                    "OP1": "<",
                    "3": "x^2 + 2x + 2",
                    "OP2" : "<",
                    "5" : "3"
                }
            }
        ]
    },
    "Latex_4" : {
        "1" : "[FRAC 1]\\int_{0}^{[FRAC 2]y}f(x)dx",
        "frac_list" : [
            {
                "[FRAC 1]" : {
                    "OP" : "frac",
                    "1" : "1",
                    "2" : "3"
                }
            },
            {
                "[FRAC 2]" : {
                    "OP" : "frac",
                    "1" : "5",
                    "2" : "12"
                }
            }
        ]
    },
    "Latex_5" : {
        "1" : "B(2,0)"
    },
    "Latex_6" : {
        "1" : "(x + 1)(x - [FRAC 1]) = 0",
        "frac_list" : [
            {
                "[FRAC 1]" : {
                    "OP" : "frac",
                    "1" : "55",
                    "2" : "78"
                }
            }
        ]
    },
    "Latex_7" : {
        "1" : "_{3}P_{2}+_{3}\\Pi_{2} = 3 \\times 2 + 3^2 = 15"
    },
    "Latex_8" : {
        "1" : "\\begin{cases} x+y = 2 \\\\ 2x - 3y = 4 \\end{cases}"
    },
    "Latex_9" : {
        "1" : "[INEQUAL 1]",
        "Inequal_list" : [
            {
                "[INEQUAL 1]": {
                    "1": "0.\\dot{1} + 0.\\dot{1}0\\dot{1}",
                    "OP1": "\\leq",
                    "3": "0.\\dot{9}\\dot{9}"
                }
            }
        ]
    },
    "Latex_10" : {
        "1" : "\\begin{cases} x+2 & ([INEQUAL 1]) \\\\ x-4 & ([INEQUAL 2]) \\end{cases}",
        "Inequal_list" : [
            {
                "[INEQUAL 1]": {
                    "1": "x",
                    "OP1": "\\geq",
                    "3": "1"
                }
            },
            {
                "[INEQUAL 2]": {
                    "1": "x",
                    "OP1": "<",
                    "3": "1"
                }
            }
        ]
    },
    "Latex_11" : {
        "1" : "P([INEQUAL 1]) = 0.1",
        "Inequal_list" : [
            {
                "[INEQUAL 1]" : {
                    "1" : "X",
                    "OP1" : ">",
                    "2" : "2"
                }
            }
        ]
    }
}
"""

json2kor_ass1 = """
{
    "Latex_1" : {
        "1" : "선분 에이비는 선분 씨디"
    },
    "Latex_2" : {
        "1" : "[FRAC 1]은 엑스제곱 더하기 이엑스 더하기 이 더하기 십의 세제곱 더하기 십의 이사인엑스제곱",
        "frac_list" : [
            {
                "[FRAC 1]" : {
                    "OP" : "frac",
                    "1" : "와이 더하기 이",
                    "2" : "엑스 더하기 일"
                }
            }
        ]
    },
    "Latex_3" : {
        "1" : "[INEQUAL 1]",
        "Inequal_list" : [
            {
                "[INEQUAL 1]": {
                    "1": "일",
                    "OP1": "<",
                    "3": "엑스 제곱 더하기 이엑스 더하기 이",
                    "OP2" : "<",
                    "5" : "삼"
                }
            }
        ]
    },
    "Latex_4" : {
        "1" : "[FRAC 1]인테그랄 영부터 [FRAC 2]와이까지 에프엑스 디엑스",
        "frac_list" : [
            {
                "[FRAC 1]" : {
                    "OP" : "frac",
                    "1" : "일",
                    "2" : "삼"
                }
            },
            {
                "[FRAC 2]" : {
                    "OP" : "frac",
                    "1" : "오",
                    "2" : "십이"
                }
            }
        ]
    },
    "Latex_5" : {
        "1" : "점 비 이 컴마 영"
    },
    "Latex_6" : {
        "1" : "괄호 열고 엑스 더하기 일 괄호 닫고 괄호 열고 엑스 빼기 [FRAC 1] 괄호 닫고는 영",
        "frac_list" : [
            {
                "[FRAC 1]" : {
                    "OP" : "frac",
                    "1" : "오십오",
                    "2" : "칠십팔"
                }
            }
        ]
    },
    "Latex_7" : {
        "1" : "삼 순열 이 더하기 삼 중복순열 이는 삼 곱하기 이 더하기 삼의 제곱은 십오"
    },
    "Latex_8" : {
        "1" : "엑스 더하기 와이는 이, 그리고 이엑스 빼기 삼와이는 사"
    },
    "Latex_9" : {
        "1" : "[INEQUAL 1]",
        "Inequal_list" : [
            {
                "[INEQUAL 1]": {
                    "1": "영 점 순환마디 일 더하기 영 점 순환마디 일영일",
                    "OP1": "\\leq",
                    "3": "영점 순환마디 구구"
                }
            }
        ]
    },
    "Latex_10" : {
        "1" : "[INEQUAL 1]일 때 엑스 더하기 이 그리고 [INEQUAL 2]일 때 엑스 빼기 사",
        "Inequal_list" : [
            {
                "[INEQUAL 1]": {
                    "1": "엑스",
                    "OP1": "\\geq",
                    "3": "일"
                }
            },
            {
                "[INEQUAL 2]": {
                    "1": "엑스",
                    "OP1": "<",
                    "3": "일"
                }
            }
        ]
    },
    "Latex_11" : {
        "1" : "[INEQUAL 1]일 때는 피는 영점 일",
        "Inequal_list" : [
            {
                "[INEQUAL 1]" : {
                    "1" : "엑스",
                    "OP1" : ">",
                    "2" : "이"
                }
            }
        ]
    }
}
"""

json2kor_shot = [
    {"role": "system", "content": json2kor_sys},
    {"role": "user", "content": json2kor_usr1},
    {"role": "assistant", "content": json2kor_ass1}
]

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
당신은 이미지와 텍스트를 입력받아, 텍스트를 이미지를 토대로 부드럽게 만들어주는 역할을 수행합니다.
이미지에는 어떤 수학문제가 한국어로 적혀있습니다.
텍스트는 이 이미지에서 글자들을 추출하여서, 그 중에서 수식들만 한국어로 번역한 뒤 원래 자리에 배치한 형태를 하고 있습니다.
분리된 라텍스는 텍스트에서 '[' 와 ']' 사이에 들어가 있으므로 쉽게 구분이 가능합니다.
예를 들어 보겠습니다. "함수 [와이는 루트 이엑스 더하기 육 빼기 삼]에 대한 다음 설명 중 옳은 것은" 이라는 텍스트에서, [와이는 루트 이엑스 더하기 육 빼기 삼]이 번역된 라텍스라는 것을 알 수 있습니다.
당신이 할 일은, 이러한 라텍스들과 원래 문제 사이의 연결이 어색하지 않게 이를 부드럽게 만들고, 대괄호를 제거하는 것입니다.
어떠한 수식들은 대괄호가 여러번 중첩되어 나타날 수 있습니다. 이때는 안쪽에서 바깥쪽으로 텍스트를 부드럽게 만들면 됩니다.
"""

merge_shot = [
    {"role": "system", "content": merge_sys},
    {"role": "user", "content": soft_usr1},
    {"role": "assistant", "content": soft_ass1}
]