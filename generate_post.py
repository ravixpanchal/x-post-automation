from datetime import datetime
import os
import random
from send_to_slack import send_tweet_to_slack

# A pool of 30 high-quality AI-related tweets/posts
AI_POSTS = [
    "AI agents are transitioning from simple chat interfaces to autonomous entities capable of reasoning, planning, and tool use. The future of software engineering is collaborative. #AIAgents #GenAI #FutureOfWork",
    "Open-source LLMs like Llama and Mistral are closing the gap with proprietary models. Democratization of AI is key to open innovation and custom enterprise solutions. #OpenSource #AI #MachineLearning",
    "Prompt engineering is maturing into 'agentic system design'. It's no longer just about the prompt, but the control loops, verification steps, and tool integrations. #AI #SoftwareEngineering",
    "The shift from training larger models to optimizing inference-time compute (like search/reasoning steps) is showing massive performance leaps. Quality over brute scale. #GenAI #LLM #DeepLearning",
    "AI isn't going to replace developers, but developers who use AI will replace developers who don't. Learn to leverage AI as a force multiplier for your productivity. #Programming #AI #SoftwareEngineering",
    "Small Language Models (SLMs) are becoming incredibly capable and cost-effective. Running local, fine-tuned models on edge devices is the next big wave. #EdgeAI #SLM #MachineLearning",
    "Vector databases and RAG (Retrieval-Augmented Generation) are essential for reducing hallucinations. Combining structured databases with unstructured LLM search is the sweet spot. #RAG #AI #Database",
    "AI-assisted coding tools like Github Copilot and Antigravity are reframing the developer experience. Coding is shifting from syntax writing to system architecture. #AI #Coding #DevTool",
    "Multi-modal AI is changing how we interact with technology. Models that understand text, audio, images, and video simultaneously open up completely new UX possibilities. #AI #Multimodal #Tech",
    "Building robust AI systems requires testing for edge cases, prompt injection, and output formatting. Evaluation frameworks are now the most critical part of the AI stack. #AIOps #LLMEvals",
    "AI agents are now capable of debugging code, writing unit tests, and refactoring legacy systems. The software development lifecycle is being automated at speed. #AIAgent #SoftwareArchitecture",
    "Fine-tuning vs. RAG: Fine-tuning is for teaching a model a new style or format; RAG is for giving it access to dynamic, factual knowledge. Most projects need a mix of both. #GenAI #LLM",
    "With models getting cheaper and faster, the cost of building complex agentic loops is dropping. We can now afford multiple verification and reflection steps per query. #GenAI #AIAgents",
    "AI safety and alignment are not just ethics topics; they are core engineering challenges. Building guardrails and jailbreak detection is crucial for production systems. #AISafety #AIEngineering",
    "The next generation of developer tools will not just autocomplete, but actively pair-program with us, maintaining context across the entire repository. #AICoding #DeveloperTools",
    "We are moving from a world of static APIs to dynamic agentic APIs. Systems will talk to each other through natural language and structured schema negotiated on the fly. #AIAgent #APIs",
    "The Indian AI startup ecosystem is heating up, with builders focusing on localized LLMs, voice assistants for vernacular languages, and global SaaS tools. #IndiaAI #Startups #Tech",
    "We are seeing the rise of AI-native applications—apps that couldn't exist without an LLM at their core. These aren't wrappers; they are entirely new paradigms of software. #AINative #Startup",
    "The limit of model performance is no longer just the training data, but synthetic data generation and RLHF (Reinforcement Learning from Human Feedback). #DeepLearning #LLMs",
    "Using AI to write code requires a strong verification loop. Always run tests, check edge cases, and perform static analysis on AI-generated code before shipping. #SoftwareTesting #AICoding",
    "AI-powered search is replacing traditional keywords. Semantic search understands intent, context, and user history to deliver highly relevant results instantly. #SemanticSearch #AI",
    "The best way to learn AI engineering is by building. Spin up a local model, write a simple RAG pipeline, and experiment with prompt engineering. Hands-on is unmatched. #LearningAI #Developer",
    "AI is democratizing software creation. Non-technical founders can now build functional prototypes in hours, shifting the focus to distribution and product-market fit. #NoCode #AI #Product",
    "From text-to-image to text-to-video, generative media is progressing exponentially. The creative workflow is evolving to focus on curation, direction, and editing. #GenerativeAI #Design",
    "As AI systems handle more tasks autonomously, observability becomes paramount. We need transparent logs to trace why an agent took a specific action. #LLMObservability #AIAgents",
    "The real challenge in enterprise AI is not the LLM, but data quality and data access. Cleaning legacy databases and building secure pipelines is the first step. #EnterpriseAI #BigData",
    "AI-native databases are designed from the ground up for vector search and high-dimensional embeddings, making semantic retrieval lightning fast. #VectorDatabase #TechStack",
    "Embrace the AI coding assistant as a junior partner. It's great at boilerplate and syntax but needs your guidance on architecture, business logic, and security. #PairProgramming #AI",
    "We are entering the era of localized, offline AI. Having powerful LLMs run completely on-device without internet access ensures 100% privacy and zero latency. #LocalAI #Privacy",
    "AI agents that can interact with the browser are unlocking automation for web tasks. From booking tickets to scraping data, the web is now accessible to machines. #WebAutomation #AI"
]

