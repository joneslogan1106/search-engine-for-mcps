import math
import ast
import os
from textblob import TextBlob as tb

def get_current_mcps(showFullRelativePath=True):
    mcps = []
    directory_path = "./../mcps/"
    try:
        # Get a list of all entries (files and directories) in the specified path
        all_entries = os.listdir(directory_path)

        # To list only directories, you can filter using os.path.isdir()
        if showFullRelativePath == True:
            directories_only = [os.path.join(directory_path, entry) for entry in all_entries if os.path.isdir(os.path.join(directory_path, entry))]
            mcps = directories_only
            return mcps
        elif showFullRelativePath == False:
            directories_only = [os.path.join(entry) for entry in all_entries if os.path.isdir(os.path.join(directory_path, entry))]
            mcps = directories_only
            return mcps

    except FileNotFoundError:
        print(f"Error: Directory not found at '{directory_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

class VectorCompare:
    def magnitude(self, concordance):
        if not isinstance(concordance, dict):
            raise ValueError('Supplied Argument should be of type dict')
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        if not isinstance(concordance1, dict):
            raise ValueError('Supplied Argument 1 should be of type dict')
        if not isinstance(concordance2, dict):
            raise ValueError('Supplied Argument 2 should be of type dict')
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        denominator = self.magnitude(concordance1) * self.magnitude(concordance2)
        return topvalue / denominator if denominator != 0 else 0

    def concordance(self, document):
        if not isinstance(document, str):
            raise ValueError('Supplied Argument should be of type string')
        con = {}
        for word in document.split():
            if word in con:
                con[word] += 1
            else:
                con[word] = 1
        return con
    

class DocumentAggregator:
    def __init__(self, directories, output_dir='data'):
        self.directories = directories
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        for dir_path in get_current_mcps():
            print(dir_path)
            self.aggregate_documents(dir_path)
    
    def aggregate_documents(self, input_dir, extensions=(".txt", ".md", ".log", ".csv", ".json", ".xml")):
        """
        Aggregates all readable documents in a directory into a single file and saves it to 'data/'.
        """
        dir_name = os.path.basename(os.path.abspath(input_dir))
        output_file = os.path.join(self.output_dir, f"{dir_name}_aggregated.txt")

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for root, _, files in os.walk(input_dir):
                for filename in files:
                    if filename.lower().endswith(extensions):
                        file_path = os.path.join(root, filename)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as infile:
                                outfile.write(f"\n=== {file_path} ===\n")
                                outfile.write(infile.read())
                                outfile.write("\n")
                        except Exception as e:
                            print(f"Skipping {file_path} due to error: {e}")

    def __iter__(self):
        """
        Iterates over all documents in the 'data' directory.
        Yields (filename, content) tuples.
        """
        for filename in os.listdir(self.output_dir):
            file_path = os.path.join(self.output_dir, filename)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        yield filename, f.read()
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")
class TFIDF():

    def __init__(self, directories):
        self.da = DocumentAggregator(directories)

    def tf(self, word, blob):
        return blob.words.count(word) / len(blob.words)

    def n_containing(self, word, bloblist):
        return sum(1 for blob in bloblist if word in blob.words)

    def idf(self, word, bloblist):
        return math.log(len(bloblist) / (1 + self.n_containing(word, bloblist)))

    def tfidf(self, word, blob, bloblist):
        if word == "And" or word == "and" or word == "Of" or word == "of" or word == "For" or word == "FOR" or word == "for" or word == "AND" or word == "Not" or word == "NOT" or word == "not" or word == "nor" or word == "NOR" or word == "but" or word == "BUT" or word == "But" or word == "or" or word == "OR" or word == "Or" or word == "THE" or word == "The" or word == "the" or word == "to" or word == "To" or word == "TO" or word == "IN" or word == "in" or word == "In" or word == "Is" or word == "IS" or word == "is":
            return 0
        return self.tf(word, blob) * self.idf(word, bloblist)
    

    def run(self):
        bloblist = [tb(content) for filename, content in self.da]
        for i, blob in enumerate(bloblist):
            scores = {word: self.tfidf(word, blob, bloblist) for word in blob.words}
            sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            #for word, score in sorted_words[:10]:
            #    print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
            with open(f"tfidf/{get_current_mcps(False)[i]}.txt", "w") as file:
                pass # No content written
            with open(f"tfidf/{get_current_mcps(False)[i]}.txt", "w") as f:
                f.write(str(sorted_words))
            f.close()

if __name__ == "__main__":
    while True:
        user_input = input("> ")
        if user_input == "help":
            print(" cache    - Aggrevates all the documents, and makes the TFIDF file for said documents.")
            print(" search   - tests stuff")
            print(" exit     - Exits the program")
        elif user_input == "cache":
            tf = TFIDF([get_current_mcps()])
            tf.run()
        elif user_input == "search":
            print("This option assumes you already ran the cache command")
            current_mcps = get_current_mcps(False)
            sorted_words_per_mcp = []
            for i in current_mcps:
                with open(f"./tfidf/{i}.txt") as f:
                    lines = f.readlines()
                    for line in lines:
                        sorted_words_per_mcp.append([i, line.strip()])  # keep `i` directly

            converted_data = []

            for mcp_id, raw_string in sorted_words_per_mcp:
                try:
                    parsed = ast.literal_eval(raw_string)  # e.g., ('output', -0.0001, '16')
                    parsed_list = list(parsed)
                    converted_data.append({
                        "mcp": mcp_id,
                        "data": parsed_list
                    })
                except Exception as e:
                    print(f"Error parsing line from MCP {mcp_id}: {e}")
                    converted_data.append({
                        "mcp": mcp_id,
                        "data": []
                    })
            print(converted_data[0]['mcp'])
            print(converted_data[0]['data'][0])
            print(converted_data[0]['data'][0][0])
            print(converted_data[0]['data'][0][1])
        elif user_input == "exit":
            break
        else:
            print(f"Unknown instruction {user_input}")