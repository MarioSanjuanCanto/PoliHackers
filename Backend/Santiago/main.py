import server, stt, os, n8n_connector, ALIA


FILE_PATH_TO_UPLOAD = r"C:\Users\santi\PycharmProjects\deep\PoliHackers\Backend\Santiago\output_audio.wav"

FILENAME_TO_DOWNLOAD = os.path.basename(FILE_PATH_TO_UPLOAD)
DOWNLOAD_SAVE_PATH = r"C:\Users\santi\PycharmProjects\deep\PoliHackers\Backend\Santiago\download_audio.wav"


def main():
    server.upload_audio(FILE_PATH_TO_UPLOAD)
    server.download_file(FILENAME_TO_DOWNLOAD, DOWNLOAD_SAVE_PATH)
    response = stt.sptotext(DOWNLOAD_SAVE_PATH)
    translation = ALIA.translate(response)
    n8n_connector.request_models(response)
    print(translation)


if __name__ == "__main__":
    main()