VARIATION_PREFIXES = [
    "💡 AI Insight: ",
    "🚀 Tech Perspective: ",
    "📌 Developer Note: ",
    "🔥 Industry Trend: ",
    "⚡ Quick Thought: ",
    "🤖 AI Trends: ",
    "🧠 Engineering Insight: ",
    "✨ Key Takeaway: ",
]

VARIATION_SUFFIXES = [
    " What are your thoughts on this?",
    " How are you seeing this shift in your workflow?",
    " Do you agree with this trend?",
    " What has your experience been with this?",
    " Share your perspective below!",
]

import json

def generate_and_send_post():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    history_file = os.path.join(script_dir, "posted_history.json")
    twits_dir = os.path.join(script_dir, "Twits")

    # Read previously sent tweets from history file and legacy Twits directory
    existing_tweets = set()
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                history_list = json.load(f)
                for t in history_list:
                    existing_tweets.add(t.strip())
        except Exception:
            pass

    if os.path.exists(twits_dir):
        for filename in os.listdir(twits_dir):
            if filename.endswith(".txt"):
                try:
                    with open(os.path.join(twits_dir, filename), "r") as f:
                        existing_tweets.add(f.read().strip())
                except Exception:
                    pass

    # Find unused base posts
    unused_posts = [post for post in AI_POSTS if post.strip() not in existing_tweets]

    if unused_posts:
        selected_tweet = random.choice(unused_posts)
    else:
        print("All base posts used once. Generating a clean, unique variation...")
        # Generate a unique variation using professional prefixes/suffixes (no dates)
        candidates = []
        for base in AI_POSTS:
            for prefix in VARIATION_PREFIXES:
                var1 = f"{prefix}{base}"
                if var1 not in existing_tweets:
                    candidates.append(var1)
            for suffix in VARIATION_SUFFIXES:
                var2 = f"{base}{suffix}"
                if var2 not in existing_tweets:
                    candidates.append(var2)

        if candidates:
            selected_tweet = random.choice(candidates)
        else:
            # Fallback: combine prefix and suffix if all single variations were used
            base = random.choice(AI_POSTS)
            selected_tweet = f"{random.choice(VARIATION_PREFIXES)}{base}{random.choice(VARIATION_SUFFIXES)}"

    print("Tweet Content:", selected_tweet)

    # Send to Slack
    send_tweet_to_slack(selected_tweet)

if __name__ == "__main__":
    generate_and_send_post()