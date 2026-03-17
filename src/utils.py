# Import the regular expression module
# It helps us clean and manipulate text using pattern matching
import re

# Import GoogleTranslator from deep_translator library
# This will allow us to translate text from any language to English
from deep_translator import GoogleTranslator


# ---------------------------------------------------------
# FUNCTION: clean_text
# ---------------------------------------------------------
# This function cleans raw transcript text before sending it
# to the AI model. Cleaning improves the quality of summarization.

def clean_text(text):

    # Step 1: Remove line breaks (\n) and replace them with spaces
    # This converts multi-line transcript text into a single line
    text = text.replace("\n", " ")

    # Step 2: Remove punctuation characters
    # The regex pattern [^\w\s] means:
    # remove everything that is NOT a word character or whitespace
    text = re.sub(r"[^\w\s]", " ", text)

    # Step 3: Remove extra spaces created during cleaning
    # \s+ means one or more whitespace characters
    text = re.sub(r"\s+", " ", text)

    # Step 4: Remove leading and trailing spaces
    return text.strip()


# ---------------------------------------------------------
# FUNCTION: translate_to_english
# ---------------------------------------------------------
# This function translates text to English if the transcript
# is in another language (for example Hindi).
# AI summarization models usually perform better with English text.

def translate_to_english(text):

    try:

        # Create a translator instance
        # source="auto" automatically detects the input language
        # target="en" translates the text into English
        translated = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(text)

        # Return the translated text
        return translated

    except Exception:

        # If translation fails for any reason,
        # return the original text instead of crashing the program
        return text