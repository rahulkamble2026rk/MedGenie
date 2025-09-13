
from groq import Groq
from googleapiclient.discovery import build
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def initialize_groq_client(api_key):
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        raise ValueError(f"Failed to initialize Groq client: {e}")

def search_youtube_video(query, api_key):
    """Search for a relevant YouTube video based on the query."""
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(
            part='snippet',
            q=query + " medical explanation",  # Append context to refine search
            type='video',
            maxResults=1,
            safeSearch='moderate'
        )
        response = request.execute()
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            video_title = response['items'][0]['snippet']['title']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            logger.debug(f"Found YouTube video: {video_title} ({video_url})")
            return video_url, video_title
        else:
            logger.warning("No YouTube videos found for query: %s", query)
            return None, None
    except Exception as e:
        logger.error(f"Error searching YouTube: {e}")
        return None, None

def generate_response(client, prompt, context="", model="llama-3.3-70b-versatile", youtube_api_key=None):
    try:
        if not client or not hasattr(client, 'chat'):
            raise ValueError("Invalid Groq client")
       
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an advanced AI assistant specializing in medical inquiries. "
                        "Provide accurate, well-researched, and user-friendly responses. "
                        "Structure your response with the following sections using Markdown headers: "
                        "## Symptoms\n- List the symptoms described or implied by the user's query.\n"
                        "## Causes\n- List possible causes of the symptoms.\n"
                        "## Remedies\n- Suggest safe remedies or treatments, emphasizing consulting a doctor for serious conditions.\n"
                        "If you cannot provide a confident answer due to insufficient information or complexity, state: "
                        "'This query requires professional medical evaluation. Please consult a nearby doctor or visit a hospital.' "
                        "Ensure clarity, avoid speculation, prioritize safety, and use bullet points for lists."
                    ),
                },
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{prompt}"}
            ],
            max_tokens=1000,
            temperature=0.5,
            top_p=1
        )
        raw_content = response.choices[0].message.content.strip() if response.choices else "No response available"
        
        # Search for a YouTube video if youtube_api_key is provided
        youtube_link = ""
        if youtube_api_key:
            video_url, video_title = search_youtube_video(prompt, youtube_api_key)
            if video_url and video_title:
                youtube_link = f"\n\n[Watch a video on this topic: {video_title}]({video_url})"
        
        # Format the response
        lines = raw_content.split("\n")
        formatted_response = ""
        for line in lines:
            line = line.strip()
            if line.startswith("##"):
                formatted_response += f"\n{line}\n"
            elif line.startswith("* ") or line.startswith("- "):
                formatted_response += f"- {line[2:]}\n"
            else:
                formatted_response += f"{line}\n"
        
        # Append YouTube link if available
        formatted_response = (formatted_response.strip() + youtube_link) or "No valid response generated"
        return formatted_response
    except Exception as e:
        return f"Error generating response: {str(e)}"