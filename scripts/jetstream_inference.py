
import json
from pathlib import Path

from openai import OpenAI, APIConnectionError, APIStatusError, APITimeoutError


def main():
    # Read credentials from outside the GitHub repository.
    config_path = (
        Path.home() / ".config" / "cloudmesh-ai" / "jetstream.json"
    )

    with config_path.open(encoding="utf-8") as file:
        config = json.load(file)

    # Validate the required settings.
    for key in ("base_url", "api_key", "model"):
        if not config.get(key):
            raise ValueError(f"Missing configuration setting: {key}")

    client = OpenAI(
        base_url=config["base_url"],
        api_key=config["api_key"],
        timeout=45.0,
        max_retries=0,
    )

    print("Cloudmesh Jetstream LLM — Python Inference Test")
    print("Model:", config["model"])
    print("Sending test inference request...")

    response = client.chat.completions.create(
        model=config["model"],
        messages=[
            {
                "role": "user",
                "content": (
                    "Explain in two sentences why smoke testing "
                    "is important in multi-cloud DevOps."
                ),
            }
        ],
        max_tokens=2048,
    )
    choice = response.choices[0]

    print("\nFinish reason:", choice.finish_reason)

    if response.usage:
        print("Generated tokens:", response.usage.completion_tokens)

    print("\nLLM Response:")

    answer = choice.message.content

    if answer and answer.strip():
        print(answer)
        print("\nInference request completed successfully.")
    else:
        print("(No final text returned — further diagnosis needed.)")
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        print("ERROR: Private Jetstream configuration file not found.")
        raise SystemExit(1)
    except APIStatusError as error:
        print(f"ERROR: Jetstream API returned HTTP {error.status_code}.")
        raise SystemExit(1)
    except (APIConnectionError, APITimeoutError):
        print("ERROR: Could not connect to the Jetstream API.")
        raise SystemExit(1)
    except (ValueError, json.JSONDecodeError) as error:
        print(f"Configuration error: {error}")
        raise SystemExit(1)