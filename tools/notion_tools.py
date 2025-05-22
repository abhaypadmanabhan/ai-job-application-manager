# ai-job-application-manager/tools/notion_tools.py
import os
from dotenv import load_dotenv
from smolagents import tool
from notion_client import Client, APIResponseError
import json # Added for more robust error parsing if needed

@tool
def append_text_to_notion_page(page_id: str, text_to_append: str) -> str:
    """
    Appends text content as new paragraph blocks to the end of a specific Notion page.
    Each line in text_to_append will become a new paragraph.

    Args:
        page_id: The ID of the Notion page to append content to.
        text_to_append: The string content to append. Newlines will create separate paragraphs.

    Returns:
        A success message or an error message.
    """
    notion_api_key = os.environ.get("NOTION_API_KEY")
    if not notion_api_key:
        return "Error: NOTION_API_KEY environment variable not set."

    notion = Client(auth=notion_api_key)
    
    content_blocks = []
    if not text_to_append or not text_to_append.strip():
        return "Error: No text provided to append (text_to_append is empty or whitespace)."

    lines = text_to_append.strip().split('\n')
    for line in lines:
        if line.strip(): 
            content_blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": line.strip()}}]
                }
            })
    
    if not content_blocks:
        return "Error: Text to append resulted in no content blocks (e.g., only whitespace or empty lines)."

    try:
        print(f"[append_text_to_notion_page tool] Attempting to append {len(content_blocks)} block(s) to Page ID: '{page_id}'")
        notion.blocks.children.append(block_id=page_id, children=content_blocks)
        print(f"[append_text_to_notion_page tool] Successfully appended content to page {page_id}.")
        return f"Successfully appended content to Notion page {page_id}."
    except APIResponseError as e:
        error_detail = "Unknown API error"
        try:
            # e.body is bytes, decode to string then parse as JSON
            error_body_dict = json.loads(e.body.decode()) if isinstance(e.body, bytes) else e.body
            error_detail = error_body_dict.get('message', str(e)) if isinstance(error_body_dict, dict) else str(e)
        except Exception as parse_error: 
            print(f"[append_text_to_notion_page tool] Error parsing APIResponseError body: {parse_error}")
            error_detail = str(e) # Fallback to string representation of the original API error
            
        error_message = f"Notion API Error (page_id: {page_id}): {error_detail}. Ensure page is shared with the integration, the Page ID is correct, and the integration has append permissions."
        print(f"[append_text_to_notion_page tool] {error_message}")
        return error_message
    except Exception as e:
        error_message = f"An unexpected error occurred while appending to Notion page {page_id}: {type(e).__name__} - {str(e)}"
        print(f"[append_text_to_notion_page tool] {error_message}")
        return error_message

if __name__ == '__main__':
    load_dotenv()
    import datetime # <<< --- ADD THIS IMPORT HERE ---

    test_page_id = os.getenv("NOTION_PAGE_ID_FOR_LOGGING") 
    if not test_page_id:
        print("Please set NOTION_PAGE_ID_FOR_LOGGING in your .env file to test.")
    else:
        if not os.getenv("NOTION_API_KEY"):
            print("Please ensure NOTION_API_KEY is also set in your .env file for this test.")
        else:
            print(f"Attempting to append test content to Notion Page ID: {test_page_id}...")
            
            job_log_entry = (
                f"--- Test Entry from notion_tools.py ---\n"
                f"Timestamp: {datetime.datetime.now().isoformat()}\n" # This line needs datetime
                f"This is a test append operation.\n"
                f"If you see this, the tool is working with your API key and Page ID."
            )
            result = append_text_to_notion_page(
                page_id=test_page_id,
                text_to_append=job_log_entry
            )
            print(f"\nTest Result: {result}")