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
        margin: 20px;
    }
    .title {
        font-size: 1.4em;
        font-weight: bold;
        margin-bottom: 15px; /* Adjusted for more space */
    }
    .trend-text {
        font-style: italic;
        margin-left: 15px;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    .investment-opportunities {
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    ul.opportunities-list {
        list-style-type: disc;
        margin-left: 30px;
        line-height: 1.6;
    }
    li {
        margin-top: 8px;
    }
    """
    html += "</style></head><body>"

    # Add the trend title and text
    html += "<div class='title'>Trend</div>"
    html += f"<div class='trend-text'>{llm_output.trend}</div>"

    # Add the investment opportunities title and list
    html += "<div class='investment-opportunities'>Investment Opportunities</div>"
    html += "<ul class='opportunities-list'>"
    for opportunity in llm_output.investment_opportunities:
        html += f"<li>{opportunity}</li>"
    html += "</ul>"

    # Close the HTML tags
    html += "</body></html>"

    return html



def main():
    st.title("InvestIQ: AI-powered Investment Insights")
    username = st.text_input("Twitter Username",
                             placeholder="Enter a Twitter username",
                             help="Enter the Twitter handle without '@'")
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
