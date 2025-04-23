import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class TaskPlannerPro:
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
        logger.debug("\n #### `TaskPlanner` is initiating the process to generate a task plan")
        messages = [
            {
                "role": "system", 
                "content": (
                    "You are a principal engineer specializing in Pyramid architecture. Generate an ordered list of task groups for implementing a system based on the user's instruction and provided file list.\n\n"
                    "Guidelines:\n"
                    "1. MUST Only include files from the provided 'file_list' for all tasks, no exception.\n"
                    "2. Follow Pyramid architecture principles:\n"
                    "   - Foundation layers (data models, core utilities) must precede higher layers\n"
                    "   - Business logic layer depends on foundation layer\n"
                    "   - Presentation layer depends on business logic layer\n"
                    "   - Example: database schema → data models → services → controllers → views\n"
                    "3. Apply lead-follow principle across tech stacks:\n"
                    "   - Place lead file of each stack in its own early group to establish patterns\n" 
                    "   - Group follower files that can be executed concurrently\n"
                    "   - Example: Place 'UserModel.js' before 'ProductModel.js' and 'OrderModel.js'\n"
                    "4. IMPORTANT: Only .svg and .md files can be grouped together in the same group for concurrent execution.\n"
                    "   - All code files (.py, .js, .ts, .java, etc.) must be in their own individual groups\n"
                    "   - Never group any real code files together as they cannot share context when run concurrently\n"
                    "5. Backend dependencies:\n"
                    "   - Database schema before models\n"
                    "   - Models before business logic\n"
                    "   - Data access before business logic\n"
                    "   - Example: 'schema.sql' → 'user_model.py' → 'user_service.py' → 'user_controller.py'\n"
                    "6. Each file appears only once in the entire plan\n"
                    "7. Provide `file_name` (full path) and `techStack` for each task\n"
                    "8. Generate a commit message using format: <type>: <description>\n"
                    "   Types: bugfix, feature, optimize, update, config, document, format, restructure, enhance, verify\n"
                    "   Example: 'feature: implement user authentication system'\n"
                    "9. Always implement smaller components first before main components:\n"
                    "   - Smaller, self-contained utilities and helpers should precede larger components\n"
                    "   - This makes integration easier and allows for incremental testing\n"
                    "   - Example: implement utility functions before the classes that use them\n"
                    "10. CRITICAL: Always place SVG files in the first group of the plan, regardless of other dependencies.\n"
                    "11. Follow implementation order from original development plan strictly.\n"
                    "Response Format:\n"
                    '{\n'
                    '    "groups": [\n'
                    '        {\n'
                    '            "group_name": "Foundation Layer Setup",\n'
                    '            "tasks": [\n'
                    '                {\n'
                    '                    "file_name": "/full/path/to/database/schema.sql",\n'
                    '                }\n'
                    '            ]\n'
                    '        },\n'
                    '        {\n'
                    '            "group_name": "Data Models Implementation",\n'
                    '            "tasks": [\n'
                    '                {\n'
                    '                    "file_name": "/full/path/to/models/user_model.py",\n'
                    '                }\n'
                    '            ]\n'
                    '        },\n'
                    '        {\n'
                    '            "group_name": "Product Model Implementation",\n'
                    '            "tasks": [\n'
                    '                {\n'
                    '                    "file_name": "/full/path/to/models/product_model.py",\n'
                    '                }\n'
                    '            ]\n'
                    '        }\n'
                    '    ],\n'
                    '    "commits": "feature: implement core data models and foundation layer"\n'
                    '}'
                    f"Current working project is {self.repo.get_repo_path()}\n\n"
                    "Return only valid JSON without additional text or formatting."
                )
            },
            {
                "role": "user",
                "content": f"Create a grouped task list following Pyramid architecture using only files from:\n{file_list} - MUST Only include files from the provided 'file_list' for all task, no exception\n\nPrioritize grouping by logical components and system layers (foundation, business logic, integration, UI, etc.). IMPORTANT: SVG files must always be placed in the first group of the plan. Only .svg and .md files can be grouped together in the same group. All code files must be in their own individual groups as they cannot share context when run concurrently. Apply the lead-follow principle across all relevant stacks (e.g., models, views, controllers, HTML, CSS, JS). Place each lead file in its own group to be completed first. Order groups to provide context, adhering to Pyramid principles. Analyze dependencies: if A depends on B, B precedes A. Each file appears once. Always implement smaller, self-contained components first before larger ones to facilitate easier integration and testing. Follow implementation order from original development plan strictly. Original instruction: {instruction}\n\n"
            }
        ]

        try:
            response = await self.ai.arch_prompt(messages, 4096, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### `TaskPlanner` has successfully generated the task plan")
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### `TaskPlanner` has repaired and processed the JSON response")
            return plan_json
        except Exception as e:
            logger.error(f"  `TaskPlanner` encountered an error while generating the task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, instruction, file_lists, original_prompt_language):
        """
        Get development plans based on the user's instruction.

        Args:
            instruction (str): The user's instruction for task planning.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### `TaskPlanner` is generating task plans")
        plan = await self.get_task_plan(instruction, file_lists, original_prompt_language)
        logger.debug("\n #### `TaskPlanner` has completed generating the task plans")
        return plan