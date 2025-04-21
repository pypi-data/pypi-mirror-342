import openai
import os
import base64
import time
from dataclasses import dataclass
from typing import Any
import asyncio


# relative imports
from .data import *


cache_api_key = set()
cache_model_name = set()


@dataclass(frozen=True)
class TextNode:
    """
    # TextNode
    
    ## Description
    Represents an immutable text node with metadata attributes. A TextNode object represents a single message in a conversation.

    ## Attributes 
    ```
    role: str      # The role of the TextNode ('assistant' or 'user').
    content: str   # The content of the TextNode.
    owner: str     # The owner name of the TextNode.
    tokens: int    # The number of tokens associated with the TextNode.
    date: str      # The creation date of the TextNode.
    ```

    ## Methods
    ```
    __str__() -> str   # Returns the string representation of the object in JSON-like format.
    __iter__() -> dict # Returns an iterator for the object's attributes as key-value pairs. Useful for unpacking the object with the dict() constructor.
    ```
    """
    
    role: str
    content: str
    owner: str
    tokens: int
    date: str
    
    def __str__(self) -> str:
        return str({"role":self.role, 
                    "content":self.content, 
                    "owner":self.owner, 
                    "tokens":self.tokens, 
                    "date":self.date})
        
    def __iter__(self) -> dict:
        return iter(eval(self.__str__()).items())
    
    

class Model(object):
    """
        # Model
        
        ## Description
        A convenient wrapper class for managing AI models and their API keys. This class provides methods
        for defining, validating, and working with OpenAI-based API clients, ensuring that both the model
        name and the API key are correctly set and tested before use.
    """

    def __init__(self, 
        api_key: str, 
        model: str = "gpt-4o"
    ) -> None:
        """
        # Model
        
        ## Description
        A convenient wrapper class for managing AI models and their API keys. This class provides methods
        for defining, validating, and working with OpenAI-based API clients, ensuring that both the model
        name and the API key are correctly set and tested before use.

        ## Attributes
        ```python
        model_api_key: str            # Public attribute for retrieving or setting the API key.
        model_model: str              # Public attribute for retrieving or setting the model name.
        __default_attributes: dict    # Internal dictionary storing default attribute values (e.g., default model name).
        __model: str                  # Private attribute holding the model name after validation.
        __api_key: str                # Private attribute holding the validated API key.
        __client: openai.OpenAI       # Private attribute storing the initialized OpenAI client.
        ```

        ## Methods
        ```python
        __str__() -> str
            # Returns a human-readable string showing the model name and partially hidden API key.

        __repr__() -> str
            # Returns a formal string representation of the Model instance.

        __eq__(other: Model) -> bool
            # Checks for equality by comparing both the model name and the API key.

        model_model -> str
            # Getter property for retrieving the current model name.

        model_api_key -> str
            # Getter property for retrieving the current API key.

        model_client -> openai.OpenAI
            # Getter property for retrieving the associated OpenAI client.

        model_model.setter(new_model: str) -> None
            # Setter property that validates and assigns a new model name, updating a global cache if necessary.

        model_api_key.setter(new_api_key: str) -> None
            # Setter property that validates the API key, tests connectivity, and updates the global cache before initializing a new OpenAI client.

        model_client.setter(api_key: str) -> None
            # Setter property that explicitly sets the OpenAI client, ensuring the API key matches the stored one.
        ```
        
        ---
        
        # __init__

        ## Description
        Initialize the Model instance with a given API key and an optional model name.
        The model name defaults to "gpt-4o" if not provided.

        ## Parameters
        ```
        api_key: str  
            # The API key for authenticating requests. Must start with 'sk-' and be at least 20 characters long.
        model: str = "gpt-4o"  
            # The name of the model to be used (defaults to "gpt-4o").
        ```

        ## Raises
        ```
        Exception
            # Raised if the provided model name is invalid or if the API key fails validation.
        ```
        """


        self.model_api_key: str = str(api_key)
        
        self.model_model: str = str(model)
        
        self.__default_attributes: dict[str, Any] = {
            "model": "gpt-4o"
        }
        
    
    # -------- MAGIC METHODS --------
    def __str__(self) -> str:
        """
            # __str__

            ## Description
            Return a human-readable string representation of the Model instance,
            displaying the current model name and API key.
        """

        return f"<Model | model={self.__model}, api_key={self.__api_key[:8]}...{self.__api_key[-8:]}>"
    
    def __repr__(self) -> str:
        """
            # __repr__

            ## Description
            Return a formal string representation of the Model instance, suitable for
            logging and debugging. This output includes the model name (if different
            from the default) and the API key.
        """

        is_model: bool = self.model_model == self.__default_attributes["model"]
        
        str_model: str = f"model={repr(self.model_model)}," if not is_model else ""
        
        return f"Model({str_model} api_key={repr(self.__api_key)})"
    
    def __eq__(self, other) -> bool:
        """
            # __eq__

            ## Description
            Compare this Model instance with another Model instance for equality.
            Two Model instances are considered equal if they share the same model name
            and the same API key.

            ## Parameters
            ```
            other: Model
                # The object to compare with the current Model instance.
            ```
        """

        if not isinstance(other, type(self)):
            return False

        is_model: bool = self.model_model == other.model_model
        is_api_key: bool = self.model_api_key == other.model_api_key
        
        return is_model and is_api_key
    
    
    # -------- GET --------
    @property
    def model_model(self) -> str:
        """
            # model_model (getter)

            ## Description
            Retrieve the name of the AI model currently in use.
        """

        return self.__model
    
    @property
    def model_api_key(self) -> str:
        """
            # model_api_key (getter)

            ## Description
            Retrieve the current API key used by the Model instance.
        """

        return self.__api_key
    
    @property
    def model_client(self) -> openai.OpenAI:
        """
            # model_client (getter)

            ## Description
            Retrieve the OpenAI client instance associated with this Model.
            The client is automatically created whenever the API key is set or updated.
        """

        return self.__client
    
    
    # -------- SET --------
    @model_model.setter
    def model_model(self, new_model: str) -> None:
        """
            # model_model (setter)

            ## Description
            Set the model name for the AI. This method checks if the new model name is already
            cached, and if not, it verifies the name against an allowed list of model names. 
            If valid, it stores the new model name and updates a global cache.

            ## Parameters
            ```
            new_model: str
                # The new model name to set.
            ```

            ## Raises
            ```
            Exception
                # Raised if 'new_model' is not among the acceptable model names.
            ```
        """

        global cache_model_name
        new_model: str = str(new_model)
        if new_model not in cache_model_name:
            if new_model not in chat_weaver_models:
                raise Exception(f"'{new_model}' is not acceptable.")
            self.__model: str = new_model
            cache_model_name.add(self.__model)
        else:
            self.__model: str = new_model
    
    @model_api_key.setter
    def model_api_key(self, new_api_key: str) -> None:
        """
            # model_api_key (setter)

            ## Description
            Set the API key for the Model instance. This method verifies the API key format,
            checks if it is already cached, and if not, it performs a test request to ensure
            the key is valid. Upon success, it initializes a new OpenAI client.

            ## Parameters
            ```
            new_api_key: str
                # The new API key to set (must start with 'sk-' and be at least 20 characters).
            ```

            ## Raises
            ```
            ValueError
                # Raised if the API key format is invalid.
            Exception
                # Raised if there is an issue with the test request or any other validation failure.
            ```
        """

        global cache_api_key
        new_api_key: str = str(new_api_key)
        
        if new_api_key not in cache_api_key:
            try:
                if not new_api_key.startswith("sk-") or len(new_api_key) < 20:
                    raise ValueError("Invalid API key format.")
                
                openai.OpenAI(api_key=new_api_key).chat.completions.list()
            except Exception as e:
                self.__is_api_key_modified = True
                raise Exception(f"Invalid API key: {e}")
            
            cache_api_key.add(new_api_key)
            self.__api_key = new_api_key
            self.model_client = new_api_key
        else:
            self.__api_key = new_api_key
            self.model_client = new_api_key
            
    @model_client.setter
    def model_client(self, api_key) -> None:
        """
            # model_client (setter)

            ## Description
            Explicitly set the OpenAI client by providing an API key. If the key matches
            the Model instance's current API key, a new OpenAI client is created. Otherwise,
            an exception is raised because the correct way to change the API key is via
            the 'model_api_key' property.

            ## Parameters
            ```
            api_key: str
                # The API key used to initialize the new OpenAI client. Must match the current stored API key.
            ```

            ## Raises
            ```
            Exception
                # Raised if the provided 'api_key' does not match the stored Model API key.
            ```
        """

        if self.model_api_key == api_key:
            self.__client = openai.OpenAI(api_key=api_key)
        else:
            raise Exception(f"<If you're trying to change the api_key, please do it from the model_api_key proprety>")




