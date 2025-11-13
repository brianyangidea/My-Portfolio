import vlc
import time

def play_mp3(file_path, volume=100):
    """
    Plays an MP3 file in a non-blocking loop using VLC.
    
    Parameters:
        file_path (str): Path to the MP3 file
        volume (int): Volume (0–100)
    
    Returns:
        player (vlc.MediaPlayer): The VLC player object, so you can stop it later
    """
    # Create VLC instance
    instance = vlc.Instance("--input-repeat=-1")  # -1 = infinite loop
    player = instance.media_player_new()

    # Load file and set up
    media = instance.media_new(file_path)
    player.set_media(media)
    player.audio_set_volume(volume)

    # Play the music (non-blocking)
    player.play()

    print(f"🎶 Now looping '{file_path}' at volume {volume}% (non-blocking)")
    return player


# Example usage:
p = play_mp3("royalty_free_music/Palismanto_Title_Card.mp3", volume=80)
print("Your program continues running here.")
time.sleep(10)
p.stop()  # Stop the music when you’re done
