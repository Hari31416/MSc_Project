import vlc
import time
import os

# from pygame import mixer
import os
from twilio.rest import Client
from decouple import config
import datetime

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"


class Notification:
    """
    A class which deals with notifications.

    Parameters
    ----------
    filepath : str
        The path of the song to be played.

    Methods
    -------
    play_n_stop(max_time=None)
        This function plays a song using vlc.

    change_filepath(filepath)
        This function changes the filepath of the song to be played.

    play_pygame(max_time=None)
        This function plays a song using pygame.

    play_vlc(max_time=None)
        This function plays a song using vlc.

    send_text(message, media=None)
        This function sends a text message.

    init_whatsapp_text()
        If the function `send_whatsapp_text` does not work, this\\
        function can be used to initialize Whatsapp sandbox by Twillio.

    send_whatsapp_text(message, media=None)
        This function sends a whatsapp text message.
    """

    def __init__(
        self, filepath=r"C:\Users\harik\Music\My Media\notification\the_tardis.mp3"
    ) -> None:
        self.filepath = filepath
        self.tools = ["vlc", "pygame"]
        return None

    def change_filepath(self, filepath):
        """
        Changes the filepath of the song to be played.

        Parameters
        ----------
        filepath : str
            The path of the song to be played.

        Returns
        -------
        None
        """
        self.filepath = filepath

    def play_vlc(self, max_time=None, file=None):
        """
        This function plays a song using vlc.

        Parameters
        ----------
        filepath : str
            The path of the song to be played.
        max_time : int, optional
            The maximum time in seconds to play the song. The default is None.

        Returns
        -------
        None
        """
        if file is not None:
            self.filepath = file
        p = vlc.MediaPlayer(self.filepath)
        p.play()
        if max_time:
            time.sleep(max_time)
            p.stop()

    def play_pygame(self, max_time=None, file=None):
        """
        This function plays a song using pygame.

        Parameters
        ----------
        filepath : str
            The path of the song to be played.
        max_time : int, optional
            The maximum time in seconds to play the song. The default is None.

        Returns
        -------
        None
        """
        from pygame import mixer

        if file is not None:
            self.filepath = file

        mixer.init()
        mixer.music.load(self.filepath)
        mixer.music.play()
        if max_time:
            time.sleep(max_time)
            mixer.music.stop()

    def play_n_stop(self, max_time=None, file=None, tool="vlc"):
        """
        This function plays a song using vlc or pygame.

        Parameters
        ----------
        filepath : str
            The path of the song to be played.
        max_time : int, optional
            The maximum time in seconds to play the song. The default is None.

        Returns
        -------
        None
        """
        if file is not None:
            self.filepath = file

        if tool == "vlc":
            self.play_vlc(max_time, file)
        elif tool == "pygame":
            self.play_pygame(max_time, file)
        else:
            print("Tool not found")
            print(f"Available options are: {', '.join(self.tools)}")

    def send_text(self, message, media=None):
        """
        This function sends a text message.

        Parameters
        ----------
        message : str
            The message to be sent.

        media : str, optional
            The media to be sent. The default is None.

        Returns
        -------
        None
        """
        account_sid = config("TWILIO_ACCOUNT_SID")
        auth_token = config("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=message, media_url=media, from_="+12183355935", to="+919838422934"
        )
        print(message.sid)

    def init_whatsapp_text(self):
        """
        If the function `send_whatsapp_text` does not work, this\\
        function can be used to initialize Whatsapp sandbox by Twillio.
        We need to send a reply to the message send by this function.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        account_sid = config("TWILIO_ACCOUNT_SID")
        auth_token = config("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_="whatsapp:+14155238886",
            body=f"Your WhatsApp appointment is coming up on {datetime.date.today().strftime('%d-%m-%Y')}",
            to="whatsapp:+919838422934",
        )
        print(message.sid)

    def send_whatsapp_text(self, message, media=None):
        """
        This function sends a text message.

        Parameters
        ----------
        message : str
            The message to be sent.

        media : str, optional
            The media to be sent. The default is None.

        Returns
        -------
        None
        """
        account_sid = config("TWILIO_ACCOUNT_SID")
        auth_token = config("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_="whatsapp:+14155238886",
            body=message,
            media_url=media,
            to="whatsapp:+919838422934",
        )
        print(message.sid)
