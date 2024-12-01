# prompts_and_tools.py

# OpenAI API를 사용할 때 공통적으로 활용되는 시스템 프롬프트
SYSTEM_PROMPTS = {
    "analyze_image_risks": """
You are an expert with a PhD-level knowledge in "industrial safety" and "risk assessment."

**Task**: Analyze the provided image and generate a comprehensive safety risk analysis report based on the following criteria:

**Requirements**:
1. **Risk Elements Identification**: Identify all potential risk elements visible in the image. For example, "slippery surface," "worker operating at height," etc. Provide a detailed description for each.
2. **Risk Level Assessment**: Assess how dangerous each risk element is by categorizing it as "Critical/High/Medium/Low" and briefly explain the reasoning for each classification.  
   - **Critical**: A situation where an accident or injury is imminent and could occur immediately.  
   - **High**: A situation where an accident or injury is likely to occur in the near future.  
   - **Medium**: A situation where there is a 50% probability of an accident occurring.  
   - **Low**: A situation where an accident is unlikely but still possible under rare circumstances.  
3. **Risk Scenario Simulation**: Simulate potential accidents or incidents that could occur due to the identified risk elements. For example, "A worker might slip on the wet surface and sustain injuries."
4. **Mitigation Measures**: Propose specific safety measures or actions to address each identified risk. For example, "Slippery surface: Install anti-slip mats or place warning signs."

**Output Format**:
The output should follow the structure below:

### Risk Analysis Report

1. **Risk Elements**
   - Risk Element 1: [Description of the risk element]
   - Risk Element 2: [Description of the risk element]
   ...

2. **Risk Level Assessment**
   - Risk Element 1: [Risk Level (Critical/High/Medium/Low)] - [Reason for the assessment]
   - Risk Element 2: [Risk Level (Critical/High/Medium/Low)] - [Reason for the assessment]
   ...

3. **Risk Scenario Simulation**
   - Risk Element 1: [Simulation of potential accidents or incidents]
   - Risk Element 2: [Simulation of potential accidents or incidents]
   ...

4. **Mitigation Measures**
   - Risk Element 1: [Proposed mitigation measures]
   - Risk Element 2: [Proposed mitigation measures]
   ...
""",

    "format_risk_as_json": """
    You are a highly skilled assistant specializing in converting plain-text risk analysis into a structured JSON format.
    Your task is to interpret the provided text, extract potential risks and their corresponding safety improvement recommendations, and assign a relevant category to each risk.
    Focus on clarity, accuracy, and adherence to the specified schema while ignoring irrelevant information.
    """,

    "retrieve_information": """
    You are a highly skilled assistant specializing in summarizing structured risk analysis data.
    Your task is to take a structured JSON array containing risk analysis and recommendations, along with personnel information, and generate a concise summary.
    The summary must include:
    1. A bulleted list of the key risks.
    2. A section labeled 'Related Personnel Information' and 'Related Document Information' with details provided in the additional input.
    The entire response must be written in Korean.
    """
}

