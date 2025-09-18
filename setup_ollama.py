#!/usr/bin/env python3
"""
Ollama Setup Helper

This script helps you set up Ollama and get it running with a suitable model.
"""

import subprocess
import sys
import time
import requests
from pathlib import Path


def check_ollama_installed():
    """Check if Ollama is installed and accessible."""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[OK] Ollama is installed: {result.stdout.strip()}")
            return True
        else:
            print("[INFO] Ollama not found in PATH")
            return False
    except FileNotFoundError:
        print("[INFO] Ollama not found in PATH")
        return False


def check_ollama_running():
    """Check if Ollama server is running."""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            print("[OK] Ollama server is running")
            return True
        else:
            print("[INFO] Ollama server not responding")
            return False
    except requests.exceptions.RequestException:
        print("[INFO] Ollama server not running")
        return False


def start_ollama_server():
    """Start Ollama server."""
    print("[INFO] Starting Ollama server...")
    try:
        # Start Ollama serve in background
        process = subprocess.Popen(['ollama', 'serve'],
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)

        # Wait a bit for server to start
        time.sleep(3)

        if check_ollama_running():
            print("[OK] Ollama server started successfully")
            return True
        else:
            print("[ERROR] Failed to start Ollama server")
            return False
    except Exception as e:
        print(f"[ERROR] Error starting Ollama server: {e}")
        return False


def list_available_models():
    """List available Ollama models."""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:  # More than just the header
                print("[INFO] Available models:")
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        model_name = line.split()[0]
                        print(f"   - {model_name}")
                return [line.split()[0] for line in lines[1:] if line.strip()]
            else:
                print("[INFO] No models installed")
                return []
        else:
            print("[ERROR] Failed to list models")
            return []
    except Exception as e:
        print(f"[ERROR] Error listing models: {e}")
        return []


def pull_recommended_model():
    """Pull a recommended model for character conversations."""
    recommended_models = [
        "llama3.2:3b",    # Good balance of quality and speed
        "llama3.2:1b",    # Faster, lower quality
        "phi3:mini",      # Very fast, decent quality
        "gemma2:2b"       # Good alternative
    ]

    print("[INFO] Recommended models for character conversations:")
    for i, model in enumerate(recommended_models, 1):
        print(f"   {i}. {model}")

    print("\n[INFO] Trying to pull llama3.2:3b (recommended)...")

    try:
        process = subprocess.Popen(['ollama', 'pull', 'llama3.2:3b'],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 text=True, universal_newlines=True)

        print("[INFO] Downloading model... (this may take a few minutes)")
        for line in process.stdout:
            if 'success' in line.lower() or 'pulling' in line.lower():
                print(f"   {line.strip()}")

        process.wait()

        if process.returncode == 0:
            print("[OK] Model llama3.2:3b downloaded successfully!")
            return True
        else:
            print("[ERROR] Failed to download model")
            return False

    except Exception as e:
        print(f"[ERROR] Error downloading model: {e}")
        return False


def test_conversation():
    """Test a simple conversation with the installed model."""
    print("\n[INFO] Testing conversation capability...")

    # Add src to path
    sys.path.append(str(Path(__file__).parent / "src"))

    try:
        from src.utils.ollama_client import OllamaClient

        client = OllamaClient()
        if client.check_connection():
            print(f"[OK] Connected to Ollama with model: {client.model}")

            # Simple test
            response = client.generate_response(
                prompt="Hello! Please introduce yourself briefly.",
                system_prompt="You are a helpful AI assistant. Respond in 1-2 sentences."
            )

            if response.get('success'):
                print(f"[TEST] AI Response: {response['response']}")
                print("[OK] Conversation system working!")
                return True
            else:
                print(f"[ERROR] Test failed: {response.get('error')}")
                return False
        else:
            print("[ERROR] Cannot connect to Ollama")
            return False

    except Exception as e:
        print(f"[ERROR] Error testing conversation: {e}")
        return False


def main():
    """Main setup function."""
    print("=" * 60)
    print("OLLAMA SETUP HELPER FOR CHARACTER CONVERSATIONS")
    print("=" * 60)

    # Step 1: Check if Ollama is installed
    if not check_ollama_installed():
        print("\n[SETUP REQUIRED]")
        print("Ollama is not installed. Please:")
        print("1. Go to: https://ollama.com/download")
        print("2. Download and install Ollama for your OS")
        print("3. Run this script again")
        return

    # Step 2: Check if server is running
    if not check_ollama_running():
        print("\n[ACTION] Starting Ollama server...")
        if not start_ollama_server():
            print("Please try running 'ollama serve' manually in another terminal")
            return

    # Step 3: Check for models
    print("\n[INFO] Checking available models...")
    models = list_available_models()

    if not models:
        print("\n[ACTION] No models found. Downloading recommended model...")
        if not pull_recommended_model():
            print("Please try running 'ollama pull llama3.2:3b' manually")
            return
    else:
        print(f"[OK] Found {len(models)} model(s)")

    # Step 4: Test conversation
    if not test_conversation():
        print("[ERROR] Conversation test failed")
        return

    # Final success message
    print("\n" + "=" * 60)
    print("[SUCCESS] OLLAMA SETUP COMPLETE!")
    print("=" * 60)
    print("🎉 You can now have conversations with Dr. Marina and Dr. Alex!")
    print("\nNext steps:")
    print("1. Run: python chat_with_characters.py")
    print("2. Choose a character to talk to")
    print("3. Start chatting!")
    print("\nTips:")
    print("- Ask about their work and experiences")
    print("- Give them new experiences with 'experience [text]'")
    print("- Check their memories with 'memory'")
    print("- Switch between characters with 'switch'")


if __name__ == "__main__":
    main()