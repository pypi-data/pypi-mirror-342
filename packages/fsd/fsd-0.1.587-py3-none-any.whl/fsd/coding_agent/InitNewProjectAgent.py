import os
import aiohttp
import asyncio
import json
import sys
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class InitNewProjectAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()
        self.template_repos = {
            1: "https://github.com/Zinley-dev/react-template",
            2: "https://github.com/Zinley-dev/vue-template",
            3: "https://github.com/Zinley-dev/nextjs-template",
            4: "https://github.com/Zinley-dev/angular-template",
            5: "https://github.com/Zinley-dev/svelte-template"
        }

    async def get_initNewProject_plan(self, user_prompt):
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
                    "You are an expert agent that determines if this is a new project or modifications to an existing one. If it's a new project, we need to clone a template repository to start with. Analyze the project structure and user prompt carefully to determine the appropriate action.\n\n"
                    
                    "Available template options:\n"
                    "1. React - For single-page applications with component-based architecture\n"
                    "2. Vue - For progressive JavaScript framework applications\n"
                    "3. Next.js - For React-based server-side rendering and static site generation\n"
                    "4. Angular - For enterprise-scale applications with TypeScript\n"
                    "5. Svelte - For compile-time framework with minimal runtime code\n\n"
                    
                    "Your response must be valid JSON in this exact format:\n"
                    "{\n"
                    '    "pipeline": "number between 0-5",\n'
                    '    "folder_name": "appropriate project folder name"\n'
                    "}\n\n"
                    
                    "Pipeline values:\n"
                    "0: No need for a new project template - modify existing project\n"
                    "1-5: Corresponds to the template options above\n\n"
                    
                    "Rules for template selection:\n"
                    "- If the user explicitly requests a new React project (e.g., 'Create a new React app for a todo list'), use template 1\n"
                    "   Example: 'Build me a React application for tracking expenses' → pipeline: 1, folder_name: 'expense-tracker'\n"
                    "- If the user requests a new Vue project (e.g., 'Start a Vue project for an e-commerce site'), use template 2\n"
                    "   Example: 'I need a Vue.js shopping cart application' → pipeline: 2, folder_name: 'shopping-cart'\n"
                    "- If the user requests a new Next.js project (e.g., 'I need a Next.js blog application'), use template 3\n"
                    "   Example: 'Create a server-rendered Next.js website with blog functionality' → pipeline: 3, folder_name: 'blog-site'\n"
                    "- If the user requests a new Angular project (e.g., 'Create an Angular dashboard application'), use template 4\n"
                    "   Example: 'Build an enterprise dashboard with Angular and TypeScript' → pipeline: 4, folder_name: 'enterprise-dashboard'\n"
                    "- If the user requests a new Svelte project (e.g., 'Build a Svelte app for weather forecasting'), use template 5\n"
                    "   Example: 'I want a lightweight Svelte application for data visualization' → pipeline: 5, folder_name: 'data-viz'\n"
                    "- If a new project is needed but no specific tech stack is mentioned, use React (option 1) as default\n"
                    "   Example: 'Create a new web app for task management' → pipeline: 1, folder_name: 'task-manager'\n"
                    "- If the user is clearly asking to modify an existing project, set pipeline to 0 and folder_name to empty string\n"
                    "   Example: 'Fix the login component in my existing app' → pipeline: 0, folder_name: ''\n"
                    "- If this is an existing well-structured project and the user requests a different tech stack, still return pipeline 0 since we can only clone a template repo for completely new projects\n"
                    "   Example: 'Convert this React app to Vue' → pipeline: 0, folder_name: ''\n"
                    "- If the user requests a new project with a tech stack not in our available template list (e.g., Django, Flask, Express, Laravel, etc.), return pipeline 0\n"
                    "   Example: 'Create a new Django web application' → pipeline: 0, folder_name: ''\n\n"
                    
                    "For folder_name:\n"
                    "- Use kebab-case (lowercase with hyphens) for folder names\n"
                    "- Make it descriptive of the project's purpose\n"
                    "- Keep it concise (typically 1-3 words)\n"
                    "- Ensure it aligns with the user's prompt and project purpose\n"
                    "- If pipeline is 0, set folder_name to an empty string\n\n"
                    
                    "IMPORTANT: Provide ONLY valid JSON with no additional text, explanations, or markdown."
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

    async def clone_template_repository(self, pipeline, folder_name):
        """
        Clone the appropriate project repository based on the pipeline value.
        
        Args:
            pipeline (int): The pipeline value (1-5) representing the project to use.
            folder_name (str): The name of the folder to clone the repository into.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if pipeline == 0 or pipeline == '0':
            return True
            
        try:
            pipeline_int = int(pipeline)
            if pipeline_int < 1 or pipeline_int > 5:
                logger.error(f"Invalid pipeline value: {pipeline}. Must be between 1-5.")
                return False
                
            repo_url = self.template_repos[pipeline_int]
            framework_name = repo_url.split('/')[-1].replace('-template', '')
            
            # Get the absolute path for the target folder
            target_path = os.path.join(self.repo.get_repo_path(), folder_name)
            
            logger.info(f"#### `SnowX` is starting clone of `{framework_name}` project into folder `{folder_name}`")
            logger.info(f"#### Project repository URL: `{repo_url}`")
            logger.info(f"#### Target path: `{target_path}`")
            
            # Create the folder if it doesn't exist
            if not os.path.exists(target_path):
                logger.info(f"#### `SnowX` is creating directory `{folder_name}`")
                os.makedirs(target_path)
            else:
                logger.info(f"#### Directory `{folder_name}` already exists")
                
            # Clone the repository
            logger.info(f"#### `SnowX` is cloning repository... this may take a moment")
            result = subprocess.run(
                ["git", "clone", repo_url, target_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.error(f"Failed to clone repository: {result.stderr}")
                return False
            
            logger.info(f"#### `SnowX` has successfully cloned `{framework_name}` project")
                
            # Remove the .git directory to start fresh
            git_dir = os.path.join(target_path, ".git")
            if os.path.exists(git_dir):
                logger.info(f"#### `SnowX` is removing .git directory to start fresh")
                if os.name == 'nt':  # Windows
                    subprocess.run(["rmdir", "/S", "/Q", git_dir], shell=True)
                else:  # Unix/Linux/MacOS
                    subprocess.run(["rm", "-rf", git_dir])
                    
            logger.info(f"#### Project setup complete: `{framework_name}` in `{folder_name}`")
            return True
            
        except Exception as e:
            logger.error(f"Error cloning project repository: {str(e)}")
            return False
            

    async def get_initNewProject_plans(self, user_prompt):
        plan = await self.get_initNewProject_plan(user_prompt)
        logger.debug(f"`SnowX` has successfully completed preparing for the user prompt: {user_prompt}")
        
        # If plan has a pipeline value that's not 0, clone the appropriate repository
        if 'pipeline' in plan and plan['pipeline'] != 0 and plan['pipeline'] != '0' and 'folder_name' in plan and plan['folder_name']:
            result = await self.clone_template_repository(plan['pipeline'], plan['folder_name'])
            if result:
                plan['template_cloned'] = True
            else:
                logger.info(f" #### `SnowX` failed to clone template repository")
        
        return plan
