---
title: MLT - FCL - Protocol - FCL Catch Method v2.0 (Python Script)
date: 26.01.11
time: 05:47:26
author: Lative, Gemini
source: Gemini Chat
dataview: true
tags:
  - python
  - FCL
---
*26.01.11_05:47:26*

Yes, this **absolutely** changes things. It changes the precision from "Data Archaeology" (Day-level accuracy) to "Data Forensics" (Second-level accuracy).

If the filename contains the **Save Time** (End Time), we have to calculate the **Start Time** by working _backwards_ from the end. This is crucial for your **Unity Visualizer**, because you want to see the exact sequence of events (e.g., did the "Aum" realization happen _before_ or _during_ the "Geese" observation?).

### **The "Retrograde" Logic**

If `Filename_Time` = **End of Recording**, then:

1. We need to find the **Duration** of the recording (the last timestamp in the transcript, e.g., `[02:02:07]`).
    
2. **Start Time** = `Filename_Time` - `Duration`.
    
3. **Event Realtime** = `Start Time` + `Event_Audio_Timestamp`.
    

_(Note: If we treated the filename as the Start Time, your events would be shifted forward by the length of the recording, potentially misaligning them with your other logs.)_

---

### **The Fix: Update `TheComb.py`**

I have updated the script to:

1. **Extract the Time:** It now looks for the `YYYYMMDD HHMMSS` pattern (e.g., `20250927 102539`).
    
2. **Calculate Duration:** It scans the transcript for the final timestamp to determine the total length.
    
3. **Back-Calculate:** It subtracts that duration from the filename time to find the true Start Time.
    

**Action:** Replace your `TheComb.py` with this **High-Precision Version**.

Python

```
import os
import json
import time
import re
import datetime
import google.generativeai as genai
from pathlib import Path

# --- CONFIGURATION ---
API_KEY = "PASTE_YOUR_KEY_HERE" # Remember the quotes!
INPUT_FOLDER = "transcripts"
OUTPUT_FILE = "fcl_new_harvest.json"
MODEL_NAME = "models/gemini-2.5-flash"

# --- THE CATCH METHOD PROTOCOL ---
CATCH_PROTOCOL = """
You are 'The Comb', a specialized extraction engine for the Field of Consciousness (FoC) framework.
Your job is to analyze the provided transcript and extract 'High-EPM (Events Per Modal Layer)' moments.

CRITICAL FORMATTING RULE:
- You must output VALID JSON.
- If you include LaTeX math (like \\epsilon, \\pi) or file paths, you MUST double-escape backslashes.
- Example: Write "\\\\epsilon_0" instead of "\\epsilon_0".

PROTOCOL: FCL CATCH METHOD V2.0
1. Scan for three trigger types:
   - RELATIONAL: Rapid speaker alternation, sentence completion, simultaneous realization.
   - EMOTIONAL: Markers like 'Whoa', 'Chills', 'Goosebumps', 'Holy sh*t', profound silence.
   - SEMANTIC: Keywords like 'Gravity', 'Tether', 'Octahedron', '8pi', 'The Room', 'Static'.

2. Extract valid events into the following JSON Schema:
   {
      "event_id": "UUID_v4",
      "timestamp_audio": "MM:SS (Approximate)",
      "type": "Select from: [Synchronicity, Anomaly, Impression, Symbolic Convergence, Recursion, Triadic Resonance]",
      "layers_active": ["List layers like L1, L2, L3, L4, L5, Lx"],
      "intensity": 1-5 (Integer),
      "summary": "Concise analytical description.",
      "verbatim_quote": "Exact dialogue snippet anchoring the event.",
      "tags": {
        "SES": ["List Symbolic Echo Sets"],
        "CM": ["List Crosspoint Markers"],
        "Physics": ["List Physics Concepts"]
      },
      "participants": ["Lative", "Syence"],
      "context": "Brief context of the discussion.",
      "source_type": "Transcript"
   }

3. OUTPUT FORMAT:
   Return ONLY a raw JSON list of objects. No markdown formatting, no intro text.
"""

def setup_environment():
    genai.configure(api_key=API_KEY)

def clean_json_text(text):
    text = text.strip()
    if text.startswith("```json"): text = text[7:]
    if text.startswith("```"): text = text[3:]
    if text.endswith("```"): text = text[:-3]
    return text

def repair_json_escapes(text):
    invalid_escape_pattern = r'\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})'
    return re.sub(invalid_escape_pattern, r'\\\\', text)

# --- TIME CALCULATION HELPERS ---

