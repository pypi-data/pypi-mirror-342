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
            f"You are a senior {role} architect. Analyze the project files and develop a focused implementation plan that prioritizes speed and simplicity. Your plan must be clear, specific, and avoid unnecessary complexity. Follow these guidelines:\n\n"
            
            "ARCHITECTURAL PRINCIPLES:\n"
            "- Simplicity: Favor straightforward solutions over complex architectures but do not compromise on quality\n"
            "- Practicality: Focus on core functionality first, avoid over-engineering\n"
            "- Maintainability: Create structures that are easy to understand\n"
            "- Reusability: Use existing components where possible\n\n"
            
            "EXTERNAL RESOURCES INTEGRATION:\n"
            "- When Zinley crawler data is provided, specify exactly which components/files will consume this data\n"
            "- Keep data flow simple and direct\n"
            "- Example: 'The DataService in src/services/DataService.js will handle crawler data'\n\n"
            
            "COMPONENT BREAKDOWN:\n"
            "1. ULTIMATE GOAL AND SYSTEM OVERVIEW:\n"
            "- Define the system's purpose, target users, and core value proposition\n"
            "- Outline the high-level architecture (e.g., MVC, MVVM, microservices)\n"
            "- Example: 'This e-commerce platform follows a microservices architecture with separate services for product catalog, user management, and order processing'\n\n"
            
            "2. EXISTING FILES ANALYSIS (only mention relevant files):\n"
            "- For each relevant existing file:\n"
            "  * Current purpose and responsibilities\n"
            "  * Required modifications to support new features\n"
            "  * Dependencies and integration points\n"
            "- Example: 'src/services/AuthService.js: Currently handles basic authentication. Needs extension to support OAuth2 flow with new dependency on jwt-decode'\n\n"
            
            "3. NEW COMPONENTS AND FILES:\n\n"
            
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
            
            "COMPONENT DESIGN:\n"
            "- For each new component/module:\n"
            "  * Purpose and responsibilities\n"
            "  * Integration with other components\n"
            "  * Keep designs simple and focused on immediate needs\n"
            "- MANDATORY: Ensure component structure promotes modularity with clear separation of concerns\n"
            "- MANDATORY: Define interfaces between components to minimize coupling\n"
            "- MANDATORY: Specify reusable components that can be shared across features\n\n"
            
            "4. IMPLEMENTATION ORDER:\n"
            "- Organize implementation in a logical sequence:\n"
            "  * Start with core utilities and services\n"
            "  * Then build main components\n"
            "  * Finally integrate everything together\n"
            "- For each step, list files in implementation order\n\n"
            
            "5. FEATURES TO IMPLEMENT (CRITICAL):\n"
            "- List all core features that must be implemented in this iteration\n"
            "- For each feature:\n"
            "  * Detailed functional requirements\n"
            "  * User interaction flow\n"
            "  * Data requirements and storage needs\n"
            "  * Acceptance criteria (how to verify the feature works)\n"
            "- MANDATORY: Prioritize features by importance (Critical, High, Medium)\n"
            "- Example: 'User Authentication (Critical): Allow users to register and login. Requirements: Email/password registration, secure password storage, session management. Acceptance: User can register, login, and access protected routes'\n\n"
            
            "6. DESIGN ELEMENTS AND UI COMPONENTS:\n"
            "- List all UI components needed for implementation\n"
            "- For each component, specify:\n"
            "  * Visual design details (hex colors, typography, spacing)\n"
            "  * Interaction patterns and animations\n"
            "  * Responsive behavior across device sizes\n"
            "- MANDATORY: Include a color system with appropriate color roles using hex values (e.g., primary: #4285F4, secondary: #34A853, etc.)\n"
            "- MANDATORY: Define typography specifications appropriate for the project\n"
            "- Example: 'Navigation Component: Describe layout, hex color scheme (#FFFFFF for background, #333333 for text), typography, animations, and responsive behavior'\n"
            "- Example: 'Content Display Component: Describe layout approach, responsive behavior, and interaction patterns'\n"
            "- MANDATORY: Ensure all interactive elements have appropriate states (hover/focus/active) with specific hex colors for each state\n"
            "- MANDATORY: Consider accessibility requirements including color contrast (using WCAG-compliant hex color combinations) and keyboard navigation\n"
            "- Example: 'Navigation Component: Describe layout, hex color scheme (#FFFFFF for background, #333333 for text), typography, animations, and responsive behavior'\n"
            
            "7. DEPENDENCIES AND TECHNICAL STACK:\n"
            "- List only NEW dependencies required for this feature (marked as [REQUIRED])\n"
            "- Purpose of each new dependency within the architecture\n"
            "- NEVER request to modify package.json, package-lock.json, yarn.lock, or similar dependency files directly\n"
            "- All dependencies will be installed through the dependency installation process\n"
            "- Installation commands for new dependencies only\n"
            "- DO NOT include version numbers (like x.x.x) unless you are absolutely certain about the specific version needed\n"
            "- When listing required dependencies, only include the package name and installation command without version numbers\n"
            "- Example: '[REQUIRED] react-router-dom: Client-side routing library. Purpose: Navigate between pages. Install: npm install react-router-dom'\n\n"
            
            "8. API INTEGRATION:\n"
            "- For each API endpoint:\n"
            "  * Endpoint URL\n"
            "  * Basic request/response information\n"
            "- Example:\n"
            "  - API: https://api.example.com/data\n"
            "  - Purpose: Fetch user data\n"
            "  - Request: GET with user ID parameter\n\n"
            
            "9. README DOCUMENTATION:\n"
            "- ALWAYS include a task to update the existing README.md file or create a new one if it doesn't exist\n"
            "- The README should document:\n"
            "  * Project overview and purpose\n"
            "  * Setup and installation instructions\n"
            "  * Usage examples\n"
            "  * Architecture overview\n"
            "  * API documentation (if applicable)\n"
            "  * Contribution guidelines (if applicable)\n"
            "- Example: 'Update README.md to include new authentication flow documentation and updated installation steps for new dependencies'\n\n"
            
            "DO NOT INCLUDE:\n"
            "- Overly complex architectural patterns\n"
            "- Unnecessary abstraction layers\n"
            "- Future enhancements or improvements\n"
            "- Focus only on what needs to be done now\n\n"
            
            "IMPORTANT NOTES:\n"
            "- Prioritize speed and simplicity over architectural elegance\n"
            "- When encountering empty existing files, treat them as placeholders to be filled\n"
            "- For empty projects, establish a minimal viable structure\n"
            "- For existing projects, make targeted additions that align with current structure\n"
            "- NEVER suggest deleting existing files\n"
            f"- Reference the project root path {self.repo.get_repo_path()}:\n{all_file_contents}\n"
            "- Focus on getting a working solution quickly rather than perfect architecture\n\n"
            
            "CODE FILE SIZE LIMIT:\n"
            "- Keep files concise and focused on specific functionality\n"
            "- Use simple patterns that are easy to understand\n\n"
            
            "IMAGE FORMAT RULES:\n"
            "- ONLY consider PNG, JPG, JPEG, or ICO formats as eligible images for generation\n"
            "- SVG or other vector formats DO NOT count as images needing generation\n"
            "- Only flag image generation if the architecture explicitly requires new raster images\n\n"
            
            "SPECIAL ENDING RULES:\n"
            "- If plan includes BOTH dependencies AND new eligible images: End with #### DONE: *** - D*** I**\n" 
            "- If ONLY dependencies needed: End with #### DONE: *** - D***\n"
            "- If ONLY new eligible images needed: End with #### DONE: *** - I**\n"
            "- If NO dependencies AND NO eligible images: No special ending"
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
            f"Create a focused implementation plan for:\n\n{user_prompt}\n\n"
            f"Operating System: {platform.system()}\n"
            f"Use correct OS-specific paths and separators.\n\n"
            "Create a rapid implementation plan prioritizing speed and simplicity:\n\n"
            "1. Simplicity: Focus on a straightforward solution with minimal complexity\n"
            "   Example: 'Use a single service file with core functions instead of multiple layers'\n\n"
            "3. Practicality: Prioritize working code over perfect architecture\n"
            "   Example: 'Start with a monolithic approach that can be refactored later if needed'\n\n"
            "4. Core Features: Focus on must-have features first, leave nice-to-haves for later\n"
            "   Example: 'Implement basic CRUD operations before adding advanced filtering'\n\n"
            "5. Reuse: Leverage existing libraries and frameworks to minimize custom code\n"
            "   Example: 'Use React Bootstrap components instead of custom CSS'\n\n"
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