class Bot(Model):
    """
    # Bot
    
    ## Description
    Represents a conversational AI bot based on a specific model. This class allows customization of rules, bot name, and associated model behavior. It supports managing user prompts, handling responses, and integrating optional images or files.
    """
    
    def __init__(
        self, 
        *args, 
        rules: str | None = chat_weaver_rules["default"], 
        name: str = "AI Bot", 
        cw_model: Model | None = None, 
        **kwargs
    ) -> None:
        """
            # Bot
            
            ## Description
            Represents a conversational AI bot based on a specific model. This class allows customization of rules, 
            bot name, and associated model behavior. It supports managing user prompts, handling responses, and 
            integrating optional images or files.

            ## Attributes 
            ```python
            bot_rules: str         # The rules that define the bot's behavior and responses.
            bot_name: str          # The name of the bot (default is "AI Bot").
            bot_time_format: str   # The format used for time-related operations (default is "%d/%m/%Y %H:%M:%S").
            __rules: str           # Internal representation of the bot's rules.
            __name: str            # Internal representation of the bot's name.
            __time_format: str     # Internal format string for time-based functionalities.
            __model: Model         # The model instance associated with this bot.
            ```

            ## Methods
            ```python
            __init__(*args, rules, name, cw_model, **kwargs) -> None
                # Initializes the bot's attributes (rules, name, time format) and sets or creates the underlying Model.

            __str__() -> str
                # Returns a user-friendly string representation of the bot.

            __repr__() -> str
                # Returns a formal string representation of the bot, including its name, rules, and underlying Model info.

            __eq__(other: Bot) -> bool
                # Checks for equality by comparing the rules, name, and model of both Bot instances.

            bot_Model -> Model
                # Getter property that returns the underlying Model instance by calling super().

            bot_rules -> str
                # Getter property returning the bot's rules with the current bot name appended.

            bot_name -> str
                # Getter property returning the bot's name.

            bot_time_format -> str
                # Getter property returning the bot's internal time format.

            bot_rules.setter(new_rules: str | None) -> None
                # Setter property to update the bot's rules, falling back to a default if None is provided.

            bot_name.setter(new_name: str) -> None
                # Setter property to update the bot's name.

            bot_time_format.setter(new_time_format: str) -> None
                # Setter property to update the bot's time format, raising a ValueError if invalid.

            response(prompt, user, history, image_path, file_path) -> dict[str, Any]
                # Generates a response to a user's prompt, optionally including conversation history, images, or files.
            ```
            
            ---
            
            # __init__

            ## Description
            Initialize the Bot instance. This constructor sets default values for the bot's time format, name, 
            and rules. It also manages an optional Model instance (cw_model). If no cw_model is provided, 
            the constructor relies on the parent Model class to initialize the model.

            ## Parameters
            ```python
            *args: Any
                # Additional arguments passed to the superclass (Model) if no cw_model is provided.
            rules: str | None
                # The rules that define the bot's behavior; defaults to a standard rule set if None.
            name: str
                # The name of the bot; defaults to "AI Bot".
            cw_model: Model | None
                # An existing Model instance. If None, a new Model is created using *args and **kwargs.
            **kwargs: Any
                # Additional keyword arguments passed to the superclass (Model) if no cw_model is provided.
            ```

            ## Raises
            ```python
            TypeError
                # Raised if 'cw_model' is provided but is not an instance of Model.
            ```
        """

        # time format
        self.bot_time_format = "%d/%m/%Y %H:%M:%S" 
        
        # name
        self.bot_name = str(name)
        
        # rules
        self.bot_rules = rules
        
        # define super() [Model]
        if not isinstance(cw_model, Model) and cw_model != None:
            raise TypeError(f"<Invalid 'cw_model' type: Expected 'Model' instance, got {type(cw_model)}>")
        if cw_model == None:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(model=cw_model.model_model, api_key=cw_model.model_api_key)
        
        # default attributes
        self.__default_attributes = {
            "name": "AI Bot", 
            "rules": chat_weaver_rules["default"]
        }
        
    
    # -------- MAGIC METHODS --------
    def __str__(self) -> str:
        """
            # __str__

            ## Description
            Return a user-friendly string representation of the bot. By default, this includes the bot's name.
        """

        return f"<Bot | {self.__name}>"
    
    def __repr__(self) -> str:
        """
            # __repr__

            ## Description
            Return a formal string representation of the bot, useful for debugging or logging. This includes
            the bot name, any custom rules (if different from the default), and the representation of the 
            associated Model instance.
        """

        is_name: bool = self.bot_name == self.__default_attributes["name"]
        is_rules: bool = self.bot_rules == self.__default_attributes["rules"]
        
        str_name: str = f"name={repr(self.bot_name)}," if not is_name else ""
        str_rules: str = f"rules={repr(self.bot_rules)}," if not is_rules else ""
        
        return f"Bot({str_name} {str_rules} cw_model={super().__repr__()})"
    
    def __eq__(self, other) -> bool:
        """
            # __eq__

            ## Description
            Compare this Bot instance to another Bot instance for equality. Two Bot instances are considered
            equal if they share the same rules, name, and underlying Model.

            ## Parameters
            ```python
            other: Bot
                # The Bot instance to compare with the current instance.
            ```

            ## Returns
            ```python
            bool
                # True if both Bot instances match in rules, name, and model; False otherwise.
            ```
        """

        if not isinstance(other, Bot):
            return False
        
        is_rules = self.bot_rules == other.bot_rules
        is_name = self.bot_name == other.bot_name
        
        is_model = eval(self.bot_Model.__repr__()) == eval(other.bot_Model.__repr__())
        
        return is_rules and is_name and is_model
    
    
    # -------- GET --------
    @property
    def bot_Model(self) -> Model:
        """
            # bot_Model (getter)

            ## Description
            Retrieve the underlying Model instance for this Bot by invoking the superclass directly.
            This method allows for model-based operations without exposing the internals of the Bot class.
        """

        return super()
    
    @property
    def bot_rules(self) -> str:
        """
            # bot_rules (getter)

            ## Description
            Retrieve the current rules used by the bot. The returned string automatically includes
            the bot's name for context in conversations.
        """

        return self.__rules + f" Your name is {self.bot_name}"
    
    @property
    def bot_name(self) -> str:
        """
            # bot_name (getter)

            ## Description
            Retrieve the current name of the bot.
        """

        return self.__name
    
    @property
    def bot_time_format(self) -> str:
        """
            # bot_time_format (getter)

            ## Description
            Retrieve the format string used by the bot for time-based operations.
        """

        return self.__time_format
    
    
    # -------- SET --------
    @bot_rules.setter
    def bot_rules(self, new_rules: str | None) -> None:
        """
            # bot_rules (setter)

            ## Description
            Update the bot's rules. If no rules are provided (None), the bot defaults to a predefined
            ruleset. Otherwise, the new rules are stored internally.

            ## Parameters
            ```python
            new_rules: str | None
                # The new rules to be applied. Defaults to a standard rule set if None.
            ```
        """

        self.__input_rules: str | None = str(new_rules) if new_rules != None else chat_weaver_rules["default"]
        self.__rules: str = self.__input_rules
    
    @bot_name.setter
    def bot_name(self, new_name: str) -> None:
        """
            # bot_name (setter)

            ## Description
            Assign a new name to the bot. This name is also used within the bot's rules to personalize responses.

            ## Parameters
            ```python
            new_name: str
                # The new name to assign to the bot.
            ```
        """

        self.__name: str = str(new_name)
    
    @bot_time_format.setter
    def bot_time_format(self, new_time_format: str) -> None:
        """
            # bot_time_format (setter)

            ## Description
            Set a new time format for the bot. This format is validated by attempting to format the current time.
            If the format is invalid, a ValueError is raised.

            ## Parameters
            ```python
            new_time_format: str
                # A valid Python time format string (e.g., "%Y-%m-%d %H:%M:%S").
            ```

            ## Raises
            ```python
            ValueError
                # Raised if 'new_time_format' is not a valid time format.
            ```
        """

        try:
            time.strftime(new_time_format, time.localtime(time.time()))
            self.__time_format = new_time_format
        except:
            raise ValueError(f"<Invalid 'new_time_format' format: Expected valid time format>")
    
    
    # -------- ACTIONS --------
    def response(self, prompt: str, 
                 user: str = "User", 
                 history: list | None = None, 
                 image_path: str | None = None, 
                 file_path: str | None = None) -> dict[str, Any]:
        """
            # response

            ## Description
            Generate a response to a user's prompt, potentially including conversation history, images, or files. 
            This method constructs the conversation messages, optionally uploads a file to OpenAI for reference, 
            and returns both the content of the response and usage metrics (token counts, timings, etc.).

            ## Parameters
            ```python
            prompt: str
                # The user's query or statement to which the bot should respond.
            user: str = "User"
                # The name used to identify the user in the conversation context.
            history: list | None
                # A list of previous conversation messages, if any, to maintain context.
            image_path: str | None
                # The file path to an image that should be encoded and attached to the user's message.
            file_path: str | None
                # The file path to any additional file to be uploaded and referenced by the model.
            ```

            ## Returns
            ```python
            dict[str, Any]
                # A dictionary containing:
                #  - "content": The response text generated by the model.
                #  - "prompt_tokens", "completion_tokens", "total_tokens": Token usage statistics.
                #  - "start_date": The timestamp when the user's prompt was processed.
                #  - "delta_time": The elapsed time to obtain the response.
                #  - "final_date": The timestamp when the response was completed.
            ```
        """
        
        self.__start_date = time.strftime(self.bot_time_format, time.localtime(time.time())) # user prompt date
        
        self.__prompt = prompt
        
        messages = [
            {"role": "developer", "content": self.__rules + f"User name is: {user}"}, 
            {"role": "user", "content": [{"type": "text", "text": self.__prompt}]}
        ]
        
        if image_path != None:
            with open(image_path, "rb") as f:
                base64_image = base64.b64encode(f.read()).decode("utf-8")
            image = f"data:image/png;base64,{base64_image}"
            
            image_message ={
                "type": "image_url",
                "image_url": {"url": image}
                }
            
            messages[1]["content"].append(image_message)
            
        if file_path != None:
            file = self.model_client.files.create(
                file=open(file_path, "rb"), 
                purpose="user_data"
            )
            
            file_message = {
                "type": "file", 
                "file": {"file_id": file.id}
            }
            
            messages[1]["content"].append(file_message)
        
        messages = [dict(message) for message in history] + messages if history != None else messages
        
        start = time.perf_counter()
        response = self.model_client.chat.completions.create(
            model=self.model_model,
            messages=messages
        )
        end = time.perf_counter()
        self.__final_date = time.strftime(self.bot_time_format, time.localtime(time.time())) # assistant resposne date
        
        response.usage.completion_tokens
        response.usage.prompt_tokens
        response.usage.total_tokens
        
        content = response.choices[0].message.content if response.choices[0].message.content != None else response.choices[0].message.refusal
        
        return {"content": content, 
                "prompt_tokens": response.usage.prompt_tokens, 
                "completion_tokens": response.usage.completion_tokens, 
                "total_tokens": response.usage.total_tokens,
                "start_date": self.__start_date,
                "delta_time": end-start, 
                "final_date": self.__final_date}



