# ai-job-application-manager/tools/resume_tuner_tool.py
import os
import json # For potential future structured output, though text is fine for now
from smolagents import tool
from dotenv import load_dotenv
import litellm

@tool
def suggest_resume_improvements(
    resume_text: str, 
    job_description_text: str, 
    compatibility_analysis: dict
) -> str:
    """
    Suggests specific improvements to a resume to better align it with a given 
    job description, based on a provided compatibility analysis.

    Args:
        resume_text: The full text of the candidate's current resume.
        job_description_text: The full text of the job description.
        compatibility_analysis: A dictionary containing compatibility insights 
                                (e.g., compatibility_score, strengths, weaknesses, keyword_analysis).

    Returns:
        A string containing actionable suggestions for improving the resume, 
        or an error message string if suggestions cannot be generated.
    """
    print(f"[suggest_resume_improvements tool] Received resume (len: {len(resume_text)}), JD (len: {len(job_description_text)}), and analysis.")

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        return "Error: GEMINI_API_KEY not found in environment for LLM call within tool."

    # Construct the prompt for the LLM
    prompt_parts = [
        "You are an expert resume writing consultant and career coach.",
        "Your task is to provide specific, actionable suggestions to improve the provided resume to better match the given job description.",
        "Use the insights from the 'Compatibility Analysis' to guide your suggestions.",
        "Focus on:",
        "  - How to rephrase existing bullet points or add new ones to highlight relevant skills and achievements.",
        "  - Incorporating important keywords from the job description naturally into the resume.",
        "  - Addressing any weaknesses or gaps identified in the compatibility analysis by suggesting how to present existing experience more effectively or by identifying areas for skill development (if applicable).",
        "  - Ensuring the resume clearly demonstrates the candidate's suitability for the role described in the job description.",
        "Provide clear, bullet-pointed suggestions. Start with a brief overall recommendation.",
        "\n--- Candidate's Current Resume ---",
        resume_text,
        "\n--- Target Job Description ---",
        job_description_text,
        "\n--- Compatibility Analysis Insights ---"
    ]

    if isinstance(compatibility_analysis, dict):
        prompt_parts.append(f"Overall Compatibility Score: {compatibility_analysis.get('compatibility_score', 'N/A')}%")
        if compatibility_analysis.get("strengths"):
            prompt_parts.append("\nIdentified Strengths to Leverage:")
            for strength in compatibility_analysis["strengths"]:
                prompt_parts.append(f"- {strength}")
        if compatibility_analysis.get("weaknesses"):
            prompt_parts.append("\nIdentified Weaknesses/Gaps to Address:")
            for weakness in compatibility_analysis["weaknesses"]:
                prompt_parts.append(f"- {weakness}")
        if compatibility_analysis.get("keyword_analysis"):
            prompt_parts.append("\nRelevant Keywords from JD:")
            for kw_item in compatibility_analysis["keyword_analysis"]:
                prompt_parts.append(f"- Keyword: '{kw_item.get('keyword')}', Resume Presence: {kw_item.get('present_in_resume')}")
    else:
        prompt_parts.append("Compatibility analysis data was not in the expected format or was missing.")

    prompt_parts.append("\n--- Provide Resume Improvement Suggestions Below (as bullet points) ---")
    prompt = "\n".join(prompt_parts)

    try:
        print("[suggest_resume_improvements tool] Sending prompt to LLM for resume suggestions...")
        
        response = litellm.completion(
            model="gemini/gemini-1.5-flash-latest", # Consider gemini-1.5-pro for more nuanced suggestions
            messages=[{"role": "user", "content": prompt}],
            # temperature=0.5 # Suggestions should be fairly grounded
        )
        
        resume_suggestions = response.choices[0].message.content.strip()
        
        print(f"[suggest_resume_improvements tool] Successfully generated resume suggestions. Length: {len(resume_suggestions)}")
        return resume_suggestions

    except Exception as e:
        error_msg = f"Error during LLM call in suggest_resume_improvements: {type(e).__name__} - {str(e)}"
        print(f"[suggest_resume_improvements tool] {error_msg}")
        return f"Error: Could not generate resume suggestions. {error_msg}"

if __name__ == '__main__':
    load_dotenv()
    print("--- Testing suggest_resume_improvements tool ---")

    sample_resume_text = """
    Abhay Padmanabhan
    San Francisco, CA | apadmanabhan@ucdavis.edu | +1 628-688-7615

    Education
    Master of Science in Business Analytics - UC Davis (Expected June 2024)
    Relevant Coursework: Machine Learning, Data Visualization.

    Skills
    Programming: Python (Pandas, NumPy, Scikit-learn), SQL
    Tools: Tableau, Git
    """

    sample_jd_text = """
    Job Title: Data Analyst - Marketing Team
    Company: GrowthMetrics Co.
    Location: Remote

    Responsibilities:
    - Analyze marketing campaign data to identify trends and insights.
    - Create dashboards in Tableau to report on KPIs.
    - Work with SQL to query databases for customer segmentation.
    - Present findings to the marketing team.

    Qualifications:
    - Bachelor's or Master's in Analytics, Statistics, or related.
    - Strong SQL skills.
    - Experience with Python for data analysis (Pandas).
    - Proficiency in Tableau or similar BI tool.
    - Excellent communication skills.
    """
    
    mock_analysis_for_resume_tune = {
        "compatibility_score": 60,
        "strengths": [
            "Python (Pandas, NumPy, Scikit-learn) and SQL skills are a good match.",
            "Tableau experience listed.",
            "Master's in Business Analytics is relevant."
        ],
        "weaknesses": [
            "Resume does not explicitly mention experience with 'marketing campaign data' or 'customer segmentation'.",
            "Communication skills (presenting findings) could be highlighted more with specific examples."
        ],
        "keyword_analysis": [
            {"keyword": "SQL", "present_in_resume": True},
            {"keyword": "Tableau", "present_in_resume": True},
            {"keyword": "Marketing Analytics", "present_in_resume": False},
            {"keyword": "Customer Segmentation", "present_in_resume": False}
        ],
        "summary": "Candidate has strong foundational technical skills (Python, SQL, Tableau) but could better tailor the resume to highlight marketing analytics experience and communication impact."
    }

    if not os.getenv("GEMINI_API_KEY"):
        print("GEMINI_API_KEY not found in .env. Skipping direct test of suggest_resume_improvements.")
    else:
        print("\nGenerating resume improvement suggestions...")
        suggestions = suggest_resume_improvements(
            resume_text=sample_resume_text, 
            job_description_text=sample_jd_text,
            compatibility_analysis=mock_analysis_for_resume_tune
        )
        print("\n--- Resume Improvement Suggestions ---")
        print(suggestions)
        print("-" * 30)