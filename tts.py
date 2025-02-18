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
        
    def play_audio_stream(self, text_stream, voice_num=1):
        text_buffer = ""
        response = ""
        for text_chunk in text_stream:
            text_buffer += text_chunk
            
            if any(punct in text_buffer for punct in '.!?') or len(text_buffer) > 100:
                response += text_buffer
                generator = self.pipeline(
                    text_buffer,
                    voice=self.v[voice_num],
                    speed=1,
                    split_pattern=r'[.!?]\s+'  
                )
                
                for i, (gs, ps, audio) in enumerate(generator):
                    print(f"Playing segment {i}: {gs}")

                    sd.play(audio, 24000)
                    sd.wait()
                
                text_buffer = ""  
        
        # Process any remaining text in the buffer
        if text_buffer.strip():
            generator = self.pipeline(
                text_buffer,
                voice=self.v[voice_num],
                speed=1,
                split_pattern=r'[.!?]\s+'
            )
            
            for i, (gs, ps, audio) in enumerate(generator):
                print(f"Playing segment {i}: {gs}")
                sd.play(audio, 24000)
                sd.wait()

        return response
