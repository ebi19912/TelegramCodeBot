Project Overview: TelegramCodeBot is an advanced AI agent designed to streamline the software development lifecycle directly within the Telegram interface. It transforms high-level user requirements into structured, functional code, significantly reducing the gap between idea and implementation.

Key Technical Features:

Conversational Requirement Engineering: Implements a structured state machine (ConversationHandler) to gather critical project metadata including project type (Web, Bot, Scraper, Automation), target language, and specific functional requirements.

Contextual Prompt Construction: Dynamically builds complex prompts for the Gemini Pro engine, enforcing strict coding standards, standard library usage, and clean architecture principles.

Multi-Language Support: Versatile enough to generate code in Python, JavaScript, and other major languages, tailored to the user's selected ecosystem.

Large Payload Handling: Features a smart chunking mechanism to bypass Telegram's 4096-character message limit, ensuring that even large codebases are delivered completely and readably.

User-Centric UX: Provides an intuitive flow with /start, /restart, and /cancel commands, allowing for efficient iterative development and refinement of generated code.

Technical Stack:

AI Engine: Google Generative AI (Gemini Pro).

Framework: Python Telegram Bot (Async API).

Language: Python 3.x.

Core Concept: LLM-based Code Generation & Software Prototyping.
