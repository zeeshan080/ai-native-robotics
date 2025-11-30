"""Content personalization agent using OpenAI Agents SDK."""

import os
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel

from chatkit_backend.db.models import UserPreferences


# Personalization system prompt
PERSONALIZATION_PROMPT = """You are a content personalization agent for an AI-Native Robotics Textbook.

Your task is to adapt educational content based on the learner's profile while preserving technical accuracy.

## User Profile
- Education Level: {education_level}
- Programming Experience: {programming_experience}
- Robotics Background: {robotics_background}
- AI/ML Experience: {ai_ml_experience}
- Learning Goals: {learning_goals}
- Preferred Language: {preferred_language}

## Adaptation Rules

### By Programming Experience:
- **None/Beginner**: Add more code comments, explain syntax, use simpler examples
- **Intermediate**: Assume basic familiarity, focus on robotics-specific patterns
- **Advanced**: Skip basics, add performance considerations and advanced patterns

### By Robotics Background:
- **No Background**: Add real-world analogies (e.g., compare robot sensors to human senses)
- **Has Background**: Use technical terminology, reference common robotics concepts

### By AI/ML Experience:
- **None/Basic**: Explain AI concepts in simple terms with examples
- **Intermediate/Advanced**: Reference model architectures, training concepts

### By Preferred Language:
- **English (en)**: Keep content in English
- **Urdu (ur)**: Translate content to Urdu while keeping these terms in English:
  - ROS 2, Gazebo, Isaac Sim, URDF, SDF, SLAM
  - Python, node, topic, service, action
  - Joint, link, sensor, actuator, IMU
  - Neural network, LLM, transformer
  - Any code, commands, file paths, or variable names

## Output Format - CRITICAL
Your response MUST be in valid Markdown format:
- Use `#`, `##`, `###` for headings
- Use `**bold**` for emphasis
- Use ``` for code blocks with language identifier
- Use `- ` for bullet lists
- Use `1. ` for numbered lists
- Use `> ` for blockquotes
- Separate paragraphs with blank lines

## Output Requirements
1. Output ONLY the personalized content in Markdown format
2. Do NOT include any preamble like "Here is the personalized content:"
3. Do NOT wrap the output in markdown code fences
4. Preserve code examples with appropriate comments
5. Keep the same overall content organization
6. Do not add "Summary" or "Key Takeaways" sections
7. Ensure technical accuracy is maintained

## Important
- Be concise - adapt, don't bloat
- Focus on clarity over completeness
- Match the learner's level, not below or above

Now, personalize the following content and output ONLY valid Markdown:

{original_content}
"""


def get_personalization_model() -> OpenAIChatCompletionsModel:
    """Get the LLM model for personalization."""
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        model_name = os.getenv("GEMINI_DEFAULT_MODEL", "gemini-2.5-flash")
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        model_name = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o-mini")
        base_url = None

    # Create AsyncOpenAI client
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    return OpenAIChatCompletionsModel(
        model=model_name,
        openai_client=client,
    )


def create_personalizer_agent() -> Agent:
    """Create a personalization agent."""
    return Agent(
        name="content-personalizer",
        instructions="You are a content personalization agent for educational robotics content.",
        model=get_personalization_model(),
    )


def build_personalization_prompt(
    preferences: UserPreferences,
    original_content: str,
) -> str:
    """Build the personalization prompt with user context."""
    robotics_bg = "Has robotics experience" if preferences.robotics_background else "No robotics background"
    goals = ", ".join(preferences.learning_goals)

    return PERSONALIZATION_PROMPT.format(
        education_level=preferences.education_level.replace("_", " ").title(),
        programming_experience=preferences.programming_experience.replace("_", " ").title(),
        robotics_background=robotics_bg,
        ai_ml_experience=preferences.ai_ml_experience.replace("_", " ").title(),
        learning_goals=goals,
        preferred_language="Urdu" if preferences.preferred_language == "ur" else "English",
        original_content=original_content,
    )


async def personalize_content(
    preferences: UserPreferences,
    original_content: str,
) -> str:
    """
    Personalize content based on user preferences.

    Args:
        preferences: User's learning preferences
        original_content: Original lesson content in Markdown

    Returns:
        Personalized content in Markdown format
    """
    from agents import Runner

    agent = create_personalizer_agent()
    prompt = build_personalization_prompt(preferences, original_content)

    result = await Runner.run(
        starting_agent=agent,
        input=prompt,
    )

    # Extract the final output
    if result.final_output:
        return result.final_output
    return original_content  # Fallback to original if personalization fails
