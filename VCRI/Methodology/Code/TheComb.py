import os
import json
import time
import re
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURATION ---
API_KEY = "API_KEY" # <--- Paste Key Here
INPUT_FOLDER = "transcripts"       
OUTPUT_FILE = "fcl_harvest_v3.json" 
MODEL_NAME = "models/gemini-1.5-flash" 

# --- THE COMB PROTOCOL V3.0 ---
CATCH_PROTOCOL = """
You are 'The Comb', a specialized extraction engine for the Field of Consciousness (FoC) framework.
Your job is to analyze the provided transcript and extract 'High-EPM (Events Per Modal Layer)' moments.

CRITICAL FORMATTING RULE:
- You must output VALID JSON.
- Double-escape backslashes (e.g., "\\\\epsilon").

PROTOCOL: FCL CATCH METHOD V3.0 (UPDATED)
1. Scan for FOUR trigger types:
   - RELATIONAL: Rapid speaker alternation, sentence completion, simultaneous realization.
   - EMOTIONAL: Markers like 'Whoa', 'Chills', 'Goosebumps', 'Holy sh*t', profound silence.
   - SEMANTIC: Keywords like 'Gravity', 'Tether', 'Octahedron', '8pi', 'The Room', 'Static'.
   - PHENOMENOLOGICAL: Specific visual/sensory details. Keywords: 'texture', 'filament', 'grid', 'flash', 'geometric', 'cobweb', 'layer', 'gradient', 'seeing through eyelids', 'hands', 'tactile', 'nausea', 'visual imprint'.

2. Extract valid events into this JSON Schema:
   {
      "event_id": "UUID_v4",
      "timestamp_audio": "MM:SS (Approximate relative time in file)",
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
   Return ONLY a raw JSON list of objects. Example: [ {...}, {...} ]
"""

def setup_environment():
    genai.configure(api_key=API_KEY)

def extract_datetime_from_filename(filename):
    """
    Repairs timestamps using the filename.
    Handles '20250927 102539' (ConRec) and '20250420_033211' (Chat export).
    """
    # Regex to capture YYYYMMDD followed optionally by HHMMSS (space or underscore separator)
    match = re.search(r"(\d{8})[ _]?(\d{6})?", filename)
    
    if match:
        date_part = match.group(1)
        time_part = match.group(2)
        
        try:
            if time_part:
                # Full Date + Time found
                dt_str = f"{date_part} {time_part}"
                dt = datetime.strptime(dt_str, "%Y%m%d %H%M%S")
            else:
                # Date only found, default to noon
                dt = datetime.strptime(date_part, "%Y%m%d")
                dt = dt.replace(hour=12, minute=0, second=0)
            
            # Return SQL-style string
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None
    return None

def clean_json_text(text):
    text = text.strip()
    if text.startswith("```json"): text = text[7:]
    if text.startswith("```"): text = text[3:]
    if text.endswith("```"): text = text[:-3]
    return text

def repair_json_escapes(text):
    invalid_escape_pattern = r'\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})'
    return re.sub(invalid_escape_pattern, r'\\\\', text)

def process_file(filepath, filename):
    print(f"Scanning: {filename}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        model = genai.GenerativeModel(MODEL_NAME, system_instruction=CATCH_PROTOCOL)
        response = model.generate_content(content)
        clean_text = clean_json_text(response.text)
        
        try:
            events = json.loads(clean_text)
        except json.JSONDecodeError:
            print(f"   ...JSON error. Attempting regex repair...")
            repaired_text = repair_json_escapes(clean_text)
            try:
                events = json.loads(repaired_text)
            except:
                return []

        # --- THE REPAIR PATCH ---
        # Immediately fix the date using the filename
        file_dt = extract_datetime_from_filename(filename)
        
        for event in events:
            # Tag source
            if "metadata" not in event: event["metadata"] = {}
            event["metadata"]["source_file"] = filename
            
            # If we found a valid date in filename, apply it
            if file_dt:
                # If the AI guessed a relative time (like "04:36"), we could refine this later.
                # For now, we stamp the event with the File's creation/end time.
                event["timestamp_realtime"] = file_dt

        print(f" -> Caught {len(events)} events.")
        return events

    except Exception as e:
        print(f" -> ERROR: {e}")
        return []

def main():
    setup_environment()
    
    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        print(f"Created '{INPUT_FOLDER}'. Add .md files and run again.")
        return

    all_new_events = []
    files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith('.md')]
    
    print(f"Initializing The Comb v3. Found {len(files)} transcripts.")
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