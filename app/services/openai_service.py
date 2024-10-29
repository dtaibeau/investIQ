import os
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class Tweet(BaseModel):
    created_at: str
    text: str


class TweetSummaryRequest(BaseModel):
    tweets: list[Tweet] = Field(..., description="List of tweets to summarize")


class SummaryOutput(BaseModel):
    trend: str = Field(..., description="Overall trend identified from tweets.")
    investment_opportunities: list[str] = Field(..., description="Investment opportunities based on the trend.")


def generate_ai_summary(tweets):
    tweet_objects = [
        Tweet(
            created_at=tweet["created_at"].isoformat() if tweet["created_at"] else "Unknown",
            text=tweet["text"]
        )
        for tweet in tweets
    ]

    # extract text from tweet objects
    tweet_texts = [tweet.text for tweet in tweet_objects]

    prompt_template = PromptTemplate.from_template(
        """You are given a list of tweets, and your task is to identify and analyze the different trends,
         and provide insight into what investment opportunities may be most ideal based on the trends analyzed.

        Tweets:
        {tweets}

        Provide the output in JSON format with two keys:
        - 'trend': A string describing the overall trend.
        - 'investment_opportunities': A list of strings describing potential investment opportunities.
        """
    )

    llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)
    # parser = PydanticOutputParser(pydantic_object=SummaryOutput)
    structured_llm = llm.with_structured_output(SummaryOutput, method="json_mode")
    chain = prompt_template | structured_llm

    try:
        summary_output = chain.invoke({"tweets": tweet_texts})

        if isinstance(summary_output, SummaryOutput):
            return summary_output.model_dump()
        else:
            raise ValueError("Unexpected output format from the LLM chain.")

    except Exception as e:
        print(f"Error generating AI summary: {e}")
        return None