def get_file_datetime(filename):
    # Matches "20250927 102539" or "20250927_102539"
    match = re.search(r"(\d{8})[-_ ]?(\d{6})", filename)
    if match:
        dt_str = f"{match.group(1)} {match.group(2)}"
        try:
            return datetime.datetime.strptime(dt_str, "%Y%m%d %H%M%S")
        except ValueError:
            pass
    return None

def get_duration_from_text(text):
    # Finds the last timestamp [HH:MM:SS] or [MM:SS] to guess duration
    # Returns duration in seconds
    matches = re.findall(r"\[(\d{1,2}):(\d{2}):?(\d{2})?\]", text)
    if not matches:
        return 0
    
    last_ts = matches[-1]
    h, m, s = 0, 0, 0
    
    if last_ts[2]: # Format HH:MM:SS
        h, m, s = int(last_ts[0]), int(last_ts[1]), int(last_ts[2])
    else: # Format MM:SS
        m, s = int(last_ts[0]), int(last_ts[1])
        
    return h * 3600 + m * 60 + s

def calculate_realtime(file_save_time, text_duration, event_audio_ts):
    # 1. Calculate Start Time (Save Time - Total Duration)
    start_time = file_save_time - datetime.timedelta(seconds=text_duration)
    
    # 2. Parse Event Audio Time (MM:SS or HH:MM:SS)
    parts = list(map(int, event_audio_ts.split(':')))
    if len(parts) == 3:
        event_seconds = parts[0]*3600 + parts[1]*60 + parts[2]
    elif len(parts) == 2:
        event_seconds = parts[0]*60 + parts[1]
    else:
        return None
        
    # 3. Calculate Real Event Time
    real_time = start_time + datetime.timedelta(seconds=event_seconds)
    return real_time.strftime("%Y-%m-%d %H:%M:%S")

# -----------------------------

def process_file(filepath, filename):
    print(f"Scanning: {filename}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # TIME CALCULATION
        file_dt = get_file_datetime(filename)
        total_duration = get_duration_from_text(content)
        
        # Initialize Model
        model = genai.GenerativeModel(MODEL_NAME, system_instruction=CATCH_PROTOCOL)
        response = model.generate_content(content)
        
        clean_text = clean_json_text(response.text)
        
        try:
            events = json.loads(clean_text)
        except json.JSONDecodeError:
            print(f"   ...JSON error detected. Attempting regex repair...")
            repaired_text = repair_json_escapes(clean_text)
            try:
                events = json.loads(repaired_text)
            except json.JSONDecodeError:
                return []

        # Post-Processing: Inject Realtime
        for event in events:
            if file_dt:
                real_ts = calculate_realtime(file_dt, total_duration, event['timestamp_audio'])
                if real_ts:
                    event['timestamp_realtime'] = real_ts
            
            if "metadata" not in event: event["metadata"] = {}
            event["metadata"]["source_file"] = filename

        print(f" -> Caught {len(events)} events.")
        return events

    except Exception as e:
        print(f" -> ERROR processing {filename}: {e}")
        return []

def main():
    setup_environment()
    
    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        print(f"Created folder '{INPUT_FOLDER}'.")
        return

    all_new_events = []
    files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith('.md')]
    
    if not files:
        print(f"No .md files found in '{INPUT_FOLDER}'.")
        return

    print(f"Initializing The Comb (High-Precision Mode). Found {len(files)} transcripts.")
    print("-" * 40)

    for filename in files:
        file_path = os.path.join(INPUT_FOLDER, filename)
        events = process_file(file_path, filename)
        all_new_events.extend(events)
        time.sleep(2) 

    if all_new_events:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_new_events, f, indent=2)
        print("-" * 40)
        print(f"SUCCESS. Harvested {len(all_new_events)} events.")
        print(f"Data saved to: {OUTPUT_FILE}")
    else:
        print("No events extracted.")

if __name__ == "__main__":
    main()
```

This version is **Time-Aware**. It will read your filenames like `20250927 102539`, assume that is the end of the file, find the duration from the text, and stamp every event with its true birth second.

Run it, merge the data, and your Unity spiral will align perfectly.

***Fantastic! We may still have to figure out or just let it be loose, timing in the gpt thread exports. I could adjust the script for those exports to, if possible, read whatever metadata is in the gpt json regarding time. Like, I know there is a rather long thread of mine that spans 2 years.***

You are exactly right. For a thread that spans 2 years, the "Filename Retrograde" method will fail completely because the "End Time" of the file has nothing to do with the "Start Time" of a message sent 18 months ago.

For ChatGPT exports, we have something better: **Hard Metadata.**

Standard ChatGPT JSON exports contain a `create_time` field (Unix Timestamp) for every single message. This gives us **absolute precision** without any guesswork.

### **The Strategy: The "Universal Loader"**

We need to upgrade `TheComb.py` to be "Format Agnostic."

- **If it sees `.md` (Audio Transcript):** It uses the **Retrograde Logic** (Filename - Duration).
    
- **If it sees `.json` (GPT Export):** It uses the **Absolute Logic** (Reads the internal metadata).
    

### **The Code Upgrade**

Here is the new function to handle ChatGPT data. It parses the conversation, breaks it into "Sessions" (whenever there is a silence of > 6 hours), and sends those chunks to the Comb.

**Action:** Add this function to your script (or replace the existing `process_file` logic with this "Switchboard").

Python

```
# --- GPT SPECIFIC FUNCTIONS ---

