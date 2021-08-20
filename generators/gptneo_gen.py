import transformers

print(transformers.__version__)
from transformers import pipeline

import pandas as pd
from tqdm import tqdm

# generator = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')
# generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')

eval1_data = pd.read_csv("/home/tskunara/Data generation/eval1_sources_data.csv")

gptneo_gen = []

batch_size = 500

checkpoint = 0
iterations = checkpoint

for article in tqdm(eval1_data["title"][checkpoint:]):

    gptneo_gen.append(
        generator(str(article), do_sample=True, min_length=100, max_length=250, top_p=0.96, repetition_penalty=1.2)[0][
            'generated_text'])
    iterations += 1

    if iterations % batch_size == 0:
        temp_data = eval1_data[checkpoint:iterations]

        temp_data["gpt-neo"] = pd.DataFrame(gptneo_gen)

        temp_data.to_csv("/home/tskunara/Data generation/eval1_sources_data_v2_"
                         + str(checkpoint) + "_to_" + str(iterations) + "_gptneo1B.csv", index=False)

temp_data.to_csv("/home/tskunara/Data generation/eval1_sources_data_v2_"
                 + str(checkpoint) + "_to_" + str(iterations) + "_gptneo1B.csv", index=False)