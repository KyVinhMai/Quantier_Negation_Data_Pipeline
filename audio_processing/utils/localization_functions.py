from pydub import AudioSegment
import math
from minimum_word_distance import minimum_word_length
from preprocessing_functions import process_text
from spacy.tokens import Doc
import en_core_web_sm
nlp = en_core_web_sm.load()


def whisper_time_stamps(utterance: str, raw_result: dict) -> tuple[float,float]:
    """
    raw_result[segments] = list of dictionaries
    segment["text"]

    Ex.  {'
    id': 3,
    'seek': 0,
    'start': 20.56,
    'end': 28.16,
    'text': " City, the average rent is over $2,000. Vanessa and her mom also face other barriers, like credit's",
    'tokens': [4392, 11, 264, 4274, 6214, 307, 670, 1848, 17, 11, 1360, 13, 27928, 293, 720, 1225, 611, 1851, 661, 13565, 11, 411, 5397, 311],
    'temperature': 0.0,
    'avg_logprob': -0.17815227336711711,
    'compression_ratio': 1.628099173553719,
    'no_speech_prob': 0.06631708890199661
    }
    """
    first_word = utterance.lower().split()[0]
    for segment in raw_result["segments"]:
        if first_word in segment["text"].lower():
            if minimum_word_length(process_text(segment['text']), process_text(utterance), first_word):
                return segment["start"] * 1000, segment["end"] * 1000

def extract_sentence(start:float, end:float, audio_name: str) -> AudioSegment:
    "Segments the audio given the timestamps"
    audio_file = AudioSegment.from_wav(audio_name)
    return audio_file[start:end] if end else audio_file[start:]

def fa_return_timestamps(waveform, trellis, word_segments, i: int) -> tuple[float, float]:
    sample_rate = 44100
    ratio = waveform.size(1) / (trellis.size(0) - 1)
    word = word_segments[i]
    x0 = int(ratio * word.start)
    x1 = int(ratio * word.end)

    return float(f"{x0 / sample_rate:.3f}") * 1000, float(f"{x1 / sample_rate:.3f}") * 1000

def localize_segment(json_transcript, utterance) -> int:
    """
    Finds the location of utterance by searching through the document

    Returns whether the utterance is in the first half of the audio by taking
    the average of the amount of sentences in the doc and splitting it.
    """
    doc_file = Doc(nlp.vocab).from_json(eval(json_transcript))
    sentences = [str(sent) for sent in doc_file.sents]
    transcript_len = len(sentences)
    avg = math.floor(transcript_len / 2)

    index = 0
    for i, sent in enumerate(sentences):
        if utterance in sent:
            index = i
            break

    return 2 if index > avg else 1

