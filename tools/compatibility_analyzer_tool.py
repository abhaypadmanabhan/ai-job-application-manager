# ai-job-application-manager/tools/compatibility_analyzer_tool.py
import os
import json
from smolagents import tool, LiteLLMModel # For consistency, use LiteLLMModel if agent needs to call other agents/LLMs
from dotenv import load_dotenv
# Alternatively, to make a direct call to Gemini without smolagents/LiteLLM for this specific tool:
# import google.generativeai as genai

@tool
def analyze_resume_jd_match(resume_text: str, job_description_text: str) -> dict:
    """
    Analyzes the compatibility between a resume and a job description using an LLM.

    Args:
        resume_text: The full text of the resume.
        job_description_text: The full text of the job description.

    Returns:
        A dictionary containing the analysis (e.g., compatibility_score, strengths, 
        weaknesses, keyword_analysis) or an error dictionary if the analysis fails.
    """
    print(f"[analyze_resume_jd_match tool] Received resume (len: {len(resume_text)}) and JD (len: {len(job_description_text)}).")

    # Ensure API key is available for the LLM call
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        return {"error": "GEMINI_API_KEY not found in environment for LLM call within tool."}

    # --- Option 1: Using LiteLLM for the call (consistent with ManagerAgent's LLM) ---
    try:
        # Initialize a new LiteLLMModel instance for this specific call
        # This is generally okay for tools that need to call an LLM.
        # Ensure GEMINI_API_KEY is set in the environment; LiteLLM will pick it up.
        llm_for_analysis = LiteLLMModel(model_id="gemini/gemini-1.5-flash-latest")
        
        prompt = f"""
You are an expert HR analyst. Your task is to analyze the provided resume against the job description.
Please provide a detailed analysis in JSON format with the following keys:
- "compatibility_score": An estimated score from 0 to 100 representing how well the resume matches the job description.
- "strengths": A list of strings, where each string highlights a key strength or relevant experience from the resume that matches a requirement in the job description.
- "weaknesses": A list of strings, identifying key areas where the resume is weaker, or skills/experiences mentioned in the job description that are missing or not prominent in the resume.
- "keyword_analysis": A list of dictionaries, where each dictionary has "keyword" (a crucial keyword/skill from the JD) and "present_in_resume" (boolean: true if found or strongly implied, false otherwise). List 3-5 most important keywords.
- "summary": A brief overall summary (2-3 sentences) of the candidate's fit for the role.

Resume Text:
---
{resume_text}
---

Job Description Text:
---
{job_description_text}
---

Provide your analysis strictly in the JSON format described above.
"""
        print("[analyze_resume_jd_match tool] Sending prompt to LLM for analysis...")
        # Using the 'completion' method of LiteLLMModel which is a more direct way to get a response
        # The 'run' method is more for agentic loops.
        # Note: The exact method to get a raw completion might vary slightly based on LiteLLMModel's API.
        # Typically, LiteLLM itself has a `litellm.completion()` function.
        # If LiteLLMModel doesn't directly expose a simple completion, we might use litellm.completion directly.

        # Let's assume LiteLLMModel can make a direct call or we use litellm.completion
        import litellm
        response = litellm.completion( # Using litellm.completion directly
            model="gemini/gemini-1.5-flash-latest", 
            messages=[{"role": "user", "content": prompt}],
            # api_key=gemini_api_key # litellm.completion picks up GEMINI_API_KEY from env
        )
        
        # Extract the response content
        llm_output_text = response.choices[0].message.content
        print(f"[analyze_resume_jd_match tool] Received raw output from LLM: {llm_output_text[:200]}...")

        # Attempt to parse the JSON output from the LLM
        # LLMs can sometimes produce slightly malformed JSON, so use try-except
        try:
            # The LLM might sometimes wrap the JSON in backticks or "json" language specifier
            if llm_output_text.strip().startswith("```json"):
                llm_output_text = llm_output_text.strip()[7:-3].strip()
            elif llm_output_text.strip().startswith("```"):
                 llm_output_text = llm_output_text.strip()[3:-3].strip()

            analysis_result = json.loads(llm_output_text)
            print("[analyze_resume_jd_match tool] Successfully parsed LLM JSON output.")
            return analysis_result
        except json.JSONDecodeError as e:
            error_msg = f"Error: Could not parse JSON response from LLM. Error: {e}. LLM Output: {llm_output_text}"
            print(f"[analyze_resume_jd_match tool] {error_msg}")
            return {"error": error_msg, "raw_llm_output": llm_output_text}

    except Exception as e:
        error_msg = f"Error during LLM call in analyze_resume_jd_match: {type(e).__name__} - {str(e)}"
        print(f"[analyze_resume_jd_match tool] {error_msg}")
        # import traceback # Uncomment for debugging
        # traceback.print_exc()
        return {"error": error_msg}


    # --- Option 2: Using google-generativeai directly (if you prefer and have it installed) ---
    # This provides more direct control over the Gemini API call if needed.
    # try:
    #     genai.configure(api_key=gemini_api_key)
    #     model = genai.GenerativeModel('gemini-1.5-flash-latest') # Or 'gemini-pro' for more power
    #     prompt = f"""... (same prompt as above) ..."""
    #     print("[analyze_resume_jd_match tool] Sending prompt to Gemini for analysis...")
    #     response = model.generate_content(prompt)
    #     llm_output_text = response.text
    #     print(f"[analyze_resume_jd_match tool] Received raw output from Gemini: {llm_output_text[:200]}...")
    #     # ... (JSON parsing as above) ...
    # except Exception as e:
    #     # ... (error handling as above) ...

