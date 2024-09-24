from transformers import pipeline
import openvino
from openvino.runtime import Core
from transformers import AutoConfig, AutoTokenizer
from optimum.intel.openvino import OVModelForCausalLM
from utils.llm_config import SUPPORTED_LLM_MODELS
import time
import re

def seperate_sentences(text):
    # Regular expression to split on '.', '!', or '?' followed by space or end of string
    sentence_endings = re.compile(r'(?<=[.!?]) +')
    sentences = sentence_endings.split(text)
    return [sentence.strip() for sentence in sentences if sentence]

def load_model(model_xml, model_bin):
        model_configuration = SUPPORTED_LLM_MODELS["English"]["phi-3-mini-instruct"]

        model_dir = "../../models/storyTeller/phi-3-mini-instruct/INT4_compressed_weights"
        print(f"Loading model from {model_dir}")

        ov_config = {"PERFORMANCE_HINT": "LATENCY", "NUM_STREAMS": "1", "CACHE_DIR": ""}

        # if "GPU" in device.value and "qwen2-7b-instruct" in model_id.value:
        #     ov_config["GPU_ENABLE_SDPA_OPTIMIZATION"] = "NO"

        # On a GPU device a model is executed in FP16 precision. For red-pajama-3b-chat model there known accuracy
        # issues caused by this, which we avoid by setting precision hint to "f32".
        # if model_id.value == "red-pajama-3b-chat" and "GPU" in core.available_devices and device.value in ["GPU", "AUTO"]:
        #     ov_config["INFERENCE_PRECISION_HINT"] = "f32"

        model_name = model_configuration["model_id"]
        tok = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

        ov_model = OVModelForCausalLM.from_pretrained(
            model_dir,
            device="CPU",
            ov_config=ov_config,
            config=AutoConfig.from_pretrained(model_dir, trust_remote_code=True),
            trust_remote_code=True,
        )
        return ov_model, tok

def group_sentences(sentences):
        grouped = []
        # Loop through the sentences and group every 'group_size' sentences
        for i in range(0, len(sentences), 3):
            group = " ".join(sentences[i:i+3])  # Join the group into a single string
            grouped.append(group)
        return grouped

