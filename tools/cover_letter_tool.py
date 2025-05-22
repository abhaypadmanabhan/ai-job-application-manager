# ai-job-application-manager/tools/cover_letter_tool.py
import os
import json # Though we might not strictly need to parse JSON from LLM here
from smolagents import tool
from dotenv import load_dotenv
import litellm # For making direct LLM calls

@tool
def draft_cover_letter(
    resume_text: str, 
    job_description_text: str, 
    company_name: str, 
    job_title: str, 
    candidate_name: str = "Abhay Padmanabhan", # Defaulting to your name, can be an arg
    compatibility_analysis: dict = None 
) -> str:
    """
    Drafts a tailored cover letter based on the resume, job description, 
    company name, job title, and optional compatibility analysis.

    Args:
        resume_text: The full text of the candidate's resume.
        job_description_text: The full text of the job description.
        company_name: The name of the company to address the letter to.
        job_title: The specific job title being applied for.
        candidate_name: The name of the candidate (defaults to "Abhay Padmanabhan").
        compatibility_analysis: (Optional) A dictionary containing compatibility insights 
                                (e.g., strengths, weaknesses) between the resume and JD.

    Returns:
        The drafted cover letter as a string, or an error message string if drafting fails.
    """
    print(f"[draft_cover_letter tool] Received data for: {job_title} at {company_name}")
    print(f"[draft_cover_letter tool] Resume length: {len(resume_text)}, JD length: {len(job_description_text)}")

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        return "Error: GEMINI_API_KEY not found in environment for LLM call within tool."

    # Construct the prompt for the LLM
    prompt_parts = [
        f"You are a professional cover letter writing assistant for {candidate_name}.",
        f"Draft a compelling and tailored cover letter for the position of '{job_title}' at '{company_name}'.",
        "The tone should be professional, enthusiastic, and confident.",
        "The cover letter should highlight how the candidate's skills and experiences from the resume align with the requirements in the job description.",
        "Structure the letter with an introduction, body paragraphs (2-3), and a conclusion with a call to action.",
        "Ensure it is concise and impactful, typically 3-4 paragraphs long.",
        "\n--- Candidate's Resume ---",
        resume_text,
        "\n--- Job Description ---",
        job_description_text,
    ]

    if compatibility_analysis and isinstance(compatibility_analysis, dict):
        prompt_parts.append("\n--- Resume/JD Compatibility Analysis Insights (use these to strengthen the letter) ---")
        if compatibility_analysis.get("strengths"):
            prompt_parts.append("Key Strengths to Emphasize:")
            for strength in compatibility_analysis["strengths"][:3]: # Use top 3 strengths
                prompt_parts.append(f"- {strength}")
        if compatibility_analysis.get("weaknesses"):
            prompt_parts.append("\nAddress or reframe these potential perceived weaknesses if possible (subtly):")
            for weakness in compatibility_analysis["weaknesses"][:2]: # Address top 1-2 weaknesses if sensible
                prompt_parts.append(f"- {weakness}")
        if compatibility_analysis.get("summary"):
             prompt_parts.append(f"\nOverall Fit Summary: {compatibility_analysis.get('summary')}")
    
    prompt_parts.append("\n--- Draft the Cover Letter Below ---")
    prompt = "\n".join(prompt_parts)

    try:
        print("[draft_cover_letter tool] Sending prompt to LLM for cover letter drafting...")
        
        response = litellm.completion(
            model="gemini/gemini-1.5-flash-latest", # Or use a more powerful model like gemini-1.5-pro for better writing
            messages=[{"role": "user", "content": prompt}],
            # temperature=0.7 # Adjust temperature for creativity vs. factuality if needed
        )
        
        cover_letter_draft = response.choices[0].message.content.strip()
        
        # Basic cleanup: LLMs sometimes add "Here is the cover letter:"
        if cover_letter_draft.lower().startswith("here is the cover letter:") or \
           cover_letter_draft.lower().startswith("here's the cover letter:"):
            cover_letter_draft = cover_letter_draft.split(":", 1)[1].strip()
        if cover_letter_draft.lower().startswith("here is a draft of the cover letter:") or \
           cover_letter_draft.lower().startswith("here's a draft of the cover letter:"):
            cover_letter_draft = cover_letter_draft.split(":", 1)[1].strip()


        print(f"[draft_cover_letter tool] Successfully drafted cover letter. Length: {len(cover_letter_draft)}")
        return cover_letter_draft

    except Exception as e:
        error_msg = f"Error during LLM call in draft_cover_letter: {type(e).__name__} - {str(e)}"
        print(f"[draft_cover_letter tool] {error_msg}")
        # import traceback # Uncomment for debugging
        # traceback.print_exc()
        return f"Error: Could not draft cover letter. {error_msg}"

