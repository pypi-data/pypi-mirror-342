"sk-3IqRE3pkeXovwZGgAjFNp9nm8xD-VQo10eL1GhfAFiT3BlbkFJIYA9c1qojZd689jp4AnJFCxBXfI-Q2xwDZueFa6rIA"
import src.chatweaver
from rich import print
import pathlib
from src.chatweaver import *
import pathlib
import src.chatweaver as cw
import time

my_api = "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"
here = str(pathlib.Path(__file__).parent / "data.txt")


def save_chats(n, path=str(pathlib.Path(__file__).parent / "data.txt")):
    model = cw.Model(
        model="gpt-4o", api_key=my_api
        )

    bot = cw.Bot(
        rules="You are a helpful assistant.", 
        name="AiBot", 
        cw_model=model
        )

    chat = cw.Chat(
        replies_limit=10, 
        user="Diego", 
        cw_bot=bot
        )
    
    chat.get_response("Hello, how are you?")
    chat.get_response("What is your name?")
    
    chats = {}
    
    for i in range(n):
        chat_copy: cw.Chat = cw.load(repr(chat))
        q = "write a RANDOM title please about anything in the world, u can invent it. DONT WRITE ANYTHING BESIDE THE TITLE."
        if i%2 == 0:
            t = chat_copy.get_response(q)
            chat_copy.chat_title = t
            print(i)
            
        chats[i] = repr(chat_copy)

    with open(path, "w") as f:
        f.write(repr(chats))


def general_test():
    from src.chatweaver import Model, Bot, Chat, CWArchive
    
    # 1. Create a Model
    model = Model(api_key=my_api, model="gpt-4o")

    # 2. Create a Bot with custom rules, tied to the Model
    rules = "You are a friendly and knowledgeable assistant."
    bot = Bot(
        cw_model=model,
        rules=rules,
        name="HelpfulBot"
    )

    # 3. Start a Chat session using the Bot
    chat = Chat(
        cw_bot=bot,
        title="Demo Session",
        replies_limit=3,  # limit to 3 user+assistant replies
        user="Tester"
    )

    # 4. Interact with the Chat
    response1 = chat.get_response("Hello, how are you?")
    print("Bot:", response1)

    response2 = chat.get_response("Can you tell me a joke?")
    print("Bot:", response2)

    # Check Chat details
    print("Current replies used:", chat.chat_replies)
    print("Total tokens so far:", chat.chat_cost)

    # 5. Save the Chat to an Archive
    archive = CWArchive(path="demo_archive.txt", asynchronous=True, delay=0.07)
    archive.add(chat)
    archive.save()

    # 6. Retrieve data from the archive and display
    loaded_data = archive.archive_data
    for item_id, obj in loaded_data.items():
        print(f"Item ID {item_id} -> {obj}")


def test_model() -> None:
    from src.chatweaver import Model

    # Initialize the Model with a valid API key and optionally specify the model name
    model_instance = Model(api_key=my_api, model="gpt-4o")

    # Check basic info
    print(str(model_instance))  
    # Example Output: <Model | model=gpt-4o, api_key=sk-1234567...4564>

    # Update the model name (must be in the allowed set of models)
    model_instance.model_model = "gpt-4o"

    # Update the API key (re-initializes the OpenAI client if validation succeeds)
    model_instance.model_api_key = my_api

    # Retrieve the OpenAI client to make requests manually (if needed)
    client = model_instance.model_client
    
    # Compare with another Model instance
    another_model = Model(api_key=my_api, model="gpt-4o")
    print(model_instance == another_model)  # True, if both model name and API key match


def test_bot() -> None:
    from src.chatweaver import Bot, Model

    # 1. Using an existing Model
    existing_model = Model(api_key=my_api, model="gpt-4o")
    bot = Bot(
        cw_model=existing_model,
        rules="You are a helpful assistant with a witty sense of humor.",
        name="FriendlyBot"
    )

    # 2. Or let Bot create a new Model internally
    another_bot = Bot(
        api_key=my_api,   # Passed to Model's constructor
        rules="You are a formal assistant that provides concise answers.",
        name="ConciseBot"
    )

    # 3. Generating a response to a user prompt
    response_data = bot.response(
        prompt="What is the capital of France?",
        user="Alice",
        image_path=None,
        file_path=None
    )

    # Check response
    print("Bot response:", response_data["content"])
    print("Token usage:", response_data["total_tokens"])


