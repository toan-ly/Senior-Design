# MedAssist User Guide/Manual

## General Information
<div align="justify">
MedAssist is a completely free mental health platform featuring a chatbot powered by a Retrevial-Augmented Generation (RAG) Large Language Model (LLM). Our platform offers users a simple and easy way to interact with a chatbot trained on only DSM-5 material for more accurate responses and impactful interactions. <br><br>

Users can reflect on past interactionsby creating journal entries, view summaries of past interactions, monitor their health report, and submit feedback. MedAssist is purely an informative source and users seeking real professional or medical assistance are urged to reach out to a trained psychiatrist or doctor. Users can view the resources page to get started or contact the national suicide-prevention hotline for emergencies.
</div>

## Organization
This guide consists of eight main sections:

1. [**Environment Setup**](#environmental-setup-using-uv) section explains how to install dependencies and configure the environment.  

2. [**FAQ**](#frequently-asked-questions) section includes answers to commonly asked questions.

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


## Frequently Asked Questions
<div align="justify">
<b>Q: Is MedAssist a medical diagnosis tool?</b> <br>
<b>A:</b> No. MedAssist is an informational platform designed to provide structured mental health information based on DSM-5 materials. It does not diagnose conditions or replace professional care. <br><br>
  
<b>Q: What should I do in an emergency?</b> <br>
<b>A:</b> MedAssist is <b>not</b> intended for emergency use. If you are experiencing a mental health emergency, please contact local emergency services. <br><br>

<b>Q: Does MedAssist store my conversations?</b> <br>
<b>A:</b> Conversation summaries and user-created content (such as journals or feedback) may be stored to support system features, depending on your settings. <br><br>

<b>Q: Can I remove all my information after deleting my account?</b> <br>
<b>A:</b> Of course! All account information is completely deleted from our database after being scrambled as soon as a deletion request goes through.
</div>

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
<div align="justify">
The Resources section offers a variety of third-party options for professional-grade mental health services. Users who are seeking to speak with a psychologist or are having a mental health emergency are heavily urged to use these sources rather than continue to interact with the MedAssist Chatbot. <br><br>

Once users have navigated to the Resources page from the Home screen, they will see a listing of different sources ranked on importance. Each listing features a short summary of the resource, its importance, and a link for users to navigate to its source.
</div>

## Feedback
<div align="justify">
The Feedback section allows users to write out detailed comments, requests, or questions to the MedAssist's system administrators. This allows MedAssist to grow with its users, help clarify individual concerns users may have, and address any bugs or glitches that fall through the cracks. <br><br>

Users can access the Feedback drop-down from any page within MedAssist. Once the drop-down has opened users can simply write out their message and hit sumbit to send it off. Upon submission a 'Thank you' notification will appear on screen and users will be directed to check their inbox after some time has been passed to view the response/resolution.
</div>

## Mail
<div align="justify">
The Mail section is a simple inbox connected to each user's account. It contains system generated notifications as well as responses to any feedback messages they may have submitted. <br><br>

The inbox screen can be accessed via any page within MedAssist via the 'Envelope' icon on the navbar. Once the drop-down screen has appeared users can see a list of any messages in their inbox. Users are also able to delete old messages they no longer want.
</div>

## Account Settings
<div align="justify">
The Account Settings page lets user modify several aspects of their account. User can change their username, password, and email. They can also delete their account from this page. <br><br>

Settings can be accessed via the 'Account' icon on the top left of the navbar. Once clicked a drop-down page will appear along with a listing of each of the settings described above.
</div>
