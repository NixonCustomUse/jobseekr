import logging

from anthropic import Anthropic
from config import CLAUDE_API_KEY, CLAUDE_MODEL

logger = logging.getLogger(__name__)


class JobMatcher:
    def __init__(self):
        self.client = Anthropic(api_key=CLAUDE_API_KEY) if CLAUDE_API_KEY else None

    def match_score(self, resume_text, skills, job):
        if not self.client:
            return {"score": 0, "reason": "LLM not configured"}

        prompt = f"""You are a job matching assistant for the Malaysian hospitality industry.
Given a candidate's profile and a job posting, return a match score from 0-100.

Candidate Resume:
{resume_text[:2000]}

Candidate Skills:
{skills}

Job Title: {job['title']}
Company: {job['company']}
Location: {job['location']}
Description: {job.get('description', '')[:2000]}

Return only a JSON object with keys: score (int), reason (str).
"""

        try:
            msg = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}],
            )
            import json
            result = json.loads(msg.content[0].text)
            return result
        except Exception as e:
            logger.error("Match score failed: %s", e)
            return {"score": 0, "reason": "LLM error"}
