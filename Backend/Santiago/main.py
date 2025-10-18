import server, stt, os

FILE_PATH_TO_UPLOAD = r"C:\Users\santi\PycharmProjects\deep\hackathon\output_audio.wav"

FILENAME_TO_DOWNLOAD = os.path.basename(FILE_PATH_TO_UPLOAD)
DOWNLOAD_SAVE_PATH = r"C:\Users\santi\PycharmProjects\deep\hackathon\output_audio_descargado.wav"


def main():
    server.download_file(FILENAME_TO_DOWNLOAD, DOWNLOAD_SAVE_PATH)
    response = stt.translate(DOWNLOAD_SAVE_PATH)


if __name__ == "__main__":
    main()


