import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class PrePromptAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_prePrompt_plan(self, user_prompt):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        all_file_contents = self.repo.print_tree()
        messages = [
            {
                "role": "system", 
                "content": (
                    "As a prompt engineer, analyze the project files and user prompt. Respond in JSON format:\n\n"
                    "role: Choose an engineer role suited for the task.\n"
                    "pipeline: Choose pipeline (2-9):\n"
                    "2. Create/add files only\n" 
                    "3. Move files only\n"
                    "4. Code changes (features, bugs, UI, images needing code)\n"
                    "5. Install dependencies only\n"
                    "6. Open/run/compile project only\n"
                    "7. Deploy project only\n"
                    "8. Generate standalone images\n"
                    "9. Questions/explanations (no code changes)\n"
                    "original_prompt_language: Use specified language or detect from prompt.\n"
                    "{\n"
                    '    "role": "",\n'
                    '    "pipeline": "2-9",\n'
                    '    "original_prompt_language": ""\n'
                    "}\n"
                    "Provide valid JSON only."
                )
            },
            {
                "role": "user",
                "content": f"User prompt:\n{user_prompt}\n\nProject structure:\n{all_file_contents}\n"
            }
        ]

        try:
            response = await self.ai.prompt(messages, 4096, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"The `PrePromptAgent` encountered an error during plan generation: {e}")
            return {
                "reason": str(e)
            }

    async def get_prePrompt_plans(self, user_prompt):
        plan = await self.get_prePrompt_plan(user_prompt)
        logger.debug(f"The `PrePromptAgent` has successfully completed preparing for the user prompt: {user_prompt}")
        return plan
