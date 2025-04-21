from enum import Enum



class UserRole(Enum):
    SYSTEM_ROLE = "system"
    USER_ROLE = "user"

class AgentType(Enum):
    DICTIONARY_AGENT = "dictionary"
    TRANSLATOR_AGENT = "translator"
    
class AIModel(Enum):
    LLAMA_3_70B_VERSATILE = "llama-3.3-70b-versatile"
    
    GEMMA_2_9_IT = "gemma2-9b-it"


DOCUMENTATION_RULES = """
Clarity and Simplicity: Documentation should avoid jargon and complex language, focusing instead on clear, concise explanations that cater to the target audience's level of expertise. Plain language, simple examples, and a focus on practical information are essential.

Comprehensive Coverage: A good documentation set covers all aspects of the codebase—overview, setup, dependencies, code structure, APIs, and usage examples—without overwhelming the reader with excessive detail. Comprehensive coverage also includes documenting edge cases, limitations, and known issues.

Organization and Structure: Documentation should be logically structured, making it easy for users to find information. Using a table of contents, consistent headers, and grouping related topics together allows readers to locate information quickly.

Up-to-Date Information: Good documentation is current with the latest version of the codebase. Outdated documentation can be worse than none, as it misleads users. Regular updates and clear versioning can help users understand changes over time.

Example-Rich Content: Real-world examples, code snippets, and use cases help users understand how to use functions, classes, and modules. Examples also provide a testing ground for users to understand specific functionality before using it in their code.

Clear API Documentation: For codebases with extensive API interactions, documenting each endpoint or function with parameters, return types, expected inputs, and outputs is essential. Any peculiarities or non-standard behaviors should also be clearly noted.

Error and Debugging Guidance: Good documentation doesn’t just show what works; it also helps when things go wrong. Including common errors, debugging tips, and troubleshooting sections can save users considerable time.

Searchable and Accessible: Whether it’s a single README file or a full documentation site, users should be able to quickly search for and navigate to the relevant information.

Consistent Style and Formatting: A consistent tone, style, and formatting across documentation help readers follow along without distraction. Using code blocks, bullet points, tables, and diagrams where appropriate enhances readability.

Assumptions and Prerequisites: Clarify any assumptions about the user’s environment or knowledge level. Noting prerequisites (e.g., necessary libraries, hardware requirements) allows users to prepare accordingly, minimizing setup issues.

Maintenance Tips and Code Style: Including code conventions, architecture guidelines, and naming conventions makes it easier for other developers to follow best practices and contribute effectively.

Open to Contributions: For open-source projects, guidelines on how to contribute to the codebase, submit issues, or suggest documentation changes can foster a stronger development community and improve the quality of the documentation over time.
"""



COMMANDS: dict[str, str] = {

        "w_doc_f": """
        "You are a senior developer with 40 years of experience in professional programming and software DOCUMENTATION.
        This code comes from a folder that contains code. generate a code documentation for it with as much code illustrations and details you can, use markdown format for your answer. Don't add any text just the documentation
        """,
        "w_m_doc": """
        You are a senior developer with 40 years of experience in professional programming and software DOCUMENTATION.
        This are code documentation generated from separated folders make it cohesive and include as much code example as possible. Use Markdown format for your answer don't add any text just the documentation.
        Your response should follow this rules : ${DOCUMENTATION_RULES}
        """,
        "comment_path": f"""
        You are an expert software developer documentation assistant.
        Given the following file or folder path relative to a project root, provide a very brief, concise description (max 10 words) of its likely purpose or content.
        This description will be used as a comment next to the item in a directory tree structure.
        Focus on common conventions for this type of file/folder name or extension. Be generic if unsure.
        You can base yourself on on a file's content if it is a file.
        Examples:
        - path: 'src/components/Button.tsx' -> comment: 'Reusable UI button component'
        - path: 'config/database.js' -> comment: 'Database configuration settings'
        - path: 'tests/' -> comment: 'Contains automated tests'
        - path: 'package.json' -> comment: 'Project metadata and dependencies'
        - path: 'README.md' -> comment: 'Project overview and instructions'
        - path: '.github/workflows/' -> comment: 'CI/CD automation workflows'
        """
}
