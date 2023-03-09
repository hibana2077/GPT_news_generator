
import streamlit as st
import openai

def usage_info_plot(usage:dict):
    import plotly.express as px
    completion_tokens,prompt_tokens = usage["completion_tokens"],usage["prompt_tokens"]
    fig = px.pie(values=[completion_tokens,prompt_tokens],names=["completion_tokens","prompt_tokens"])
    return fig

def get_news(api_key,message,model = "gpt-3.5-turbo"):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        api_key = api_key,
        model = model,
        messages = message)
    return (response.choices[0]["message"]["content"],response.usage)

def main_page():
    st.title("GPT-3.5-turbo News Generator")
    st.write("This is a simple web app that uses gpt-3.5-turbo to generate news content.")
    st.write("It's a demo of what you can do with gpt-3.5-turbo.")
    st.write("The code is available on [GitHub](https://github.com/hibana2077/GPT_news_generator).")

def generate_news_page():
    st.title("Generate News")
    openai_API_key = st.text_input("OpenAI API Key", type="password")
    language = st.selectbox("Language", ["english", "chinese"])
    if language == "english":
        news_category = st.selectbox("News Category", ["World", "Business", "Technology", "Entertainment", "Sports", "Science", "Health"])
        Key_words = st.text_input("Key words")
        news_length = st.slider("News Length (words)", 100, 1000, 500, 35)
        some_text = st.text_input("Some Text")
        if st.button("Generate News"):
            message = [
                {"role": "prompt", "content": f"News Category: {news_category}"},
                {"role": "prompt", "content": f"Key words: {Key_words}"},
                {"role": "prompt", "content": f"News Length: {news_length}"},
                {"role": "prompt", "content": f"Some Text: {some_text}"},
                {"role": "system", "content": "Please generate news using the above information."},
                {"role": "system", "content": "return text can use markdown."}
            ]
            news = get_news(api_key=openai_API_key, message=message,model="gpt-3.5-turbo")
            st.write(news)
            st.markdown("---")
            st.write("Usage Info:")
            st.plotly_chart(usage_info_plot(news[1]))
            st.write(f"Article cost: {(news[1]['completion_tokens']/1000)*0.002:.6f} USD")
    elif language == "chinese":
        news_category = st.selectbox("News Category", ["國際", "國內", "財經", "科技", "娛樂", "體育", "軍事", "社會"])
        Key_words = st.text_input("關鍵詞")
        news_length = st.slider("新聞長度 (字)", 100, 1000, 500, 35)
        title = st.text_input("標題")
        if st.button("生成新聞"):
            message = [
                {"role": "system", "content": f"新聞類別: {news_category}"},
                {"role": "system", "content": f"關鍵詞: {Key_words}"},
                {"role": "system", "content": f"新聞長度: {news_length}"},
                {"role": "system", "content": f"標題: {title}"},
                {"role": "system", "content": "請使用上述信息生成新聞。"},
                {"role": "system", "content": "返回的文本可以使用markdown。回傳時標題請用標題格式。"}
            ]
            news = get_news(api_key=openai_API_key, message=message,model="gpt-3.5-turbo")
            st.write(news[0])
            #usage info
            st.markdown("---")
            st.write("花費資訊:")
            st.plotly_chart(usage_info_plot(news[1]))
            st.write(f"文章生成成本: {(news[1]['completion_tokens']/1000)*0.002:.6f} USD")
            

pages = {
    "Main": main_page,
    "Generate News": generate_news_page,
}

if __name__ == "__main__":
    page = st.sidebar.selectbox("Choose a page", ["Main", "Generate News"])
    pages[page]()