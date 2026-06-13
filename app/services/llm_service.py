import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from app.utils.logger import get_logger

logger = get_logger(__name__)

load_dotenv()

def get_llm() -> ChatGroq:
    api= os.getenv("GROQ_API_KEY")


    model_name= os.getenv("GROQ_MODEL_NAME")

    logger.info("got model name")


    
    if api is None:

        logger.info("inside if")
        raise ValueError("API key not found") 
    
    try:
     
        groq = ChatGroq(
        api_key= api,
        model = model_name,
        temperature = 0.2
        )

        logger.info("groq created")

        return groq
    

    except Exception as e:
        logger.exception(e)
        raise

  
async def generate_llm_evaluation(prompt : str) -> str:
   
    llm = get_llm()
    response = await llm.ainvoke(prompt)

    logger.info("got llm response")

    return response.content