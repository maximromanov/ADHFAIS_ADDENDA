import os, csv, re
import openai
import json, random, time
import random
import string
import sys

# Check if an argument is provided
if len(sys.argv) != 3:
    print("Please provide two arguments: 1) the first language; 2) OpenAI key")
    sys.exit(1)

# Get the argument
input_arg = sys.argv[1].lower()
openAIapiKey = sys.argv[2]
fileLimit = 505

# Execute based on input argument
if input_arg == 'english':
    language1 = "English"
    language2 = "Arabic"
    targetFolder = "texts_English_to_Arabic"
    print(f"Generating texts in {language1} and translating them into {language2}")
elif input_arg == 'arabic':
    language1 = "Arabic"
    language2 = "English"
    targetFolder = "texts_Arabic_to_English"
    print(f"Generating texts in {language1} and translating them into {language2}")
else:
    print("Invalid argument. Please use 'Arabic' or 'English'.")



################################################################################################
# FUNCTIONS
################################################################################################

def random_string(length=10):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))


################################################################################################
# OPEN AI VARIABLES
################################################################################################

openai.api_key = openAIapiKey

loopCount = 1

themes = ["politics", "economy", "culture", "traveling", "history", "sports", "weather",
          "engineering", "science", "humanities", "literature", "music", "climate",
          "technology", "oceans", "forests", "animals", "urban life", "rural life",
          "spirituality", "religion", "ethics", "philosophy", "programming", "art",
          "finances", "mortgage", "pets", "archeology", "democracy", "tyranny",
          "fascism", "autocracy", "capitalism", "socialism", "slavery", "repressions"]

models = [
	"gpt-3.5-turbo",
    "gpt-3.5-turbo-0613",
	"gpt-3.5-turbo-0301",
	#"text-davinci-003",
	#"text-ada-001"
]

################################################################################################

repeatFor = 100

for i in range(repeatFor):
    files = os.listdir(targetFolder)
    num_files = len(files)
    # Stop script execution if the number of files larger than the set limit (fileLimit == 500)
    if num_files >= fileLimit:
        print(f"The number of files is {fileLimit} or greater. Stopping script.")
        sys.exit(0)
    else:
        print(f"The number of files is {num_files}. Pressing on...")

    start_time = time.time()  # Capture the start time before loop execution

    themeRandom1, themeRandom2 = random.sample(themes, 2)

    # Insert code to be executed here
    print(f"Executing iteration {i + 1}: {themeRandom1}, {themeRandom2}")


    roleDescription = f"""
        Please, generate a text in {language1} on some subject at the intersection of {themeRandom1} and {themeRandom2}. The length of the text should be between 2000 and 2500 tokens.
        """.strip()
    
    #print(roleDescription)

    response = openai.ChatCompletion.create(
        model = models[0],
        messages=[{"role": "user", "content": roleDescription}])

    returned1 = response["choices"][0]["message"]["content"]


    roleDescription = f"""
        Please, translate the following text into {language2}. Try to keep as close to the original text as possible.
        """.strip()
    
    response = openai.ChatCompletion.create(
        model = models[0],
        messages=[{"role": "user", "content": roleDescription +"\n\n"+ returned1}])

    returned2 = response["choices"][0]["message"]["content"]

    finalText = returned1 + "\n\n===TRANSL===\n\n" + returned2

    #print(finalText)
    prefix = f"{themeRandom1}_{themeRandom2}__".replace(" ", "_")

    filename = f"./{targetFolder}/{prefix}" + random_string(length=10) + ".txt"
    with open(filename, "w", encoding = "utf8") as f9:
        f9.write(finalText)

    #print(returnedEng)
    #print(returnedAra)

    #input()

    end_time = time.time()  # Capture the end time after loop execution
    elapsed_time = end_time - start_time  # Calculate elapsed time
    
    # Convert to minutes and seconds
    minutes = int(elapsed_time // 60)
    seconds = elapsed_time % 60

    print(f"Time taken for iteration {i + 1}: {minutes} minutes and {seconds:.2f} seconds")


