<a href="https://livekit.io/">
  <img src="./.github/assets/livekit-mark.png" alt="LiveKit logo" width="100" height="100">
</a>

# Python Voice Agent

<p>
  <a href="https://cloud.livekit.io/projects/p_/sandbox"><strong>Deploy a sandbox app</strong></a>
  •
  <a href="https://docs.livekit.io/agents/overview/">LiveKit Agents Docs</a>
  •
  <a href="https://livekit.io/cloud">LiveKit Cloud</a>
  •
  <a href="https://blog.livekit.io/">Blog</a>
</p>

A basic example of a voice agent using LiveKit and Python.

## Dev Setup

Clone the repository and install dependencies to a virtual environment:

```console
cd voice-pipeline-agent-python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set up the environment by copying `.env.example` to `.env.local` and filling in the required values:

- `LIVEKIT_URL`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`
- `OPENAI_API_KEY`
- `DEEPGRAM_API_KEY`

You can also do this automatically using the LiveKit CLI:

```console
lk app env
```

Run the agent:

```console
python3 agent.py dev
```

This agent requires a frontend application to communicate with. You can use one of our example frontends in [livekit-examples](https://github.com/livekit-examples/), create your own following one of our [client quickstarts](https://docs.livekit.io/realtime/quickstarts/), or test instantly against one of our hosted [Sandbox](https://cloud.livekit.io/projects/p_/sandbox) frontends.

# AI Voice Assistant Deployment Guide

This guide provides step-by-step instructions for setting up and deploying an AI Voice Assistant application using LiveKit and Fly.io. Follow the steps carefully to ensure a successful deployment.

## Step 1: Setup Your Local Environment

1. **Create a Project Folder**

   - Open your terminal and create a new directory for your project:
     ```bash
     mkdir ai-voice-assistant
     cd ai-voice-assistant
     ```

2. **Create a Python Virtual Environment**

   - Create a virtual environment named `ai`:
     ```bash
     python3 -m venv ai
     ```

3. **Activate the Virtual Environment**

   - Activate the virtual environment with the following command:
     ```bash
     source ai/bin/activate
     ```

4. **Install Required Packages**
   - Install the necessary Python packages:
     ```bash
     pip3 install livekit-agents livekit-plugins-openai livekit-plugins-silero python-dotenv
     ```

## Step 2: Setup LiveKit

1. **Create a LiveKit Account**

   - Visit [LiveKit Cloud](https://cloud.livekit.io) and sign up for an account.

2. **Create a New Project**

   - After logging in, create a new project in your LiveKit dashboard.

3. **Generate API Keys**

   - Navigate to the API section and generate a new API key and secret key.

4. **Configure Environment Variables**
   - Set up environment variables in your terminal with the following command, replacing placeholders with your actual keys:
     ```bash
     export LIVEKIT_URL="wss://your-url-from-livekit-cloud-dashboard.livekit.cloud"
     export LIVEKIT_API_KEY="api-key-from-livekit-cloud-dashboard"
     export LIVEKIT_API_SECRET="api-secret-from-livekit-cloud-dashboard"
     export OPENAI_API_KEY="openai-api-key"
     ```

## Step 3: Deploy on Fly.io

1. **Install Fly CLI**

   - Use Homebrew to install the Fly.io command-line interface:
     ```bash
     brew install flyctl
     ```

2. **Authenticate with Fly.io**

   - Log in to your Fly.io account using the command:
     ```bash
     fly auth login
     ```

3. **Launch Your App on Fly.io**

   - Run the following command to set up your application in the Fly.io environment:
     `bash
     fly launch
     `
     OR fly app create <app name>

4. **Set Environment Variables on Fly.io**

   - Configure environment variables for your app using Fly secrets:
     ```bash
     fly secrets set --app python-agent-example \
     LIVEKIT_URL="wss://your-url-from-livekit-cloud-dashboard.livekit.cloud" \
     LIVEKIT_API_KEY="api-key-from-livekit-cloud-dashboard" \
     LIVEKIT_API_SECRET="api-secret-from-livekit-cloud-dashboard" \
     OPENAI_API_KEY="openai-api-key"
     ```

5. **Deploy Your Application**
   - Deploy the app using the Fly.io configuration file:
     ```bash
     fly deploy -c fly.toml
     ```

## Step 4: Run the Client

1. **Access the Hosted Playground**

   - Visit the [LiveKit Agents Playground](https://agents-playground.livekit.io/).

2. **Connect to Your Project**
   - Enter the WebSocket URL (`wss://your-url-from-livekit-cloud-dashboard.livekit.cloud`) and your room token to join the chat room.

By following these steps, you will successfully deploy your AI Voice Assistant application and connect to it using the LiveKit playground. For further assistance, refer to the official documentation of [LiveKit](https://docs.livekit.io/) and [Fly.io](https://fly.io/docs/).
