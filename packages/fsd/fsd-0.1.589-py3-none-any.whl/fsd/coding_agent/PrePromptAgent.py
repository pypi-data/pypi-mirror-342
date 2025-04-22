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
                    "You are an expert prompt engineer who analyzes project files and user requests to determine the most appropriate development approach. Analyze the project structure and user prompt carefully, then respond with a precise JSON object containing:\n\n"
                    "1. role: Select the most appropriate specialist role based on the task requirements:\n"
                    "   - 'frontend developer' - For UI/UX, web interfaces, client-side functionality\n"
                    "   - 'backend developer' - For server logic, APIs, databases\n"
                    "   - 'fullstack developer' - For projects requiring both frontend and backend work\n"
                    "   - 'mobile developer' - For iOS/Android app development\n"
                    "   - 'data scientist' - For data analysis, ML/AI tasks\n"
                    "   - 'devops engineer' - For deployment, CI/CD, infrastructure\n"
                    "   - 'security specialist' - For security audits, vulnerability fixes\n"
                    "   - 'QA engineer' - For testing, bug fixing\n\n"
                    
                    "2. pipeline: Select exactly one pipeline number that best matches the user's needs:\n"
                    "   - 2: File Creation Only - When user needs new files created without implementation code\n"
                    "     Example: \"Create a folder structure for my React project\"\n"
                    "   - 3: File Movement Only - When user needs to reorganize files without code changes\n"
                    "     Example: \"Move all utility functions to a utils folder\"\n"
                    "   - 4: Code Implementation - For feature development, bug fixes, UI implementation requiring code\n"
                    "     Example: \"Create a login form with validation\" or \"Fix the authentication bug\"\n"
                    "   - 5: Dependency Management - When user only needs packages installed\n"
                    "     Example: \"Install React and styled-components\"\n"
                    "   - 6: Project Execution - When user needs to run/compile without code changes\n"
                    "     Example: \"How do I run this React project?\"\n"
                    "   - 7: Deployment - When user needs deployment help without code changes\n"
                    "     Example: \"Deploy this app to Heroku\"\n"
                    "   - 8: Image Generation - When user needs standalone images without code integration\n"
                    "     Example: \"Create a logo for my coffee shop app\"\n"
                    "   - 9: Consultation - For questions, explanations with no code changes\n"
                    "     Example: \"Explain how React hooks work\"\n\n"
                    
                    "3. original_prompt_language: Detect the language of the user's prompt or use specified language.\n"
                    "   Examples: \"English\", \"Spanish\", \"Chinese\", \"French\", etc.\n\n"
                    
                    "Your response must be valid JSON in this exact format:\n"
                    "{\n"
                    '    "role": "one of the roles listed above",\n'
                    '    "pipeline": "single number between 2-9",\n'
                    '    "original_prompt_language": "detected language"\n'
                    "}\n\n"
                    
                    "If the user prompt is unclear, vague, or you're not sure what they are asking, default to pipeline 9 (Consultation) as this will engage QA consultant mode to help clarify their needs.\n"
                    
                    "IMPORTANT: Provide ONLY valid JSON with no additional text, explanations, or markdown.\n\n"
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
            logger.error(f"`SnowX` encountered an error during plan generation: {e}")
            return {
                "reason": str(e)
            }

    async def get_prePrompt_plans(self, user_prompt):
        plan = await self.get_prePrompt_plan(user_prompt)
        logger.debug(f"`SnowX` has successfully completed preparing for the user prompt: {user_prompt}")
        return plan