class Chat(Bot):
    """
        # Chat

        ## Description
        Represents a chat session built upon the Bot class. This class manages conversation history, 
        response generation, and chat metadata such as reply limits, creation date, and cost calculation. 
        It maintains a log of messages, integrates model responses, and allows for attachments like 
        images or files in the prompts.
    """
    
    def __init__(self, 
                 *args, 
                 title: str = "New Chat", 
                 replies_limit: int | None = 10, 
                 user: str = "User", 
                 cw_bot: Bot | None = None,
                 **kwargs) -> None:
        """
            # Chat

            ## Description
            Represents a chat session built upon the Bot class. This class manages conversation history, 
            response generation, and chat metadata such as reply limits, creation date, and cost calculation. 
            It maintains a log of messages, integrates model responses, and allows for attachments like 
            images or files in the prompts.

            ## Attributes
            ```python
            chat_time_format: str              # The time format used for chat timestamps (default: "%d/%m/%Y %H:%M:%S").
            chat_replies_limit: int            # The maximum number of replies allowed in the chat (or infinity if None).
            chat_history: list[TextNode]       # The conversation history as a list of TextNode objects.
            chat_user: str                     # The user participating in the chat session.
            chat_creation_date: str            # The timestamp when the chat was created.
            chat_replies: int                  # The current number of replies in the chat (computed from history).
            chat_cost: int                     # The total cost calculated based on the tokens used in all messages.
            chat_title: str                    # The title of the chat session.
            ```

            ## Methods
            ```python
            __init__(*args, title: str = "New Chat", replies_limit: int | None = 10, user: str = "User", cw_bot: Bot | None = None, **kwargs) -> None
                # Initializes the chat session with a title, time format, creation date, reply limit, user, 
                # and optionally an existing Bot or a new Bot.

            __str__() -> str
                # Returns a user-friendly string representation of the chat, including the title, reply limit, 
                # current reply count, and creation date.

            __repr__() -> str
                # Returns a formal string representation of the chat with details about its attributes 
                # and the associated Bot state.

            __lt__(other: Chat) -> bool
                # Compares two Chat instances based on their creation dates for chronological ordering.

            __eq__(other: Chat) -> bool
                # Determines if two Chat instances are equal by comparing their relevant attributes 
                # (reply limit, user, title, creation date, replies, history, and underlying Bot).

            chat_Bot -> Bot
                # Property to get the underlying Bot instance, granting direct access to its attributes and methods.

            chat_time_format -> str
                # Property to get the current time format used for timestamps.

            chat_replies_limit -> int
                # Property to get the maximum number of allowed replies (or infinity if None was provided).

            chat_history -> list[TextNode]
                # Property to get the conversation history, stored as a list of TextNode objects.

            chat_user -> str
                # Property to get the name of the user participating in the chat.

            chat_creation_date -> str
                # Property to get the creation date of the chat session, formatted according to 'chat_time_format'.

            chat_replies -> int
                # Property to get the number of replies (counted as user+assistant message pairs).

            chat_cost -> int
                # Property to get the total cost (sum of token usage across all messages in 'chat_history').

            chat_title -> str
                # Property to get the title of the chat session.

            set_all(return_self: bool = True, **kwargs: Any) -> None
                # Updates multiple Chat, Bot, and Model attributes at once using keyword arguments. 
                # Returns the Chat instance by default for chaining.

            chat_replies_limit.setter(new_replies_limit: int | None) -> None
                # Sets a new reply limit, treating None as infinity.

            chat_history.setter(new_history: list[TextNode] | list[dict[str, str]] | None) -> None
                # Sets the conversation history, supporting both TextNode objects and dictionaries convertible to TextNode.

            chat_time_format.setter(new_time_format: str) -> None
                # Sets a new time format and validates it.

            chat_creation_date.setter(new_creation_date: str) -> None
                # Sets a new creation date, ensuring it matches the current time format.

            chat_user.setter(new_user: str) -> None
                # Updates the user participating in the chat.

            chat_title.setter(new_title: str) -> None
                # Updates the title of the chat session.

            get_response(prompt: str, user: str | None = None, image_path: str | None = None, file_path: str | None = None) -> str
                # Generates a response based on the given prompt (and optional attachments). 
                # The assistant's reply is stored in the chat history.

            __update_history(prompt: str, response: dict[str, Any], owner_user: str | None) -> None
                # Internal method to append user and assistant messages to the chat history, respecting the reply limit.
            ```
            
            ---
            
            # __init__

            ## Description
            Initialize a new Chat session, setting attributes such as title, time format, creation date, 
            user, and reply limits. If an existing Bot instance is not provided, a new Bot instance is 
            created using the arguments passed to the constructor.

            ## Parameters
            ```python
            *args: Any
                # Positional arguments forwarded to the Bot (or Model) constructor if cw_bot is not provided.
            title: str
                # The title of the chat session (default: "New Chat").
            replies_limit: int | None
                # The maximum number of replies allowed (default: 10). If None, no limit is imposed.
            user: str
                # The user participating in the chat (default: "User").
            cw_bot: Bot | None
                # An existing Bot instance. If None, a new Bot is created with *args and **kwargs.
            **kwargs: Any
                # Additional keyword arguments passed to the Bot (or Model) constructor if cw_bot is not provided.
            ```

            ## Raises
            ```python
            TypeError
                # Raised if 'cw_bot' is provided but is not an instance of Bot.
            ```
        """
        
        # title
        self.chat_title = str(title)
        # time format
        self.chat_time_format: str = "%d/%m/%Y %H:%M:%S"
        # creation_date
        self.chat_creation_date: str = time.strftime(self.chat_time_format, time.localtime(time.time()))
        # replies_limit
        self.chat_replies_limit: int = replies_limit
        # replies
        self.__replies: int = 0
        # history
        self.chat_history: list[TextNode] = []
        # user
        self.chat_user: str = str(user)
        
        # bot
        if not isinstance(cw_bot, Bot) and cw_bot != None:
            raise TypeError(f"<Invalid 'cw_bot' type: Expected 'Bot' instance, got {type(cw_bot)}>")
        if cw_bot == None:
            super().__init__(*args, **kwargs)
            self.__bot: Bot = Bot(*args, **kwargs)
        else:
            self.__bot: Bot = cw_bot
            super().__init__(rules=self.__bot.bot_rules, name=self.__bot.bot_name, model=self.__bot.model_model, api_key=self.__bot.model_api_key)
        
        # default attributes
        self.__default_attributes = {
            "replies_limit": 10, 
            "user": "User", 
            "title": "New Chat"
        }
    
    
    # -------- MAGIC METHODS --------
    def __str__(self):
        """
            # __str__

            ## Description
            Return a user-friendly string representation of the chat session. 
            This typically includes the chat title, the maximum number of replies, 
            the current number of replies, and the creation date.
        """

        return f"<Chat | title={repr(self.chat_title)}, replies_limit={self.chat_replies_limit}, replies={self.chat_replies}, creation_date={repr(self.chat_creation_date)}>"
    def __repr__(self):
        """
            # __repr__

            ## Description
            Return a formal string representation of the chat, including key attributes such as 
            reply limit, user, title, and the associated Bot (by calling the superclass's __repr__). 
            This representation can be used for debugging or logging purposes.
        """

        is_replies_limit: bool = self.chat_replies_limit == self.__default_attributes["replies_limit"]
        is_user: bool = self.chat_user == self.__default_attributes["user"]
        is_title: bool = self.chat_title == self.__default_attributes["title"]
        
        str_replies_limit: str = f"replies_limit={repr(self.chat_replies_limit)}," if not is_replies_limit else ""
        str_user: str = f"user={repr(self.chat_user)}," if not is_user else ""
        str_title: str = f"title={repr(self.chat_title)}," if not is_title else ""
        
        return f"Chat({str_replies_limit} {str_user} {str_title} cw_bot={super().__repr__()}).set_all(_Chat__history={self.chat_history}, _Chat__creation_date={repr(self.chat_creation_date)})"
    def __lt__(self, other) -> bool:
        """
            # __lt__

            ## Description
            Compare this Chat instance to another Chat instance based on their creation dates. 
            This method allows sorting Chat objects chronologically.

            ## Parameters
            ```python
            other: Chat
                # The Chat instance to compare against the current one.
            ```

            ## Returns
            ```python
            bool
                # True if this Chat's creation date is earlier than the other Chat's creation date, False otherwise.
            ```
        """

        # Convert the string to a time object and compare
        self_time = time.strptime(self.chat_creation_date, self.chat_time_format)
        other_time = time.strptime(other.chat_creation_date, self.chat_time_format)
        return self_time < other_time
    def __eq__(self, other) -> bool:
        """
            # __eq__

            ## Description
            Compare this Chat instance to another Chat instance for equality. Two chats are considered 
            equal if they have the same reply limit, user, title, creation date, number of replies, 
            conversation history, and underlying Bot.

            ## Parameters
            ```python
            other: Chat
                # The Chat instance to compare against the current one.
            ```

            ## Returns
            ```python
            bool
                # True if all chat attributes match; False otherwise.
            ```
        """

        is_replies_limit = self.chat_replies_limit == other.chat_replies_limit
        is_user = self.chat_user == other.chat_user
        is_title = self.chat_title == other.chat_title
        
        is_creation_date = self.chat_creation_date == other.chat_creation_date
        is_replies = self.chat_replies == other.chat_replies
        is_history = self.chat_history == other.chat_history
        
        is_bot = eval(self.chat_Bot.__repr__()) == eval(other.chat_Bot.__repr__())
        
        return is_replies_limit and is_user and is_title and is_creation_date and is_replies and is_history and is_bot
    
    
    # -------- GET --------
    @property
    def chat_Bot(self) -> Bot:
        """
            # chat_Bot (getter)

            ## Description
            Retrieve the Bot instance associated with this Chat by invoking the superclass. 
            This allows direct access to the underlying bot's attributes and methods.
        """

        return super()
    
    @property
    def chat_time_format(self) -> str:
        """
            # chat_time_format (getter)

            ## Description
            Retrieve the current time format used by this Chat for timestamps, such as creation date 
            and message logs.
        """

        return self.__time_format
    
    @property
    def chat_replies_limit(self) -> int:
        """
            # chat_replies_limit (getter)

            ## Description
            Retrieve the maximum number of replies allowed in this chat. If no limit is set 
            (i.e., None was provided), the value is represented internally as infinity.
        """

        return self.__replies_limit
    
    @property
    def chat_history(self) -> list[TextNode]:
        """
            # chat_history (getter)

            ## Description
            Retrieve the chat's conversation history, stored as a list of TextNode objects.
            Each TextNode contains information such as the role (user or assistant), content, owner, 
            token count, and timestamp.
        """

        return self.__history
    
    @property
    def chat_user(self) -> str:
        """
            # chat_user (getter)

            ## Description
            Retrieve the name of the user participating in the chat session.
        """

        return self.__user
    
    @property
    def chat_creation_date(self) -> str:
        """
            # chat_creation_date (getter)

            ## Description
            Retrieve the creation date of the chat session, formatted according to `chat_time_format`.
        """

        return self.__creation_date
    
    @property
    def chat_replies(self) -> int:
        """
            # chat_replies (getter)

            ## Description
            Retrieve the number of replies in the conversation. This value is computed as 
            half the length of the chat history, since each user message and bot response 
            together count as one "reply."
        """

        self.__replies = len(self.__history) // 2
        return self.__replies
    
    @property
    def chat_cost(self) -> int:
        """
            # chat_cost (getter)

            ## Description
            Retrieve the total cost of the chat. This value is calculated by summing the token 
            counts of all TextNode entries in the chat's history.
        """

        return sum([node.tokens for node in self.chat_history])
    
    @property
    def chat_title(self) -> str:
        """
            # chat_title (getter)

            ## Description
            Retrieve the chat session's title.
        """

        return self.__title
    
    # -------- SET --------
    def set_all(self, return_self: bool = True, **kwargs: Any) -> None:
        """
            # set_all

            ## Description
            Update multiple attributes of the Chat (and its underlying Bot and Model) based on 
            the provided keyword arguments. This function iterates through all attributes 
            and updates them accordingly. By default, it returns `self` for easy method chaining.

            ## Parameters
            ```python
            return_self: bool = True
                # If True, returns the Chat instance itself after updates; otherwise, returns None.
            **kwargs: Any
                # Keyword arguments where each key corresponds to a private attribute path
                # (e.g., "_Chat__user", "_Bot__rules", or "_Model__api_key") and each value is the new value to set.
            ```

            ## Returns
            ```python
            Chat | None
                # Returns self if return_self is True, otherwise None.
            ```
        """
        
        for key, value in kwargs.items():
            match key:
                # Chat
                case "_Chat__replies_limit":
                    self.chat_replies_limit = value
                case "_Chat__history":
                    self.chat_history = value
                case "_Chat__creation_date":
                    self.chat_creation_date = value
                case "_Chat__user":
                    self.chat_user = value
                case "_Chat__title":
                    self.chat_title = value
                # Bot
                case "_Bot__rules":
                    self.bot_rules = value
                case "_Bot__name":
                    self.bot_name = value
                # Model
                case "_Model__model":
                    self.model_model = value
                case "_Model__api_key":
                    self.model_api_key = value
        
        return self if return_self else None
    
    @chat_replies_limit.setter
    def chat_replies_limit(self, new_replies_limit: int | None) -> None:
        """
            # chat_replies_limit (setter)

            ## Description
            Set a new reply limit for the chat. If None is provided, the limit is treated as infinity.

            ## Parameters
            ```python
            new_replies_limit: int | None
                # The new reply limit. If None, there is no limit.
            ```

            ## Raises
            ```python
            TypeError
                # Raised if the new value cannot be converted to an integer when it is not None.
            ```
        """

        try:
            self.__replies_limit = float("inf") if new_replies_limit == None else int(new_replies_limit)
        except:
            raise TypeError(f"<Invalid 'new_replies_limit' format: Expected 'int', got {type(new_replies_limit)}>")
    
    @chat_history.setter
    def chat_history(self, new_history: list[TextNode] | list[dict[str, str]] | None) -> None:
        """
            # chat_history (setter)

            ## Description
            Set a new conversation history for the chat. The history can be a list of TextNode objects or 
            a list of dictionaries convertible into TextNode objects.

            ## Parameters
            ```python
            new_history: list[TextNode] | list[dict[str, str]] | None
                # A list of TextNode objects or dictionaries defining message content. If None or empty, 
                # the chat history is reset to an empty list.
            ```

            ## Raises
            ```python
            TypeError
                # Raised if the elements in new_history are neither TextNode nor dict, 
                # or if the dict structure is invalid for converting to a TextNode.
            ```
        """

        if new_history:
            if all([isinstance(node, TextNode) for node in new_history]):
                self.__history = new_history
            elif all([isinstance(node, dict) for node in new_history]):
                try: 
                    self.__history = [TextNode(**node) for node in new_history]
                except:
                    raise TypeError("<Invalid 'new_history' format>")
            else:
                raise TypeError("<Invalid 'new_history' format>")
        else:
            self.__history = []
    
    @chat_time_format.setter
    def chat_time_format(self, new_time_format: str) -> None:
        """
            # chat_time_format (setter)

            ## Description
            Update the time format used by this chat for timestamps. 
            Attempts to format the current time with the new format to ensure validity.

            ## Parameters
            ```python
            new_time_format: str
                # A valid Python time format string (e.g., "%d/%m/%Y %H:%M:%S").
            ```

            ## Raises
            ```python
            ValueError
                # Raised if the format string cannot be used to format the current time.
            ```
        """

        try:
            time.strftime(new_time_format, time.localtime(time.time()))
            self.__time_format = new_time_format
        except:
            raise ValueError(f"<Invalid 'new_time_format' format: Expected valid time format>")
        
    @chat_creation_date.setter
    def chat_creation_date(self, new_creation_date: str) -> None:
        """
            # chat_creation_date (setter)

            ## Description
            Set a new creation date for the chat. The date must match the current `chat_time_format`.

            ## Parameters
            ```python
            new_creation_date: str
                # A date string conforming to chat_time_format.
            ```

            ## Raises
            ```python
            ValueError
                # Raised if the provided date string does not match the chat_time_format.
            ```
        """

        # check if new_creation_date is a valid date format
        try:
            # try to convert the string to a datetime object
            time.strptime(new_creation_date, self.chat_time_format)
            self.__creation_date = new_creation_date
        except:
            raise ValueError(f"<Invalid 'new_creation_date' format: Expected {repr(self.chat_time_format)}>")
    
    @chat_user.setter
    def chat_user(self, new_user: str) -> None:
        """
            # chat_user (setter)

            ## Description
            Update the user participating in the chat session.

            ## Parameters
            ```python
            new_user: str
                # The name or identifier of the new user.
            ```
        """

        self.__user = str(new_user)
    
    @chat_title.setter
    def chat_title(self, new_title: str) -> None:
        """
            # chat_title (setter)

            ## Description
            Update the chat session's title.

            ## Parameters
            ```python
            new_title: str
                # The new title for the chat.
            ```
        """

        self.__title = str(new_title)
    
    # -------- ACTIONS --------
    def get_response(self, 
                     prompt: str, 
                     user: str | None = None, 
                     image_path: str | None = None,
                     file_path: str | None = None) -> str:
        """
            # get_response

            ## Description
            Generate a response for a given user prompt. Optionally, an image or file can be attached
            for context. The returned text is then appended to the chat history as two TextNode objects 
            (one for the user and one for the assistant).

            ## Parameters
            ```python
            prompt: str
                # The user's message to the chat.
            user: str | None = None
                # The name or identifier of the user for this prompt. Defaults to the chat_user if None.
            image_path: str | None = None
                # The path to an image file to be base64-encoded and attached to the prompt.
            file_path: str | None = None
                # The path to a file to be uploaded and referenced by the underlying bot.
            ```

            ## Returns
            ```python
            str
                # The assistant's response content.
            ```
        """

        response = self.response(prompt=prompt, 
                                 user=self.__user if user == None else str(user), 
                                 history=self.__history if self.__history else None, 
                                 image_path=image_path,
                                 file_path=file_path)
        
        self.__update_history(prompt=prompt, response=response, owner_user=user)
        return response["content"]
    
    def __update_history(self, prompt: str, response: str, owner_user: str | None = None) -> None:
        """
            # __update_history

            ## Description
            A private method that updates the conversation history with a new user prompt and 
            the corresponding assistant response. Each conversation turn consists of two TextNode objects:
            one for the user and one for the assistant. If the reply limit is reached, this method 
            removes the oldest user and assistant messages from the history before appending the new ones.

            ## Parameters
            ```python
            prompt: str
                # The user's message to append to the chat history.
            response: dict[str, Any]
                # The dictionary containing response content and metadata returned by the underlying bot.
            owner_user: str | None
                # The name or identifier of the user for this prompt. Defaults to chat_user if None.
            ```
        """

        owner_user: str = self.__user if owner_user == None else str(owner_user)
        
        user_node: TextNode = TextNode(role="user", content=prompt, owner=owner_user, tokens=response["prompt_tokens"], date=response["start_date"])
        
        assistant_node: TextNode = TextNode(role="assistant", content=response["content"], owner=self.bot_name, tokens=response["completion_tokens"], date=response["final_date"])
        
        if self.__replies + 1 <= self.__replies_limit:
            self.__replies: int = self.__replies + 1
            
            self.__history.append(user_node)
            self.__history.append(assistant_node)
        else:
            self.__history.pop(0)
            self.__history.pop(0)
            
            self.__history.append(user_node)
            self.__history.append(assistant_node)









