from optimum.intel.openvino import OVStableDiffusionPipeline
from openvino.runtime import Core
import time

class imageGen:
    def __init__(self):
        pass

    def group_sentences(self, sentences):
        grouped = []
        # Loop through the sentences and group every 'group_size' sentences
        for i in range(0, len(sentences), 3):
            group = " ".join(sentences[i:i+3])  # Join the group into a single string
            grouped.append(group)
        return grouped
    
    def generate_images_from_text(self,sentences):
        start_time = time.time()
        model_id = "OpenVINO/stable-diffusion-v1-5-int8-quant"
        pipeline = OVStableDiffusionPipeline.from_pretrained(model_id)
        pipeline.reshape(batch_size=1, height=512, width=512, num_images_per_prompt=1)
        pipeline.compile()

        image_paths = []

        for i, prompt in enumerate(sentences):
            output = pipeline("draw this as a child friendly illustration:" + prompt, num_inference_steps=50, output_type="pil")
            output.images[0].save(f"C:/Users/intelaipc/IntelAIPCProject/UI/electron/images/img{i}.png")
            image_paths += f"C:/Users/intelaipc/IntelAIPCProject/UI/electron/images/img{i}.png"
        
        print(f"Time taken to generate images: {time.time() - start_time} seconds")
        return image_paths
    
sentences = ["In the bustling town of Greenfield, there was a lively debate about the best way to keep the town clean and green. The townspeople were divided between two ideas: recycling and composting. The mayor, Mr. Green, decided to hold a town meeting at Greenfield's Community Center to discuss the matter.", 
             "They both had strong arguments, but they needed to find common ground. Lily said, 'Recycling helps us reuse things and save our beautiful planet!' Tom nodded and added, 'Composting turns our food scraps into rich soil that helps plants grow.' ",
             "The townspeakers were intrigued by their conversation and asked, 'But which one is better?' Lily and Tom smiled and explained that both recyling and compostering were important. They showed everyone how recycyling saves energy and resources, while compost helps reduce waste and enriches the soil.",
             "The people of GreenField were amazed by the science behind both ideas. They realized that working together, they could create a cleaner and greener town.",
             "However, just as the townspeoples were about to make a decision, a twisted turn of events occurred. A mysterious creature came out into the room"]

jen = imageGen()

jen.generate_images_from_text(sentences)