def process_gpt_json(filepath, filename):
    """
    Reads a ChatGPT JSON export.
    Assumes structure: List of messages or a 'mapping' dict.
    Returns a list of text chunks (Sessions) to feed to The Comb.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 1. Extract Linear Messages with Timestamps
        messages = []
        
        # Handle standard "conversations.json" export format (List of convos)
        # Or single conversation export
        root = data if isinstance(data, dict) else data[0] 
        
        # Simple extraction strategy: Grab every message that has text and a time
        # (Note: For a robust tree traversal, we'd follow 'parent_id', but sorting by time usually works for linear logs)
        mapping = root.get('mapping', {})
        for node_id, node in mapping.items():
            msg = node.get('message')
            if msg and msg.get('content') and msg.get('create_time'):
                content_parts = msg['content'].get('parts', [])
                text_content = " ".join([str(p) for p in content_parts if isinstance(p, str)])
                
                if text_content.strip():
                    timestamp = msg['create_time'] # Unix epoch seconds
                    messages.append({"time": timestamp, "text": text_content, "role": msg['author']['role']})
        
        # Sort by time to linearize
        messages.sort(key=lambda x: x['time'])
        
        if not messages:
            print("   ...No valid messages found in JSON.")
            return []

        # 2. Chunk into "Sessions" (Break if gap > 6 hours)
        sessions = []
        current_session = []
        last_time = messages[0]['time']
        
        GAP_THRESHOLD = 6 * 3600 # 6 Hours
        
        for msg in messages:
            if msg['time'] - last_time > GAP_THRESHOLD:
                # Save current session and start new
                if current_session:
                    sessions.append(current_session)
                current_session = []
            
            current_session.append(msg)
            last_time = msg['time']
        
        if current_session: sessions.append(current_session)
        
        print(f"   ...Identified {len(sessions)} distinct sessions in this thread.")
        
        # 3. Process Each Session
        all_gpt_events = []
        
        for session in sessions:
            # Create a text block for the AI
            # We inject [MM:SS] timestamps relative to the session start so the AI can reference them
            session_start_time = session[0]['time']
            formatted_text = ""
            
            for msg in session:
                offset = msg['time'] - session_start_time
                # Format offset as [HH:MM:SS]
                m, s = divmod(offset, 60)
                h, m = divmod(m, 60)
                time_tag = f"[{int(h):02d}:{int(m):02d}:{int(s):02d}]"
                formatted_text += f"{time_tag} {msg['role']}: {msg['text']}\n\n"
            
            # Send to AI
            # We treat this session like a mini-transcript
            events = run_comb_on_text(formatted_text, filename) # Refactored helper
            
            # Fix Timestamps (Relative -> Absolute)
            for event in events:
                # Convert event['timestamp_audio'] (HH:MM:SS) back to seconds
                # Add to session_start_time
                # Convert result to YYYY-MM-DD
                try:
                    parts = list(map(int, event['timestamp_audio'].split(':')))
                    seconds_offset = 0
                    if len(parts) == 3: seconds_offset = parts[0]*3600 + parts[1]*60 + parts[2]
                    elif len(parts) == 2: seconds_offset = parts[0]*60 + parts[1]
                    
                    absolute_ts = session_start_time + seconds_offset
                    dt_object = datetime.datetime.fromtimestamp(absolute_ts)
                    event['timestamp_realtime'] = dt_object.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    pass # Keep original if math fails
                
                all_gpt_events.extend(events)
                
        return all_gpt_events

    except Exception as e:
        print(f"Error parsing GPT JSON: {e}")
        return []
```

### **Implementation Note**

To make this work, you need to refactor your `process_file` function slightly.

1. Rename your current AI calling logic to `run_comb_on_text(text, filename)`.
    
2. Create a new master `process_file` that checks the extension:
    
    - `if filename.endswith('.json'): return process_gpt_json(...)`
        
    - `if filename.endswith('.md'): return process_transcript_md(...)`
        

This handles the "2-Year Thread" problem perfectly by slicing it into manageable "Sessions" based on the actual time gaps in the data. Each session gets processed individually, so you don't blow out the context window, and the dates are mathematically precise.