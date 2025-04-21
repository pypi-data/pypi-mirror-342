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

        logger.debug("\n #### The `CodingAgent` is initializing setup with provided instructions and context")

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
            {"role": "user", "content": f"Development plan: {instructions['Implementation_plan']} and original raw request, use if Implementation_plan missing some pieces: {instructions['original_prompt']}"},
            {"role": "assistant", "content": "Understood!"},
            {"role": "user", "content": f"Current working file: {context}"},
            {"role": "assistant", "content": "Understood!"},
        ]

        if context_files:
            all_file_contents = ""

            for file_path in context_files:
                file_content = read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}\n{file_content}"

            self.conversation_history.append({"role": "user", "content": f"These are all the supported files to provide context for this task: {all_file_contents}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood. I'll use this context when implementing changes."})

        if crawl_logs:
            self.conversation_history.append({"role": "user", "content": f"This is supported data for this entire process, use it if appropriate: {crawl_logs}"})
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

        message_content = [{"type": "text", "text": "User has attached these images. Use them correctly, follow the original Development plan, and use these images as support!"}]

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
            self.conversation_history.append({"role": "user", "content": f"Here is the current content of {file_name} that needs to be updated:\n{current_file_content}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood. I'll use this file content as context for the updates."})

        lazy_prompt = "You are diligent and tireless. You NEVER leave comments describing code without implementing it. You always COMPLETELY IMPLEMENT the needed code."

        # Determine specialized prompt based on file extension
        specialized_prompt = ""
        if is_svg:
            specialized_prompt = (
                "Create SVG that matches project's existing visual style and use case.\n"
                "For brand assets and vector graphics:\n"
                "- Keep official colors, proportions and brand identity intact\n"
                "- Follow brand guidelines strictly and maintain visual consistency\n"
                "- For social media icons and logos:\n"
                "  • Respect official brand guidelines and specifications\n"
                "  • Maintain exact proportions defined by brand manuals\n"
                "  • Use official brand colors with correct hex codes\n"
                "  • Keep minimum clear space requirements\n"
                "  • Follow usage restrictions and trademark rules\n"
                "- Optimize SVG code for performance and file size\n"
                "- Ensure cross-browser compatibility and responsiveness\n"
                "- Use semantic element names and proper grouping\n"
                "- Include ARIA labels and accessibility attributes\n"
                "- Implement smooth animations and transitions if needed\n"
            )
        else:
            specialized_prompt = (
                f"As a world-class {techStack} developer:\n"
                "For Code Quality & Style:\n"
                "- Write clean, maintainable code following DRY/KISS principles\n" 
                "- Use meaningful names and proper documentation\n"
                "- Follow consistent formatting and style conventions\n"
                "- Structure code logically with separation of concerns\n"
                "- Handle errors gracefully with proper validation\n"
                "\nFor UI/UX Implementation:\n"
                "- Create clean, responsive designs that work across devices\n"
                "- Use consistent spacing, typography and visual hierarchy\n" 
                "- Follow accessibility best practices (WCAG 2.1)\n"
                "- Optimize performance and loading times\n"
                "- Match existing styling patterns in the codebase\n"
                "\nFor Architecture & Testing:\n"
                "- Write modular, reusable components/functions\n"
                "- Follow tech stack best practices and patterns\n"
                "- Add appropriate tests for functionality\n"
                "- Verify imports exist before using them\n"
                "- Ensure security through proper validation\n"
            )

        user_prompt = specialized_prompt + (
            f"Current time, only use if need: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo}\n"
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
            if lines and "> REPLACE" in lines[-1]:
                self.conversation_history.append({"role": "assistant", "content": content})
                return content
            else:
                logger.info(" #### Extending response - generating additional context (1/10)")
                self.conversation_history.append({"role": "assistant", "content": content})
                # The response was cut off, prompt AI to continue
                continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                self.conversation_history.append({"role": "user", "content": continuation_prompt})

                continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                continuation_content = continuation_response.choices[0].message.content
                continuation_lines = [line.strip() for line in continuation_content.splitlines() if line.strip()]

                if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                    # Combine the incomplete and continuation responses
                    complete_content = content + continuation_content
                    self.conversation_history = self.conversation_history[:-2]
                    self.conversation_history.append({"role": "assistant", "content": complete_content})
                    return complete_content
                else:
                    logger.info(" #### Extending response - generating additional context (2/10)")
                    content = content + continuation_content
                    self.conversation_history.append({"role": "assistant", "content": content})
                    # The response was cut off, prompt AI to continue
                    continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                    self.conversation_history.append({"role": "user", "content": continuation_prompt})

                    continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                    continuation_content1 = continuation_response.choices[0].message.content
                    continuation_lines = [line.strip() for line in continuation_content1.splitlines() if line.strip()]

                    if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                        # Combine the incomplete and continuation responses
                        complete_content = content + continuation_content1
                        self.conversation_history = self.conversation_history[:-4]
                        self.conversation_history.append({"role": "assistant", "content": complete_content})
                        return complete_content
                    else:
                        logger.info(" #### Extending response - generating additional context (3/10)")
                        content = content + continuation_content1
                        self.conversation_history.append({"role": "assistant", "content": content})
                        # The response was cut off, prompt AI to continue
                        continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                        self.conversation_history.append({"role": "user", "content": continuation_prompt})

                        continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                        continuation_content2 = continuation_response.choices[0].message.content
                        continuation_lines = [line.strip() for line in continuation_content2.splitlines() if line.strip()]

                        if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                            # Combine the incomplete and continuation responses
                            complete_content = content + continuation_content2
                            self.conversation_history = self.conversation_history[:-6]
                            self.conversation_history.append({"role": "assistant", "content": complete_content})
                            return complete_content
                        else:
                            logger.info(" #### Extending response - generating additional context (4/10)")
                            content = content + continuation_content2
                            self.conversation_history.append({"role": "assistant", "content": content})
                            continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                            self.conversation_history.append({"role": "user", "content": continuation_prompt})

                            continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                            continuation_content3 = continuation_response.choices[0].message.content
                            continuation_lines = [line.strip() for line in continuation_content3.splitlines() if line.strip()]

                            if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                                complete_content = content + continuation_content3
                                self.conversation_history = self.conversation_history[:-8]
                                self.conversation_history.append({"role": "assistant", "content": complete_content})
                                return complete_content
                            else:
                                logger.info(" #### Extending response - generating additional context (5/10)")
                                content = content + continuation_content3
                                self.conversation_history.append({"role": "assistant", "content": content})
                                continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                                self.conversation_history.append({"role": "user", "content": continuation_prompt})

                                continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                                continuation_content4 = continuation_response.choices[0].message.content
                                continuation_lines = [line.strip() for line in continuation_content4.splitlines() if line.strip()]

                                if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                                    complete_content = content + continuation_content4
                                    self.conversation_history = self.conversation_history[:-10]
                                    self.conversation_history.append({"role": "assistant", "content": complete_content})
                                    return complete_content
                                else:
                                    logger.info(" #### Extending response - generating additional context (6/10)")
                                    content = content + continuation_content4
                                    self.conversation_history.append({"role": "assistant", "content": content})
                                    continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                                    self.conversation_history.append({"role": "user", "content": continuation_prompt})

                                    continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                                    continuation_content5 = continuation_response.choices[0].message.content
                                    continuation_lines = [line.strip() for line in continuation_content5.splitlines() if line.strip()]

                                    if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                                        complete_content = content + continuation_content5
                                        self.conversation_history = self.conversation_history[:-12]
                                        self.conversation_history.append({"role": "assistant", "content": complete_content})
                                        return complete_content
                                    else:
                                        logger.info(" #### Extending response - generating additional context (7/10)")
                                        content = content + continuation_content5
                                        self.conversation_history.append({"role": "assistant", "content": content})
                                        continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                                        self.conversation_history.append({"role": "user", "content": continuation_prompt})

                                        continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                                        continuation_content6 = continuation_response.choices[0].message.content
                                        continuation_lines = [line.strip() for line in continuation_content6.splitlines() if line.strip()]

                                        if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                                            complete_content = content + continuation_content6
                                            self.conversation_history = self.conversation_history[:-14]
                                            self.conversation_history.append({"role": "assistant", "content": complete_content})
                                            return complete_content
                                        else:
                                            logger.info(" #### Extending response - generating additional context (8/10)")
                                            content = content + continuation_content6
                                            self.conversation_history.append({"role": "assistant", "content": content})
                                            continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                                            self.conversation_history.append({"role": "user", "content": continuation_prompt})

                                            continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                                            continuation_content7 = continuation_response.choices[0].message.content
                                            continuation_lines = [line.strip() for line in continuation_content7.splitlines() if line.strip()]

                                            if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                                                complete_content = content + continuation_content7
                                                self.conversation_history = self.conversation_history[:-16]
                                                self.conversation_history.append({"role": "assistant", "content": complete_content})
                                                return complete_content
                                            else:
                                                logger.info(" #### Extending response - generating additional context (9/10)")
                                                content = content + continuation_content7
                                                self.conversation_history.append({"role": "assistant", "content": content})
                                                continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                                                self.conversation_history.append({"role": "user", "content": continuation_prompt})

                                                continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                                                continuation_content8 = continuation_response.choices[0].message.content
                                                continuation_lines = [line.strip() for line in continuation_content8.splitlines() if line.strip()]

                                                if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                                                    complete_content = content + continuation_content8
                                                    self.conversation_history = self.conversation_history[:-18]
                                                    self.conversation_history.append({"role": "assistant", "content": complete_content})
                                                    return complete_content
                                                else:
                                                    logger.info(" #### Extending response - generating additional context (10/10)")
                                                    content = content + continuation_content8
                                                    self.conversation_history.append({"role": "assistant", "content": content})
                                                    continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                                                    self.conversation_history.append({"role": "user", "content": continuation_prompt})

                                                    continuation_response = await self.ai.coding_prompt(self.conversation_history, 4096, 0.2, 0.1)
                                                    continuation_content9 = continuation_response.choices[0].message.content
                                                    continuation_lines = [line.strip() for line in continuation_content9.splitlines() if line.strip()]

                                                    if continuation_lines and "> REPLACE" in continuation_lines[-1]:
                                                        complete_content = content + continuation_content9
                                                        self.conversation_history = self.conversation_history[:-20]
                                                        self.conversation_history.append({"role": "assistant", "content": complete_content})
                                                        return complete_content
                                                    else:
                                                        complete_content = content + continuation_content9
                                                        self.conversation_history = self.conversation_history[:-20]
                                                        self.conversation_history.append({"role": "assistant", "content": complete_content})
                                                        logger.error(f"  The `CodingAgent` encountered an error while getting coding request")
                                                        return complete_content

        except Exception as e:
            logger.error(f" The `CodingAgent` encountered an error while getting coding request")
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
        logger.debug("\n #### The `CodingAgent` is clearing conversation history")
        self.conversation_history = []

    def destroy(self):
        """De-initialize and destroy this instance."""
        logger.debug("\n #### The `CodingAgent` is being destroyed")
        self.repo = None
        self.conversation_history = None
        self.ai = None