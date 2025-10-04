import streamlit as st
from newspaper import Article
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Streamlit app title and input box
st.title("News Summarization")
url = st.text_input("Paste a news article URL")

# Button and article fetching
if st.button("Summarize"):
    if url:
        try:
            article = Article(url)
            article.download()
            article.parse()
            text = article.text
            author = article.authors
            publish_date = article.publish_date
            title = article.title

            # Print details
            st.subheader("Article Details:")
            st.write("Article Name:", title if title else "No title")
            st.write("Author(s):", ", ".join(author) if author else "No author")
            st.write("Publish Date:", publish_date if publish_date else "No publish date")

            # Print original article
            st.subheader("Original Article:")
            st.write(text[:1000] + "...")

            # Extractive summary generation
            if len(text.split()) > 50:
                parser = PlaintextParser.from_string(text, Tokenizer("english"))
                summarizer = LsaSummarizer()
                summary_sentences = summarizer(parser.document, 3)
                summary = " ".join(str(sentence) for sentence in summary_sentences)

                st.subheader("Summary of Article:")
                st.write(summary)
            else:
                st.warning("This article is too short to summarize!")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid URL")