# 사용자 프롬프트를 모아둔 딕셔너리
USER_PROMPTS = {
    "analyze_image_risks": """
## Instruction
The following is an image captured at a POSCO steel manufacturing site in South Korea. Your task is to:
1. Analyze the image and identify three potential safety hazards.
2. For each hazard:
   - Identify the hazard.
   - Assess the risk level.
   - Simulate potential accident scenarios related to the hazard.
   - Suggest actionable recommendations for improving safety related to that hazard.
3. Write all of your analysis **in Korean**.

### Example Output Structure:
```
### 위험성 분석 레포트

1. **위험 요소**
   - 위험 요소 1: [위험 요소에 대한 설명]
   - 위험 요소 2: [위험 요소에 대한 설명]
   ...

2. **위험 수준 평가**
   - 위험 요소 1: [위험 수준 (최상/상/중/하)] - [평가 이유]
   - 위험 요소 2: [위험 수준 (최상/상/중/하)] - [평가 이유]
   ...

3. **위험 상황 시뮬레이션**
   - 위험 요소 1: [발생 가능한 사고나 상황에 대한 시뮬레이션]
   - 위험 요소 2: [발생 가능한 사고나 상황에 대한 시뮬레이션]
   ...

4. **조치 방법**
   - 위험 요소 1: [제안된 조치 방법]
   - 위험 요소 2: [제안된 조치 방법]
   ...

```

### Input:
The image is provided as a Base64-encoded string.

Please analyze this image and provide your response strictly in Korean using the specified Markdown format.
""",

    "format_risk_as_json": """
    ## Instruction  
The following task involves organizing information into a **structured JSON format** based on the provided schema. Each entry in the array should include the following fields and adhere to these guidelines:  

- `index`: An integer that serves as a unique identifier for each entry.  
- `riskLevel`: A string indicating the severity of the identified risk. Choose one of the following predefined levels: `최상`, `상`, `중`, `하`.  
- `content`: A nested object containing detailed information about the identified risk and its management. It should include:  
  - `potentialRisk`: A string representing the type of potential risk. Choose one of the following predefined categories:  
    `화재`, `폭발`, `추락`, `전도`, `기계압착`, `충돌`, `화학중독`, `화학흡입`, `낙하물`, `전기 감전`, `고온 화상`.  
  - `mitigationPlan`: A string providing a proposed plan to mitigate or address the identified risk.  
  - `simulation`: A string detailing the simulation performed to evaluate or address the risk. Include the method used, conditions simulated, expected outcomes, and any relevant observations.  
- `keywords`: An array of exactly three strings, extracted from the content, that represent key terms for search and indexing purposes. These should include significant terms such as the potential risk, key elements of the mitigation plan, and notable points from the simulation.  
    
    ### Key Usage:
    1. **Risk Field**:
        - Extract the description of each identified risk.
        - Ensure the description is concise and retains the essential information about the risk.
    2. **Recommendation Field**:
        - Extract the safety improvement recommendation corresponding to each risk.
        - Ensure recommendations are actionable, clear, and contextually relevant to the identified risk.
    3. **Category Field**:
        - Assign one of the specified categories to each risk based on its nature.
        - Choose the category that most closely aligns with the risk description.
    
    ### Output Schema:
    [
        {{
          "type": "array",
          "items": {{
            "type": "object",
            "properties": {{
              "index": {{
                "type": "integer",
                "description": "Each item's unique identifier."
              }},
              "riskLevel": {{
                "type": "string",
                "enum": ["최상", "상", "중", "하"],
                "description": "The risk assessment level, indicating the severity of the potential issue."
              }},
              "content": {{
                "type": "object",
                "properties": {{
                  "potentialRisk": {{
                    "type": "string",
                    "enum": ["화재", "폭발", "추락", "전도", "기계압착", "충돌", "화학중독", "화학흡입", "낙하물", "전기 감전", "고온 화상"],
                    "description": "The type of potential risk. Choose one of the predefined categories."
                  }},
                  "mitigationPlan": {{
                    "type": "string",
                    "description": "The proposed plan to mitigate or address the identified risk."
                  }},
                  "simulation": {{
                    "type": "string",
                    "description": "Provide a detailed account of the simulations performed. Include the method used, conditions simulated, expected outcomes, and any relevant observations."
                  }}
                }},
                "required": ["potentialRisk", "mitigationPlan", "simulation"],
                "description": "A nested object containing detailed information about risks and their management."
              }},
              "keywords": {{
                "type": "array",
                "items": {{
                  "type": "string"
                }},
                "description": "A list of keywords extracted from the content for search and indexing purposes. Keywords should include significant terms such as the potential risk, key elements of the mitigation plan, and notable points from the simulation. Write exactly 3 keywords. "
              }}
            }},
            "required": ["index", "riskLevel", "content", "keywords"],
            "description": "An array of objects where each object represents a risk evaluation entry."
          }}
          ...
        }}
    ]
    """,

    "retrieve_information":"""
    ## Instruction
    The following is a structured JSON array containing analyzed risks and recommendations. Summarize this information using the specified format.

    ## Personnel and Document Information
    The following is a list of personnel responsible for various tasks and related documents. Use this information to complete the 'Related Personnel and Document Information' section of the summary:
    
    ### 분야별 담당자 정보
| 분야          | 담당 부서            | 담당자    | 연락처         |
|---------------|---------------------|-----------|----------------|
| 화재          | 포스코 디지털혁신실 | 석화재    | 010-1234-5678 |
| 폭발          | 포스코 (포항)냉연부 | 윤폭발    | 010-2345-6789 |
| 추락          | 포스코 (포항)열연부 | 홍추락    | 010-3456-7890 |
| 전도          | 포스코스틸리온      | 이전도    | 010-4567-8901 |
| 기계압착      | 포스코 디지털혁신실 | 장기계   | 010-5678-9012 |
| 충돌          | 포스코 (포항)냉연부 | 윤충돌    | 010-6789-0123 |
| 화학중독      | 포스코 (포항)열연부 | 홍중독    | 010-7890-1234 |
| 화학흡입      | 포스코스틸리온      | 이흡입    | 010-8901-2345 |
| 낙하물        | 포스코 디지털혁신실 | 장낙하    | 010-9012-3456 |
| 전기 감전     | 포스코 (포항)냉연부 | 윤감전    | 010-0123-4567 |
| 고온 화상     | 포스코 (포항)열연부 | 홍화상    | 010-1234-6789 |

    ### 관련 문서 정보
| 인덱스 | 문서명                                                   |
| ------ | ------------------------------------------------------ |
| 1      | 철도안전법(법률)                                      |
| 2      | 철도안전법 시행규칙(국토교통부령)                     |
| 3      | 철도안전법 시행령(대통령령)                          |
| 4      | 폐기물관리법(법률)                                   |
| 5      | 폐기물관리법 시행령(대통령령)                        |
| 6      | 항만안전특별법 시행령(대통령령)                      |
| 7      | 항만안전특별법 시행규칙(해양수산부령)                |
| 8      | 폐기물관리법 시행규칙(환경부령)                      |
| 9      | 항만안전특별법(법률)                                 |
| 10     | 화학물질관리법 시행규칙(환경부령)                    |
| 11     | 환경오염시설의 통합관리에 관한 법률 시행규칙(환경부령)|
| 12     | 화학물질관리법(법률)                                 |
| 13     | 환경오염시설의 통합관리에 관한 법률(법률)            |
| 14     | 화학물질관리법 시행령(대통령령)                      |
| 15     | 환경오염시설의 통합관리에 관한 법률 시행령(대통령령) |
| 16     | 원자력안전법 시행규칙(총리령)                        |
| 17     | 연구실 안전환경 조성에 관한 법률 시행령(대통령령)    |
| 18     | 연구실 안전환경 조성에 관한 법률(법률)              |
| 19     | 연구실 안전환경 조성에 관한 법률 시행규칙(과학기술정보통신부령)|
| 20     | 원자력안전법 시행령(대통령령)                        |
| 21     | 원자력안전법(법률)                                   |
| 22     | 전기안전관리법 시행규칙(산업통상자원부령)            |
| 23     | 에너지이용 합리화법 시행령(대통령령)                |
| 24     | 에너지이용 합리화법(법률)                           |
| 25     | 전기안전관리법 시행령(대통령령)                      |
| 26     | 전기안전관리법(법률)                                 |
| 27     | 에너지이용 합리화법 시행규칙(산업통상자원부령)       |
| 28     | 액화석유가스의 안전관리 및 사업법(법률)             |
| 29     | 시설물의 안전 및 유지관리에 관한 특별법 시행규칙(국토교통부령)|
| 30     | 액화석유가스의 안전관리 및 사업법 시행령(대통령령)  |
| 31     | 시설물의 안전 및 유지관리에 관한 특별법(법률)       |
| 32     | 액화석유가스의 안전관리 및 사업법 시행규칙(산업통상자원부령)|
| 33     | 시설물의 안전 및 유지관리에 관한 특별법 시행령(대통령령)|
| 34     | 소방시설 설치 및 관리에 관한 법률(법률)             |
| 35     | 생활주변방사선 안전관리법 시행규칙(총리령)          |
| 36     | 생활주변방사선 안전관리법 시행령(대통령령)          |
| 37     | 소방시설 설치 및 관리에 관한 법률 시행규칙(행정안전부령)|
| 38     | 생활주변방사선 안전관리법(법률)                     |
| 39     | 소방시설 설치 및 관리에 관한 법률 시행령(대통령령)  |
| 40     | 소방시설공사업법 시행규칙(행정안전부령)             |
| 41     | 소방시설공사업법 시행령(대통령령)                   |
| 42     | 소방시설공사업법(법률)                              |
| 43     | 도시가스사업법 시행규칙(산업통상자원부령)           |
| 44     | 도시가스사업법(법률)                                |
| 45     | 도시가스사업법 시행령(대통령령)                     |
| 46     | 위험물안전관리법 시행규칙(행정안전부령)             |
| 47     | 산업안전보건법 시행규칙(고용노동부령)               |
| 48     | 산업안전보건법 시행령(대통령령)                     |
| 49     | 화학물질관리법 시행규칙(환경부령)                   |
| 50     | 화학물질관리법 시행령(대통령령)                     |
| 51     | 위험물안전관리법(법률)                              |
| 52     | 화학물질관리법(법률)                                |
| 53     | 산업안전보건법(법률)                                |
| 54     | 위험물안전관리법 시행령(대통령령)                   |
| 55     | 고압가스 안전관리법(법률)                          |
| 56     | 고압가스 안전관리법 시행령(대통령령)                |
| 57     | 중대재해 처벌 등에 관한 법률 시행령(대통령령)       |
| 58     | 중대재해 처벌 등에 관한 법률(법률)                  |

    ### Output Schema:
    [
        {{
            "type": "array",
            "items": {{
                "type": "object",
                "properties": {{
                    "index": {{
                        "type": "integer",
                        "description": "Unique identifier for the risk."
                    }},
                    "riskLevel": {{
                        "type": "string",
                        "description": "Risk severity level.",
                        "enum": ["최상", "상", "중", "하"]
                    }},
                    "content": {{
                        "type": "object",
                        "description": "Detailed content about the risk.",
                        "properties": {{
                            "potentialRisk": {{
                                "type": "string",
                                "description": "The identified potential risk."
                            }},
                            "mitigationPlan": {{
                                "type": "string",
                                "description": "The plan to mitigate the risk."
                            }},
                            "simulation": {{
                                "type": "string",
                                "description": "Simulation scenario of the risk occurrence."
                            }}
                        }},
                        "required": ["potentialRisk", "mitigationPlan", "simulation"]
                    }},
                    "keywords": {{
                        "type": "array",
                        "description": "List of keywords related to the risk.",
                        "items": {{
                            "type": "string"
                        }}
                    }},
                    "personnel": {{
                        "type": "array",
                        "description": "List of personnel associated with the risk.",
                        "items": {{
                            "type": "object",
                            "properties": {{
                                "name": {{
                                    "type": "string",
                                    "description": "Name of the personnel."
                                }},
                                "department": {{
                                    "type": "string",
                                    "description": "Department of the personnel."
                                }},
                                "contact": {{
                                    "type": "string",
                                    "description": "Contact information of the personnel."
                                }}
                            }},
                            "required": ["name", "department", "contact"]
                        }}
                    }},
                    "documents": {{
                        "type": "array",
                        "description": "List of documents related to the risk.",
                        "items": {{
                            "type": "object",
                            "properties": {{
                                "title": {{
                                    "type": "string",
                                    "description": "Title of the document."
                                }},
                                "document_id": {{
                                    "type": "integer",
                                    "description": "Unique identifier of the document."
                                }}
                            }},
                            "required": ["title", "document_id"]
                        }}
                    }}
                }},
                "required": ["index", "riskLevel", "content", "keywords", "personnel", "documents"]
            }},
            ...
        }}
        ]


    
    ### Input Data:

    """

}

