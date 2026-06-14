import os
from dotenv import load_dotenv
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from app.utils.logger import get_logger

from app.schemas.response_schema import LLMEvaluationOutput

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

def get_output_parser() -> PydanticOutputParser:

    logger.info("getting output parser")

    return PydanticOutputParser(pydantic_object=LLMEvaluationOutput)



def get_format_instructions() -> str:
  
    parser = get_output_parser()

    logger.info("getting parser format")

    return parser.get_format_instructions()

  
async def generate_llm_evaluation(prompt : str) -> str:
    llm = get_llm()
    parser = get_output_parser()

    response = await llm.ainvoke(prompt)
    raw_output = response.content

    try:
        parsed_output = parser.parse(raw_output)
    except OutputParserException as exc:
        raise ValueError(
            "LLM returned output that could not be parsed into the required structure."
        ) from exc

    return parsed_output
   
    