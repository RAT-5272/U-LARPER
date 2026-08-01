# Limitations
"""
This was made specifically for the U-LARPER architecture and thus lacks some features like:
- Thinking (a "Thinking" channel): The decoder should NOT be able to reason, that will be left to the reasoning core.

And also includes some features like:
- Blend of attachments and plain text: The model is meant to reason about any form of media indiscriminately,
  separating media and text already goes against this principle. Special modality delimiter tokens are also inserted in a separate stage
"""



# Special Tokens and their meaning
"""
Conversational:
[Ꝟ Header Ꝟ]           This marks the start of a conversation
[Ꝟ ConversationID Ꝟ]   Represents the ID of the current conversation per user
[Ꝟ Timestamp Ꝟ]        Start time of the conversation
[Ꝟ LatestTimestamp Ꝟ]  Time the last user message was sent
[Ꝟ HeaderEnd Ꝟ]        This marks the end of the metadata

[Ꝟ ResponseID Ꝟ]       Marks the start of a response and increments for every response per conversation, allowing for branching, edits, retries, or even message referencing
[Ꝟ ParentResponseID Ꝟ] ResponseID of the parent response, exists for same reasons as ResponseID
[Ꝟ Sender Ꝟ]           The entity that is sending message, it's source
[Ꝟ Channel Ꝟ]          The channel that the message is sent to, "Rules" marks guidelines, "Main" is the visible conversation, "Info" is for tool results or similar things. Channels are left in plain text to allow easy future expansion (e.g. adding a "Subagents" channel).
[Ꝟ StartMessage Ꝟ]     The start of a message to be sent to a specified channel
[Ꝟ EndMessage Ꝟ]       Marks the end of a message, does not mark EOS
[Ꝟ EndTurn Ꝟ]          The models EOS token

[Ꝟ ToolCall Ꝟ]         Explicitly shows that what comes next is a tool call.

Training:
[Ꝟ Mask Ꝟ]             Represents that this token has been hidden
"""

# Multistep with tool calls (expanded for readability)
# This was kinda hard to think of
"""
[Ꝟ Header Ꝟ]

[Ꝟ ConversationID Ꝟ] 1
[Ꝟ Timestamp Ꝟ] 1346412134
[Ꝟ LatestTimestamp Ꝟ] 1346412554
... Other metadata possibly

[Ꝟ HeaderEnd Ꝟ]




[Ꝟ ResponseID Ꝟ] 0
[Ꝟ ParentResponseID Ꝟ] 0
[Ꝟ Sender Ꝟ] System

[Ꝟ Channel Ꝟ] Rules
[Ꝟ StartMessage Ꝟ] Tools: Allowed [Ꝟ EndMessage Ꝟ] [Ꝟ EndTurn Ꝟ]



[Ꝟ ResponseID Ꝟ] 1
[Ꝟ ParentResponseID Ꝟ] 0
[Ꝟ Sender Ꝟ] User

[Ꝟ Channel Ꝟ] Main
[Ꝟ StartMessage Ꝟ] Hello, can you please help me? [Ꝟ EndMessage Ꝟ] [Ꝟ EndTurn Ꝟ]



[Ꝟ ResponseID Ꝟ] 2
[Ꝟ ParentResponseID Ꝟ] 1
[Ꝟ Sender Ꝟ] Assistant

[Ꝟ Channel Ꝟ] Main
[Ꝟ StartMessage Ꝟ] Sure, I'm always happy to help! What is it you need help with? [Ꝟ EndMessage Ꝟ] [Ꝟ EndTurn Ꝟ]



[Ꝟ ResponseID Ꝟ] 3
[Ꝟ ParentResponseID Ꝟ] 2
[Ꝟ Sender Ꝟ] User

[Ꝟ Channel Ꝟ] Main
[Ꝟ StartMessage Ꝟ] Can you tell me what the weather is in Tokyo? [Ꝟ EndMessage Ꝟ] [Ꝟ EndTurn Ꝟ]



[Ꝟ ResponseID Ꝟ] 4
[Ꝟ ParentResponseID Ꝟ] 3
[Ꝟ Sender Ꝟ] Assistant

[Ꝟ Channel Ꝟ] Invoke
[Ꝟ StartMessage Ꝟ] [Ꝟ ToolCall Ꝟ] {"Name": "Weather", "City": "Tokyo"} [Ꝟ EndMessage Ꝟ] [Ꝟ EndTurn Ꝟ]



[Ꝟ ResponseID Ꝟ] 5
[Ꝟ ParentResponseID Ꝟ] 4
[Ꝟ Sender Ꝟ] Weather (Tool)

[Ꝟ Channel Ꝟ] Info
[Ꝟ StartMessage Ꝟ] Temperature: 4C
Humidity: 12%
Cloud Cover: 53% [Ꝟ EndMessage Ꝟ] [Ꝟ EndTurn Ꝟ]



[Ꝟ ResponseID Ꝟ] 6
[Ꝟ ParentResponseID Ꝟ] 3
[Ꝟ Sender Ꝟ] Assistant

[Ꝟ Channel Ꝟ] Main
[Ꝟ StartMessage Ꝟ] Currently, in Tokyo, Japan, the temperature is 4 degrees Celcius, the humidity is 12% and cloud cover is at 53%. This weather is not great for most outdoor activities due to the cold, but indoor activities should still be fun! [Ꝟ EndMessage Ꝟ] [Ꝟ EndTurn Ꝟ]
"""







# Simple example with files
# Still expanded for readability
"""
[Ꝟ Header Ꝟ]

[Ꝟ ConversationID Ꝟ] 1
[Ꝟ Timestamp Ꝟ] 1346412612
[Ꝟ LatestTimestamp Ꝟ] 1346412614
... Other metadata possibly

[Ꝟ HeaderEnd Ꝟ]




[Ꝟ ResponseID Ꝟ] 0
[Ꝟ ParentResponseID Ꝟ] 0
[Ꝟ Sender Ꝟ] System

[Ꝟ Channel Ꝟ] Rules
[Ꝟ StartMessage Ꝟ] Tools: Allowed [Ꝟ EndMessage Ꝟ] [Ꝟ EndTurn Ꝟ]



[Ꝟ ResponseID Ꝟ] 1
[Ꝟ ParentResponseID Ꝟ] 0
[Ꝟ Sender Ꝟ] User

[Ꝟ Channel Ꝟ] Main
[Ꝟ StartMessage Ꝟ] [ALL IMAGE DATA HERE, INCLUDING THE 8 CLS TOKENS AND ALL IMAGE TOKENS] Whats in this image? [Ꝟ EndMessage Ꝟ] [Ꝟ EndTurn Ꝟ]



[Ꝟ ResponseID Ꝟ] 2
[Ꝟ ParentResponseID Ꝟ] 1
[Ꝟ Sender Ꝟ] Assistant

[Ꝟ Channel Ꝟ] Main
[Ꝟ StartMessage Ꝟ] The image features a golden retriever jumping to catch a frisbee! [Ꝟ EndMessage Ꝟ] [Ꝟ EndTurn Ꝟ]
"""



def Format():
	pass