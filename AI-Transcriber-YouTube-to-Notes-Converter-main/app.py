import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript import extract_transcript

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def fetch_transcript(video_id):
    conn = sqlite3.connect('youtube_transcripts.db')
    c = conn.cursor()
    c.execute("SELECT transcript FROM transcripts WHERE video_id = ?", (video_id,))
    transcript_text = c.fetchone()[0]
    conn.close()
    return transcript_text


def generate_notes(transcript_text, subject):
    if subject == "Open-CV":
        prompt = """
            Title: Detailed Physics Notes from YouTube Video Transcript  on OpenCV
            
            Introduction:
                 Briefly introduce the topic of the video and its relevance to opencv.
                
            Key Concepts:
                - Explain each key concept in detail with examples or diagrams where possible.
        
            Algorithm Explanation:
                - Describe how algorithms work step by step. Include any relevant code snippets for step-by-step explanation.   
                - Describe how algorithms work step by step. Provide code snippets for better understanding.    
                
            Code Implementation:
                Provide a code snippet that demonstrates how the algorithm works using pseudocode or actual implementation. 
                Provide a code snippet that demonstrates how the algorithm is implemented using OpenCV library.
                    
            Program :
                Provide a code snippet that demonstrates how the algorithm works using OpenCV library.
                
            Output Analysis:
                 Discuss what is expected from the output of the program.
             
            Limitations/Challenges:
                 Identify any limitations or challenges faced during implementation.
                 How can these be overcome?
        
            Future Work:
                 Suggest areas for future work related to this topic.
        """
            
    elif subject == "Machine learning":
        prompt ="""
                Title: Exploring Advanced Techniques in Machine Learning

                As a machine learning enthusiast, your task is to delve into the realm of advanced techniques in machine learning, showcasing your expertise in understanding and explaining cutting-edge methodologies. The goal is to provide a comprehensive response covering the following key aspects:

                1. **Ensemble Learning:**
                    - Define and explain the concept of ensemble learning.
                    - Explore popular ensemble methods such as Random Forests, Gradient Boosting, and their applications in diverse domains.

                2. **Reinforcement Learning:**
                    - Provide an in-depth overview of reinforcement learning and its significance in training models through interaction.
                    - Discuss key algorithms like Q-learning, Deep Q Networks (DQN), and highlight their applications in real-world scenarios.

                3. **AutoML (Automated Machine Learning):**
                    - Explore the concept of Automated Machine Learning (AutoML) and its role in automating the end-to-end machine learning process.
                    - Discuss popular AutoML tools and platforms, showcasing their benefits and limitations.

                4. **Explainable AI (XAI):**
                    - Address the importance of Explainable AI (XAI) in enhancing the interpretability of machine learning models.
                    - Explore techniques and methods that contribute to making machine learning models more transparent and understandable.

                5. **Generative Adversarial Networks (GANs):**
                    - Provide a detailed explanation of Generative Adversarial Networks (GANs) and their applications in generating realistic data.
                    - Discuss the ethical considerations and challenges associated with GANs.

                6. **Hyperparameter Tuning and Optimization:**
                    - Explore the significance of hyperparameter tuning in optimizing machine learning models.
                    - Discuss techniques such as grid search, random search, and Bayesian optimization.

                7. **Current Trends and Future Directions:**
                    - Highlight current trends in advanced machine learning techniques.
                    - Discuss potential future directions, emerging technologies, and areas of research.
                8. **Program**
                    -write a python code snippet that demonstrates one of the concepts discussed above using a relevant dataset. a simple implementation of one of these techniques using Python. a simple implementation of one of these concepts using Python. a simple implementation of one of these concepts using Python. a simple implementation of one of the above concepts using Python. a simple implementation of one of the above concepts using Python.
                    

                Please provide a detailed exploration of each aspect, supported by examples, case studies, and references, to create an informative overview of advanced techniques in machine learning.
            """

    elif subject == "Large Language Models":
        prompt = """
            Title: Analyzing the Impact of Large Language Models on Modern Communication

        As a language model researcher, your task is to analyze and discuss the impact of large language models on modern communication. Generate a comprehensive response covering the following aspects:

        1. **Introduction:**
            - Define what large language models are and provide a brief overview of their capabilities.
            - Highlight their significance in transforming the landscape of communication.

        2. **Applications:**
            - Explore various applications of large language models in communication (e.g., natural language processing, content creation, chatbots).
            - Discuss specific examples where these models have demonstrated significant impact.

        3. **Challenges and Concerns:**
            - Identify potential challenges and ethical concerns associated with the use of large language models.
            - Discuss issues such as bias, misinformation, and the responsible deployment of these models.

        4. **Benefits:**
            - Highlight the positive aspects and benefits of incorporating large language models in communication.
            - Discuss how they enhance efficiency, creativity, and user experience.

        5. **Future Trends:**
            - Explore potential future trends in the development and utilization of large language models in communication.
            - Consider advancements, research directions, and potential improvements.

        Please provide a detailed analysis, supported by examples and references, to create an insightful exploration of the impact of large language models on modern communication.
        6. **Program:**
            -write a python code     snippet that demonstrates generating text using a pre-trained language model like GPT-3 or GPT-2.  
    """

    elif subject == "Data Science and Statistics":
        prompt = """
            Title: Comprehensive Notes on Data Science and Statistics from YouTube Video Transcript

            Subject: Data Science and Statistics

            Prompt:

            As an expert in Data Science and Statistics, your task is to provide comprehensive notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate detailed notes covering the key concepts discussed in the video.

            Your notes should:

            Data Science:

            Explain fundamental concepts in data science such as data collection, data cleaning, data analysis, and data visualization.
            Discuss different techniques and algorithms used in data analysis and machine learning, including supervised and unsupervised learning methods.
            Provide insights into real-world applications of data science in various fields like business, healthcare, finance, etc.
            Include discussions on data ethics, privacy concerns, and best practices in handling sensitive data.
            Statistics:

            Outline basic statistical concepts such as measures of central tendency, variability, and probability distributions.
            Explain hypothesis testing, confidence intervals, and regression analysis techniques.
            Clarify the importance of statistical inference and its role in drawing conclusions from data.
            Provide examples or case studies demonstrating the application of statistical methods in solving real-world problems.

            Your notes should aim to offer a clear understanding of both the theoretical foundations and practical applications of data science and statistics discussed in the video. Use clear explanations, examples, and visuals where necessary to enhance comprehension.

            Please provide the YouTube video transcript, and I'll generate the detailed notes on Data Science and Statistics accordingly.
        """
    elif subject == "Generative Ai":
        prompt = """
         Title = Detailed Notes on Generative AI from YouTube Video Transcript
         The generative model is a type of artificial neural network that learns how to create new content from text.
         The model is trained on large amounts of data, and can be used to generate content that is similar to the content of the original text. 
         
         The main task is to create a markdown file that includes code snippets, text, and images based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate comprehensive notes covering the key concepts discussed in the video.  
         The goal of this note is to provide a comprehensive summary of generative models 
         and their applications.
         Your notes should:
         - Highlight fundamental principles, laws, and theories discussed in the video.
         - Explain any relevant experiments, demonstrations, or real-world applications.
         - Clarify any mathematical equations or formulas introduced and provide explanations for their significance.
         - Use diagrams, illustrations, or examples to enhance understanding where necessary.
         - Discuss how generative models can be used to generate new data that resembles existing
         - Provide examples or case studies to illustrate the practical applications of the concepts discussed.
         **Program **
            - write a python code snippet that demonstrate the Genrative AI examples .
         Please provide the YouTube video transcript, and I'll generate the detailed notes on Generative AI accordingly.
         datasets.  
        """

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt + transcript_text)
    return response.text

def main():
    st.title("YouTube Transcript to Detailed Notes Converter")
    

    subject = st.selectbox("Select Subject:", ["Open-CV", "Machine learning", "Large Language Models", "Data Science and Statistics","Generative Ai"])


    youtube_link = st.text_input("Enter YouTube Video Link:")


    if youtube_link:
        video_id = youtube_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
        print(video_id)

    if st.button("Get Detailed Notes"):
        # Call function to extract transcript
        transcript_text = extract_transcript(youtube_link)
        
        if transcript_text:
            st.success("Transcript extracted successfully!")
            # Generate detailed notes
            detailed_notes = generate_notes(transcript_text, subject)
            st.markdown("## Detailed Notes:")
            st.write(detailed_notes)
        else:
            st.error("Failed to extract transcript.")

if __name__ == "__main__":
    main()
