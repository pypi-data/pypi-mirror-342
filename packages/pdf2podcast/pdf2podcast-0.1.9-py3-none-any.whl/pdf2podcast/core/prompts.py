"""
Prompt templates and mappings for podcast generation.
"""

from typing import Dict, Any, Optional

from pdf2podcast.core.base import BasePromptBuilder

# Default system prompt with core instructions
DEFAULT_SYSTEM_PROMPT = """
Generate a podcast script using ONLY the provided text content and answer to the user QUERY. Follow these STRICT requirements:
CRITICAL - DO NOT INCLUDE:
- NO sound effects (whoosh, ding, etc.)
- NO music or jingles
- NO audio transitions
- NO audio instructions or cues
- NO intro/outro music references
- NO host introductions or sign-offs
- NO references to audio elements
- NO sound descriptions in parentheses
- NO "welcome" or "thanks for listening" phrases
- NO podcast name or branding
- NO references to figures, diagrams, or visual elements
- NO Section Titles or Headings
- NO references to the instructions and requirements

Content Adaptation:
1. Complexity Level ({complexity}):
- Vocabulary: {complexity_settings[vocabulary]}
- Structure: {complexity_settings[structure]}
- Examples: {complexity_settings[examples]}
- Depth: {complexity_settings[depth]}
- Style: {complexity_settings[style]}

2. Target Audience ({target_audience}):
- Expected Background: {audience_settings[background]}
- Content Focus: {audience_settings[focus]}
- Terminology Usage: {audience_settings[terminology]}
- Example Types: {audience_settings[examples]}
- Engagement Style: {audience_settings[engagement]}

Structure Requirements:
1. Introduction (15%):
- Establish topic context
- Create connection with audience
- Present key themes

2. Core Discussion (65%):
- Develop main concepts
- Explore key points
- Provide insights and analysis
- Build comprehensive understanding

3. Supporting Elements (10%):
- Deepen understanding
- Offer additional perspectives 
- Enrich main discussion
- Include relevant anecdotes or examples
- Highlight significant implications

4. Conclusion (10%):
- Synthesize key points
- Reinforce central themes
- Provide concluding thoughts
- Encourage further exploration

Content Requirements:
- Use ONLY information from source text
- DO NOT add references to the source text
- The script must meet minimum length requirements
- If response is shorter, expand with more details, examples, clarifications, and deeper explanations
- Make sure every section is fully developed
- Answer any provided query
- Maintain consistent complexity level
- Match audience expectations
- Clear verbal descriptions
- Natural transitions
- Pure narration style
- Focus on substance
- No external examples
- Respond only with the script without any additional text or explanations
"""

# Detailed complexity mappings
COMPLEXITY_MAPPING = {
    "simple": {
        "vocabulary": "Use basic terms with clear explanations of any technical concepts",
        "structure": "Present ideas in a straightforward, linear progression",
        "examples": "Illustrate points with everyday scenarios and familiar contexts",
        "depth": "Focus on foundational concepts and practical understanding",
        "style": "Conversational and approachable, like explaining to a friend",
    },
    "intermediate": {
        "vocabulary": "Balance technical terms with clear explanations",
        "structure": "Build concepts progressively with logical connections",
        "examples": "Use industry-relevant applications and practical cases",
        "depth": "Explore interconnections between concepts",
        "style": "Professional but accessible, like a knowledgeable mentor",
    },
    "advanced": {
        "vocabulary": "Employ proper technical terminology",
        "structure": "Present complex relationships and detailed analysis",
        "examples": "Include specialized cases and technical applications",
        "depth": "Cover theoretical aspects and advanced implications",
        "style": "Technical and precise, like an expert presentation",
    },
}

# Target audience adaptations
AUDIENCE_MAPPING = {
    "general": {
        "background": "No specific technical background",
        "focus": "Practical understanding and real-world relevance",
        "terminology": "Explain all technical terms",
        "examples": "Common, everyday applications",
        "engagement": "Emphasis on general interest and practical value",
    },
    "students": {
        "background": "Academic context with basic field knowledge",
        "focus": "Systematic learning and fundamental principles",
        "terminology": "Build technical vocabulary with explanations",
        "examples": "Study-relevant scenarios and academic applications",
        "engagement": "Educational approach with clear learning objectives",
    },
    "professionals": {
        "background": "Working knowledge of the field",
        "focus": "Practical applications and industry relevance",
        "terminology": "Industry-standard terms and concepts",
        "examples": "Business cases and professional scenarios",
        "engagement": "Emphasis on practical implementation and value",
    },
    "experts": {
        "background": "Deep domain knowledge",
        "focus": "Advanced concepts and theoretical implications",
        "terminology": "Specialized technical vocabulary",
        "examples": "Complex case studies and cutting-edge applications",
        "engagement": "High-level technical discussion",
    },
    "enthusiasts": {
        "background": "Interest-driven basic knowledge",
        "focus": "Interesting aspects and hobby applications",
        "terminology": "Mix of basic and intermediate terms",
        "examples": "Hobby-relevant scenarios and DIY applications",
        "engagement": "Focus on interesting aspects and practical projects",
    },
}


