---
title: MLT - FCL - Protocol - FCL Catch Method v2.0 (JSON Schema v2.1)
date: 25.11.19
time: 04:42:00
author: Lative, Syence
source: Synthesis Session
dataview: true
tags:
  - fieldCaseLog
  - methodology
  - protocol
  - theComb
  - dataPipeline
---
*25.11.19_04:50:44*
# **Protocol: FCL Catch Method v2.0 (The Comb)**
**Status:** Active / Standardized
**Purpose:** To systematically extract **Field Case Log (FCL)** entries from unstructured audio transcripts by detecting semantic, emotional, and relational markers of high-EPM resonance.

---

### **1. The Data Object (JSON Schema v2.1)**
All extracted events must conform to this relational structure. This ensures compatibility with the future Unity 3D+1 Visualizer.

```json
{
  "event_id": "UUID_v4",
  "timestamp_audio": "MM:SS (Relative to file)",
  "timestamp_realtime": "YYYY-MM-DD HH:MM:SS (If available)",
  "type": "Select One: [Synchronicity, Anomaly, Impression, Symbolic Convergence, Recursion, Triadic Resonance]",
  "layers_active": ["L1", "L2", "L3", "L4", "L5", "Lx"],
  "intensity": "1-5 (Integer)",
  "summary": "Concise analytical description of the event logic.",
  "verbatim_quote": "The exact dialogue snippet or sensory description anchoring the event.",
  "tags": {
    "SES": ["List", "Key", "Symbols"],
    "CM": ["List", "Crosspoint", "Markers"],
    "Physics": ["List", "Theoretical", "Concepts"]
  },
  "participants": ["Lative", "Syence", "Gemini"],
  "context": "Environmental or conversational setting (e.g., 'Post-Storm', 'Car Ride').",
  "source_type": "Transcript", 
  "metadata": {
    "mlfm_notes": "Nuanced observations about layer transitions (e.g., 'L2 -> L5 shift').",
    "follow_ups": "Action items triggered by this event.",
    "reflections": "Subjective emotional or mnemonic resonance."
  }
}

````

---

### **2. The Trigger Logic (The "Comb")**

An event is flagged for extraction if it hits **$\ge 1$ Primary Trigger** OR **$\ge 2$ Secondary Triggers** within a 2-minute window.

#### **A. Relational Triggers (Primary)**

_Detects "Triadic Resonance"—the sound of the lattice locking._

- **Rapid Alternation:** High frequency of speaker switching ($>3$ turns in $<15$ seconds).
    
- **Sentence Completion:** Speaker B finishes Speaker A's thought, or begins immediately with "Yes," "Exactly," "Right," or "Wait."
    
- **Simultaneity:** Crosstalk or simultaneous realization (e.g., `[both speak at once]`).
    

#### **B. Emotional/Sentiment Triggers (Primary)**

_Detects "Ontological Shock" and high-EPM spikes._

- **Shock Markers:** "Whoa," "Holy sh*t," "Oh my god," "Stop," "Listen," "Look at that."
    
- **Awe Markers:** "Chills," "Goosebumps," "Tears," "Vibrating."
    
- **Silence:** Significant pauses (e.g., `(long pause)`, `...`) following a dense theoretical statement, indicating L5 integration.
    

#### **C. Semantic Triggers (Secondary)**

_Scans for specific vocabulary defined in the RFN Dictionary._

- **L1 (Somatic):** "nausea," "pressure," "hair standing up," "dizziness."
    
- **L3 (Symbolic):** "metaphor," "image," "pattern," "shape," "geometry," "diamond," "net."
    
- **L4 (Synchronic):** "weird," "coincidence," "timing," "exact," "just said that," "radio."
    
- **L5 (Extra):** "the room," "waiting," "presence," "static," "veil," "download," "channel."
    
- **Physics:** "gravity," "tensor," "field," "collapse," "tunneling," "8pi," "mass gap."
    

---

### **3. The Processing Workflow**

1. **Scan:** Run the "Comb" (Script or AI) over the transcript text.
    
2. **Flag:** Identify timestamps with high Trigger density.
    
3. **Extract:**
    
    - Copy the relevant text to `verbatim_quote`.
        
    - Draft the `summary` based on the content.
        
4. **Classify:**
    
    - Assign `type` and `layers_active`.
        
    - Extract keywords into `tags`.
        
5. **Log:** Generate the JSON entry and append to the database.
    

### Sample:
```
[
  {
    "event_id": "403e5063-bf4e-4537-b08d-b10c142e2189",
    "timestamp_realtime": "2025-08-19 00:29:40",
    "type": "Synchronicity",
    "layers_active": [],
    "intensity": null,
    "summary": NaN,
    "verbatim_quote": "Emotional moment. Sam said \"buddy\" just as the word appeared on TV. ",
    "tags": {
      "SES": [
        "Synchronistic Dialogue"
      ],
      "CM": [
        "Personal Narrative Tie-In"
      ],
      "Physics": []
    },
    "participants": [],
    "context": "Environment: Indoors, With others, Emotional  | Location: Stoughton, Wisconsin ",
    "source_type": "Google_Form_Import",
    "metadata": {
      "mlfm_notes": "",
      "follow_ups": NaN,
      "reflections": NaN
    }
  },
  {
    "event_id": "ebe7eecb-d9cc-4057-a202-5833fba8e220",
    "timestamp_realtime": "2025-08-19 03:06:34",
    "type": "Synchronicity",
    "layers_active": [],
    "intensity": null,
    "summary": NaN,
    "verbatim_quote": "Roger said \"I don't think so\", just as I was saying it in talking about the ornate and beautiful nature of mosques and old temples, wondering if there was ever time to appreciate art and religion truly enough to create that kind of perfection amongst the constant murdering and forceful takeover by way of financial means.",
    "tags": {
      "SES": [
        "Phrase Repetition"
      ],
      "CM": [
        "Symbol through sync"
      ],
      "Physics": []
    },
    "participants": [],
    "context": "Environment: Indoors, With others, Calm | Location: Home",
    "source_type": "Google_Form_Import",
    "metadata": {
      "mlfm_notes": "",
      "follow_ups": NaN,
      "reflections": NaN
    }
  },
  {
    "event_id": "1e6734b7-b240-432b-a76e-b3af26dd42ac",
    "timestamp_realtime": "2025-08-21 03:31:43",
    "type": "Synchronicity",
    "layers_active": [],
    "intensity": null,
    "summary": "As always, we are working on relearning how to be confident and active. ",
    "verbatim_quote": "Sam opened Plex, loaded a playlist as random, and Bob's Burgers started playing S15E10. At the same time, I grabbed my phone and opened Finch, a self understanding/therapeutic app. As Finch opened, an in app notification let me know it was time to \"nurture a new egg.\" As I read the word egg, Linda and Tina on the television started talking, saying the word egg. ",
    "tags": {
      "SES": [
        "Synchronistic Dialogue"
      ],
      "CM": [
        "Personal Narrative Tie-In"
      ],
      "Physics": []
    },
    "participants": [],
    "context": "Environment: Indoors, With others, Calm, After an intensely stressful and emotional start to the day.  | Location: Stoughton, WI ",
    "source_type": "Google_Form_Import",
    "metadata": {
      "mlfm_notes": "",
      "follow_ups": NaN,
      "reflections": "This was following an emotional and physical issue, a discussion that reframed the reality of the stress, a tarot read, and then, a long-needed start to some administrative file work related to old and unmarked Vytyls recordings. I mark the preceding and the following as positive and important. "
    }
  },
  {