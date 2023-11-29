def locate_and_splice(
        audio_directory: str,
        context_target: list[str],
        json_transcript: str): #-> tuple[dict, str]:

    sentences = pf.load_json(json_transcript)
    target_con = [pf.rm_nonlexical_items(sent) for sent in context_target]
    audio_len = pf.return_audio_len(audio_directory) # Duration in seconds
    new_audio_name = audio_directory

    "Splice audio"
    while audio_len > 300:
        context_loc = lf.localize_context(sentences, target_con)  # Find where in the text the sentence could be
        audio_segment = pf.splice_audio(new_audio_name, audio_len, context_loc)  # Splice audio
        new_audio_name, _ = io.write_audio(audio_segment, new_audio_name, "segment")  # Put into audio directory
        audio_len = pf.return_audio_len(new_audio_name) # Check the length new audio file
        print(audio_len)

    whisper_transcript = wh_model.transcribe(new_audio_name)  # Get transcript

    return whisper_transcript, new_audio_name