class PodcastPromptTemplate:
    """Template provider for podcast generation prompts."""

    def __init__(
        self, system_prompt: Optional[str] = None, instructions: Optional[str] = None
    ):
        """
        Initialize template provider with optional custom system prompt.

        Args:
            system_prompt (Optional[str]): Custom system prompt to override default
        """
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        self.instructions = instructions or ""

    def format_system_prompt(self, **kwargs: Dict[str, Any]) -> str:
        """
        Format system prompt with dynamic values.

        Args:
            **kwargs: Dynamic values for formatting

        Returns:
            str: Formatted system prompt
        """
        complexity = kwargs.get("complexity", "intermediate")
        target_audience = kwargs.get("target_audience", "general")
        complexity_settings = COMPLEXITY_MAPPING[complexity]
        audience_settings = AUDIENCE_MAPPING[target_audience]

        return self.system_prompt.format(
            complexity=complexity,
            complexity_settings=complexity_settings,
            target_audience=target_audience,
            audience_settings=audience_settings,
        )

    def get_base_prompt(
        self,
        text: str,
        **kwargs: Dict[str, Any],
    ) -> str:
        """
        Get the base prompt for podcast script generation.

        Args:
            text (str): Source text
            complexity (str): Desired complexity level
            target_audience (str): Target audience category
            min_length (int): Minimum target length
            **kwargs: Additional parameters

        Returns:
            str: Formatted prompt
        """
        min_length = kwargs.get("min_length", 10000)
        query = kwargs.get("query", None)

        # Format system prompt with dynamic values
        formatted_system_prompt = self.format_system_prompt(**kwargs)

        return f"""
        {formatted_system_prompt}

        Query (if provided):
        {query}

        Instructions (if provided):
        {self.instructions}

        Source text:
        {text}
        """

    def get_expand_prompt(
        self,
        text: str,
        script: str,
        **kwargs: Dict[str, Any],
    ) -> str:
        """
        Get the prompt for expanding an existing script.

        Args:
            script (str): Current script
            min_length (int): Target minimum length
            complexity (str): Desired complexity level
            target_audience (str): Target audience category
            **kwargs: Additional parameters

        Returns:
            str: Formatted expansion prompt
        """
        min_length = kwargs.get("min_length", 10000)
        query = kwargs.get("query", None)

        # Format system prompt with dynamic values
        formatted_system_prompt = self.format_system_prompt(**kwargs)

        return f"""
        The current content is too short ({len(script)} characters).
        Expand the script to at least {min_length} characters.
        Answer the user query (if provided) and maintain the storytelling approach.
        
        Follow these system instructions:
        {formatted_system_prompt}
        
        Add more detail and examples appropriate for the audience.

        Query (if provided):
        {query}

        Instructions (if provided):
        {self.instructions}
        
        Current Script:
        {script}
        """


class PodcastPromptBuilder(BasePromptBuilder):
    """Prompt builder for podcast script generation."""

    def __init__(
        self,
        template_provider=None,
        system_prompt: Optional[str] = None,
        instructions: Optional[str] = None,
    ):
        """
        Initialize with optional custom template provider and system prompt.

        Args:
            template_provider: Template provider class (default: PodcastPromptTemplate)
            system_prompt: Optional custom system prompt to override default
        """
        if template_provider is None:
            from .prompts import PodcastPromptTemplate

            template_provider = PodcastPromptTemplate
        self.templates = template_provider(
            system_prompt=system_prompt, instructions=instructions
        )

    def build_prompt(self, text: str, **kwargs) -> str:
        """Build main generation prompt."""
        return self.templates.get_base_prompt(text, **kwargs)

    def build_expand_prompt(self, text: str, **kwargs) -> str:
        """Build expansion prompt."""
        return self.templates.get_expand_prompt(text, **kwargs)