class CWArchive(object):
    """
    # CWArchive
    
    ## Description
    Manages an archive of `Chat`, `Bot`, or `Model` objects from a given file path. Provides both synchronous and asynchronous methods for loading and saving data, as well as operations to add, remove, or retrieve items within the archive.
    """

    def __init__(self, path: str, asynchronous: bool = True, delay: float = 0.07) -> None:
        """
            # CWArchive
            
            ## Description
            Manages an archive of `Chat`, `Bot`, or `Model` objects from a given file path. Provides both synchronous and asynchronous methods for loading and saving data, as well as operations to add, remove, or retrieve items within the archive.

            ## Attributes
            ```python
            archive_path: str             # The file path used to store the archive.
            archive_data: dict            # Dictionary representing the archived items with integer IDs as keys.
            archive_id: int               # The next available ID for adding a new item to the archive.
            archive_delay: float          # The delay (in seconds) between asynchronous load operations.
            archive_asynchronous: bool    # Indicates whether the archive is loaded and saved asynchronously.
            ```

            ## Methods
            ```python
            __str__() -> str
                # Returns a user-friendly string representation of the archive in the format <Archive | path=...>.

            __repr__() -> str
                # Returns a developer-friendly string representation of the archive.

            __len__() -> int
                # Returns the number of items currently stored in the archive.

            __add__(other: Chat | Bot | Model)
                # Adds the given object to the archive and returns the updated archive.

            __sub__(other: int | Chat | Bot | Model)
                # Removes the specified item (by ID or object) from the archive and returns the updated archive.

            define(path: str, delay: float) -> None
                # Defines or updates the archive path and sets the delay for async operations.

            get_id_from_element(element: Chat | Bot | Model) -> list[int]
                # Retrieves all IDs corresponding to the specified element in the archive.

            is_valid_id(identifier: int) -> bool
                # Checks if the provided ID exists in the archive.

            add(element: Chat | Bot | Model) -> None
                # Adds a new element to the archive under the next available ID.

            remove(element: list | set | tuple | int | Chat | Bot | Model, remove_type: str | None = "all") -> None
                # Removes one or more elements from the archive by ID(s) or object(s). 
                # The 'remove_type' parameter determines whether to remove all matching IDs, the first matching ID, or the last.

            save() -> None
                # Saves the current archive data to the file, ordering items by their representation before writing.

            retrieve() -> dict[int, Any]
                # Loads and returns all items from the archive file. If asynchronous loading is enabled, items are loaded in chunks using asyncio.
            ```
            
            ---
            
            # __init__
            
            ## Description
            Initialize the CWArchive instance with a path, an asynchronous flag, and an optional delay.
            
            ## Parameters
            ```python
            path: str            # The file path to the archive
            asynchronous: bool   # Indicates whether the archive operates asynchronously
            delay: float         # Delay (in seconds) between asynchronous load operations
            ```
            
            ## Raises
            ```python
            TypeError  # Sollevato se 'asynchronous' non è un booleano
            ```
            
            ## Possible Error (Summary)
            Race conditions can occur when operating asynchronously with certain operations that are not thread-safe. This often manifests as an error during object loading.

            ### Why it happens
            - The underlying operations are not fully thread-safe.

            ### How to fix it
            - Increase the 'delay' value (e.g., start from 0.07s and adjust as needed).
            - If errors persist, disable asynchronous behavior by setting 'archive_asynchronous' to False. (this will slow down the loading time)
        """
        
        # path
        self.__path = path 
        
        # asynchronous
        if isinstance(asynchronous, bool):
            self.__asynchronous = asynchronous
            self.archive_asynchronous
        else:
            raise TypeError(f"<Unexcpected type for 'asynchronous'. Expected 'bool', got instead {type(asynchronous)}>")
        
        # delay
        self.__delay = delay
        
        # data
        self.__data = self.archive_data
        self.__data_is_modified = False
        
    
    # -------- MAGIC METHODS --------
    def __str__(self) -> str:
        """
        # __str__

        ## Description
        Return a human-readable string representation of the CWArchive instance, including the path of the archive.
        """

        return f"<Archive | path={self.__path}>"
    
    def __repr__(self) -> str:
        """
        # __repr__

        ## Description
        Return an official string representation of the CWArchive instance, suitable for debugging or logging.
        """

        return f"Archive(path={repr(self.__path)})"
    
    def __len__(self) -> int:
        """
            # __len__

            ## Description
            Return the number of elements currently stored in the archive.
        """

        return len(self.archive_data)
    
    def __add__(self, other: Chat | Bot | Model):
        """
            # __add__

            ## Description
            Add a Chat, Bot, or Model object to the archive. The object is stored under the next available ID.

            ## Parameters
            ```python
            other: Chat | Bot | Model  # The object to be added to the archive
            ```

            ## Raises
            ```
            TypeError  # Raised if 'other' is not a Chat, Bot, or Model instance
            ```
        """

        if not isinstance(other, Chat | Bot | Model):
            raise TypeError(f"<Unexpected type. Expected 'Chat' or 'Bot' or 'Model', instead got {type(other)}>")
        self.add(other)
        return self
    
    def __sub__(self, other: int | Chat | Bot | Model):
        """
        # __sub__

        ## Description
        Remove an element from the archive by either its integer ID or by a Chat, Bot, or Model instance.
        - If 'other' is an integer, it removes the element with that ID.
        - If 'other' is a Chat, Bot, or Model object, it removes the matching element.

        ## Parameters
        ```python
        other: int | Chat | Bot | Model  # The identifier or object to remove from the archive
        ```

        ## Raises
        ```
        TypeError  # Raised if 'other' is neither an integer nor a Chat/Bot/Model
        ```
    """

        if isinstance(other, int):
            self.remove(element_id=other)
            return self
        elif isinstance(other, Chat | Bot | Model):
            self.remove(element=other)
            return self
        else:
            raise TypeError(f"<Unexpected type. Expected 'int' or 'Chat' or 'Bot' or 'Model', instead got {type(other)}>")
    
    def __enter__(self, *args, **kwargs):
        return self
    
    def __exit__(self, *args, **kwargs) -> None:
        self.save()
    
    # -------- GET --------
    @property
    def archive_path(self) -> str:
        """
            # archive_path (getter)

            ## Description
            Get the path where the archive file is stored.
        """

        return self.__path
    
    @property
    def archive_asynchronous(self) -> bool:
        """
            # archive_asynchronous (getter)

            ## Description
            Get the current asynchronous flag, indicating whether the archive operates in asynchronous mode.
        """

        return self.__asynchronous
    
    @property
    def archive_data(self) -> dict:
        """
            # archive_data (getter)

            ## Description
            Get the archive's data as a dictionary. If the data has been marked as modified, 
            this property triggers a reload from the file before returning the data.
        """

        if "_CWArchive__data_is_modified" not in self.__dir__():
            self.__data_is_modified = True
        
        if self.__data_is_modified:
            self.__data = self.retrieve()
            self.__data_is_modified = False
        
        return self.__data
    
    @property
    def archive_id(self) -> int:
        """
            # archive_id (getter)

            ## Description
            Retrieve the next available integer ID that can be used to store a new element in the archive.
        """

        try:
            actual_ids: set[int] = set(self.archive_data.keys())
            all_possible_ids: set[int] = set(range(max(actual_ids)+2))
            remaining_ids: set[int] = all_possible_ids - actual_ids
            return min(remaining_ids)
        except:
            return 0
    
    @property
    def archive_delay(self) -> float:
        """
            # archive_delay (getter)

            ## Description
            Get the current delay (in seconds) used between asynchronous loading operations.
        """

        return self.__delay
    
    
    # -------- SET --------
    @archive_path.setter
    def archive_path(self, new_path: str) -> None:
        """
            # archive_path (setter)

            ## Description
            Update the archive's file path. This marks the data as modified so that it will be reloaded next time it is accessed.

            ## Parameters
            ```python
            new_path: str  # The new path for the archive file
            ```
        """
        
        if os.path.exists(new_path):
            self.__path = new_path
            self.save()
        else:
            raise FileExistsError(f"<File '{new_path}' does not exixts>")


        # move the archive to the new path
        self.__path = new_path
        self.__data_is_modified = True
    
    @archive_asynchronous.setter
    def archive_asynchronous(self, new_asynchronous) -> None:
        """
            # archive_asynchronous (setter)

            ## Description
            Enable or disable asynchronous behavior for the archive.

            ## Parameters
            ```python
            new_asynchronous: bool  # True to enable asynchronous mode, False otherwise
            ```

            ## Raises
            ```
            TypeError  # Raised if 'new_asynchronous' is not a bool
            ```
        """

        if isinstance(new_asynchronous, bool):
            self.__asynchronous = new_asynchronous
        else:
            raise TypeError(f"<Unexcpected type for 'asynchronous'. Expected 'bool', got instead {type(new_asynchronous)}>")
    
    @archive_data.setter
    def archive_data(self, new_archive_data: dict) -> None:
        """
            # archive_data (setter)

            ## Description
            Set (replace) the current archive data with a new dictionary.

            ## Parameters
            ```python
            new_archive_data: dict  # The new data to store in the archive
            ```
        """

        self.__data = new_archive_data
    
    @archive_delay.setter
    def archive_delay(self, new_delay: float) -> None:
        """
            # archive_delay (setter)

            ## Description
            Set the new delay (in seconds) for asynchronous loading operations.

            ## Parameters
            ```python
            new_delay: float  # The delay value in seconds
            ```

            ## Raises
            ```
            TypeError  # Raised if 'new_delay' cannot be cast to float
            ```
        """

        try:
            self.__delay: float = float(new_delay)
        except:
            raise TypeError("<'new_delay' type is not correct>")
        
    
    # -------- ACTIONS --------
    def get_id_from_element(self, element: Chat | Bot | Model) -> list[int]:
        """
            # get_id_from_element

            ## Description
            Retrieve a list of integer IDs corresponding to the given element (Chat, Bot, or Model). 
            If the same element is stored multiple times, multiple IDs may be returned.

            ## Parameters
            ```python
            element: Chat | Bot | Model  # The element to look up in the archive
            ```
        """

        ids: list = list()
        for k, v in self.archive_data.items():
            ids.append(k) if v == element else None
        
        return ids
    
    
    def is_valid_id(self, identifier: int) -> bool:
        """
            # is_valid_id

            ## Description
            Check if the provided integer ID exists in the archive.

            ## Parameters
            ```python
            identifier: int  # The ID to check
            ```
        """

        return identifier in list(self.archive_data.keys())
    
    
    def add(self, element: Chat | Bot | Model) -> None:
        """
            # add

            ## Description
            Add a Chat, Bot, or Model object to the archive under the next available ID.

            ## Parameters
            ```python
            element: Chat | Bot | Model  # The object to add to the archive
            ```

            ## Raises
            ```
            TypeError  # Raised if 'element' is not a Chat, Bot, or Model
            ```
        """

        if not isinstance(element, Chat | Bot | Model):
            raise TypeError(f"<Invalid 'element' type. Expected 'Chat | Bot | Model', got instead {type(element)}>")
        
        self.archive_data[self.archive_id] = element
    
    
    def remove(self, element: list | set | tuple | int | Chat | Bot | Model, remove_type: str | None = "all") -> None:
        """
            # remove

            ## Description
            Remove one or more elements from the archive. Elements can be specified by:
            - A single integer ID
            - A single Chat, Bot, or Model
            - An iterable (list, set, tuple) of IDs or Chat/Bot/Model instances.
            The 'remove_type' parameter can be used to remove all matching items, or only the first/last match.

            ## Parameters
            ```python
            element: list | set | tuple | int | Chat | Bot | Model  # The item(s) or ID(s) to remove
            remove_type: str | None = "all"                          # Removal strategy: "all", "first", or "last"
            ```

            ## Raises
            ```
            TypeError  # Raised if 'element' has invalid types
            Exception  # Raised if the element or ID to remove is not found
            ```
        """

        data = self.archive_data
        
        if isinstance(element, list | set | tuple): # Check if 'element' is an iterable
            if all([isinstance(identifier, int | Chat | Bot | Model) for identifier in element]): # Check if every item inside the iterable is int | Chat | Bot | Model.
                for index, is_type in enumerate([isinstance(identifier, Chat | Bot | Model) for identifier in element]):
                    obj = element[index]
                    if is_type:
                        selected_ids = self.get_id_from_element(element=obj)
                        if selected_ids:
                            match remove_type.lower().strip():
                                case "all":
                                    for _id in selected_ids:
                                        del data[_id]
                                case "first":
                                    del data[selected_ids[0]]
                                case "last":
                                    del data[selected_ids[-1]]
                                case _:
                                    raise ValueError(f"<The entered 'remove_type' is not allowed: '{remove_type}'>")
                        else:
                            raise Exception(f"<The item does not match any id in the archive. element: {str(obj)}>")
                    else:
                        if not self.is_valid_id(identifier=obj):
                            raise Exception(f"<Identifier not found. {obj}>")
                        del data[obj]
            else:
                raise TypeError(f"<Unexpected object type inside the iterable. Excpected 'int | Chat | Bot | Model'>")
        elif isinstance(element, Chat | Bot | Model):
            selected_ids = self.get_id_from_element(element=element)
            if selected_ids:
                match remove_type.lower().strip():
                    case "all":
                        for _id in selected_ids:
                            del data[_id]
                    case "first":
                        del data[selected_ids[0]]
                    case "last":
                        del data[selected_ids[-1]]
                    case _:
                        raise ValueError(f"<The entered 'remove_type' is not allowed: '{remove_type}'>")
            else:
                raise Exception(f"<The item does not match any id in the archive. element: {str(element)}>")
        else:
            try:
                element = int(element)
                if not self.is_valid_id(identifier=element):
                    raise Exception(f"<Identifier not found. {element}>")
                del data[element]
            except:
                raise TypeError(f"<Unexpected object type. Excpected 'list[int | Chat | Bot | Model] | set[int | Chat | Bot | Model] | tuple[int | Chat | Bot | Model] | int | Chat | Bot | Model', got instead {type(element)}>")
        
        self.archive_data = data
        
    
    def save(self) -> None:
        """
            # save

            ## Description
            Save the current archive data to the file in sorted order. 
        """

        data = {k: v for k, v in sorted(self.archive_data.items(), key=lambda item: item[1])}
        with open(self.archive_path, "w") as f:
            for id, obj in data.items():
                data[id] = repr(obj)
            
            f.write(repr(data))
            self.__data_is_modified = True
    
    
    def __chunk_data(self, dictionary: dict) -> list[dict]:
        """
            # __chunk_data

            ## Description
            Split a dictionary into smaller dictionaries (chunks) of a specified maximum size. 
            Used for batching data when loading it asynchronously.

            ## Parameters
            ```python
            dictionary: dict  # The dictionary to split into chunks
            step: int         # The size of each chunk
            ```
        """

        dictionary = list(dictionary.items())
        
        length = len(dictionary)
        #step = int((7/95)*length + (50/19))
        step = 1 if length < 100 else 3
        
        return [dict(dictionary[i:i+step]) for i in range(0, len(dictionary), step)]
    
    
    async def __async_load_chunk(self, chunk: dict[int, str]):
        """
            # __async_load_chunk

            ## Description
            Load and reconstruct objects asynchronously from a chunk of string representations.
            Each item in the chunk is processed with a delay as defined by 'archive_delay'.

            ## Error Explanation
            If an error occurs during object loading, it is often caused by operations within the 
            library that are not thread-safe. On most devices, a delay of 0.07 seconds typically 
            prevents race conditions. If the error continues:
            - Incrementally increase 'archive_delay' to reduce concurrency.
            - Alternatively, disable asynchronous mode by setting 'archive_asynchronous' to False.

            ## Parameters
            ```python
            chunk: dict[int, str]  # A dictionary mapping IDs to string representations of objects
            ```

            ## Raises
            ```
            Exception  # Raised if an error occurs during object loading
            ```
        """

        for k, v in chunk.items():
            for _ in range(6):   # try to load the object 6 times
                try:
                    None if _ == 0 else time.sleep(self.archive_delay)
                    chunk[k] = await async_load(v)
                    break
                except Exception as e:
                    if _ == 5:
                        raise Exception(f"<Error loading (id={k}): error = {e}. This issue is often caused by operations within the library that are not thread-safe. On most devices, setting a 'archive_delay' of 0.07 seconds is sufficient to prevent race conditions. \nHowever, if the error persists, you can experiment with increasing the delay value incrementally until the error no longer occurs. \nAlternatively, if achieving stability through parallel execution proves challenging, you may opt to execute the entire process sequentially by setting the attribute 'archive_asynchronous' to False.>")
        return chunk
    
    
    async def __async_retrieve(self, chunked_data: dict[list]):
        """
            # __async_retrieve

            ## Description
            Asynchronously load and reconstruct objects by processing multiple chunks of data in parallel.
            Gathers all chunks and combines them into one dictionary of loaded objects.

            ## Parameters
            ```python
            chunked_data: list[dict[int, str]]  # A list of dictionary chunks, each containing ID-to-string mappings
            ```

            ## Raises
            ```
            Exception  # Propagates any error from individual chunks
            ```
        """

        coroutines: list[dict] = []
        for chunk in chunked_data:
            coroutines.append(self.__async_load_chunk(chunk=chunk))
            
        results = await asyncio.gather(*coroutines)
        
        loaded_data: dict[int, Chat] = dict()
        for item in results:
            loaded_data.update(item)
        
        return loaded_data
    
    
    def retrieve(self) -> dict[int, Chat | Bot | Model]:
        """
            # retrieve

            ## Description
            Read the archive file from disk and reconstruct all stored objects. 
            If asynchronous mode is enabled, the data is split into chunks for parallel loading; 
            otherwise, the loading is performed sequentially.

            ## Raises
            ```
            TypeError   # Raised if the archive file contains data of an invalid type
            Exception   # Raised if the archive format is invalid or if loading fails
            ```
        """

        with open(self.archive_path, "r") as f:
            data: str = f.read()
        
        try:
            if data:
                data: dict[int, Any] = eval(data)   # {int: 'Chat', int: 'Chat', ...}
                
                if self.archive_asynchronous: # if 
                    chunked_data = self.__chunk_data(dictionary=data)
                    data = asyncio.run(self.__async_retrieve(chunked_data=chunked_data))
                else:
                    for k, v in data.items():
                        data[k] = load(v)
                return data
            else:
                return {}
        except TypeError:
            raise TypeError(f"<Invalid type>")
        except Exception as e:
            raise Exception(f"<Invalid archive format. {e}>")




