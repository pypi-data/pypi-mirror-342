import os
import sys
from datetime import datetime
import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.util.utils import process_image_files
logger = get_logger(__name__)

class CodingAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def get_current_time_formatted(self):
        """Return the current time formatted as mm/dd/yy."""
        current_time = datetime.now()
        formatted_time = current_time.strftime("%m/%d/%y")
        return formatted_time

    def initial_setup(self, context_files, instructions, context, crawl_logs, file_attachments, assets_link):
        """Initialize the setup with the provided instructions and context."""

        tree = self.repo.print_tree()

        logger.debug("\n #### The `SnowX` is initializing setup with provided instructions and context")

        prompt = f"""You are an expert software engineer specializing in coding, develop the best software product. Follow these guidelines strictly when responding to instructions:

                **Response Guidelines:**
                1. Use ONLY the following SEARCH/REPLACE block format for ALL code changes, additions, or deletions:

                   <<<<<<< SEARCH
                   [Existing code to be replaced, if any]
                   =======
                   [New or modified code]
                   >>>>>>> REPLACE

                2. For new code additions, use an empty SEARCH section:

                   <<<<<<< SEARCH
                   =======
                   [New code to be added]
                   >>>>>>> REPLACE

                3. CRITICAL: The SEARCH section MUST match the existing code with EXACT precision - every character, whitespace, indentation, newline, and comment must be identical.
                   - If the file contains code or other data wrapped/escaped in json/xml/quotes or other containers, you need to propose edits to the literal contents of the file, including the container markup.

                4. For large files, focus on relevant sections. Use comments to indicate skipped portions:
                   // ... existing code ...

                5. MUST break complex changes or large files into multiple SEARCH/REPLACE blocks.
                   - Keep SEARCH/REPLACE blocks concise
                   - Break large changes into a series of smaller blocks that each change a small portion of the file
                   - Include just the changing lines, and a few surrounding lines if needed for uniqueness
                   - Do not include long runs of unchanging lines

                6. CRITICAL: NEVER provide code snippets, suggestions, or examples outside of SEARCH/REPLACE blocks. ALL code must be within these blocks.

                7. Do not provide explanations, ask questions, or engage in discussions. Only return SEARCH/REPLACE blocks.

                8. If a request cannot be addressed solely through SEARCH/REPLACE blocks, do not respond.

                9. CRITICAL: Never include code markdown formatting, syntax highlighting, or any other decorative elements. Code must be provided in its raw form.

                10. STRICTLY FORBIDDEN: Do not hallucinate, invent, or make assumptions about code. Only provide concrete, verified code changes based on the actual codebase.

                11. MANDATORY: Code must be completely plain without any formatting, annotations, explanations or embellishments. Only pure code is allowed.

                12. SEARCH/REPLACE blocks will only replace the first match occurrence. Include multiple unique blocks if needed.

                13. Only create SEARCH/REPLACE blocks for files that have been added to the chat.

                14. To move code within a file, use 2 SEARCH/REPLACE blocks:
                    - One to delete it from its current location
                    - One to insert it in the new location

                Remember: Your responses should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed.

        """

        self.conversation_history = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Development plan: {instructions['Implementation_plan']}"},
            {"role": "assistant", "content": "I'll follow this implementation plan carefully, ensuring each component is built with precision and purpose."},
            {"role": "user", "content": f"Current working file: {context}"},
            {"role": "assistant", "content": "I'll focus on this file for implementation, applying best practices for clean, maintainable, and efficient code."},
            {"role": "user", "content": f"Reference the project root path {self.repo.get_repo_path()}:\n{tree}\n"},
            {"role": "assistant", "content": "I understand the project structure and will ensure correct import paths and directory references. I'll maintain architectural integrity while delivering elegant solutions that balance technical excellence with intuitive user experience. My code will be robust, well-tested, and follow industry standards for both backend logic and frontend interfaces."},
        ]
        if context_files:
            all_file_contents = ""

            for file_path in context_files:
                file_content = read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}\n{file_content}"

            self.conversation_history.append({
                "role": "user", 
                "content": (
                    "These context files provide essential background information for this task. "
                    "Use them to understand the project architecture, dependencies, and existing patterns. "
                    "Do NOT modify these files directly, only use them as reference:\n"
                    f"{all_file_contents}"
                )
            })
            self.conversation_history.append({
                "role": "assistant", 
                "content": "I've analyzed these context files to understand the project structure and implementation patterns. I'll ensure my changes maintain consistency with the existing codebase while delivering elegant, maintainable solutions that follow best practices."
            })

        if crawl_logs:
            self.conversation_history.append({
                "role": "user", 
                "content": (
                    "These crawl logs contain important process information and execution details. "
                    "Use them to understand the system's behavior and runtime characteristics. "
                    "Ensure your implementation handles similar execution paths correctly, optimizes performance, and maintains robust error handling:\n"
                    f"{crawl_logs}"
                )
            })
            self.conversation_history.append({
                "role": "assistant", 
                "content": "I've reviewed these logs to understand the system's behavior and execution flow. My implementation will handle these scenarios correctly with optimized algorithms, clean architecture, intuitive UI/UX design principles, comprehensive error handling, and thorough test coverage to ensure reliability across all execution paths."
            })

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
            self.conversation_history.append({
                "role": "user", 
                "content": (
                    "These user-provided files contain specific requirements, examples, or reference implementations. "
                    "Follow these specifications precisely when implementing the requested changes. "
                    "These files take precedence over general implementation patterns:\n"
                    f"{all_attachment_file_contents}"
                )
            })
            self.conversation_history.append({
                "role": "assistant", 
                "content": (
                    "I'll implement the changes according to these specifications while maintaining compatibility with the existing codebase. "
                    "As an expert-level coding agent, I commit to delivering solutions that demonstrate:"
                    "\n- Flawless logic with optimized algorithms and data structures"
                    "\n- Elegant architecture following SOLID principles and design patterns"
                    "\n- Intuitive UI/UX with responsive layouts and accessible components"
                    "\n- Robust error handling with graceful degradation"
                    "\n- Comprehensive test coverage across unit, integration, and E2E tests"
                    "\n- Clean, maintainable code with consistent formatting and documentation"
                    "\n- Security-first implementation preventing common vulnerabilities"
                    "\n- Performance optimization for both runtime and memory efficiency"
                )
            })

        # Only add image content if there are images to process
        if image_files or assets_link:
            message_content = [{
                "type": "text", 
                "text": (
                    "These images provide visual context and requirements for the implementation. "
                    "Use them to understand UI/UX requirements, design specifications, or visual references. "
                    "Ensure your implementation precisely matches these visual requirements."
                )
            }]

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
            self.conversation_history.append({
                "role": "assistant", 
                "content": (
                    "I'll ensure my implementation aligns with these visual requirements. As an expert developer, I will:"
                    "\n- Faithfully reproduce all UI elements with pixel-perfect precision"
                    "\n- Implement responsive designs that work across all device sizes"
                    "\n- Ensure accessibility compliance (WCAG) for all interactive elements"
                    "\n- Optimize assets for performance without sacrificing quality"
                    "\n- Maintain consistent visual language throughout the implementation"
                    "\n- Apply animation and transition effects appropriately"
                    "\n- Ensure cross-browser compatibility for all visual components"
                )
            })



    async def get_coding_request(self, file, techStack, codingModel):
        """
        Get coding response for the given instruction and context from Azure OpenAI.

        Args:
            is_first (bool): Flag to indicate if it's the first request.
            file (str): Name of the file to work on.
            techStack (str): The technology stack for which the code should be written.
            prompt (str): The specific task or instruction for coding.

        Returns:
            str: The code response.
        """
        file_name = os.path.basename(file)
        file_ext = os.path.splitext(file_name)[1].lower()
        is_svg = file_ext == '.svg'

        # Read current file content
        current_file_content = read_file_content(file)
        if current_file_content:
            self.conversation_history.append({"role": "user", "content": f"Here is the current content of {file_name} that needs to be updated:\n{current_file_content}\n\nPlease make sure to perform the right implementation matching with all current coding files to work perfectly together and respect the original development plan. Your implementation should integrate seamlessly with the existing codebase structure and functionality."})
            self.conversation_history.append({"role": "assistant", "content": "I'll carefully modify this file according to the requirements while preserving its structure and functionality. I'll ensure my implementation integrates seamlessly with the existing codebase and maintains consistency with other files in the project."})

        lazy_prompt = (
            "You are an expert-level developer who delivers flawless code with these principles:\n\n"
            "1. Technical Excellence - MANDATORY:\n"
            "   - Write clean, maintainable code with optimal algorithms and data structures\n"
            "   - Implement proper error handling, validation, and edge cases\n"
            "   - Follow language-specific best practices and design patterns\n"
            "   - Optimize for performance, security, and scalability\n"
            "   - Never leave TODOs, placeholders, or incomplete implementations\n"
            "   - Use appropriate naming conventions and consistent code style\n"
            "   - Apply proper modularization and encapsulation principles\n\n"
            "2. Complete Implementation - ZERO EXCEPTIONS:\n"
            "   - Deliver production-ready code that can be deployed immediately\n"
            "   - Fully implement all features, including error handling and edge cases\n"
            "   - Make informed architectural decisions based on requirements\n"
            "   - Ensure all code paths are handled, including exceptional scenarios\n"
            "   - Implement proper validation for all inputs and outputs\n"
            "   - Include comprehensive error recovery mechanisms\n"
            "   - Provide complete implementations for all required functionality\n\n"
            "3. UI/UX Excellence - CRITICAL FOR FRONTEND:\n"
            "   - Create pixel-perfect implementations matching designs\n"
            "   - Ensure responsive layouts that work across all devices\n"
            "   - Implement smooth animations and transitions\n"
            "   - Maintain accessibility compliance (WCAG AA minimum)\n"
            "   - Optimize rendering performance and minimize layout shifts\n"
            "   - Implement proper focus management and keyboard navigation\n"
            "   - Handle all interactive states (hover, active, focus, disabled)\n"
            "   - Ensure cross-browser compatibility and consistent rendering\n\n"
            "4. Integration Mastery - ESSENTIAL:\n"
            "   - Ensure seamless integration with existing systems and APIs\n"
            "   - Maintain consistency with established patterns in the codebase\n"
            "   - Consider the entire system architecture in your implementation\n"
            "   - Follow existing conventions for error handling and logging\n"
            "   - Respect existing authentication and authorization mechanisms\n"
            "   - Properly handle asynchronous operations and state management\n"
            "   - Ensure backward compatibility with existing interfaces\n\n"
            "5. Testing & Quality Assurance - NON-NEGOTIABLE:\n"
            "   - Write comprehensive unit, integration, and e2e tests\n"
            "   - Cover edge cases, error scenarios, and happy paths\n"
            "   - Implement proper logging for debugging and monitoring\n"
            "   - Include performance testing for critical operations\n"
            "   - Test for security vulnerabilities and edge cases\n"
            "   - Ensure test coverage for all business-critical functionality\n"
            "   - Implement proper mocking for external dependencies\n\n"
            "6. Documentation & Maintainability - REQUIRED:\n"
            "   - Document complex logic, APIs, and architectural decisions\n"
            "   - Write clear, self-documenting code with meaningful names\n"
            "   - Structure code for future extensibility and maintenance\n"
            "   - Include inline comments for complex algorithms and business rules\n"
            "   - Document public interfaces with parameter descriptions and return values\n"
            "   - Explain architectural decisions and their rationale\n"
            "   - Provide usage examples for reusable components\n"
        )

        # Determine specialized prompt based on file extension
        specialized_prompt = ""
        if is_svg:
            specialized_prompt = (
                "You are a professional SVG designer and developer. Create SVG content that matches the project's requirements.\n\n"
                "SVG Creation Guidelines:\n"
                "- For brand assets (logos, icons):\n"
                "  • CORRECT: `<svg viewBox=\"0 0 100 100\" xmlns=\"http://www.w3.org/2000/svg\"><circle cx=\"50\" cy=\"50\" r=\"40\" fill=\"#FF0000\"/><text x=\"50\" y=\"55\" text-anchor=\"middle\" fill=\"#FFFFFF\" font-family=\"Arial\">Logo</text></svg>`\n"
                "  • INCORRECT: `<svg><circle cx=\"50\" cy=\"50\" r=\"40\" fill=\"red\"/><text>Logo</text></svg>` (missing viewBox, proper attributes)\n"
                "- For UI elements:\n"
                "  • CORRECT: `<svg viewBox=\"0 0 24 24\" aria-labelledby=\"checkboxTitle\" role=\"img\"><title id=\"checkboxTitle\">Checkbox</title><rect x=\"3\" y=\"3\" width=\"18\" height=\"18\" rx=\"2\" fill=\"none\" stroke=\"#333333\" stroke-width=\"2\"/><path d=\"M7 12L10 15L17 8\" stroke=\"#333333\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>`\n"
                "  • INCORRECT: `<svg><rect x=\"0\" y=\"0\" width=\"20\" height=\"20\"/><path d=\"M5 10L10 15L15 5\"/></svg>` (missing accessibility, proper sizing)\n"
                "- For data visualization:\n"
                "  • CORRECT: `<svg viewBox=\"0 0 200 100\" xmlns=\"http://www.w3.org/2000/svg\"><g class=\"bar-chart\"><rect x=\"10\" y=\"10\" width=\"20\" height=\"80\" fill=\"#4285F4\"><title>Q1: 80%</title></rect><!-- Additional bars with proper attributes --></g></svg>`\n"
                "  • INCORRECT: `<svg><rect x=\"10\" y=\"10\" width=\"20\" height=\"80\" fill=\"blue\"/></svg>` (missing semantic grouping, tooltips)\n\n"
                "Technical Requirements:\n"
                "- Use semantic element names (e.g., <g>, <path>, <circle>)\n"
                "- Include proper ARIA attributes for accessibility\n"
                "- Optimize paths and reduce unnecessary nodes\n"
                "- Use viewBox for responsive scaling\n"
                "- Implement smooth animations with <animate> or CSS\n"
                "- Follow SVG 1.1/2.0 specifications\n"
            )
        else:
            specialized_prompt = (
                f"As a senior {techStack} developer, implement code following these guidelines:\n\n"
                "Code Implementation Excellence:\n"
                "- Logical Perfection: Implement robust business logic with comprehensive validation, proper error handling, and thorough edge case management. Ensure all functions have clear inputs, outputs, and side effects. Use strong typing where applicable and validate all parameters.\n"
                "- Architecture Excellence: Follow SOLID principles and established design patterns. Maintain clean separation of concerns with proper layering (presentation, business logic, data access). Use dependency injection for better testability and loose coupling between components.\n"
                "- UI/UX Mastery: Create accessible interfaces following WCAG standards. Implement responsive designs that work across all device sizes. Add appropriate loading states, error states, and success feedback. Ensure keyboard navigation and screen reader compatibility.\n"
                "- Error Handling Excellence: Implement comprehensive error handling with specific error types and informative messages. Add proper logging with contextual information for debugging. Include graceful degradation and recovery mechanisms for critical operations.\n"
                "- Performance Optimization: Optimize rendering and data processing for speed and efficiency. Implement proper caching strategies, lazy loading, and pagination where appropriate. Minimize network requests and optimize bundle sizes.\n"
                "- Security Excellence: Implement proper authentication, authorization, and input validation. Protect against common vulnerabilities (XSS, CSRF, injection attacks). Use secure storage for sensitive data and follow the principle of least privilege.\n"
                "- Testing Thoroughness: Write comprehensive tests covering unit, integration, and edge cases. Include positive and negative test scenarios. Mock external dependencies appropriately and test asynchronous operations correctly.\n"
                "- Documentation Clarity: Provide clear, thorough documentation for all code components. Include purpose, parameters, return values, exceptions, and usage examples. Document architectural decisions and complex algorithms with explanations of the reasoning.\n"
            )

        user_prompt = specialized_prompt + (
            f"Current time (use if relevant): {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo}\n"
            f"Note: Empty file indicator: This file is currently empty, content is \\\"\\\", this is just a note, not content\"'\n"
            f"Note: For empty files, use an empty SEARCH section between SEARCH and ======= markers\n\n"
            f"Expert Coding Reminders:\n"
            f"- Logic: Ensure robust business logic with comprehensive input validation, proper error handling for all edge cases, and defensive programming techniques. Implement thorough validation for all user inputs and API responses.\n"
            f"- Architecture: Maintain clean separation of concerns using layered architecture (presentation, business, data access). Follow established design patterns like Repository, Factory, Strategy, and Observer where appropriate. Use dependency injection for better testability.\n"
            f"- UI/UX: Create accessible interfaces following WCAG standards with proper ARIA attributes. Implement responsive designs with fluid layouts and appropriate breakpoints. Add intuitive user interactions with proper feedback mechanisms, loading states, and error notifications.\n"
            f"- Performance: Optimize rendering and data processing with efficient algorithms. Implement proper caching strategies at multiple levels, lazy loading for resources, pagination for large datasets, and debouncing/throttling for frequent events.\n"
            f"- Security: Implement proper authentication with secure token management, fine-grained authorization checks, and thorough input sanitization. Protect against XSS, CSRF, SQL injection, and other common vulnerabilities. Follow the principle of least privilege.\n"
            f"- Testing: Write comprehensive test suites covering unit tests for individual functions, integration tests for component interactions, and end-to-end tests for critical user flows. Include positive, negative, and boundary test cases.\n"
            f"- Documentation: Provide clear, thorough documentation including function purpose, parameters, return values, exceptions thrown, and usage examples. Document architectural decisions, complex algorithms, and business rules with clear explanations.\n"
            f"- Maintainability: Write clean, self-documenting code with meaningful variable/function names and consistent formatting. Follow the DRY principle and keep functions small and focused on a single responsibility.\n"
            f"- Scalability: Design systems that can handle increasing load with horizontal scaling capabilities. Use asynchronous processing for long-running tasks, implement proper database indexing, and consider eventual consistency where appropriate.\n"
            f"- Error Handling: Implement a comprehensive error handling strategy with specific error types, detailed logging with contextual information, and graceful degradation. Provide user-friendly error messages while logging detailed technical information.\n"
            f"- File Structure: Always check the provided file structure to make correct import paths. Ensure imports match the actual project organization.\n"
            f"- CSS Integration: Match and use CSS files correctly. Reference the right class names and follow the project's styling conventions.\n"
            f"- Tech Stack Alignment: Use syntax and patterns appropriate for the specific technology stack being used.\n"
            f"- Minimal Imports: Only import what is needed and will be used in the implementation.\n"
        )

        user_prompt += f"{lazy_prompt}\n" if not is_svg else ""
        user_prompt += f"I have mentioned all requirement rules, now providing updates for this {file_name}.\n"
        user_prompt += "NOTICE: Your response must contain ONLY SEARCH/REPLACE blocks for code changes. Nothing else is allowed."

        if self.conversation_history and self.conversation_history[-1]["role"] == "user":
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

        self.conversation_history.append({"role": "user", "content": user_prompt})

        try:
            response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
            content = response.choices[0].message.content
            lines = [line.strip() for line in content.splitlines() if line.strip()]
            if lines and ("> REPLACE" in lines[-1] or ">>>>>>> REPLACE" in lines[-1]):
                self.conversation_history.append({"role": "assistant", "content": content})
                return content
            else:
                logger.info(" #### Extending response - generating additional context (1/10)")
                # The response was cut off, need to continue
                continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue ONLY from where you left off without repeating or overlapping any preivous content, do no re-generate the same content which already there from last response for this coding file. Do NOT start from the beginning. Only provide the missing part that completes the last SEARCH/REPLACE block. Ensure the continuation ends with '>>>>>>> REPLACE'."
                
                # Store the initial incomplete response
                initial_content = content
                current_content = initial_content
                
                # Track conversation temporarily but don't add to history yet
                temp_conversation = self.conversation_history.copy()
                temp_conversation.append({"role": "assistant", "content": initial_content})
                temp_conversation.append({"role": "user", "content": continuation_prompt})
                
                # Make up to 10 attempts to get a complete response
                max_attempts = 10
                for attempt in range(1, max_attempts + 1):
                    logger.info(f" #### Extending response - generating additional context ({attempt}/10)")
                    
                    continuation_response = await self.ai.coding_prompt(temp_conversation, 4096, 0.2, 0.1)
                    continuation_content = continuation_response.choices[0].message.content
                    continuation_lines = [line.strip() for line in continuation_content.splitlines() if line.strip()]
                    
                    # Add to the accumulated content
                    current_content += continuation_content
                    
                    # Update temporary conversation
                    temp_conversation.append({"role": "assistant", "content": continuation_content})
                    
                    if continuation_lines and ("> REPLACE" in continuation_lines[-1] or ">>>>>>> REPLACE" in continuation_lines[-1]):
                        # Successfully completed the response
                        self.conversation_history.append({"role": "assistant", "content": current_content})
                        return current_content
                    
                    # Prepare for next attempt if needed
                    if attempt < max_attempts:
                        temp_conversation.append({"role": "user", "content": continuation_prompt})
                
                # If we've reached this point, we've made all attempts and still don't have a complete response
                # Add the best we have to the conversation history
                self.conversation_history.append({"role": "assistant", "content": current_content})
                logger.error(f"  The `SnowX` encountered an error while getting coding request - incomplete response after {max_attempts} attempts")
                return current_content

        except Exception as e:
            logger.error(f" The `SnowX` encountered an error while getting coding request")
            logger.error(f" {e}")
            raise


    async def get_coding_requests(self, file, techStack):
        """
        Get coding responses for a file from Azure OpenAI based on user instruction.

        Args:
            is_first (bool): Flag to indicate if it's the first request.
            file (str): Name of the file to work on.
            techStack (str): The technology stack for which the code should be written.
            prompt (str): The coding task prompt.

        Returns:
            str: The code response or error reason.
        """
        return await self.get_coding_request(file, techStack)

    def clear_conversation_history(self):
        """Clear the conversation history."""
        logger.debug("\n #### The `SnowX` is clearing conversation history")
        self.conversation_history = []

    def destroy(self):
        """De-initialize and destroy this instance."""
        logger.debug("\n #### The `SnowX` is being destroyed")
        self.repo = None
        self.conversation_history = None
        self.ai = None