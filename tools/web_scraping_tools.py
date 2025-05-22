# ai-job-application-manager/tools/web_scraping_tools.py
import os
from smolagents import tool
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

@tool
def scrape_job_board(url: str, job_title_keywords: list[str] = None) -> list[dict]:
    """
    Scrapes a job board URL (HTTP/HTTPS) or a local HTML file (file:///) for job postings.
    Optionally filters by keywords in the job title (case-insensitive).

    Args:
        url: The URL (http, https) or local file path (file:///path/to/file.html) of the job board.
        job_title_keywords: A list of keywords to filter job titles by. 
                            If None or empty, all jobs found are returned.

    Returns:
        A list of dictionaries, where each dictionary contains 'title', 'company', 
        'url', and 'description'. Returns a list containing a single error dictionary
        if a significant error occurs.
    """
    jobs = []
    html_content = ""
    base_url_for_links = url 

    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme == "file":
            print(f"[scrape_job_board tool] Reading local file: {url}")
            # On macOS/Linux, path is parsed_url.path. On Windows, it often starts with an extra '/'
            file_path = parsed_url.path
            if os.name == 'nt' and file_path.startswith('/') and len(file_path) > 2 and file_path[2] == ':':
                file_path = file_path[1:] # Remove leading '/' for paths like /C:/...
            
            if not os.path.exists(file_path):
                error_msg = f"Local file not found: {file_path}"
                print(f"[scrape_job_board tool] {error_msg}")
                return [{"error": error_msg}]
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            # For local files, set base_url for resolving relative links to the file's directory
            base_url_for_links = 'file://' + os.path.dirname(os.path.abspath(file_path)) + '/'
            if os.name == 'nt': # Ensure correct formatting for Windows file URIs as base
                 base_url_for_links = 'file:///' + os.path.dirname(os.path.abspath(file_path)).replace(os.sep, '/') + '/'


        elif parsed_url.scheme in ["http", "https"]:
            print(f"[scrape_job_board tool] Attempting to scrape HTTP/S URL: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status() # Raises HTTPError for bad responses (4XX or 5XX)
            html_content = response.content
            base_url_for_links = url # Original URL is the base for web links
        else:
            error_msg = f"Unsupported URL scheme: '{parsed_url.scheme}'. Tool supports http, https, file."
            print(f"[scrape_job_board tool] {error_msg}")
            return [{"error": error_msg}]

        soup = BeautifulSoup(html_content, 'html.parser')
        # These selectors are for the test_jobs.html structure. Adapt for real sites.
        job_elements = soup.find_all('div', class_='job-listing') 

        if not job_elements:
            print(f"[scrape_job_board tool] No job elements found with class 'job-listing' on {url}.")
            return [] # Return empty list if no matching elements, not an error.

        print(f"[scrape_job_board tool] Found {len(job_elements)} potential job elements.")
        for i, job_elem in enumerate(job_elements):
            title_elem = job_elem.find('h2', class_='job-title')
            company_elem = job_elem.find('p', class_='company-name')
            link_elem = job_elem.find('a', href=True)
            description_elem = job_elem.find('div', class_='job-description')

            title = title_elem.text.strip() if title_elem else f"Job Title N/A {i+1}"
            company = company_elem.text.strip() if company_elem else "Company N/A"
            
            job_url_path = "N/A"
            if link_elem and link_elem.get('href'):
                job_url_path = urljoin(base_url_for_links, link_elem['href'])
            
            description = description_elem.text.strip() if description_elem else "No description available."
            
            if job_title_keywords:
                matches_keywords = any(keyword.lower() in title.lower() for keyword in job_title_keywords)
                if not matches_keywords:
                    continue

            jobs.append({
                "title": title,
                "company": company,
                "url": job_url_path,
                "description": description[:250] + "..." if len(description) > 250 else description
            })
        
        print(f"[scrape_job_board tool] Successfully extracted {len(jobs)} jobs matching criteria.")
        return jobs

    except requests.exceptions.RequestException as e:
        print(f"[scrape_job_board tool] HTTP request failed for {url}: {str(e)}")
        return [{"error": f"HTTP request failed for {url}: {str(e)}"}]
    except FileNotFoundError:
        error_msg = f"Local file not found (FileNotFoundError) for path derived from: {url}"
        print(f"[scrape_job_board tool] {error_msg}")
        return [{"error": error_msg}]
    except Exception as e:
        print(f"[scrape_job_board tool] An error occurred during scraping {url}: {type(e).__name__} - {str(e)}")
        # import traceback # Uncomment for full traceback during debugging
        # traceback.print_exc()
        return [{"error": f"An unexpected error ({type(e).__name__}) occurred during scraping {url}: {str(e)}"}]

if __name__ == '__main__':
    project_root_for_test_html = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_html_file_path = os.path.join(project_root_for_test_html, "test_jobs.html")

    test_html_content = """
    <html><head><title>Test Jobs</title></head><body>
        <h1>Job Listings</h1>
        <div class="job-listing">
            <h2 class="job-title">Software Engineer</h2>
            <p class="company-name">TestCorp</p>
            <a href="details/swe.html">View SWE Job</a>
            <div class="job-description">We are looking for a skilled Software Engineer proficient in Python and AI.</div>
        </div>
        <div class="job-listing">
            <h2 class="job-title">Data Analyst</h2>
            <p class="company-name">AnalyzeIt Inc.</p>
            <a href="https://example.com/jobs/data-analyst-123">View Data Analyst Job</a>
            <div class="job-description">Seeking a Data Analyst to work with large datasets. SQL and Python required.</div>
        </div>
    </body></html>
    """
    try:
        with open(test_html_file_path, "w", encoding="utf-8") as f:
            f.write(test_html_content)
        print(f"Created/updated test_jobs.html at: {test_html_file_path}")
    except IOError as e:
        print(f"Error creating test_jobs.html: {e}")
        exit() # Exit if test file cannot be created.

    abs_file_path = os.path.abspath(test_html_file_path)
    if os.name == 'nt':
        test_file_uri = f"file:///{abs_file_path.replace(os.sep, '/')}"
    else:
        test_file_uri = f"file://{abs_file_path}"

    print(f"\nTesting scrape_job_board with local file URI: {test_file_uri}")
    scraped_jobs = scrape_job_board(test_file_uri)
    if scraped_jobs and isinstance(scraped_jobs, list) and (len(scraped_jobs) == 0 or not scraped_jobs[0].get("error")):
        print(f"Found {len(scraped_jobs)} jobs:")
        for job in scraped_jobs:
            print(f"  Title: {job.get('title')}, Company: {job.get('company')}, URL: {job.get('url')}")
    else:
        print("No jobs found from local file or an error occurred:")
        if scraped_jobs: print(scraped_jobs)

    print(f"\nTesting with filter for 'Analyst'")
    scraped_jobs_filtered = scrape_job_board(test_file_uri, job_title_keywords=["Analyst"])
    if scraped_jobs_filtered and isinstance(scraped_jobs_filtered, list) and (len(scraped_jobs_filtered) == 0 or not scraped_jobs_filtered[0].get("error")):
        print(f"Found {len(scraped_jobs_filtered)} filtered jobs:")
        for job in scraped_jobs_filtered:
            print(f"  Title: {job.get('title')}, Company: {job.get('company')}, URL: {job.get('url')}")
    else:
        print("No filtered jobs found from local file or an error occurred:")
        if scraped_jobs_filtered: print(scraped_jobs_filtered)