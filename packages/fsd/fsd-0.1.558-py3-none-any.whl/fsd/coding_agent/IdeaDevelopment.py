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

        all_file_contents = self.repo.print_tree()

        system_prompt = (
            f"You are a senior {role}. Analyze the project files and develop a comprehensive implementation plan, must be clear, do not mention something too generic, clear for focus only please. Follow these guidelines meticulously:\n\n"
            "Guidelines:\n"
            "- External Resources: Integrate Zinley crawler data properly when provided later. Specify files needing crawled data.\n"
            "- File Integrity: Modify existing files or create new ones as needed.\n" 
            "- README: Note if updates needed\n"
            "- Structure: Use clear file/folder organization\n"
            "- UI: Design for all platforms\n\n"

            "1. Strict Guidelines:\n\n"

            "1.0 Ultimate Goal:\n"
            "- State the project's goal, final product's purpose, target users, and how it meets their needs. Concisely summarize objectives and deliverables.\n\n"

            "1.1 Existing Files (mention if need for this task only):\n"
            "- Provide thorough descriptions of implementations in existing files, specifying the purpose and functionality of each.\n"
            "- Suggest necessary algorithms, dependencies, functions, or classes for each existing file.\n"
            "- Identify dependencies or relationships with other files and their impact on the system architecture.\n"
            "- Describe the use of image, video, or audio assets in each existing file, specifying filenames, formats, and their placement.\n"

            "1.2 New Files:\n\n"

            "CRITICAL: Directory Structure\n"
            "- MANDATORY: Provide a tree structure that ONLY shows:\n"
            "  1. New files being added\n"
            "  2. Files being moved (must show source and destination)\n"
            "- DO NOT include existing files that are only being modified\n"
            "- DO NOT include directories not directly involved in additions/moves\n"
            "Example of CORRECT tree structure:\n"
            "```plaintext\n"
            "project_root/\n"
            "├── src/                          # New file being added here\n"
            "│   └── components/\n"
            "│       └── Button.js             # New file\n"
            "└── new_location/                 # File being moved here\n"
            "    └── utils.js                  # Moved from: old/location/utils.js\n"
            "```\n\n"

            "File Organization:\n"
            "- Plan files organization deeply following enterprise setup standards. Ensure that the file hierarchy is logical, scalable, and maintainable.\n"
            "- Provide comprehensive details for implementations in each new file, including the purpose and functionality.\n"
            "- Mention required algorithms, dependencies, functions, or classes for each new file.\n"
            "- Explain how each new file will integrate with existing files, including data flow, API calls, or interactions.\n"
            "- Describe the usage of image, video, or audio assets in new files, specifying filenames, formats, and their placement.\n"
            "- Provide detailed descriptions of new images, including content, style, colors, dimensions, and purpose. Specify exact dimensions and file formats per guidelines (e.g., Create `latte.svg` (128x128px), `cappuccino.png` (256x256px)).\n"
            "- For new social media icons, specify the exact platform (e.g., Facebook, TikTok, LinkedIn, Twitter) rather than using generic terms like 'social'. Provide clear details for each icon, including dimensions, styling, and file format.\n"
            "- For all new generated images, include the full path for each image (e.g., `assets/icons/latte.svg`, `assets/products/cappuccino.png`, `assets/icons/facebook.svg`).\n"
            f"-Mention the main new project folder for all new files and the current project root path: {self.repo.get_repo_path()}.\n"
            "- Ensure that all critical files organization planning are included in the plan such as `index.html` at the root level for web projects, `index.js` for React projects, etc. For JavaScript projects, must check for and include `index.js` in both client and server directories if applicable. For other project types, ensure all essential setup and configuration files are accounted for.\n"
            "- Never propose creation of files that cannot be generated through coding, such as fonts, audio files, or special file formats. Stick to image files (SVG, PNG, JPG), coding files (all types), and document files (e.g., .txt, .md, .json).\n"

            "1.4 Dependencies: (Don't have to mention if no relevant)\n"
            "- List all essential dependencies, indicating if already installed\n"
            "- Use latest versions unless specific versions requested\n" 
            "- Only include CLI-installable dependencies (npm, pip, etc)\n"
            "- Provide exact installation commands\n"
            "- Ensure all dependencies are compatible\n\n"

            "1.5 API Usage\n"
            "If any API needs to be used or is mentioned by the user:\n"
            "- Specify the full API link in the file that needs to implement it\n"
            "- Clearly describe what needs to be done with the API. JUST SPECIFY EXACTLY THE PURPOSE OF USING THE API AND WHERE TO USE IT.\n"
            "- MUST provide ALL valuable information for the input and ouput, such as Request Body or Response Example, and specify the format if provided.\n"
            "- If the user mentions or provides an API key, MUST clearly state the key so other agents have context to code.\n"
            "Example:\n"
            f"- {self.repo.get_repo_path()}/api_handler.py:\n"
            "  - API: https://api.openweathermap.org/data/2.5/weather\n"
            "  - Implementation: Use this API to fetch current weather data for a specific city.\n"
            "  - Request: GET request with query parameters 'q' (city name) and 'appid' (API key)\n"
            "  - API Key: If provided by user, mention it here (e.g., 'abcdef123456')\n"
            "  - Response: JSON format\n"
            "    Example response:\n"
            "    {\n"
            "      \"main\": {\n"
            "        \"temp\": 282.55,\n"
            "        \"humidity\": 81\n"
            "      },\n"
            "      \"wind\": {\n"
            "        \"speed\": 4.1\n"
            "      }\n"
            "    }\n"
            "  - Extract 'temp', 'humidity', and 'wind speed' from the response for display.\n"

            "DO NOT MENTION THESE ACTIONS - (SINCE THEY WILL BE HANDLED AUTOMATICALLY): \n"
            "- Navigating to any location\n"
            "- Opening browsers or devices\n"
            "- Opening files\n"
            "- Any form of navigation\n"
            "- Verifying changes\n"
            "- Any form of verification\n"
            "- Clicking, viewing, or any other non-coding actions\n"

            "Important: When you encounter a file that already exists but is empty, do not propose to create a new one. Instead, treat it as an existing file and suggest modifications or updates to it.\n"
            "FOR EACH FILE THAT NEEDS TO BE WORKED ON, WHETHER NEW, EXISTING, OR IMAGE, BE CLEAR AND SPECIFIC. MENTION ALL DETAILS, DO NOT PROVIDE ASSUMPTIONS, GUESSES, OR PLACEHOLDERS.\n"
            "No Yapping: Provide concise, focused responses without unnecessary elaboration or repetition. Stick strictly to the requested information and guidelines.\n\n"
            "Only return sections that are needed for the user request. Do not return non-relevant sections. STRICTLY ENFORCE IMAGE FORMAT RULES:\n\n"
            "- ONLY consider PNG, png, JPG, jpg, JPEG, jpeg, or .ico formats as eligible images\n"
            "- IMMEDIATELY REJECT any other image formats including SVG\n"
            "- SVG or other formats DO NOT COUNT as images needing generation\n"
            "- Only flag image generation if the plan EXPLICITLY includes generating new images in the eligible formats\n\n"
            "Special ending rules:\n"
            "- If plan includes BOTH dependencies AND new images in eligible formats: End with #### DONE: *** - D*** I**\n" 
            "- If ONLY dependencies need installing: End with #### DONE: *** - D***\n"
            "- If ONLY new eligible format images need generating: End with #### DONE: *** - I**\n"
            "- If NO dependencies AND NO eligible format images: No special ending"
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current project structure and files summary:\n{all_file_contents}\n"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! Give me user prompt so i can support them."})

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
                self.conversation_history.append({"role": "user", "content": f"This is data for potential existing files you may need to modify or update or provided context. Even if a file's content is empty. \n{all_working_files_contents}"})
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
            self.conversation_history.append({"role": "user", "content": f"User has attached these files for you, use them appropriately: {all_attachment_file_contents}"})
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
                "For each image, describe:\n"
                "1. Visual Elements:\n"
                "   - Shapes, colors (hex codes), alignment\n"
                "   - Layout and spacing\n\n"
                "2. Content:\n"
                "   - Text, fonts, sizes\n"
                "   - Icons and graphics\n\n" 
                "3. Implementation:\n"
                "   - Dimensions and spacing\n"
                "   - Component structure\n\n"
                "4. Purpose:\n"
                "   - Replica vs inspiration\n"
                "   - Alignment with requirements\n\n"
                "Description must enable perfect implementation without original image."
            )
            self.conversation_history.append({"role": "user", "content": image_detail_prompt})
            self.conversation_history.append({"role": "assistant", "content": "I will analyze each image with extreme detail, providing comprehensive specifications for all visual elements, content, measurements, and implementation requirements. My descriptions will be precise enough to enable perfect reproduction based on the user's needs for either exact replication or inspiration."})

    async def get_idea_plan(self, user_prompt, original_prompt_language):
        logger.debug("Generating idea plan based on user prompt")
        prompt = (
            f"Create a detailed implementation plan for:\n\n{user_prompt}\n\n"
            f"Operating System: {platform.system()}\n"
            f"Use correct OS-specific paths and separators.\n\n"
            f"#### Project Overview\n"
            f"- Ultimate goal and objectives\n"
            f"- Desired outcome\n"
            f"- Success criteria\n\n"
            "#### Design System\n"
            "1. Visual Language:\n"
            "   - Color palette (hex codes)\n" 
            "   - Typography:\n"
            "     * System fonts only: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial\n"
            "     * Font sizes (rem):\n"
            "       - h1: 2rem\n"
            "       - h2: 1.75rem \n"
            "       - h3: 1.5rem\n"
            "       - Body: 1rem\n"
            "       - Small: 0.875rem\n"
            "   - Layout principles\n\n"
            "2. Core Features:\n"
            "   - Essential components\n"
            "   - Key functionality\n"
            "   - Navigation structure\n\n"
            "#### Implementation Requirements\n"
            "For each file:\n"
            "1. Current state\n"
            "2. Required changes\n"
            "3. Technical details\n"
            "4. Integration points\n\n"
            "#### Asset Requirements\n"
            "For each NEW image to generate:\n"
            "1. File path: /full/path/to/save/image\n"
            "2. Format: SVG/PNG/JPG\n"
            "3. Size: Exact dimensions in pixels\n"
            "4. Detailed description:\n"
            "   - Visual elements\n"
            "   - Colors (hex codes)\n"
            "   - Layout/composition\n"
            "   - Text/fonts if any\n"
            "   - Style/mood\n\n"
            "For each EXISTING image:\n"
            "1. Current file path\n"
            "2. How it will be used\n"
            "3. Any required modifications\n\n"
            "SVG (mandatory for):\n"
            "- ALL icons and UI elements\n"
            "- ALL logos and brand assets\n\n"
            "PNG/JPG for:\n"
            "- Complex images\n"
            "- Photos\n"
            "- Banner graphics\n\n"
            "Standard Sizes:\n"
            "- Icons: 24x24px to 512x512px\n"
            "- Images: 400x400px to 2048x2048px\n\n"
            f"#### Dependencies\n"
            f"If needed, specify {platform.system()}-specific install commands:\n"
            f"```bash\n"
            f"npm install [package]@[version]\n"
            f"pip install [package]==[version]\n"
            f"```\n\n"
            f"Response language: {original_prompt_language}\n\n"
            "Only include relevant sections. No implementation code.\n"
            "If plan needs dependencies and new PNG/JPG/JPEG/ico images: end with #### DONE: *** - D*** I**\n"
            "If only dependencies needed: end with #### DONE: *** - D***\n"
            "If only images needed: end with #### DONE: *** - I**\n"
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
