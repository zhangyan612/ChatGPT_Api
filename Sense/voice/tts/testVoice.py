# Import asyncio
import asyncio
import edgeTTSVoice


if __name__ == "__main__":
    # Create an event loop
    loop = asyncio.get_event_loop_policy().get_event_loop()

    try:
        # Run the generate_voice function
        loop.run_until_complete(edgeTTSVoice.generate_voice("This is test voice generating from another file"))
    finally:
        # Close the loop
        loop.close()
