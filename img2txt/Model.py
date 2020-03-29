import os, math
import sys
sys.path.append("img2txt/tf_api/models/im2txt")
# sys.path.append("./tf_api/models/im2txt")


import tensorflow as tf

# Image Full Caption API
from img2txt.tf_api.models.im2txt.im2txt import inference_wrapper
from img2txt.tf_api.models.im2txt.im2txt import configuration
from img2txt.tf_api.models.im2txt.im2txt import show_and_tell_model
from img2txt.tf_api.models.im2txt.im2txt.inference_utils import vocabulary
from img2txt.tf_api.models.im2txt.im2txt.inference_utils import caption_generator

# from tf_api.models.im2txt.im2txt import inference_wrapper
# from tf_api.models.im2txt.im2txt import configuration
# from tf_api.models.im2txt.im2txt import show_and_tell_model
# from tf_api.models.im2txt.im2txt.inference_utils import vocabulary
# from tf_api.models.im2txt.im2txt.inference_utils import caption_generator


class Model(object):
    def __init__(self, CHECKPOINT_PATH, VOCAB_FILE):
        self.CHECKPOINT_PATH = CHECKPOINT_PATH
        self.VOCAB_FILE = VOCAB_FILE



class ImageFullCaption(Model):
    def __init__(self, CHECKPOINT_PATH, VOCAB_FILE):
        Model.__init__(self, CHECKPOINT_PATH, VOCAB_FILE)

    def Inference(self):
        pass

    # Build the inference graph.
    def _loadModel(self):
        self.g = tf.Graph()
        with self.g.as_default():
            self.model = inference_wrapper.InferenceWrapper()
            self.restore_fn = self.model.build_graph_from_config(configuration.ModelConfig(), self.CHECKPOINT_PATH)
        self.g.finalize()


    def _loadVocab(self):
        self.vocab = vocabulary.Vocabulary(self.VOCAB_FILE)

    # Load the model from checkpoint.
    def _loadCheckpoint(self):
        self.restore_fn(self.sess)

    def _loadImage(self, filename):
        with tf.gfile.GFile(filename, "rb") as f:
            self.image = f.read()

    def _generate(self):
        # Prepare the caption generator. Here we are implicitly using the default
        # beam search parameters. See caption_generator.py for a description of the
        # available beam search parameters.
        self.generator = caption_generator.CaptionGenerator(self.model, self.vocab)

    def init(self):
        self._loadModel()
        self._loadVocab()
        self._generate()
        self.sess = tf.Session(graph=self.g)
        self._loadCheckpoint()

    def run(self, filename):
        self._loadImage(filename)

        captions = self.generator.beam_search(self.sess, self.image)
        print("Captions for image %s:" % os.path.basename(filename))
        
        captions_result = []
        for i, caption in enumerate(captions):
            # Ignore begin and end words.
            sentence = [self.vocab.id_to_word(w) for w in caption.sentence[1:-1]]
            sentence = " ".join(sentence)
            # print("  %d) %s (p=%f)" % (i, sentence, math.exp(caption.logprob)))

            captions_result.append(sentence)

        return captions_result

if __name__=="__main__":
    CHECKPOINT_PATH="./tf_data/model2.ckpt-3000000"
    VOCAB_FILE="./tf_data/word_counts_3.txt"
    IMAGE_FILE="./tf_data/img.jpg"

    caption = ImageFullCaption(CHECKPOINT_PATH, VOCAB_FILE)
    caption.init()
    print(caption.run(IMAGE_FILE))
