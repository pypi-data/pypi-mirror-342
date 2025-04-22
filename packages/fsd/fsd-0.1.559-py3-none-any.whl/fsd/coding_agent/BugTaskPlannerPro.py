import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class BugTaskPlannerPro:
    """
    A class to plan and manage tasks using AI-powered assistance.
    """

    def __init__(self, repo):
        """
        Initialize the TaskPlanner with necessary configurations.

        Args:
            directory_path (str): Path to the project directory.
            api_key (str): API key for authentication.
            endpoint (str): API endpoint URL.
            deployment_id (str): Deployment ID for the AI model.
            max_tokens (int): Maximum number of tokens for AI responses.
        """
        self.max_tokens = 4096
        self.repo = repo
        self.ai = AIGateway()

    async def get_task_plan(self, instruction, file_list, original_prompt_language):
        """
        Get a development plan based on the user's instruction using AI.

        Args:
            instruction (str): The user's instruction for task planning.
            file_list (list): List of available files.
            original_prompt_language (str): The language of the original prompt.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `TaskPlanner` is initiating the process to generate a task plan")
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a principal engineer specializing in bug fixing and code quality. Generate an ordered list of task groups for implementing bug fixes based on the user's instruction and provided file list.\n\n"
                    "Guidelines:\n"
                    "1. Only include files from the provided 'file_list' - no exceptions.\n"
                    "2. Follow dependency order:\n"
                    "   a. Utility/Helper functions\n" 
                    "   b. Base components\n"
                    "   c. Services and middleware\n"
                    "   d. Main application components\n"
                    "3. Group by tech stack:\n"
                    "   - Python: utils, models, services, controllers\n"
                    "   - JavaScript: utils, hooks, components, pages\n"
                    "   - Java: utils, models, services, controllers\n"
                    "   - TypeScript: types, utils, components, pages\n"
                    "4. Fix bugs in priority order:\n"
                    "   a. Critical system crashes\n"
                    "   b. Security vulnerabilities\n" 
                    "   c. Data integrity issues\n"
                    "   d. Performance issues\n"
                    "   e. UI/UX defects\n"
                    "5. Follow dependency chain:\n"
                    "   - Fix foundational bugs before dependent ones\n"
                    "   - Fix shared components before specific ones\n"
                    "6. Include testing:\n"
                    "   - Unit tests for utils/helpers\n"
                    "   - Integration tests for services\n"
                    "   - End-to-end tests for complete flows\n"
                    "7. File requirements:\n"
                    "   - Provide full file path\n"
                    "   - Specify tech stack\n"
                    "   - No duplicate files across groups\n"
                    "8. Component order:\n"
                    "   - Utils/Helpers first\n"
                    "   - Base components second\n"
                    "   - Services third\n"
                    "   - Main components last\n"
                    "9. MANDATORY Commit Message Format:\n"
                    "   bugfix(scope): <precise_description>\n"
                    "Response Format:\n"
                    '{\n'
                    '    "groups": [\n'
                    '        {\n'
                    '            "group_name": "",\n'
                    '            "tasks": [\n'
                    '                {\n'
                    '                    "file_name": "/full/path/to/file.py",\n'
                    '                    "techStack": "python"\n'
                    '                }\n'
                    '            ]\n'
                    '        }\n'
                    '    ],\n'
                    '    "commits": ""\n'
                    '}'
                    f"Current working project is {self.repo.get_repo_path()}\n\n"
                    "MUST return only valid JSON without additional text or formatting."
                )
            },
            {
                "role": "user", 
                "content": f"STRICTLY create a grouped task list for bug fixing using ONLY files from:\n{file_list} - ABSOLUTELY MUST Only include files from the provided 'file_list' for all tasks, NO EXCEPTIONS.\n\nMANDATORY: Start with smallest components (utils, helpers, base components) before main components. Group by tech stack following the examples provided. CRITICAL: Each file MUST appear in exactly ONE group - NO duplicates allowed. Respect all dependency chains and ensure comprehensive testing coverage. Original instruction: {instruction}\n\n"
            }
        ]

        try:
            response = await self.ai.arch_prompt(messages, 4096, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### The `TaskPlanner` has successfully generated the task plan")
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### The `TaskPlanner` has repaired and processed the JSON response")
            return plan_json
        except Exception as e:
            logger.error(f"  The `TaskPlanner` encountered an error while generating the task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, instruction, file_lists, original_prompt_language):
        """
        Get development plans based on the user's instruction.

        Args:
            instruction (str): The user's instruction for task planning.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `TaskPlanner` is generating task plans")
        plan = await self.get_task_plan(instruction, file_lists, original_prompt_language)
        logger.debug("\n #### The `TaskPlanner` has completed generating the task plans")
        return plan