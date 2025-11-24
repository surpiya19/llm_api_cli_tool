#!/usr/bin/env python3
"""
Interactive Story Game - A CLI tool using Google Gemini API
Choose your adventure and let AI create dynamic stories based on your choices!
"""

import os
import sys
import json
import time
from urllib import request, parse, error

API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


def print_slow(text, delay=0.03):
    "text with typewrite effect for textual feel"
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def call_gemini(prompt, context=""):
    """calling the api"""
    if not API_KEY:
        print("Error: GEMINI_API_KEY environment variable not set!")
        sys.exit(1)

    full_prompt = f"{context}\n\n{prompt}" if context else prompt

    data = {"contents": [{"parts": [{"text": full_prompt}]}]}

    # Adding API key as URL parameter
    url = f"{BASE_URL}?key={API_KEY}"

    req = request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    try:
        with request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["candidates"][0]["content"]["parts"][0]["text"]
    except error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"API Error: {e.code} - {e.reason}")
        print(f"Details: {error_body}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def display_banner():
    """Display game banner"""
    banner = """
    ╔═══════════════════════════════════════╗
         🎭 INTERACTIVE STORY GAME 🎭         
    ║   Powered by Google Gemini AI         ║
    ╚═══════════════════════════════════════╝
    """
    print(banner)


def choose_genre():
    """Letting user choose a story genre"""
    print("\nChoose your adventure genre:")
    genres = [
        "🏰 Fantasy",
        "🚀 Sci-Fi Space Opera",
        "🕵️ Mystery Detective",
        "🧟 Horror Survival",
        "🤠 Western",
        "🏴‍☠️ Pirate",
    ]

    for i, genre in enumerate(genres, 1):
        print(f"{i}. {genre}")

    while True:
        try:
            choice = int(input("\nEnter number (1-6): "))
            if 1 <= choice <= 6:
                return genres[choice - 1]
        except ValueError:
            pass
        print("Invalid choice. Try again.")


def play_game():
    """Main game loop"""
    display_banner()

    genre = choose_genre()
    print(f"\n✨ Starting your {genre} adventure...\n")

    # Initializing story
    init_prompt = f"""Create the opening scene for an interactive {genre} story. 
    Make it engaging and exciting (3-4 sentences). 
    End with a critical decision point and present exactly 3 choices labeled A, B, C.
    Keep it concise and thrilling."""

    story_context = f"Genre: {genre}\n"
    current_scene = call_gemini(init_prompt)

    turn = 1
    max_turns = 8

    while turn <= max_turns:
        print("=" * 60)
        print_slow(current_scene)
        print("=" * 60)

        # Get user choice
        choice = input("\nYour choice (A/B/C) or 'quit' to exit: ").strip().upper()

        if choice == "QUIT":
            print("\n👋 Thanks for playing!")
            break

        if choice not in ["A", "B", "C"]:
            print("Please choose A, B, or C.")
            continue

        # Update story context
        story_context += f"\nTurn {turn}: {current_scene}\nPlayer chose: {choice}\n"

        if turn == max_turns:
            # Generate ending
            prompt = f"""Based on choice {choice}, write a dramatic conclusion to this story (4-5 sentences). 
            Make it satisfying and memorable. This is the final scene."""
            current_scene = call_gemini(prompt, story_context)
            print("\n" + "=" * 60)
            print_slow(current_scene)
            print("=" * 60)
            print("\n🎬 THE END 🎬")
            break
        else:
            # Continue story
            prompt = f"""The player chose {choice}. Continue the story with the consequence of this choice.
            Make it exciting (3-4 sentences) and end with a new critical decision.
            Present exactly 3 new choices labeled A, B, C. Keep responses concise."""
            current_scene = call_gemini(prompt, story_context)

        turn += 1
        time.sleep(0.5)

    # Ask to play again
    again = input("\n🎮 Play again? (y/n): ").strip().lower()
    if again == "y":
        print("\n" * 2)
        play_game()
    else:
        print("\n👋 Thanks for playing! May your stories never end!")


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted. Thanks for playing!")
        sys.exit(0)
