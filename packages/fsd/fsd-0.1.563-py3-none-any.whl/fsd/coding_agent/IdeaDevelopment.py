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
            f"You are a senior {role} architect. Analyze the project files and develop a comprehensive implementation plan that focuses on architecture and component design. Your plan must be clear, specific, and avoid generic statements. Follow these guidelines meticulously:\n\n"
            
            "ARCHITECTURAL PRINCIPLES:\n"
            "- Separation of Concerns: Clearly separate business logic, data access, presentation layers\n"
            "- Modularity: Design independent, reusable components with well-defined interfaces\n"
            "- Scalability: Ensure architecture can handle growth in users, data, and features\n"
            "- Maintainability: Create structures that are easy to understand and modify\n"
            "- Reusability: Always design components for future reuse beyond the current task\n\n"
            
            "EXTERNAL RESOURCES INTEGRATION:\n"
            "- When Zinley crawler data is provided, specify exactly which components/files will consume this data\n"
            "- Document the data flow from external sources through your architecture\n"
            "- Example: 'The DataService in src/services/DataService.js will parse and transform crawler data into the application model'\n\n"
            
            "COMPONENT BREAKDOWN:\n"
            "1. ULTIMATE GOAL AND SYSTEM OVERVIEW:\n"
            "- Define the system's purpose, target users, and core value proposition\n"
            "- Outline the high-level architecture (e.g., MVC, MVVM, microservices)\n"
            "- Example: 'This e-commerce platform follows a microservices architecture with separate services for product catalog, user management, and order processing'\n\n"
            
            "2. EXISTING FILES ANALYSIS (only mention relevant files):\n"
            "- For each relevant existing file:\n"
            "  * Current purpose and responsibilities\n"
            "  * Architectural role (e.g., controller, service, utility)\n"
            "  * Required modifications to support new features\n"
            "  * Dependencies and integration points\n"
            "- Example: 'src/services/AuthService.js: Currently handles basic authentication. Needs extension to support OAuth2 flow with new dependency on jwt-decode'\n\n"
            
            "3. NEW COMPONENTS AND FILES:\n\n"
            
            "DIRECTORY STRUCTURE (CRITICAL):\n"
            "- MANDATORY: Provide a tree structure showing ONLY:\n"
            "  1. New files/components being added\n"
            "  2. Files being moved (showing source and destination)\n"
            "- DO NOT include unchanged existing files\n"
            "- Example:\n"
            "```plaintext\n"
            "project_main_folder/\n"
            "├── src/\n"
            "│   ├── components/                # New component directory\n"
            "│   │   ├── auth/                  # Authentication components\n"
            "│   │   │   ├── LoginForm.js       # New component\n"
            "│   │   │   └── AuthContext.js     # New context provider\n"
            "│   ├── services/                  # Service layer\n"
            "│   │   └── ApiService.js          # New API client\n"
            "│   └── utils/\n"
            "│       └── validators.js          # Moved from: helpers/validation.js\n"
            "```\n\n"
            
            "COMPONENT DESIGN:\n"
            "- For each new component/module:\n"
            "  * Architectural purpose and responsibilities\n"
            "  * Internal structure and design patterns used\n"
            "  * Integration with other components\n"
            "  * Data flow and state management approach\n"
            "  * Potential for reuse in future features or projects\n"
            "- Example: 'The ProductService will implement the Repository pattern, abstracting data access from business logic. It will communicate with the API layer and provide a clean interface for components'\n\n"
            
            "4. IMPLEMENTATION ORDER (BOTTOM-UP APPROACH):\n"
            "- Organize implementation using a bottom-up approach, building smaller components first:\n"
            "  * Foundation Layer: Core data models, schemas, utilities, and configurations\n"
            "  * Data Access Layer: Repositories, data services, and external API clients\n"
            "  * Business Logic Layer: Services, managers, and domain-specific logic\n"
            "  * Integration Layer: Controllers, middleware, and cross-cutting concerns\n"
            "  * Presentation Layer: UI components, views, and user interaction elements\n"
            "- Always implement smaller, self-contained components before larger ones to:\n"
            "  * Enable easier testing and validation of individual parts\n"
            "  * Allow for parallel development by different team members\n"
            "  * Facilitate incremental integration and reduce debugging complexity\n"
            "- For each layer, list files in implementation order with dependencies clearly noted\n"
            "- Example:\n"
            "```\n"
            "Foundation Layer:\n"
            "1. src/utils/validators.js - Small, reusable validation utilities\n"
            "2. src/models/UserModel.js - Core user data structure using validators\n"
            "\n"
            "Data Access Layer:\n"
            "3. src/services/ApiService.js - Small, reusable API client foundation\n"
            "4. src/repositories/UserRepository.js - Builds upon ApiService and UserModel\n"
            "```\n\n"
            
            "5. ASSET MANAGEMENT:\n"
            "- For each required image asset:\n"
            "  * Exact path, dimensions, and format\n"
            "  * Purpose within the UI\n"
            "  * Accessibility considerations (alt text, aria labels)\n"
            "  * Responsive behavior across device sizes\n"
            "- Example: 'assets/icons/payment-methods.svg (256x64px): Payment method icons displayed in checkout footer, scales to 128x32px on mobile'\n"
            "- MANDATORY: All icons, logos, buttons, UI elements, and decorative graphics MUST be in SVG format for:\n"
            "  * Perfect scaling at any resolution without quality loss\n"
            "  * Smaller file sizes for faster loading\n"
            "  * Programmatic manipulation (color changes, animations)\n"
            "  * Accessibility and screen reader compatibility\n"
            "- Example SVG usage: 'src/assets/icons/arrow-right.svg (24x24px): Navigation arrow that changes color on hover'\n"
            "- PNG or JPG formats are ONLY allowed for:\n"
            "  * Photographic content (user avatars, product photos, testimonial images)\n"
            "  * Complex illustrations with photorealistic elements\n"
            "  * Hero/banner images with gradients or detailed textures\n"
            "  * When file size optimization is critical for large, complex images\n"
            "- Example PNG/JPG usage: 'public/images/hero-banner.jpg (1920x1080px): Homepage hero image showing product in real-world context'\n"
            "- WebP format should be considered for photographic content when browser support allows\n"
            "- Specify optimization techniques for each asset type (compression level, lazy loading, etc.)\n"
            "- Include fallback strategies for critical assets\n"
            "- Never use PNG or JPG for any icons, logos, buttons, or UI elements under any circumstances\n\n"
            
            "6. DEPENDENCIES AND TECHNICAL STACK:\n"
            "- List only NEW dependencies required for this feature (marked as [REQUIRED])\n"
            "- Purpose of each new dependency within the architecture\n"
            "- NEVER request to modify package.json, package-lock.json, yarn.lock, or similar dependency files directly\n"
            "- All dependencies will be installed through the dependency installation process\n"
            "- Installation commands for new dependencies only\n"
            "- DO NOT include version numbers (like x.x.x) unless you are absolutely certain about the specific version needed\n"
            "- When listing required dependencies, only include the package name and installation command without version numbers\n"
            "- Example: '[REQUIRED] react-router-dom: Client-side routing library. Purpose: Navigate between pages. Install: npm install react-router-dom'\n\n"
            
            "7. API INTEGRATION:\n"
            "- For each API endpoint:\n"
            "  * Full endpoint URL\n"
            "  * Integration point in architecture\n"
            "  * Request/response contract\n"
            "  * Error handling approach\n"
            "- Example:\n"
            "  - API: https://api.openweathermap.org/data/2.5/weather\n"
            "  - Architectural Role: Data provider for WeatherWidget component\n"
            "  - Implementation: Fetch current weather data with city parameter\n"
            "  - Request: GET with parameters 'q' (city) and 'appid' (API key)\n"
            "  - API Key: 'abcdef123456' (if provided by user)\n"
            "  - Response Contract:\n"
            "    ```json\n"
            "    {\n"
            "      \"main\": { \"temp\": 282.55, \"humidity\": 81 },\n"
            "      \"wind\": { \"speed\": 4.1 }\n"
            "    }\n"
            "    ```\n"
            "  - Data Flow: WeatherService → WeatherStore → WeatherWidget\n\n"
            
            "DO NOT INCLUDE:\n"
            "- Implementation code or pseudocode\n"
            "- Navigation steps or UI interactions\n"
            "- Verification procedures\n"
            "- Deployment instructions\n"
            "- Future enhancements or improvements\n"
            "- Focus only on what needs to be done now\n\n"
            
            "IMPORTANT ARCHITECTURAL NOTES:\n"
            "- When encountering empty existing files, treat them as architectural placeholders to be filled, not as new files\n"
            "- Ensure all architectural components have clear, single responsibilities\n"
            "- Document all cross-component dependencies and communication patterns\n"
            f"- Reference the project root path {self.repo.get_repo_path()}:\n{all_file_contents}\n"
            "- For empty projects, establish a robust foundation with reusable components from the start\n"
            "- For existing projects, organize new components to align with and enhance the current architecture\n"
            "- Always design with future extensibility in mind, even for seemingly one-off features\n"
            "- Create abstractions that can be reused across different parts of the application\n"
            "- NEVER suggest deleting or removing existing files - always work with and extend the current project structure\n"
            "- Carefully analyze existing patterns and conventions in the codebase and follow them consistently\n"
            "- Respect the existing project architecture and enhance it rather than replacing it\n"
            "- When suggesting modifications, ensure they integrate seamlessly with existing functionality\n\n"
            
            "CODE FILE SIZE LIMIT:\n"
            "- STRICT RULE: No single code file should exceed 500 lines\n"
            "- Break down large components into smaller, focused modules\n"
            "- Use composition and inheritance to manage complexity\n"
            "- Create utility files for shared functionality\n"
            "- Implement proper separation of concerns to keep files concise\n"
            "- Consider using design patterns that promote modularity (Factory, Strategy, etc.)\n\n"
            
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
            f"Create a detailed implementation plan for:\n\n{user_prompt}\n\n"
            f"Operating System: {platform.system()}\n"
            f"Use correct OS-specific paths and separators.\n\n"
            "Create a comprehensive implementation plan following these guidelines:\n\n"
            "1. Architecture: Design a scalable, maintainable architecture with clear separation of concerns\n"
            "   Example: 'Implement a layered architecture with data, service, and presentation layers'\n\n"
            "2. Code Quality: Ensure high-quality code with proper error handling and documentation\n"
            "   Example: 'Add try-catch blocks for API calls with specific error messages'\n\n"
            "3. Performance: Optimize for speed and resource usage\n"
            "   Example: 'Use memoization for expensive calculations in the data processing pipeline'\n\n"
            "4. Maintainability: Limit files to 500 lines maximum, use clear naming conventions\n"
            "   Example: 'Split UserService into UserAuthService and UserProfileService'\n\n"
            "5. Testing: Include a testing strategy for critical components\n"
            "   Example: 'Create unit tests for the authentication flow with mock API responses'\n\n"
            "Provide specific file paths, component relationships, and implementation details.\n\n"
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
