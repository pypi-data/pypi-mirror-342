import os
import aiohttp
import asyncio
import json
import sys
from json_repair import repair_json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.util.utils import process_image_files
logger = get_logger(__name__)

class ContextPrepareAgent:
    def __init__(self, repo):
        """
        Initialize the ContextPrepareAgent with the repository.

        Args:
            repo: The repository object containing project information.
        """
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_file_planning(self, idea, file_attachments, focused_files, assets_link):

        """
        Request file planning from AI for a given idea and project structure.

        Args:
            idea (str): The user's task or development plan.
            file_attachments (list): List of attached files.
            focused_files (list): List of files the user is focusing on.
            assets_link (list): List of asset links.

        Returns:
            dict: JSON response with the plan including working files and context files.
        """
        logger.debug("\n #### Context prepare agent is initiating file planning process")
        prompt = (
            "Based on the provided development plan and project structure, create a JSON response with a 'working_files' list. "
            "The response should be valid JSON without any additional text or formatting. "
            "'working_files' should include full paths for up to 7 most relevant existing files that are directly related to this task. "
            "Include only files that are absolutely necessary for the task's completion. "
            "Files should be prioritized based on: "
            "1. Files explicitly mentioned in user attachments "
            "2. Files the user is currently focused on "
            "3. Files from the project tree that are directly related to the task "
            "4. The main linter/formatter config file if it exists "
            "Important guidelines: "
            "- Include complete file paths from project root, matching exactly as they appear in the structure "
            "- Only include files that actually exist in the project "
            "- Exclude third-party libraries, generated folders, and dependency files (node_modules/, build/, etc.) "
            "- For dependencies, only include primary manifest files (package.json, pom.xml, etc.) "
            "- Exclude all image and media files (.png, .jpg, .mp4, etc.) "
            "- Return an empty list if no relevant files are found "
            "Use this JSON format:"
            "{\n"
            "    \"working_files\": [\"/absolute/path/to/project/root/folder1/subfolder/file1.extension\", \"/absolute/path/to/project/root/folder2/file2.extension\"],\n"
            "}\n\n"
            "If the list is empty, return:"
            "{\n"
            "    \"working_files\": [],\n"
            "}\n\n"
            f"The current project path is \"{self.repo.get_repo_path()}\". Ensure all file paths start with this project path and EXACTLY match the paths in the provided project structure.\n"
            "Return only valid JSON without Markdown symbols or invalid escapes."
        )

        all_focused_files_contents = ""
        all_attachment_file_contents = ""

        if focused_files:
            for file_path in focused_files:
                file_content = read_file_content(file_path)
                if file_content:
                    all_focused_files_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if all_focused_files_contents:
            prompt += f"\nUser has focused on these files in the current project, MUST include those files in working_files and find relevant context files related to those attached: {all_focused_files_contents}"

        # Process image files
        image_files = process_image_files(file_attachments)
        
        # Remove image files from file_attachments
        file_attachments = [f for f in file_attachments if not f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))]

        if file_attachments:
            for file_path in file_attachments:
                file_content = read_file_content(file_path)
                if file_content:
                    all_attachment_file_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if all_attachment_file_contents:
            prompt += f"\nUser has attached these files for you, use them appropriately: {all_attachment_file_contents}"

        user_content = [{"type": "text", "text": prompt}]

        # Add image files to the user content
        for base64_image in image_files:
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"{base64_image}"
                }
            })

        if assets_link:
            for image_url in assets_link:
                user_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                })
                
        messages = [
            {
                "role": "system",
                "content": user_content
            },
            {
                "role": "user",
                "content": f"This is the user's request to do:\n{idea}\nThis is the current project structure:\n{self.repo.print_summarize_with_tree()}\n"
            }
        ]

        try:
            logger.debug("\n #### Context prepare agent is sending request to AI for file planning")
            response = await self.ai.prompt(messages, 4096, 0.2, 0.1)
            logger.debug("\n #### Context prepare agent has received response from AI")
            plan_json = json.loads(response.choices[0].message.content)
            
            # Ensure working_files list exists and contains only unique elements
            plan_json["working_files"] = list(set(plan_json.get("working_files", [])))
            
            return plan_json
        except json.JSONDecodeError:
            logger.debug("\n #### Context prepare agent encountered JSON decode error, attempting repair")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"  Context prepare agent encountered an error: `{e}`")
            return {
                "working_files": [],
                "reason": str(e)
            }

    async def get_file_plannings(self, idea, focused_files):
        logger.debug("\n #### Context prepare agent is starting file planning process")
        return await self.get_file_planning(idea, focused_files)