if __name__ == '__main__':
    load_dotenv()
    print("--- Testing draft_cover_letter tool ---")

    # Use the same sample resume and JD from compatibility_analyzer_tool for consistency
    sample_resume_text = """
    Abhay Padmanabhan
    San Francisco, CA | apadmanabhan@ucdavis.edu | +1 628-688-7615 | linkedin.com/in/abhaypadmanabhan | github.com/abhaypadmanabhan

    Education
    University of California, Davis (UCD)                             June 2024 (Expected)
    Master of Science in Business Analytics                           Davis, CA
    Relevant Coursework: Advanced Statistics, Machine Learning, Data Visualization, Big Data Technologies.

    Skills
    Programming: Python (Pandas, NumPy, Scikit-learn, TensorFlow, PyTorch), R, SQL
    Tools: Tableau, Power BI, Apache Spark, Docker, Git, Jupyter Notebooks
    Cloud: AWS (S3, EC2, SageMaker), Azure
    """

    sample_jd_text = """
    Job Title: Junior Data Scientist - AI Team
    Company: Innovatech Solutions Inc.
    Location: San Francisco, CA

    We are seeking a motivated Junior Data Scientist to join our cutting-edge AI team. 
    The ideal candidate will have a passion for machine learning and a strong foundation in statistical analysis. 

    Responsibilities:
    - Develop and implement machine learning models.
    - Analyze large datasets to extract actionable insights.

    Qualifications:
    - Master's or PhD in Data Science, Computer Science, Statistics, or a related field.
    - Proficiency in Python and its data science libraries (Pandas, NumPy, Scikit-learn).
    """
    sample_company = "Innovatech Solutions Inc."
    sample_job_title = "Junior Data Scientist - AI Team"

    # Optionally, include a mock compatibility analysis
    mock_analysis = {
        "compatibility_score": 75, # Example score
        "strengths": [
            "Strong Python and Scikit-learn skills directly match qualifications.",
            "Master's degree in Business Analytics is highly relevant."
        ],
        "weaknesses": [
            "Limited explicit mention of NLP, though ML background is strong."
        ],
        "keyword_analysis": [
            {"keyword": "Python", "present_in_resume": True},
            {"keyword": "Machine Learning", "present_in_resume": True},
            {"keyword": "NLP", "present_in_resume": False} # Example
        ],
        "summary": "Good overall fit with strong foundational skills; NLP experience could be further explored."
    }

    if not os.getenv("GEMINI_API_KEY"):
        print("GEMINI_API_KEY not found in .env. Skipping direct test of draft_cover_letter.")
    else:
        print(f"\nDrafting cover letter for {sample_job_title} at {sample_company}...")
        # Test without compatibility analysis first
        # letter1 = draft_cover_letter(sample_resume_text, sample_jd_text, sample_company, sample_job_title)
        # print("\n--- Cover Letter Draft 1 (without analysis insights) ---")
        # print(letter1)
        # print("-" * 30)

        # Test with compatibility analysis
        print("\nDrafting cover letter with compatibility analysis insights...")
        letter2 = draft_cover_letter(sample_resume_text, sample_jd_text, sample_company, sample_job_title, compatibility_analysis=mock_analysis)
        print("\n--- Cover Letter Draft 2 (with analysis insights) ---")
        print(letter2)
        print("-" * 30)