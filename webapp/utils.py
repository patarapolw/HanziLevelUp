import subprocess


def do_speak(sentence, speaker='ting-ting'):
    return subprocess.Popen(['say', '-v', speaker, sentence])