def test_textnode():
    from src.chatweaver import TextNode

    # Create a TextNode representing a user's message
    user_message = TextNode(
        role="user",
        content="What's the weather like today?",
        owner="Alice",
        tokens=8,
        date="2025-01-01 09:15:00"
    )

    # Print the node in a JSON-like string representation
    print(str(user_message))
    # Output:
    # {
    #   'role': 'user', 
    #   'content': "What's the weather like today?", 
    #   'owner': 'Alice', 
    #   'tokens': 8, 
    #   'date': '2025-01-01 09:15:00'
    # }

    # Convert the TextNode to a dictionary for further processing
    node_dict = dict(user_message)
    print(node_dict["content"])  # "What's the weather like today?"


def test_chat() -> None:
    from src.chatweaver import Chat, Bot, TextNode

    # 1. Creating a Chat with a custom Bot
    my_bot = Bot(api_key=my_api, rules="You are a friendly assistant.")
    my_chat = Chat(
        cw_bot=my_bot,
        title="My AI Discussion",
        replies_limit=5,
        user="Alice"
    )

    # 2. Getting a response
    assistant_reply = my_chat.get_response("Hello, can you tell me a joke?")
    print("Assistant says:", assistant_reply)

    # 3. Accessing chat history
    for node in my_chat.chat_history:
        print(node.role, node.content, sep=": ")

    # 4. Viewing total token usage
    print("Total token usage:", my_chat.chat_cost)

    # 5. Changing chat title
    my_chat.chat_title = "Jokes and More"

    # 6. Setting multiple attributes at once
    my_chat.set_all(
        _Chat__replies_limit=None,   # No longer limit the replies
        _Bot__rules="Stay professional in your answers."
    )

    print("Updated chat limit:", my_chat.chat_replies_limit)
    print("Updated bot rules:", my_chat.chat_Bot.bot_rules)


def test_archive() -> None:
    with CWArchive(path="my_archive.txt") as archive:
        # 1. Create an archive (asynchronous by default) with a specific file path
        #archive = CWArchive(path="my_archive.txt")
        
        # 2. Add a new Chat object to the archive
        my_chat = Chat(api_key=my_api, title="Session 4")
        archive + my_chat

        # 3. Save the archive to disk
        # archive.save()

        # 4. Retrieve data from the archive (asynchronously, in chunks by default)
        loaded_data = archive.archive_data # It is better using the archive_data attribute instead of the retrieve method
        for item_id, item_obj in loaded_data.items():
            print(item_id, item_obj)

        # 5. Remove the chat by its ID (e.g., 0)
        archive.remove(0)
        archive.save()  # Reflect changes on disk

        # 6. Disable asynchronous loading if you run into concurrency issues
        archive.archive_asynchronous = False


if __name__ == "__main__":
    #general_test()
    #test_model()
    #test_bot()
    #test_textnode()
    #test_chat()
    #test_archive()
    
    # Save 100 chats to a file
    #save_chats(100, str(pathlib.Path(__file__).parent / "100.txt"))
    #save_chats(80, str(pathlib.Path(__file__).parent / "80.txt"))
    #save_chats(50, str(pathlib.Path(__file__).parent / "50.txt"))
    #save_chats(20, str(pathlib.Path(__file__).parent / "20.txt"))
    #save_chats(10, str(pathlib.Path(__file__).parent / "10.txt"))
    #save_chats(5, str(pathlib.Path(__file__).parent / "5.txt"))
    
    #save_chats(500, str(pathlib.Path(__file__).parent / "500.txt"))
    #save_chats(1000, str(pathlib.Path(__file__).parent / "1000.txt"))
    
    files = ["5.txt", "10.txt", "20.txt", "50.txt", "80.txt", "100.txt"]
    for file in files:
        start = time.perf_counter()
        archive = CWArchive(path=str(pathlib.Path(__file__).parent / file), asynchronous=True, delay=0.07)
        end = time.perf_counter()
        print(f"LOAD {file}: \t{end - start:.4f} s \t\tlen:{len(archive)}")





















































# LOAD 100 CHATS
# nothing: 239.9952 s
# with api cache: 83.0718 s
# async: 48.7602 s 
# defaults: 39.4698 s