class llm:
    def __init__(self, model_xml, model_bin):
        self.model_xml = model_xml
        self.model_bin = model_bin
        model_data = load_model(model_xml, model_bin)
        self.model = model_data[0]
        self.tokenizer = model_data[1]
        self.story = None
        self.question1 = None
        self.question2 = None

    def generate_response(self, prompt, examples):
        # Example text to be processed
        formatted_prompt = "".join([f"{ex['input']}: {ex['output']}\n" for ex in examples]) + prompt

        # Tokenize the text, now including the examples as part of the context
        inputs = self.tokenizer(formatted_prompt, return_tensors="pt")

        # Perform inference
        outputs = self.model.generate(**inputs, max_new_tokens=300, temperature=1.2, top_p=0.9, no_repeat_ngram_size=3)


        # Decode the generated tokens to text
        decoded_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        if decoded_output.startswith(prompt):
            decoded_output = decoded_output[len(formatted_prompt):].strip()
        
        print("Generated Text:", decoded_output)

        return decoded_output

    def generate_story(self):
        
        start_time = time.time()

        examples = [
            {"input": "Write an educational story (3-5 paragraphs) targeted at young children using simple words. The story should be inspired from this text snippet: {}. The story should have the following features: - Science integration: embed basic science concepts within the story, explaining them through the characters' adventures and discoveries. - Characters and dialogue: create memorable characters who engage in meaningful conversations, helping to explain and explore the science concepts. - Unexpected twist: conclude with a twist that doesn't resolve as hoped, but leaves a clear lesson about life and science.", "output": "Once upon a time in the land of Policymia, there lived two leaders named Majora and Minoro. Their job was to make sure all the citizens had beautiful parks, clean water, and top-notch schools. But there were so many things to fix! How would they ever decide where to start? Majora, being the wise leader she was, knew just what to do. She invited her fellow policymakers for a big meeting at the Roundtable of Representatives. There, they discussed the most important problems Policymia faced. This was called identifying 'key policy areas.' It meant figuring out which topics needed attention first. Next came assessing support – finding out if everyone agreed on the solutions. Some people thought building more playgrounds was the way to go, while others wanted better libraries. To understand everyone's thoughts, Majora used something called 'polling.' Just like taking a vote, polling helped her see what ideas were popular among her friends (the majority) and also those across the aisle (people who didn't belong to her political group). While talking to her friends and colleagues, Majora discovered that almost everyone loved science! And why not? Science could help create amazing inventions, protect nature, and even cure sicknesses. So, the policymakers decided to build a super cool SCIENCE CENTER right at the heart of Policymia! But then, an unexpected problem popped up! A grumpy neighboring kingdom threatened to block Policymia's plans because they feared losing visitors to the new center. Oh no! However, instead of giving up, Majora saw this challenge as an opportunity. If they could work together with the grumpy neighbors, maybe both lands could benefit. That way, everybody wins, showing the true spirit of teamwork and collaboration in the world of policies!"},
            {"input": "Write an educational story (3-5 paragraphs) targeted at young children using simple words. The story should be inspired from this text snippet: {}. The story should have the following features: - Science integration: embed basic science concepts within the story, explaining them through the characters' adventures and discoveries. - Characters and dialogue: create memorable characters who engage in meaningful conversations, helping to explain and explore the science concepts. - Unexpected twist: conclude with a twist that doesn't resolve as hoped, but leaves a clear lesson about life and science.", "output": "In the heart of Harmonyville, nestled between two neighboring countries, lay a magnificent bridge. Not only did it connect the land masses, but it also joined hearts and minds of folks living on either side. Let's call our beloved structure 'The Friendship Bridge'. One bright morning, Sarah from Sunnyhill and Maria from Starshine decided to explore this marvelous architectural feat. As they skipped along its vibrant pathway adorned with multicolored flags fluttering cheerily, Sarah asked, 'Maria, do you know how bridges stand strong despite all the cars going over them?' With a curious smile, Maria replied, 'Well, I think it has something to do with physics! Bridges use different types of forces like tension, compression, and torsion to balance themselves out.' Sarah gasped, 'Wow! That sounds complicated. But then again,' she pointed towards the distant mountains, 'those tall peaks must face greater force by wind and snow. Yet, they stand firm too!' As the day wore on, they reached the middle of the bridge where an information kiosk stood proudly. There, they learned about the various parts of the bridge – abutments, piers, deck, trusses...it seemed almost alive! Each part played a crucial role just like cells in our bodies. Just when things couldn't get any better, dark clouds rolled in unexpectedly. Rain began pouring down drenching everyone including Sarah and Maria. Their excitement turned into worry as they realized they might not make it back home before dark. Suddenly, the once familiar route appeared ominous under the stormy sky. Despite being scared, they remembered what they had learned earlier. Just like structures need balance and harmony, so does nature. So instead of panicking, they took deep breaths calming themselves down. After all, even amidst turmoil, understanding science can bring clarity and peace. And sometimes, facing adversities hand-in-hand brings forth stronger friendships."},
        ]
        prompt = "Write an educational story (3-5 paragraphs) targeted at young children using simple words. The story should be inspired from this text snippet: {}. The story should have the following features: - Science integration: embed basic science concepts within the story, explaining them through the characters' adventures and discoveries. - Characters and dialogue: create memorable characters who engage in meaningful conversations, helping to explain and explore the science concepts. - Unexpected twist: conclude with a twist that doesn't resolve as hoped, but leaves a clear lesson about life and science."
        
        response = self.generate_response(prompt, examples)
        print(response)

        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")

        self.story = response

        sentences = seperate_sentences(self.story)
        sentences = self.group_sentences(sentences)

        return sentences
    

    def generate_questions(self):
        start_time = time.time()

        # split the story in half
        sentences = seperate_sentences(self.story)
        half = len(sentences) // 2
        first_half = sentences[:half]
        second_half = sentences[half:]
        # generate questions using multi shot learning, like in generate_story
        examples = [
             {"input": "Generate only one question based on this story. They approached the children and explained the importance of preserving nature. The children listened intently, and Penny used her beak to point out the beauty of the forest. Oliver then shared the wonders of photosynthesis and how it helps keep the air clean. The children were amazed and promised to stop littering. As they walked back home, Penny and Oliver felt proud of their efforts to educate the younger generation about the importance of taking care of the environment.", "output": "How can the process of photosynthesis in trees contribute to a cleaner environment, and what steps can be taken to prevent harmful actions like littering in natural areas?"},
              #the following text. The question should make the reader think critically about the text: The primary role of the trees in the forest, as described by Oliver the Owl, is to act as the lungs of the planet. This means that they play a crucial role in the ecosystem by absorbing carbon to act fast to protect the trees and the environment. They approached the children and explained the importance of preserving nature. The children listened intently, and Penny used her beak to point out the beauty of the forest. Oliver then shared the wonders of photosynthesis and how it helps keep the air clean. The children were amazed and promised to stop littering. As they walked back home, Penny and Oliver felt proud of their efforts to educate the younger generation about the importance of taking care of the environment.", "output": "How can the process of photosynthesis in trees contribute to a cleaner environment, and what steps can be taken to prevent harmful actions like littering in natural areas?"},
            {"input": "Generate only one question based on this story.  Tom nodded and added, 'Composting turns our food scraps into rich soil that helps plants grow.'" , "output": "How can the characters Lily and Tom combine their ideas about recycling and composting to create a sustainable solution for the environment?"},
             #The question should make the reader think critically about the text: At the meeting, two passionate characters emerged: Lily, a young girl who loved nature, advocated for recyclable materials, while Tom, a wise old man, championed compost. They both had strong arguments, but they needed to find common ground. Lily said, 'Recycling helps us reuse things and save our beautiful planet!' Tom nodded and added, 'Composting turns our food scraps into rich soil that helps plants grow.'", "output": "How can the characters Lily and Tom combine their ideas about recycling and composting to create a sustainable solution for the environment?"},
        ]
        prompt = "Generate only one question based on the following text. The question should make the reader think critically about the text: " + " ".join(first_half)

        response1 = self.generate_response(prompt, examples)
        print(response1)
        self.question1 = response1

        prompt = "Write a question based on the following text to help a reader develop analytical thinking skills: " + " ".join(second_half)

        response2 = self.generate_response(prompt, examples)
        print(response2)
        self.question2 = response2

        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")

        return [response1, response2]


# model_xml = "C:\\Users\\intelaipc\\IntelAIPCProject\\models\\storyTeller\\phi-3-mini-instruct\\INT4_compressed_weights\\openvino_model.xml"
# model_bin = "C:\\Users\\intelaipc\\IntelAIPCProject\\models\\storyTeller\\phi-3-mini-instruct\\INT4_compressed_weights\\openvino_model.bin"

# LLM = llm(model_xml, model_bin)

# LLM.generate_story()

# print("Generating questions!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
# LLM.generate_questions()