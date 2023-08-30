import re, os
import numpy as np
from openiti.helper.ara import deNoise


folders = ["texts_Arabic_to_English", "texts_English_to_Arabic", "texts_Arabic_to_English_back", "texts_English_to_Arabic_back"]

for folder in folders:

    files = os.listdir(f"./{folder}/")
    files = [f for f in os.listdir(f"./{folder}/") if not f.startswith(".")]
    files = sorted(files)

    results = ["file\tsource\ttarget\tratio"]
    ratios = []

    for f in files:
        #print(f)
        with open(f"./{folder}/{f}", "r", encoding="utf8") as f1:
            text = f1.read()
            text = deNoise(text)
            text = re.sub(r"\n\n+", "\n\n", text)

            data = re.split("===TRANSL===", text)

            lenTest1 = len(data[0].strip().split("\n\n"))
            lenTest2 = len(data[1].strip().split("\n\n"))

            if lenTest1 == lenTest2:
                var1 = len(re.findall("\w+", data[0]))
                var2 = len(re.findall("\w+", data[1]))

                if folder == "texts_Arabic_to_English":
                    ratio = var2/var1
                elif folder == "texts_Arabic_to_English_back":
                    ratio = var1/var2
                elif folder == "texts_English_to_Arabic":
                    ratio = var1/var2
                elif folder == "texts_English_to_Arabic_back":
                    ratio = var2/var1

                row = str(f"{f}\t{var1}\t{var2}\t{ratio}")
                results.append(row)

                ratios.append(ratio)
            
            else:
                print("\tBAD FILE TO BE REMOVED: (number of §§ differs)", f)
                os.remove(f"./{folder}/{f}")



    #print(ratios)

    with open(f"{folder}.tsv", "w", encoding = "utf8") as f9a:
        f9a.write("\n".join(results))


    data = ratios

    if len(data) > 0:

        # Summary statistics
        count = len(data)
        mean = np.mean(data)
        median = np.median(data)
        std_dev = np.std(data)
        minimum = np.min(data)
        maximum = np.max(data)
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)

        print("\n\n")

        report  = f"{folder}\n# SUMMARY STATISTICS\n\n"
        report += f"Count: {count}\n"
        report += f"Mean: {mean:.2f}\n"
        report += f"Median: {median}\n"
        report += f"Standard Deviation: {std_dev:.2f}\n"
        report += f"Minimum: {minimum}\n"
        report += f"25th Percentile (Q1): {q1}\n"
        report += f"75th Percentile (Q3): {q3}\n"
        report += f"Maximum: {maximum}\n"

        print(report)
        with open(f"{folder}.txt", "w", encoding="utf8") as f9:
            f9.write(report)

        import seaborn as sns
        import matplotlib.pyplot as plt

        # Clear the current figure to ensure a fresh graph
        #plt.clf()

        # Generate the distribution curve
        #sns.kdeplot(data)
        sns.kdeplot(data, label=folder)

        # Add a legend
        plt.legend()

        # Display the plot
        #plt.show()

        plt.savefig(f"{folder}.png")


