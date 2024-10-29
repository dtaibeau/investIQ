import streamlit as st
import streamlit.components.v1 as components
from app.services.twitter_service import fetch_tweets_from_user
from app.services.openai_service import generate_ai_summary, SummaryOutput
from pydantic import ValidationError


def json_to_html(llm_output: SummaryOutput) -> str:
    html = "<html><head><style>"
    html += """
    body {
        font-family: Arial, sans-serif;
        color: white;
        padding: 15px;
    }
    .trend {
        margin-bottom: 10px;
        font-size: 1.2em;
        font-weight: bold;
    }
    .investment_opportunities {
        margin-top: 5px;
        color: white;
    }
    """
    html += "</style></head><body>"
    html += "<div class='transcript'>"

    # trend
    html += f"<div class='trend'>Trend: {llm_output.trend}</div>"

    # investment opportunities
    html += "<div class='investment_opportunities'>Investment Opportunities:</div>"
    html += "<ul>"
    for opportunity in llm_output.investment_opportunities:
        html += f"<li>{opportunity}</li>"
    html += "</ul>"

    # Close the HTML tags
    html += "</div></body></html>"

    return html

def main():
    st.title("InvestIQ: AI-powered Investment Insights")
    username = st.text_input("Twitter Username", value="KiteVC", help="Enter the Twitter handle without '@'")
    num_tweets = st.slider("Number of Tweets", 1, 50, 10)

    if st.button("Fetch and Analyze Tweets"):
        st.write("Fetching tweets...")

        tweets = fetch_tweets_from_user(username, count=num_tweets)

        if tweets:
            st.write("Analyzing for potential investment opportunities...")
            llm_output_raw = generate_ai_summary(tweets)

            try:
                # convert the raw output to a SummaryOutput instance
                llm_output = SummaryOutput.parse_obj(llm_output_raw)

                # convert to HTML and display
                html_output = json_to_html(llm_output)
                components.html(html_output, height=400, scrolling=True)

            except ValidationError as e:
                st.error(f"Failed to parse AI summary: {e}")
        else:
            st.error("Failed to fetch tweets. Check the username or API credentials.")


if __name__ == "__main__":
    main()
