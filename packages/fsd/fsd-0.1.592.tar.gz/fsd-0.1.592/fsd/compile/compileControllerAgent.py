import os
import sys


from .CompilePrePromptAgent import CompilePrePromptAgent
from .CompileProjectAnalysAgent import CompileProjectAnalysAgent
from .CompileFileFinderAgent import CompileFileFinderAgent
from .CompileGuiderAgent import CompileGuiderAgent
from .CompileTaskPlanner import CompileTaskPlanner


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.system.CompileCommandRunner import CompileCommandRunner
from fsd.util.utils import parse_payload
from fsd.log.logger_config import get_logger
from fsd.PromptImageUrlAgent.PromptImageUrlAgent import PromptImageUrlAgent
logger = get_logger(__name__)

class CompileControllerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.analysAgent = CompileProjectAnalysAgent(repo)
        self.preprompt = CompilePrePromptAgent(repo)
        self.fileFinder = CompileFileFinderAgent(repo)
        self.guider = CompileGuiderAgent(repo)
        self.taskPlanner = CompileTaskPlanner(repo)
        self.command = CompileCommandRunner(repo)
        self.imageAgent = PromptImageUrlAgent(repo)

    async def get_prePrompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt)

    async def start_CLI_compile_process(self, instruction, code_files, original_prompt_language, file_attachments, focused_files):
        logger.info("-------------------------------------------------")
    
        os_architecture = self.repo.return_os()

        file_result = await self.fileFinder.get_compile_file_plannings(instruction)

        compile_files = file_result.get('crucial_files', [])
        all_files = set(file_result.get('crucial_files', []))
        if file_attachments:
            all_files.update(file_attachments)
        if focused_files:
            all_files.update(focused_files)

        if all_files:
            files_list = "\n".join([f"  - {file}" for file in all_files])
            logger.info(f" #### `SnowX` is reading these files:\n{files_list}")

        logger.info(" #### `SnowX` is now organizing and preparing the task for execution.")
        task = await self.taskPlanner.get_task_plan(instruction, compile_files, os_architecture, original_prompt_language)
        await self.command.execute_steps(task, compile_files, code_files, original_prompt_language)
        logger.info(" #### `SnowX` has successfully completed the compilation process.")
        logger.info("-------------------------------------------------")


    async def get_started(self, user_prompt, original_prompt_language, file_attachments, focused_files):
        """Start the processing of the user prompt."""
        logger.info("-------------------------------------------------")
        logger.info(" #### `SnowX` is initiating the compilation request process.")

        await self.start_CLI_compile_process(user_prompt, [], original_prompt_language, file_attachments, focused_files)

        logger.info(f" #### `SnowX` has completed processing the user prompt: {user_prompt}.")
        logger.info("-------------------------------------------------")
