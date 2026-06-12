import logging

from anthropic import Anthropic
from config import CLAUDE_API_KEY, CLAUDE_MODEL

logger = logging.getLogger(__name__)


class CoverLetterGenerator:
    def __init__(self):
        self.client = Anthropic(api_key=CLAUDE_API_KEY) if CLAUDE_API_KEY else None

    def generate(self, user_name, resume_text, job):
        if not self.client:
            return ""

        prompt = f"""You are a cover letter writer for hospitality job applications.
Write a professional cover letter (Malaysia context) for the candidate.

Candidate Name: {user_name}
Key Experience: {resume_text[:1000]}

Job Title: {job['title']}
Company: {job['company']}
Description: {job.get('description', '')[:1500]}

Return only the cover letter text, no explanation. Keep it under 300 words.
"""

        try:
            msg = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )
            return msg.content[0].text
        except Exception as e:
            logger.error("Cover letter generation failed: %s", e)
            return ""
