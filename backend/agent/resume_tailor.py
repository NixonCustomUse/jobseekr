import logging

from anthropic import Anthropic
from config import CLAUDE_API_KEY, CLAUDE_MODEL

logger = logging.getLogger(__name__)


class ResumeTailor:
    def __init__(self):
        self.client = Anthropic(api_key=CLAUDE_API_KEY) if CLAUDE_API_KEY else None

    def tailor(self, resume_text, job):
        if not self.client:
            return resume_text

        prompt = f"""You are a resume tailoring assistant for hospitality jobs.
Rewrite the candidate's resume to highlight experience relevant to this specific job.

Original Resume:
{resume_text[:2000]}

Job Title: {job['title']}
Company: {job['company']}
Description: {job.get('description', '')[:2000]}

Return only the tailored resume text, no explanation.
"""

        try:
            msg = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            )
            return msg.content[0].text
        except Exception as e:
            logger.error("Resume tailoring failed: %s", e)
            return resume_text
