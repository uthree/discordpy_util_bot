import os
import yaml

default_token_file = {
    'using': 'main',
    'main': '<YOUR BOT TOKEN HERE>'
}
if __name__ == "__main__":
    if not os.path.exists("token.yml"):
        with open("token.yml", "w") as file:
            yaml.dump(default_token_file, file)
