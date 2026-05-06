import os
import json
from anthropic import Anthropic

anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", "dummy_key"))

def generate_business_plan(idea: str) -> dict:
    prompt = f"""
    You are an expert business consultant. Create a detailed business plan for the following idea:
    IDEA: {idea}
    
    Respond ONLY with a JSON object in this format:
    {{
        "title": "Business Name/Title",
        "executive_summary": "Summary...",
        "target_market": "Who is the customer?",
        "revenue_model": "How will it make money?",
        "competitors": ["Competitor A", "Competitor B"]
    }}
    """
    
    response = anthropic.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0.7,
        system="You are an expert business planner. Return ONLY valid JSON.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    try:
        content = response.content[0].text.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
            
        return json.loads(content)
    except Exception as e:
        print(f"Error parsing JSON from Claude: {e}")
        return {
            "title": "Generated Business Plan",
            "executive_summary": "Failed to parse. " + response.content[0].text,
            "target_market": "",
            "revenue_model": "",
            "competitors": []
        }

def generate_checklist(plan_data: dict) -> list:
    prompt = f"""
    Based on the following business plan, generate a 5-step checklist to start the business.
    Return ONLY a JSON array of objects with 'title' and 'description'.
    
    PLAN: {json.dumps(plan_data)}
    
    Example:
    [
      {{"title": "Register LLC", "description": "File articles of organization"}},
      {{"title": "Set up website", "description": "Buy domain and set up hosting"}}
    ]
    """
    
    response = anthropic.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0.5,
        system="You are an expert business planner. Return ONLY a valid JSON array.",
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        content = response.content[0].text.strip()
        if content.startswith("```json"): content = content[7:-3].strip()
        elif content.startswith("```"): content = content[3:-3].strip()
        return json.loads(content)
    except Exception as e:
        print(f"Error parsing checklist from Claude: {e}")
        return []