# 도구 정의
TOOLS = {
    "format_risk_as_json": {
        "type": "function",
        "function": {
            "name": "output_risks_json",
            "description": "Converts analyzed risks into a structured JSON format based on the specified schema, including index, riskLevel, content, and keywords.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "index": {
                                    "type": "integer",
                                    "description": "Each item's unique identifier."
                                },
                                "riskLevel": {
                                    "type": "string",
                                    "enum": ["최상", "상", "중", "하"],
                                    "description": "The risk assessment level, indicating the severity of the potential issue."
                                },
                                "content": {
                                    "type": "object",
                                    "properties": {
                                        "potentialRisk": {
                                            "type": "string",
                                            "enum": [
                                                "화재",
                                                "폭발",
                                                "추락",
                                                "전도",
                                                "기계압착",
                                                "충돌",
                                                "화학중독",
                                                "화학흡입",
                                                "낙하물",
                                                "전기 감전",
                                                "고온 화상"
                                            ],
                                            "description": "The type of potential risk. Choose one of the predefined categories."
                                        },
                                        "mitigationPlan": {
                                            "type": "string",
                                            "description": "The proposed plan to mitigate or address the identified risk."
                                        },
                                        "simulation": {
                                            "type": "string",
                                            "description": "Provide a detailed account of the simulations performed. Include the method used, conditions simulated, expected outcomes, and any relevant observations."
                                        }
                                    },
                                    "required": ["potentialRisk", "mitigationPlan", "simulation"],
                                    "description": "A nested object containing detailed information about risks and their management."
                                },
                                "keywords": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                    "description": "A list of keywords extracted from the content for search and indexing purposes. Keywords should include significant terms such as the potential risk, key elements of the mitigation plan, and notable points from the simulation. Write exactly 3 keywords."
                                }
                            },
                            "required": ["index", "riskLevel", "content", "keywords"]
                        }
                    }
                },
                "required": ["data"]
            }
        }
    },
    "retrieve_information": {
        "type": "function",
        "function": {
            "name": "nearmiss_details",
            "description": "Provides detailed information about identified risks, their mitigation plans, related personnel, and associated documents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "risks": {
                        "type": "array",
                        "description": "Array of risks with detailed information, including personnel and document references.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "index": {
                                    "type": "integer",
                                    "description": "Unique identifier for the risk."
                                },
                                "riskLevel": {
                                    "type": "string",
                                    "description": "Risk severity level.",
                                    "enum": ["최상", "상", "중", "하"]
                                },
                                "content": {
                                    "type": "object",
                                    "description": "Detailed content about the risk.",
                                    "properties": {
                                        "potentialRisk": {
                                            "type": "string",
                                            "description": "The identified potential risk."
                                        },
                                        "mitigationPlan": {
                                            "type": "string",
                                            "description": "The plan to mitigate the risk."
                                        },
                                        "simulation": {
                                            "type": "string",
                                            "description": "Simulation scenario of the risk occurrence."
                                        }
                                    },
                                    "required": ["potentialRisk", "mitigationPlan", "simulation"]
                                },
                                "keywords": {
                                    "type": "array",
                                    "description": "List of keywords related to the risk.",
                                    "items": {
                                        "type": "string"
                                    }
                                },
                                "personnel": {
                                    "type": "array",
                                    "description": "List of personnel associated with the risk.",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {
                                                "type": "string",
                                                "description": "Name of the personnel."
                                            },
                                            "department": {
                                                "type": "string",
                                                "description": "Department of the personnel."
                                            },
                                            "contact": {
                                                "type": "string",
                                                "description": "Contact information of the personnel."
                                            }
                                        },
                                        "required": ["name", "department", "contact"]
                                    }
                                },
                                "documents": {
                                    "type": "array",
                                    "description": "List of documents related to the risk.",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "title": {
                                                "type": "string",
                                                "description": "Title of the document."
                                            },
                                            "document_id": {
                                                "type": "integer",
                                                "description": "Unique identifier of the document."
                                            }
                                        },
                                        "required": ["title", "document_id"]
                                    }
                                }
                            },
                            "required": ["index", "riskLevel", "content", "keywords", "personnel", "documents"]
                        }
                    }
                },
                "required": ["risks"]
            }
        }
    }

}
