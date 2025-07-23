#!/usr/bin/env -S uv run
# /// script
# dependencies = ["requests"]
# ///

import requests
import subprocess
import traceback
import sys

def main():
    """
    Demonstrate self-healing behavior by attempting a failing HTTP request
    and calling Claude CLI for help when it fails.
    """
    print("Self-healing script demo starting...")
    print("Attempting to make HTTP request to non-existent URL...")
    
    try:
        # This URL doesn't exist and will cause an exception
        url = "https://this-url-definitely-does-not-exist-12345.com"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        print(f"Success! Response: {response.status_code}")
        
    except Exception as e:
        print(f"\nError occurred: {type(e).__name__}")
        print("Calling Claude for help...\n")
        
        # Get full traceback information
        error_info = traceback.format_exc()
        
        # Prepare prompt for Claude
        prompt = f"""pls halp - Python script failed with exception:

Script was trying to make an HTTP request to: {url}

Exception details:
{error_info}

What went wrong and how can I fix this?"""
        
        # Call Claude CLI for analysis
        try:
            result = subprocess.run([
                "claude", 
                "-p", prompt,
                "--dangerously-skip-permissions"
            ], capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                print("Claude's response:")
                print("-" * 50)
                print(result.stdout)
                print("-" * 50)
            else:
                print(f"Failed to get help from Claude: {result.stderr}")
                
        except FileNotFoundError:
            print("Claude CLI not found. Please ensure 'claude' is installed and in PATH.")
        except Exception as claude_error:
            print(f"Error calling Claude: {claude_error}")
        
        # Exit with error code to indicate failure
        sys.exit(1)

if __name__ == "__main__":
    main()