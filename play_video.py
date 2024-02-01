import cv2
import tkinter as tk


class PlayVideo:
    def __init__(self):
        self.file_path = ''
        self.cap = None

    def get_file_path(self):
        return self.file_path

    def set_file_path(self, file_path):
        self.file_path = file_path

    def play(self):
        root = tk.Tk()  # Crie a instância Tk aqui
        if self.file_path:
            self.cap = cv2.VideoCapture(self.file_path)

            if not self.cap.isOpened():
                print("Erro ao abrir o arquivo de vídeo.")
                return

            # Obtém a largura e altura do quadro do vídeo
            frame_width = int(self.cap.get(3))
            frame_height = int(self.cap.get(4))

            # Obtém a resolução da tela usando tkinter
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()

            # Calcula a proporção para redimensionar o vídeo
            width_ratio = screen_width / frame_width
            height_ratio = screen_height / frame_height
            ratio = min(width_ratio, height_ratio)

            # Redimensiona o vídeo
            new_width = int(frame_width * ratio)
            new_height = int(frame_height * ratio)

            while True:
                ret, frame = self.cap.read()

                if not ret:
                    # print("Falha ao obter o próximo quadro.")
                    break

                # Redimensiona o quadro para as novas dimensões
                resized_frame = cv2.resize(frame, (new_width, new_height))

                # Obtém as dimensões da tela novamente em caso de alteração durante a execução
                screen_width = root.winfo_screenwidth()
                screen_height = root.winfo_screenheight()

                # Calcula a posição central para centralizar o vídeo na tela
                x_offset = (screen_width - new_width) // 2
                y_offset = (screen_height - new_height) // 2

                # Cria uma janela com um nome específico
                cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

                # Move a janela para a posição central
                cv2.moveWindow('Video', x_offset, y_offset)

                # Define as dimensões da janela
                cv2.resizeWindow('Video', new_width, new_height)

                cv2.imshow('Video', resized_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            self.stop()

    def stop(self):
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()


if __name__ == '__main__':
    video = PlayVideo()
    video.file_path = r'C:\Users\assis\Downloads\Nova pasta\v.mp4'
    video.play()
