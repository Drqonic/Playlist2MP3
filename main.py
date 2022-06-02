from pytube import Playlist
from pytube.exceptions import AgeRestrictedError

import os
import sys
import threading

THREAD_LIMIT = 20


def download_video(video):
	try:
		stream = video.streams.filter(only_audio=True).first()
		file_name = stream.download()
	except AgeRestrictedError:
		print(f"Title \"{video.title}\" cannot be downloaded as it is an age restricted video.")
	else:
		os.rename(file_name, file_name[:-4] + ".mp3")


def main():
	if len(sys.argv) < 2:
		sys.exit(f"Usage: {sys.argv[0]} <Playlist URL>")

 	playlist_url = sys.argv[1]

	playlist = Playlist(playlist_url)

	print(f"Number of videos in playlist: {len(playlist.video_urls)}")

	main_thread = threading.current_thread()

	for video in playlist.videos:
		threading.Thread(target=download_video, args=(video,)).start()

		if THREAD_LIMIT == threading.active_count()-1:
			for thread in threading.enumerate():
				if thread == main_thread:
					continue

				thread.join()


if __name__ == "__main__":
	main()
