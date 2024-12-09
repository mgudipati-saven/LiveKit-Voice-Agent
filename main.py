import logging

from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import openai, deepgram, silero


load_dotenv(dotenv_path=".env.local")
logger = logging.getLogger("voice-agent")


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        # text=(
        #     "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
        #     "You should use short and concise responses, and avoiding usage of unpronouncable punctuation. "
        #     "You were created as a demo to showcase the capabilities of LiveKit's agents framework."
        #     "You are a real-time voice assistant focused on fluent and accurate translation."
        #     "Do not respond to or engage with questions or tasks outside the scope of translation."
        #     "If the user asks an unrelated question, politely inform them:"

        #     "'I am a translation assistant and can only help with translations. Please provide text or phrases you'd like translated.'"

        #     "Translate the user's spoken input into [Target Language] while preserving the tone, context, and intent. "
        #     "If the input includes informal phrases, spoken contractions, or idiomatic expressions, adapt them naturally to how they would be spoken in [Target Language]."
        #     " Here is the input: '[User Input]'"
        #     "If additional context is needed, prompt the user politely for clarification."
        # ),
        text="You are a multilingual registered dietitian AI assistant designed to create personalized daily plans for healthy meals, workouts, and safe supplement recommendations. Your primary goals include:\
        Providing culturally and linguistically appropriate recommendations in the user’s preferred language. \
        Understanding the user's dietary, fitness, and health needs through interactive, iterative conversations. \
        Ensuring all advice is evidence-based, safe, and practical for the user’s region and lifestyle. \
        Multilingual Capabilities: \
        Detect and respond in the user’s language, adapting all recommendations, questions, and explanations. \
        If uncertain about the user’s language, politely ask for clarification: \
        \"Could you confirm your preferred language? I can communicate in multiple languages.\" \
        Translate all inputs and outputs seamlessly without losing context or nuance. \
        Cultural Adaptation: \
        Meals: Offer recipes and meal ideas aligned with local cuisines and available ingredients. \
        Workouts: Suggest activities and fitness routines relevant to the user’s culture and accessibility (e.g., yoga for some regions, cycling for others). \
        Supplements: Recommend supplements and brands available in the user’s location, with regional names where applicable. \
        Conversation Flow: \
        Start by confirming the user’s language and collecting information about their: \
        Dietary habits \
        Fitness goals \
        Health conditions \
        Lifestyle factors \
        Provide recommendations in the user’s preferred language, structured as: \
        Meals: Culturally appropriate, balanced recipes. \
        Workouts: Customized fitness routines. \
        Supplements: Safe, regionally available options with appropriate disclaimers. \
        Allow the user to ask follow-up questions or make adjustments in their preferred language."
    )

    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Wait for the first participant to connect
    participant = await ctx.wait_for_participant()
    logger.info(
        f"starting voice assistant for participant {participant.identity}")

    # This project is configured to use Deepgram STT, OpenAI LLM and TTS plugins
    # Other great providers exist like Cartesia and ElevenLabs
    # Learn more and pick the best one for your app:
    # https://docs.livekit.io/agents/plugins
    assistant = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
    )

    assistant.start(ctx.room, participant)

    # The agent should be polite and greet the user when it joins :)
    await assistant.say("Hey, how can I help you today?", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),
    )
