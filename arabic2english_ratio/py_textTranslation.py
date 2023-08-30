import re, os
import numpy as np
from openiti.helper.ara import deNoise
import openai
import random, time, sys

# Check if an argument is provided
if len(sys.argv) != 2:
    print("Please provide 1 argument: 1) OpenAI key")
    sys.exit(1)

# Get the argument

openAIapiKey = sys.argv[1]
fileLimit = 505

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


folders = ["texts_Arabic_to_English", "texts_English_to_Arabic"]

for folder in folders:
    print(folder)
    language2 = folder.split("_")[1]
    print(language2)

    files = os.listdir(f"./{folder}/")
    files = [f for f in os.listdir(f"./{folder}/") if not f.startswith(".")]
    random.shuffle(files)


    for f in files:
        start_time = time.time()  # Capture the start time before loop execution

        if not os.path.isfile(f"./{folder}_back/{f}"):
            print(f)
            with open(f"./{folder}/{f}", "r", encoding="utf8") as f1:

                text = f1.read()
                text = deNoise(text)
                text = re.sub(r"\n\n+", "\n\n", text)

                data = re.split("===TRANSL===", text)

                textToTranslate = data[1]

                roleDescription = f"""
                        Please, translate the following text into {language2}. Try to keep as close to the original text as possible.
                        """.strip()
                    
                response = openai.ChatCompletion.create(
                    model = models[0],
                    messages=[{"role": "user", "content": roleDescription +"\n\n"+ textToTranslate}])

                translated = response["choices"][0]["message"]["content"]

                lenTest1 = len(textToTranslate.strip().split("\n\n"))
                lenTest2 = len(translated.strip().split("\n\n"))

                if lenTest1 == lenTest2:

                    finalText = textToTranslate + "\n\n===TRANSL===\n\n" + translated

                    with open(f"./{folder}_back/{f}", "w", encoding = "utf8") as f9:
                        f9.write(finalText)

                    #print(returnedEng)
                    #print(returnedAra)

                    #input()
                    print("\tResults are good. Saved...")

                else:
                    print("\tResults were not good. Must be re-run...")

        else:
            print("\tThe file has already been processed!")
        
        end_time = time.time()  # Capture the end time after loop execution
        elapsed_time = end_time - start_time  # Calculate elapsed time
        
        # Convert to minutes and seconds
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60

        print(f"Time taken for iteration {f}: {minutes} minutes and {seconds:.2f} seconds")








