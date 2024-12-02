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

    2. **위험 수준 평가** (위험 수준 숫자가 높을수록 위험도가 높음)
    - 위험 요소 1: [위험 수준 (1/2/3/4/5)] - [평가 이유]
    - 위험 요소 2: [위험 수준 (1/2/3/4/5)] - [평가 이유]
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
    - `riskLevel`: A string indicating the severity of the identified risk. Choose one of the following predefined levels: 1 to 5 (where 1 represents the lowest risk and 5 represents the highest risk).  
    - `content`: A nested object containing detailed information about the identified risk and its management. It should include:  
     - `potentialRisk`: A string representing the type of potential risk. Choose one of the following predefined categories:  
        [`가스중독 및 질식`, `감전`, `교통`, `기타`, `낙하 및 비래`, `무리한동작`, `베임`, `붕괴 및 도괴`, `업무상질병`, `유해물접촉`, `이상온도접촉`, `전도`, `찔림`, `추락`, `충돌 및 격돌`, `파열`, `폭발`, `협착`, `화재`]
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
                "type": "integer",
                "enum": [1, 2, 3, 4, 5],
                "description": "The risk assessment level, where 1 represents the lowest risk and 5 represents the highest risk."
              }},
              "content": {{
                "type": "object",
                "properties": {{
                  "potentialRisk": {{
                    "type": "string",
                    "enum": ['가스중독 및 질식', '감전', '교통', '기타', '낙하 및 비래', '무리한동작', 
                       '베임', '붕괴 및 도괴', '업무상질병', '유해물접촉', '이상온도접촉', '전도', 
                       '찔림', '추락', '충돌 및 격돌', '파열', '폭발', '협착', '화재'],
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
                "required": ["potentialRisk", "simulation"],
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
                        "type": "integer",
                        "enum": [1, 2, 3, 4, 5],
                        "description": "The risk assessment level, where 1 represents the lowest risk and 5 represents the highest risk."
                    }},
                    "content": {{
                        "type": "object",
                        "description": "Detailed content about the risk.",
                        "properties": {{
                            "potentialRisk": {{
                                "type": "string",
                                "description": "The identified potential risk.",
                                "enum": ['가스중독 및 질식', '감전', '교통', '기타', '낙하 및 비래', '무리한동작', 
                                            '베임', '붕괴 및 도괴', '업무상질병', '유해물접촉', '이상온도접촉', '전도', 
                                            '찔림', '추락', '충돌 및 격돌', '파열', '폭발', '협착', '화재']
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
                    "manager": {{
                        "type": "array",
                        "description": "List of managers associated with the risk.",
                        "items": {{
                            "type": "object",
                            "properties": {{
                                "name": {{
                                    "type": "string",
                                    "description": "Name of the manager."
                                }},
                                "department": {{
                                    "type": "string",
                                    "description": "Department of the manager."
                                }},
                                "contact": {{
                                    "type": "string",
                                    "description": "Contact information of the manager."
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
                                "document_summary": {{
                                    "type": "string",
                                    "description": "Summary of the document."
                                }}
                            }},
                            "required": ["title", "document_summary"]
                        }}
                    }}
                }},
                "required": ["index", "riskLevel", "content", "keywords", "manager", "documents"]
            }},
            ...
        }}
        ]
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
                                    "type": "integer",
                                    "enum": [1, 2, 3, 4, 5],
                                    "description": "The risk assessment level, where 1 represents the lowest risk and 5 represents the highest risk."
                                },
                                "content": {
                                    "type": "object",
                                    "properties": {
                                        "potentialRisk": {
                                            "type": "string",
                                            "enum": ['가스중독 및 질식', '감전', '교통', '기타', '낙하 및 비래', '무리한동작', 
                                                        '베임', '붕괴 및 도괴', '업무상질병', '유해물접촉', '이상온도접촉', '전도', 
                                                        '찔림', '추락', '충돌 및 격돌', '파열', '폭발', '협착', '화재'],
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
                                    "required": ["potentialRisk", "simulation"],
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
                                    "type": "integer",
                                    "enum": [1, 2, 3, 4, 5],
                                    "description": "The risk assessment level, where 1 represents the lowest risk and 5 represents the highest risk."
                                },
                                "content": {
                                    "type": "object",
                                    "description": "Detailed content about the risk.",
                                    "properties": {
                                        "potentialRisk": {
                                            "type": "string",
                                            "description": "The identified potential risk.",
                                            "enum": ['가스중독 및 질식', '감전', '교통', '기타', '낙하 및 비래', '무리한동작', 
                                                        '베임', '붕괴 및 도괴', '업무상질병', '유해물접촉', '이상온도접촉', '전도', 
                                                        '찔림', '추락', '충돌 및 격돌', '파열', '폭발', '협착', '화재']
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
                                "manager": {
                                    "type": "array",
                                    "description": "List of managers associated with the risk.",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {
                                                "type": "string",
                                                "description": "Name of the manager."
                                            },
                                            "department": {
                                                "type": "string",
                                                "description": "Department of the manager."
                                            },
                                            "contact": {
                                                "type": "string",
                                                "description": "Contact information of the manager."
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
                                            "document_summary": {
                                                "type": "string",
                                                "description": "Summary of the document."
                                            }
                                        },
                                        "required": ["title", "document_summary"]
                                    }
                                }
                            },
                            "required": ["index", "riskLevel", "content", "keywords", "manager", "documents"]
                        }
                    }
                },
                "required": ["risks"]
            }
        }
    }

}
