from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

def create_llm_chain():
    GROQ_API_KEY = "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"
    
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="gemma-7b-it",
        temperature=0.5,
        max_tokens=500
    )
    prompt_template = PromptTemplate(
        input_variables=["question"],
        template="""
        **Question:** {question}
        


        **Guidelines for Answer:**
        - **Accuracy:** Ensure that all information provided is medically accurate and up-to-date.
        - **Clarity:** Explain complex medical terms in simple language that patients can easily understand.
        - **Patient Focus:** Tailor your response to prioritize patient safety and understanding. Provide clear instructions or advice where applicable.

        **Final Answer:**
        Please generate a response that combines the detailed medical information, relevant research insights, and patient-friendly advice based on the information provided above. Include information about the Ayurvedic plants in the composition and suggest an alternative medicine or treatment option at the end of your response. Ensure that the response is accurate, clear, and patient-focused. 
        """
    )

    return LLMChain(llm=llm, prompt=prompt_template)


# import json

# def create_health_chain():
#     GROQ_API_KEY = "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"
    
#     llm = ChatGroq(
#         groq_api_key=GROQ_API_KEY,
#         model_name="gemma-7b-it",
#         temperature=0.5,
#         max_tokens=500
#     )
#     prompt_template = PromptTemplate(
#         input_variables=["question"],
#         template="""
#         **Question:** {question}

#         **Guidelines:**
#         - Ensure medical accuracy
#         - Explain complex terms simply
#         - Prioritize patient safety and understanding
#         - Provide detailed info and summary
#         - Maintain professional, empathetic tone

#         **Final Answer:** {{"Disease": "Provide a concise, medically accurate response about diseases.", 
#                         "Description": "Provide a concise, medically accurate description.",
#                         "Precaution": "Provide a concise, medically accurate precaution.",
#                         "Medications": "Provide a concise, medically accurate response about medications.",
#                         "Workouts": "Provide a concise, medically accurate response about workouts."}}
#         """
#     )

#     llm_chain = LLMChain(llm=llm, prompt=prompt_template)
    
#     def run():
#         response_str = llm_chain.run({"question": "health insights"})
#         print(response_str)
#         response = json.loads(response_str)

#         disease = response["Disease"]
#         description = response["Description"] 
#         precaution = response["Precaution"]
#         medications = response["Medications"]
#         workouts = response["Workouts"]

#         return disease, description, precaution, medications, workouts

#     return run

# if __name__ == "__main__":
#     health_chain = create_health_chain()
#     disease, description, precaution, medications, workouts = health_chain()
#     print("Disease:", disease)
#     print("Description:", description)
#     print("Precaution:", precaution)
#     print("Medications:", medications)
#     print("Workouts:", workouts)

# if __name__ == "__main__":
#     llm_chain = create_llm_chain()
#     print(llm_chain.run("What is the medicine for fever?"))

