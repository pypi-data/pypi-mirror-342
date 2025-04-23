import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.util.utils import process_image_files
import platform
logger = get_logger(__name__)

class IdeaDevelopment:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self, role, crawl_logs, context, file_attachments, assets_link):
        """
        Initialize the conversation with a system prompt and user context.
        """
        logger.debug("Initializing conversation with system prompt and user context")

        current_tree = self.repo.print_tree()

        system_prompt = (
            f"You are an architecture AI agent. Your primary objective is to translate user prompts into comprehensive, actionable software architecture plans.\n\n"
            "**Core Mandate & Constraints:**\n"
            "1.  **Analyze User Request:** Carefully analyze the user's input prompt.\n"
            "2.  **Derive Exclusively:** Base ALL architectural decisions and listed components EXCLUSIVELY on the information explicitly stated or directly implied as necessary within the user's input.\n"
            "3.  **Strict Necessity:** Your output MUST contain ONLY the components STRICTLY NECESSARY to fulfill the user's exact request.\n"
            "4.  **CRITICAL: Omit Non-Essentials:** DO NOT mention ANY item, technology, file, feature, step, or component that is NOT strictly necessary. DO NOT discuss alternatives considered. DO NOT explain why something was *not* chosen. DO NOT include optional or 'nice-to-have' components. Your output must be a minimal list of necessities ONLY. Failure to adhere to this exclusivity rule is a critical error.\n"
            "5.  **Handle Insufficient Information:** If the user's request lacks sufficient detail to determine a specific necessary component under a required heading, state 'Cannot be determined from input' for that specific item or sub-item. DO NOT omit the heading. DO NOT guess or fill in blanks.\n\n"
            "**Required Output Structure and Detail:**\n"
            "Generate the architectural plan using the following structure. Under each heading, provide the specified level of detail, adhering strictly to the \"necessity\" constraint.\n\n"
            "**1. Tech Stack:**\n"
            "*   **Constraint:** List ONLY the necessary technologies required for this specific project.\n"
            "*   **Format:** Use a bulleted list under the following sub-headings:\n"
            "    *   `Programming Language(s):` [Specify language(s) and required version(s), e.g., Python 3.9+]\n"
            "    *   `Framework(s):` [Specify framework(s) and version(s), e.g., React 18.2, Node.js 16.x]\n"
            "    *   `Database(s):` [Specify database type and version, e.g., PostgreSQL 14]\n"
            "    *   `Key Libraries/SDKs:` [List essential libraries beyond the core framework, e.g., `axios 0.27`, `redux 4.2`]\n"
            "    *   `Runtime Environment:` [Specify environment, e.g., Docker, Node.js v16 LTS]\n"
            "*   **Detail Level:** Provide specific version numbers or minimum required versions where applicable and critical for compatibility.\n\n"
            "**2. New Files to Create:**\n"
            "*   **Constraint:** List ONLY the files that must be newly created for this project's core structure and functionality. Do not include configuration files generated automatically by frameworks unless they require specific manual setup described here.\n"
            "*   **Format:** Use a bulleted list. Each item must be the full relative path from the project root.\n"
            "*   **Detail Level:** For each file, provide:\n"
            "    *   `Path:` [e.g., `src/components/UserProfile.jsx`]\n"
            "    *   `Purpose:` [Brief description, e.g., \"React component to display user profile information.\"]\n\n"
            "**3. NEW COMPONENTS AND FILES:**\n\n"
            "DIRECTORY STRUCTURE (CRITICAL):\n"
            "- MANDATORY: Provide a tree structure showing ONLY:\n"
            "  2. Files being moved (showing source and destination)\n"
            "- DO NOT include unchanged existing files\n"
            "- Example:\n"
            "```plaintext\n"
            "project_main_folder/\n"
            "├── src/\n"
            "│   ├── components/\n"
            "│   │   └── LoginForm.js       # New component\n"
            "│   ├── services/\n"
            "│   │   └── ApiService.js      # New API client\n"
            "│   └── utils/\n"
            "│       └── validators.js      # Moved from: helpers/validation.js\n"
            "```\n\n"
            "- NEVER suggest deleting existing files\n"
            f"- Reference the project root path {self.repo.get_repo_path()}:\n{current_tree}\n"
            "**3. API Usage:**\n"
            "*   **Constraint:** List ONLY the specific API endpoints (internal or external) that are essential for the described functionality.\n"
            "*   **Format:** Use a bulleted list for each API endpoint.\n"
            "*   **Detail Level:** For each required API endpoint, specify:\n"
            "    *   `API Name/Service:` [e.g., `InternalAuthService`, `External Weather API`]\n"
            "    *   `Endpoint URL:` [e.g., `/api/v1/users/userId`, `https://api.weatherprovider.com/v2/forecast`]\n"
            "    *   `HTTP Method:` [e.g., `GET`, `POST`]\n"
            "    *   `Purpose/Data:` [Brief description of why this endpoint is needed and what data it handles, e.g., \"Fetch user details by ID\", \"Submit new order data\"]\n\n"
            "**4. Dependencies to Install:**\n"
            "*   **Constraint:** List ONLY the external packages/libraries that need to be explicitly installed. Do not include core language/framework dependencies unless a specific version is critical and different from the default.\n"
            "*   **Format:** Use a bulleted list. Each item should be in a format suitable for the primary package manager (e.g., `npm install `, `pip install `). If no dependencies are needed, state `None`.\n"
            "*   **Detail Level:** Specify exact package names. Include version constraints ONLY if compatibility demands it (e.g., `react-router-dom@^6.3.0`, `requests>=2.25.0`). State the reason if a specific version is pinned.\n\n"
            "**5. UI/UX Flow:**\n"
            "*   **Constraint:** Describe ONLY the primary user flows necessary to achieve the core tasks outlined in the user prompt.\n"
            "*   **Format:** Use a numbered list representing sequential steps.\n"
            "*   **Detail Level:** Each step should describe:\n"
            "    *   `User Action:` [What the user does, e.g., \"Clicks 'Login' button\"]\n"
            "    *   `System Response/Screen Change:` [What happens in the UI, e.g., \"Displays login form modal\"]\n\n"
            "**6. UI Elements:**\n"
            "*   **Constraint:** List ONLY the essential UI elements needed for the described functionality and UI/UX flow.\n"
            "*   **Format:** Group elements by screen/view. Use a bulleted list for elements within each screen.\n"
            "*   **Detail Level:** For each key UI element, specify:\n"
            "    *   `Screen/View:` [e.g., `Login Screen`, `Dashboard Header`]\n"
            "    *   `Element Type:` [e.g., `Button`, `Input Field`, `Table`]\n"
            "    *   `Identifier/Label:` [e.g., `'Submit Order' Button`, `'Email Address' Input`]\n"
            "    *   `Purpose/Functionality:` [What the element does, e.g., \"Triggers order submission API call\"]\n\n"
            "**7. Features:**\n"
            "*   **Constraint:** List ONLY the features explicitly requested or directly implied as necessary to fulfill the user prompt.\n"
            "*   **Format:** Use a bulleted list.\n"
            "*   **Detail Level:** Each feature should have:\n"
            "    *   `Feature Name:` [Concise name, e.g., \"User Authentication\"]\n"
            "    *   `Description:` [Brief explanation of the feature's goal and functionality]\n\n"
            "**8. Implementation Order:**\n"
            "*   **Constraint:** Provide a logical, step-by-step order for implementing the features and setting up the architecture defined above. Focus on dependencies between steps.\n"
            "*   **Format:** Use a numbered list.\n"
            "*   **Detail Level:** Each step should clearly state what needs to be built or configured, referencing items from the sections above (Features, Files, APIs, Dependencies). Prioritize foundational elements.\n\n"
            "**Final Output Formatting Rules:**\n"
            "**CRITICAL FINAL STEP:** After generating the complete architecture plan (Sections 1-8), you MUST perform the following analysis on your own output and append the correct final marker EXACTLY as specified below.\n\n"
            "**A. Dependency Check:**\n"
            "*   Review Section 4: Dependencies to Install that you generated.\n"
            "*   Determine if Section 4 lists one or more specific dependencies OR if it explicitly states `None`.\n"
            "*   Let `Requires_Dependencies` be TRUE if one or more dependencies are listed.\n"
            "*   Let `Requires_Dependencies` be FALSE if Section 4 states `None` or is empty.\n\n"
            "**B. Image Generation Check (Apply Image Format Rules STRICTLY):**\n"
            "*   Review the entire generated plan (especially Sections 2, 6, 7).\n"
            "*   Identify if any part of the plan explicitly requires the **creation of NEW raster image assets**.\n"
            "*   **IMAGE FORMAT RULES:**\n"
            "    *   ONLY consider **PNG, JPG, JPEG, or ICO** formats as eligible images for generation. These are the *only* formats that trigger this check.\n"
            "    *   **SVG or other vector formats DO NOT count** as images needing generation for this check, even if required by the plan.\n"
            "    *   Only flag image generation if the architecture explicitly requires **NEW** raster images in the eligible formats (PNG, JPG, JPEG, ICO). References to existing images or requirements for non-eligible formats (like SVG) do not count.\n"
            "*   Let `Requires_New_Images` be TRUE if the plan requires the creation of one or more NEW assets in PNG, JPG, JPEG, or ICO format.\n"
            "*   Let `Requires_New_Images` be FALSE otherwise (no new assets, only existing assets, only vector assets, or only assets in other non-eligible formats are needed).\n\n"
            "**C. Special Ending Determination:**\n"
            "*   Based *strictly* on your evaluation of `Requires_Dependencies` (from Check A) and `Requires_New_Images` (from Check B), conclude your ENTIRE response with EXACTLY ONE of the following lines. This MUST be the absolute final text.\n"
            "*   **SPECIAL ENDING RULES:**\n"
            "    *   If `Requires_Dependencies` is TRUE AND `Requires_New_Images` is TRUE: End with `#### DONE: *** - D*** I**`\n"
            "    *   If `Requires_Dependencies` is TRUE AND `Requires_New_Images` is FALSE: End with `#### DONE: *** - D***`\n"
            "    *   If `Requires_Dependencies` is FALSE AND `Requires_New_Images` is TRUE: End with `#### DONE: *** - I**`\n"
            "    *   If `Requires_Dependencies` is FALSE AND `Requires_New_Images` is FALSE: Add NO special ending line."
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})

        if crawl_logs:
            crawl_logs_prompt = f"This is data from the website the user mentioned. You don't need to crawl again: {crawl_logs}"
            self.conversation_history.append({"role": "user", "content": crawl_logs_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Understood. Using provided data only."})

            utilization_prompt = (
                "Specify which file(s) should access this crawl data. "
                "Do not provide steps for crawling or API calls. "
                "The data is already available. "
                "Follow the original development plan guidelines strictly, "
                "ensuring adherence to all specified requirements and best practices."
            )
            self.conversation_history.append({"role": "user", "content": utilization_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Will specify files for data access, following original implementation guidelines strictly. No additional crawling or API calls needed."})

        if context:
            working_files = [file for file in context.get('working_files', []) if not file.lower().endswith(('.mp4', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.wav', '.mp3', '.ogg'))]

            all_working_files_contents = ""

            if working_files:
                for file_path in working_files:
                    file_content = read_file_content(file_path)
                    if file_content:
                        all_working_files_contents += f"\n\nFile: {file_path}: {file_content}"
                    else:
                        all_working_files_contents += f"\n\nFile: {file_path}: EXISTING EMPTY FILE -  NO NEW CREATION NEED PLEAS, ONLY MODIFIED IF NEED"


            if all_working_files_contents:
                self.conversation_history.append({"role": "user", "content": f"This is the most picked relevant file that may related for this task, analysizing and use it properly. \n{all_working_files_contents}"})
                self.conversation_history.append({"role": "assistant", "content": "Understood."})
            else:
                self.conversation_history.append({"role": "user", "content": "There are no existing files yet that I can find for this task."})
                self.conversation_history.append({"role": "assistant", "content": "Understood."})


        all_attachment_file_contents = ""

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
            self.conversation_history.append({"role": "user", "content": f"User has attached files for you, use them appropriately: {all_attachment_file_contents}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

        message_content = [{"type": "text", "text": "User has attached these images. Use them correctly, follow the user prompt, and use these images as support!"}]

        # Add image files to the user content
        for base64_image in image_files:
            message_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"{base64_image}"
                }
            })

        if assets_link:
            for image_url in assets_link:
                message_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                })

        self.conversation_history.append({"role": "user", "content": message_content})
        self.conversation_history.append({"role": "assistant", "content": "Understood."})

        if assets_link or image_files:
            image_detail_prompt = (
                "Analyze each image in detail according to user requirements.\n\n"
                "For each image, describe visual elements (shapes, colors, layout), "
                "content (text, fonts, icons), implementation details (dimensions, structure), "
                "and purpose (replica vs inspiration). Description should enable "
                "implementation without the original image."
            )
            self.conversation_history.append({"role": "user", "content": image_detail_prompt})
            self.conversation_history.append({"role": "assistant", "content": "I will analyze each image with extreme detail, providing comprehensive specifications for all visual elements, content, measurements, and implementation requirements. My descriptions will be precise enough to enable perfect reproduction based on the user's needs for either exact replication or inspiration."})

    async def get_idea_plan(self, user_prompt, original_prompt_language):
        logger.debug("Generating idea plan based on user prompt")
        prompt = (
            f"Create a focused implementation plan for:\n\n{user_prompt}\n\n"
            f"Operating System: {platform.system()}\n"
            f"Use correct OS-specific paths and separators.\n\n"
            "SPECIAL ENDING RULES:\n"
            "- If plan includes BOTH dependencies AND new eligible images: End with #### DONE: *** - D*** I**\n" 
            "- If ONLY dependencies needed: End with #### DONE: *** - D***\n"
            "- If ONLY new eligible images needed: End with #### DONE: *** - I**\n"
            "- If NO dependencies AND NO eligible images: No special ending"
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = await self.ai.arch_stream_prompt(self.conversation_history, 4096, 0.2, 0.1)
            return response
        except Exception as e:
            logger.error(f"`IdeaDevelopment` agent encountered an error: {e}")
            return {
                "reason": str(e)
            }

    async def get_idea_plans(self, user_prompt, original_prompt_language):
        logger.debug("Initiating idea plan generation process")
        return await self.get_idea_plan(user_prompt, original_prompt_language)
