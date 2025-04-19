import google.generativeai as genai

# 🔑 Set up Gemini API key
genai.configure(api_key="AIzaSyAEYftynJXvtM7hnTS3E19GKkpnjGfV-mI")

# 🎯 Use the fast, free Gemini Flash model
model = genai.GenerativeModel('gemini-1.5-flash')

# 📜 Start the short-style, AI-guided story
conversation = [
    {
        "role": "user",
        "parts": [
            "You're an AI game engine. Start a creative and random story with just a short sentence (max 6 words). After every player input, continue the story briefly in 6-7 words max. Be vivid, but super concise. If the player dies, say it clearly like 'You died' or 'Game over'."
        ]
    }
]

# ✨ Begin the game
response = model.generate_content(conversation)
ai_text = response.text.strip()
print("\n🌟 AI:", ai_text)

# Save AI’s first message
conversation.append({"role": "model", "parts": [ai_text]})

# ⚔️ Keywords that mean the player is dead
death_keywords = ["you died", "you are dead", "game over", "your journey ends", "you fall lifeless"]

# 🎮 Game loop
while True:
    try:
        player_input = input("\n🧍 You: ")
        if player_input.lower() in ["quit", "exit"]:
            print("👋 Game exited.")
            break

        # Add player input
        conversation.append({"role": "user", "parts": [player_input]})

        # Get AI continuation
        response = model.generate_content(conversation)
        ai_text = response.text.strip()
        print("\n🌟 AI:", ai_text)

        # Check for death
        if any(phrase in ai_text.lower() for phrase in death_keywords):
            print("💀 The story ends here.")
            break

        # Add AI response to convo
        conversation.append({"role": "model", "parts": [ai_text]})

    except KeyboardInterrupt:
        print("\n👋 Interrupted. See you next time.")
        break
    except Exception as e:
        print("⚠️ Error:", e)
        break