if __name__ == '__main__':
    load_dotenv()
    print("--- Testing analyze_resume_jd_match tool ---")

    # For this test, we need sample resume and JD text.
    # You can load them from your files for a more realistic test.
    sample_resume_text = """
    Abhay Padmanabhan
    San Francisco, CA | apadmanabhan@ucdavis.edu | +1 628-688-7615 | linkedin.com/in/abhaypadmanabhan | github.com/abhaypadmanabhan

    Education
    University of California, Davis (UCD)                             June 2024 (Expected)
    Master of Science in Business Analytics                           Davis, CA
    Relevant Coursework: Advanced Statistics, Machine Learning, Data Visualization, Big Data Technologies.
    Projects: Customer Churn Prediction, Market Basket Analysis.

    Skills
    Programming: Python (Pandas, NumPy, Scikit-learn, TensorFlow, PyTorch), R, SQL
    Tools: Tableau, Power BI, Apache Spark, Docker, Git, Jupyter Notebooks
    Cloud: AWS (S3, EC2, SageMaker), Azure
    Languages: English (Fluent), Hindi (Fluent)
    """

    sample_jd_text = """
    Job Title: Junior Data Scientist - AI Team

    Company: Innovatech Solutions Inc.

    Location: San Francisco, CA

    We are seeking a motivated Junior Data Scientist to join our cutting-edge AI team. 
    The ideal candidate will have a passion for machine learning and a strong foundation in statistical analysis. 
    You will work on exciting projects involving natural language processing and predictive modeling.

    Responsibilities:
    - Develop and implement machine learning models.
    - Analyze large datasets to extract actionable insights.
    - Collaborate with cross-functional teams to define project requirements.
    - Communicate findings to stakeholders through reports and visualizations.
    - Stay up-to-date with the latest advancements in AI and machine learning.

    Qualifications:
    - Master's or PhD in Data Science, Computer Science, Statistics, or a related field.
    - Proficiency in Python and its data science libraries (Pandas, NumPy, Scikit-learn).
    - Experience with machine learning algorithms and techniques.
    - Familiarity with SQL and database technologies.
    - Strong analytical and problem-solving skills.
    - Excellent communication and teamwork abilities.

    Preferred:
    - Experience with NLP techniques.
    - Knowledge of cloud platforms like AWS or Azure.
    - Familiarity with Big Data tools (e.g., Spark).
    """

    if not os.getenv("GEMINI_API_KEY"):
        print("GEMINI_API_KEY not found in .env. Skipping direct test of analyze_resume_jd_match.")
    else:
        print("\nAnalyzing sample resume against sample JD:")
        analysis = analyze_resume_jd_match(sample_resume_text, sample_jd_text)
        
        if "error" in analysis:
            print("\nAnalysis Error:")
            print(analysis["error"])
            if "raw_llm_output" in analysis:
                 print("\nRaw LLM Output (if available):")
                 print(analysis["raw_llm_output"])
        else:
            print("\nAnalysis Result (pretty printed):")
            print(json.dumps(analysis, indent=2))
            print(f"\nCompatibility Score: {analysis.get('compatibility_score')}%")
            print("\nStrengths:")
            for strength in analysis.get("strengths", []):
                print(f"- {strength}")
            print("\nWeaknesses:")
            for weakness in analysis.get("weaknesses", []):
                print(f"- {weakness}")
            print("\nKeyword Analysis:")
            for kw in analysis.get("keyword_analysis", []):
                print(f"- Keyword: {kw.get('keyword')}, Present: {kw.get('present_in_resume')}")
            print(f"\nSummary: {analysis.get('summary')}")