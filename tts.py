from kokoro import KPipeline
import soundfile as sf
import sounddevice as sd
import concurrent.futures


class tts:
    def __init__(self):
        self.pipeline = KPipeline(lang_code='a',device='cpu')
        self.v = {1: 'af_bella', 2:'af_heart',3:'af_sarah',4:'bf_emma',5:'bf_isabella',6:'af_sky'}

    def play_audio(self, text ,voice_num = 1):
        generator = self.pipeline(
            text, voice=self.v[voice_num],
            speed=1, split_pattern=r'\n+'
        )
        arr = []
        for i, (gs, ps, audio) in enumerate(generator):
            print(i)  # i => index
            print(gs) # gs => graphemes/text
            print(ps) # ps => phonemes
            arr.append(audio)


        for i in arr:
            sd.play(i, 24000)
            sd.wait()


# 🇺🇸 'a' => American English, 🇬🇧 'b' => British English
# 🇯🇵 'j' => Japanese: pip install misaki[ja]
# 🇨🇳 'z' => Mandarin Chinese: pip install misaki[zh]



if (__name__ == "__main__"):
    #af_bella
    #af_heart
    #af_sarah
    #bf_emma
    #bf_isabella
    #af_sky

    pipeline = KPipeline(lang_code='a') # <= make sure lang_code matches voice

    # This text is for demonstration purposes only, unseen during training
    text = '''
    <insert text here>

    '''
    # text = '「もしおれがただ偶然、そしてこうしようというつもりでなくここに立っているのなら、ちょっとばかり絶望するところだな」と、そんなことが彼の頭に思い浮かんだ。'
    # text = '中國人民不信邪也不怕邪，不惹事也不怕事，任何外國不要指望我們會拿自己的核心利益做交易，不要指望我們會吞下損害我國主權、安全、發展利益的苦果！'
    # text = 'Los partidos políticos tradicionales compiten con los populismos y los movimientos asamblearios.'
    # text = 'Le dromadaire resplendissant déambulait tranquillement dans les méandres en mastiquant de petites feuilles vernissées.'
    # text = 'ट्रांसपोर्टरों की हड़ताल लगातार पांचवें दिन जारी, दिसंबर से इलेक्ट्रॉनिक टोल कलेक्शनल सिस्टम'
    # text = "Allora cominciava l'insonnia, o un dormiveglia peggiore dell'insonnia, che talvolta assumeva i caratteri dell'incubo."
    # text = 'Elabora relatórios de acompanhamento cronológico para as diferentes unidades do Departamento que propõem contratos.'

    # 4️⃣ Generate, display, and save audio files in a loop.
    generator = pipeline(
        text, voice='af_bella', # <= change voice here
        speed=1, split_pattern=r'\n+'
    )
    arr = []
    for i, (gs, ps, audio) in enumerate(generator):
        print(i)  # i => index
        print(gs) # gs => graphemes/text
        print(ps) # ps => phonemes
        arr.append(audio)
        # sd.wait()# wait for audio to finish
        # sd.play(audio, 24000) 
        # sf.write(f'{i}.wav', audio, 24000) # save each audio file

    for i in arr:
        sd.play(i, 24000)
        sd.wait()# wait for audio to finish
        # sd.play(audio, 24000) 
        # sf.write(f'{i}.wav', audio, 24000) # save each audio file