class Loom(object):
    def __init__(self, *args, strands: list | None = None, name: str = "Loom AI", **kwargs) -> None:
        self.__name: str = name
        self.__strands: list = strands if strands else []
        self.__initialized: bool = False
        self.__setup_strands(*args, **kwargs)

    # -------- SETUP --------
    def __setup_strands(self, *args, **kwargs):
        # Logica per inizializzare gli agenti o strands
        self.__initialized = True
        print(f"Loom '{self.__name}' è stato inizializzato con {len(self.__strands)} strand.")

    # -------- MAGIC METHODS --------
    def __str__(self):
        return f"<Loom | {self.__name:=}, {len(self.__strands):=} strands>"
    def __repr__(self):
        return f"Loom(name={self.__name}, strands={len(self.__strands)})"

    # -------- GET --------
    def get_strands(self) -> list:
        return self.__strands
    def get_name(self) -> str:
        return self.__name
    def get_status(self) -> bool:
        return self.__initialized

    # -------- SET --------
    def set_threads(self, new_strands: list) -> None:
        self.__strands = new_strands
    def add_thread(self, strand) -> None:
        self.__strands.append(strand)
        print(f"Aggiunto nuovo thread: {strand}")

    # -------- EXECUTE --------
    def weave(self, task: str, *args, **kwargs) -> None:
        if not self.__initialized:
            raise Exception(f"Loom '{self.__name}' non è inizializzato.")
        print(f"Eseguo il compito: '{task}' con {len(self.__strands)} strand.")
        # Logica per orchestrare il weaving dei threads
        for strand in self.__strands:
            print(f"Esecuzione strand: {strand}")
        print(f"Compito '{task}' completato.")



def load(cw_string_object) -> Any:
    """
    Args:
        cw_string_object (_type_): _description_

    Raises:
        Exception: _description_

    Returns:
        Any: _description_
    """
    
    try:
        return eval(cw_string_object)
    except:
        print(cw_string_object)
        raise Exception("<The object entered cannot be converted to a chatweaver object. Invalid format.>")


async def async_load(cw_string_object) -> Any:
    """
    Args:
        cw_string_object (_type_): _description_

    Raises:
        Exception: _description_

    Returns:
        Any: _description_
    """
    local_globals = dict(globals())
    
    try:
        return await asyncio.to_thread(eval, cw_string_object, local_globals)
    except Exception as e:
        raise e
        raise Exception("<The object entered cannot be converted to a chatweaver object. Invalid format.>")