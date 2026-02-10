# MedAssist User Guide/Manual

## General Information
<div style="text-align: justify">
MedAssist is a completely free mental health platform featuring a chatbot powered by a Retrevial-Augmented Generation (RAG) Large Language Model (LLM). Our platform offers users a simple and easy way to interact with a chatbot trained on only DSM-5 material for more accurate responses and impactful interactions. <br><br>

Users can reflect on past interactionsby creating journal entries, view summaries of past interactions, monitor their health report, and submit feedback. MedAssist is purely an informative source and users seeking real professional or medical assistance are urged to reach out to a trained psychiatrist or doctor. Users can view the resources page to get started or contact the national suicide-prevention hotline for emergencies.
</div>

## Organization
This guide consists of eight main sections:

1. [**Environment**](#environmental-setup-using-uv) Setup section explains how to install dependencies and configure the environment.  

2. [**Questions/Answers**](#questions-and-answers) section includes answers to commonly asked questions.

3. [**Chat**](#chat) section explains how to interact with the chatbot, receive responses, view past summaries, and generate a health report.

4. [**Journal**](#journal) section describes how to post entries, review old records, leave reflections, and how to remove them.

5. [**Resources**](#resources) section explains how sources are displayed, why they were selected, and how to visit them.

6. [**Feedback**](#feedback) section instructs users on how to leave feedback and ask questions to system administrators. 

7. [**Mail**](#mail) section shows users how to check their inbox for system messages or for responses to their feedback submissions.

8. [**Account Settings**](#account-settings) section describes the variety of account settings users can change and how to change them.

## Environmental Setup (Using `uv`)

MedAssist uses `uv`, a modern Python environment and dependency manager, to ensure consistent setup and avoid dependency conflicts. This section explains how users can configure the environment required to run the system.

`uv` is a lightweight tool that manages Python virtual environments and installs project dependencies quickly and reliably. It replaces traditional tools such as `venv`, `pip`, and `conda` with a simpler workflow.

### Step 1: Install uv
Follow [this link](https://docs.astral.sh/uv/getting-started/installation/) to learn how to install uv

Verify installation:
```bash
uv --version
```

### Step 2: Create environment and install dependencies
```bash
uv sync
```

### Step 3: Configure environment variables
Create the following file to store your API key:
```code
configs/secrets.env
```

Add:
```env
OPENAI_API_KEY=your_api_key
```

Keep this file private and do not share it publicly.

### Step 4: Run the application
[Placeholder] 
Once the project is finalized, this section will be updated


## Questions and Answers
**Q: Is MedAssist a medical diagnosis tool?**
No. MedAssist is an informational platform designed to provide structured mental health information based on DSM-5 materials. It does not diagnose conditions or replace professional care.

**Q: What should I do in an emergency?**
MedAssist is not intended for emergency use. If you are experiencing a mental health emergency, please contact local emergency services.

**Q: Does MedAssist store my conversations?**
Conversation summaries and user-created content (such as journals or feedback) may be stored to support system features, depending on your settings.

## Chat
The Chat section is the primary way users interact with MedAssist. It allows users to ask mental health–related questions and receive responses grounded in DSM-5 material.

To use the chat feature:
1. Navigate to the `Chat section` after logging in.
2. Enter a mental health–related question or topic into the `input box`.
3. Submit the message to receive a response.

MedAssist retrieves relevant DSM-5 content and uses it to generate responses. Users may also:
- View summaries of past chat interactions
- Review key discussion points
- Generate a health-related report based on previous conversations

## Journal
The Journal section allows users to record personal reflections related to their mental health journey or past chatbot interactions.

Users can:
- Create new journal entries
- Review previous entries
- Edit or delete existing entries
- Reflect on insights gained from chatbot conversations

Journal entries are intended for personal use only and are not used to diagnose or evaluate users. This feature supports self-reflection and organization of thoughts over time

## Resources

## Feedback

## Mail

## Account Settings