if __name__ == "__main__":
    str1 = ['JOHN YDSTIE, host: ', "This is WEEKEND EDITION from NPR News. I'm John Ydstie. ", 'Coming up: Is the Internet killing our culture? But first: ', '(Soundbite of music) ', "YDSTIE: Climate Connections and NPR collaboration with National Geographic is focusing this month on the Pacific, home to millions of island dwellers. Imagine taking the state of Connecticut and breaking it up into little pieces, then sprinkle the bits over an area the size of Africa, and you have the island nations of the Pacific. There the ocean laps at islander's doorsteps and controls their weather and food supply. Now the ocean is changing as the world warms. ", "NPR's Chris Joyce travel to one of the island nations, Fiji, to talk to people about those changes and the ones they fear may be coming. ", '(Soundbite of music) ', 'Unidentified Man #1: Bula. Bula vinaka. ', 'Unidentified Man #2: Welcome to Fiji. ', '(Soundbite of people singing) ', "CHRISTOPHER JOYCE: Along the coast of Fiji's big island, Viti Levu, resort hotels and small fishing villages share the same view of the wide, blue Pacific. You will find local musicians in both places. Music is a social lubricate, like the greeting, bula, which can mean many things but mostly everything is just fine. ", "But everything isn't just fine. Fijians are noticing changes in their environment. At the University of the South Pacific in the busy capital of Suva, Kanid Kashana Koshi has been paying attention. Koshi directs the school's Centre for Environment. ", 'Mr. KANID KASHANA KOSHI (Director, University of South Pacific Center for Environment): An average global temperature rise will definitely have a lot of secondary impacts, one of which is sea level rise. Most of these are low-lying atolls and island countries, and even in countries like Fiji, where we have mountains and highlands and so on, most of the life takes place in the coastal area. ', 'JOYCE: So far, scientists have confirmed that average sea levels around the world have risen only slightly over the last century of warming, just a few centimeters. But even a small increase can push salt water into underground aquifers and contaminate fresh water, something in short supply in the Pacific Islands. And higher sea levels can be bigger surges during storms. ', 'Melchior Mataki is a senior researcher at the environment center. ', 'Mr. MELCHIOR MATAKI (Researcher, University of South Pacific): The important effects that people have been talking about recently has been on the severity and the frequency of some of the extreme weather, even slight, for example, extreme rainfalls that comes in all at one time. ', '(Soundbite of birds chirping) ', 'JOYCE: Climate scientists suspect that cyclones - the Pacific versions of hurricanes - will become more severe as the ocean warms. When a cyclone hits an island, there is no place to go. You have to live with it and you have to pay for it, something island nations are hard pressed to afford. ', 'Mr. MATAKI: The countries are already facing a lot of problems in dealing with improving the livelihood of its people. And calamities coming on top of it would suddenly put in a more precarious situation. ', '(Soundbite of people singing) ', "JOYCE: There is also a curious obstacle to discussing climate change in the Pacific. Many people in the islands are devoutly Christian. Walks through Suva on Sunday and you'll hear singing from churches throughout the city. ", '(Soundbite of people singing) ', 'JOYCE: Fijian scientists say they sometimes have trouble convincing citizens that humans can actually change the climate. Simon McGree is the chief climate scientist at the Fijian meteorological office. He keeps an editorial cartoon pinned up in his office, which shows a child on the island of Kiribati asking his father a question. ', "Mr. SIMON McGREE (Chief Climate Scientist, Fiji Meteorological Office): Papa, is sea level rising or is the island sinking? And the father saying, don't worry about rising or sinking. You know, God put Kiribati here. This is to test us if we believe man's words or God's. ", "JOYCE: I am not sure I get it. I mean, what's the point here? ", 'MR. McGREE: The lord will provide all the things. God will save us. ', "JOYCE: Is that an attitude that's prevalent in the Pacific? ", 'Mr. McGREE: Yes. Yes, very much so. ', 'JOYCE: Then, does it make it difficult to convince people that actually humans are making things different and we have to adapt? ', 'Mr. McGREE: To staunch Christian, yes, and many (unintelligible) become as staunch Christians. ', 'JOYCE: So how do you convince them? ', "Mr. McGREE: With as much data as possible. I mean, you can't argue with data. ", "JOYCE: If you actually have the data. Measurements of sea level in Fiji aren't nearly long enough to know, for sure, how much sea level has risen. The atmosphere in the Pacific has clearly warmed, though, and rainfall patterns appear to be changing. But exactly what's causing this? ", "Mr. McGREE: We're not too sure. It could be natural or it could be climate change related. ", 'JOYCE: But trying to separate climate change from normal swings in the weather is like picking the fly specks out of the pepper. ', 'Take the El Nino weather pattern. A change in the temperature of sea surface in the Western Pacific occurs every few years. El Nino or La Nina, they call them, it changes weather all across the Pacific and into the Americas. There are other weather patterns on even longer cycles in parts of the Pacific too. Climate scientists worry that a warming planet will, or may even already have, alter the El Nino cycle. ', "Mr. McGREE: It gets very complicated. In fact, I've come aware of more questions than answers. ", "JOYCE: Nonetheless, Fijians are asking McGree for answers, whether the sea level is really rising, whether there will be more cyclones and big storms. He says the science isn't strong enough yet to make predictions about Fiji but he can't help noticing changes in his own hometown of Sigatoka. ", 'Mr. MCGREE: We used to live right on the beach. And over the 14 years, well, I would come home during the school holidays and noticed that we had lost quite a bit of land. ', "Ms. DIANE McFADZIEN (Climate Policy Officer, Climate Witness Program): I always tell people that people in the Pacific, they're going to be thirsty before they're going to drown. ", "JOYCE: Diane McFadzien helped established the Climate Witness Program in the South Pacific. It's a program set up by the World Wildlife Fund and recruits people around the world to watch for unusual changes in weather and sea level. McFadzien recently talked to people on the Fijian island of Kumbara. ", "Ms. McFADZIEN: On this island, there is no fresh water and(ph) streams and they rely 100 percent on rainwater, it's only source of drinking water. And they were talking about the fact that there seems to be a lot less drinking water around. ", 'JOYCE: McFadzien is a native of the Cook Islands and also a scientist. She checked the meteorological records for the past 100 years and found that, yes, rainfall has been declining in that part of the Pacific. ', 'McFadzien says people know the weather patterns here. They live close to the sea. She says they know they are not producing the greenhouse gases that are warming the planet. ', "Ms. McFADZIEN: When we went into valley last year, for example, Kamishi(ph) members were like well, do they know in the U.S. what they're doing is really bad, or maybe we should have a mission and, you know, take some photos and go and tell people. ", 'JOYCE: But what will they tell the rest of the world? Scientists are just now trying to figure out what climate change is doing to the Pacific. The Global Environment Facility And Investment Fund is paying for research there. Scientists from universities and environmental groups are also studying coral reefs, mangrove forests and the ocean itself for signs of change. ', 'In the meantime, people, like Diane McFadzien, are trying to prepare. ', "Ms. McFADZIEN: I think it would be crazy to own a property on the beach. I just want a piece of land myself and it's very up high on the hill. So that's kind of changed. ", 'JOYCE: McFadzien may sound upbeat at the moment, but she knows that heading for the hills may someday be her only option, short of leaving her island altogether. ', 'Christopher Joyce, NPR News. ', 'YDSTIE: You can find more stories about climate change in the Pacific at npr.org/climateconnections. ']
    doc_file = nlp("".join(str1))
    print([str(sent) for sent in doc_file.sents])