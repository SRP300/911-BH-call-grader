from __future__ import annotations

from typing import Any, Dict, List


DEMO_CALLS: List[Dict[str, Any]] = [
    {
        "metadata": {
            "call_id": "#2026-0847",
            "date": "March 15, 2026",
            "operator": "Operator A",
            "duration": "4:12",
            "call_type": "Suspected Overdose",
        },
        "transcript_text": (
            "Caller: Hi, I found a person slumped over on the sidewalk. I think they overdosed—blue lips.\n"
            "Operator: I’m here. What’s your address right now?\n"
            "Caller: 742 Maple Street, apartment entrance on the north side.\n"
            "Operator: Thank you. Are they awake or breathing normally?\n"
            "Caller: They’re not waking up. Their chest is barely moving.\n"
            "Operator: Okay. Do you have naloxone, Narcan, or any overdose rescue kit available?\n"
            "Caller: Yes. I have Narcan in my bag.\n"
            "Operator: Great. Please keep distance from anything you think could be used and approach only if it’s safe.\n"
            "Operator: While we’re sending help, I want you to open their airway. Tilt their head back and check breathing.\n"
            "Caller: Okay.\n"
            "Operator: If they’re not breathing normally, do rescue breaths and prepare to use the Narcan.\n"
            "Caller: I can do that.\n"
            "Operator: You did the right thing calling. If you're worried about legal issues, the Good Samaritan Law protects people who help in an overdose emergency.\n"
            "Caller: I didn’t know that—thank you.\n"
            "Operator: How many people are with them? And do you see any pills, bags, or drug paraphernalia nearby?\n"
            "Caller: Just one person. There’s a small bag and some pills on the ground.\n"
            "Operator: Thank you. Stay on the line with me. EMS is on the way now. Tell me if their breathing changes.\n"
            "Caller: Okay, I’m staying.\n"
            "Operator: Good. Keep reassurance—help is coming. If the Narcan is ready, administer it when you can safely.\n"
            "Caller: I will.\n"
        ),
    },
    {
        "metadata": {
            "call_id": "#2026-0851",
            "date": "March 15, 2026",
            "operator": "Operator B",
            "duration": "2:45",
            "call_type": "Person Down / Unknown Medical",
        },
        "transcript_text": (
            "Caller: Hi, I found someone unconscious outside. I’m not sure what’s wrong.\n"
            "Operator: Okay, where are you?\n"
            "Caller: Near Oak and Elm. I don't know the exact address.\n"
            "Operator: Send a unit.\n"
            "Caller: Should I check on them? They’re not responding.\n"
            "Operator: Just wait.\n"
            "Caller: Are they dangerous? I think they might have taken something.\n"
            "Operator: We’ll send someone. Don’t move them.\n"
            "Caller: I don’t have any naloxone—should I still do something?\n"
            "Operator: I don’t know. Someone will be there.\n"
            "Caller: Okay… they’re making weird noises.\n"
            "Operator: OK, we’ll send a unit. Goodbye.\n"
        ),
    },
]

