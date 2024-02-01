import pytube
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from youtube_interface_download_ui import Ui_MainWindow
import os
from play_video import PlayVideo
import json


class UIInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.media = PlayVideo()
        self.url = ''
        self.destino = r'C:\Users\assis\Downloads'
        self.caminho_completo = ''
        self.yt = None
        self.info_video = {}
        self.progresso = 0
        self.janelas_reproducao = []
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.progresso.hide()
        self.ui.pushButton.hide()
        self.ui.progresso.setValue(0)
        self.ui.input_url.returnPressed.connect(self.acessar_video)
        self.ui.pushButton.clicked.connect(self.fechar_video)

    def fechar_video(self):
        self.media.stop()
        self.ui.pushButton.hide()

    def acompanhar_progresso(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        self.progresso = (bytes_downloaded / total_size) * 100
        self.ui.progresso.setValue(int(self.progresso))
        QApplication.processEvents()  # Permitir atualização da interface

    def resetar_progresso(self):
        self.ui.progresso.hide()
        self.ui.progresso.setValue(0)

    def ocultar_revelar_progresso(self, mostrar=True):
        if mostrar:
            self.ui.progresso.show()
        else:
            self.ui.progresso.hide()

    def download_video(self):
        try:
            stream = self.yt.streams.get_highest_resolution()
            stream_video = stream.download(output_path=self.destino)
            self.caminho_completo = os.path.join(self.destino, os.path.basename(stream_video))
            # QMessageBox.information(self, 'Download Concluído', 'Download concluído!')
        except Exception as e:
            # QMessageBox.warning(self, 'Erro', f'Erro ao baixar o vídeo: {e}')
            pass

    def acessar_video(self):
        self.url = self.ui.input_url.text()
        if self.url:
            self.ocultar_revelar_progresso()
            self.ui.input_url.hide()

            try:
                print(self.url)
                self.yt = pytube.YouTube(self.url, on_progress_callback=self.acompanhar_progresso)
                print('Carregar dados...')
                self.carregar_dados()
                print('Exibir informações...')
                self.exibir_info()
                print('Download vídeo...')
                self.download_video()
                self.resetar_progresso()
                self.ui.input_url.clear()
            except Exception as e:
                QMessageBox.warning(self, 'Erro', f'Erro ao acessar o vídeo: {e}')

            self.ui.input_url.show()
            self.ocultar_revelar_progresso(False)
            if self.caminho_completo:
                print(self.caminho_completo)
                self.media.file_path = self.caminho_completo
                self.ui.pushButton.show()
                self.media.play()

    # def reproduzir_video(self):
    #     if self.file_name:
    #         janela = VideoPlayerApp(self.file_name)
    #         self.janelas_reproducao.append(janela)
    #         janela.show()

    def carregar_dados(self):
        if self.yt:
            self.info_video = {
                "age_restricted": self.yt.age_restricted,
                "author": self.yt.author,
                "channel_id": self.yt.channel_id,
                "check_availability": self.yt.check_availability(),
                "description": self.yt.description,
                "keywords": self.yt.keywords,
                "length": self.yt.length,
                "publish_date": self.yt.publish_date,
                "rating": self.yt.rating,
                "thumbnail_url": self.yt.thumbnail_url,
                "title": self.yt.title,
                "video_id": self.yt.video_id,
                "views": self.yt.views,
            }

            for k, v in self.info_video.items():
                print(f'{k}:  {v}')

            # text = self.ui.input_url.text()
            # with open('dados_videos.json', 'r', encoding='utf-8') as file:
            #     read = json.loads(file.read())
            #
            # read.setdefault(text[text.find('=')+1:], self.info_video)
            #
            # with open(f'dados_videos.json', 'w', encoding='utf-8') as f:
            #     json.dump(read, f, ensure_ascii=False, indent=4)

    @staticmethod
    def formatar_tamanho_gigabytes(tamanho_bytes):
        tamanho_gb = tamanho_bytes / (1024 ** 3)
        return f'{tamanho_gb:.2f} GB'

    def exibir_info(self):
        self.ui.autor_video.setText(f'Autor do vídeo: {self.info_video["author"]}')
        self.ui.titulo_video.setText(f'Título do Vídeo: {self.info_video["title"]}')
        self.ui.descricao_video.setText(f'Descrição do Vídeo: {self.info_video["description"]}')
        self.ui.duracao.setText(f'Duração do Vídeo: {self.info_video["length"]}')
        self.ui.total_likes.setText(f'Total de Likes: {self.info_video["rating"]}')
        self.ui.visualizacoes.setText(f'Total de Visualizações: {self.info_video["views"]}')
        self.ui.thumbnail.setText(f'Thumbnail: {self.info_video["thumbnail_url"]}')
        self.ui.gigabybes.setText(f'Tamanho em gigabytes: {self.formatar_tamanho_gigabytes(self.yt.streams.get_highest_resolution().filesize)}')
        self.ui.restricao_idade.setText(f'Restrição por idade: {self.info_video["age_restricted"]}')
        self.ui.data_publicacao.setText(f'Data de Publicação: {self.info_video["publish_date"]}')
        self.ui.palavras_chaves.setText(f'Palavras-chave: {", ".join(self.info_video["keywords"])}')
        self.ui.disponivel.setText(f'Vídeo Disponível: {self.info_video["check_availability"]}')
        self.ui.id_video.setText(f'ID do Vídeo: {self.info_video["video_id"]}')
        self.ui.id_canal.setText(f'ID do Canal: {self.info_video["channel_id"]}')


def main():
    app = QApplication([])
    window = UIInterface()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
