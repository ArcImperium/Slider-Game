import random
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, QCheckBox
from PyQt5.QtCore import QTimer, Qt
import os
import sys

class UI(QWidget):
    def __init__(self, file_path=None):
        super().__init__()

        self.invert = False

        self.setWindowTitle('Slider Game')
        self.resize(400, 300)

        quit_button = QPushButton('Quit', self)
        quit_button.clicked.connect(self.quit_ui)

        self.file_button = QPushButton('Select Image')
        self.file_button.clicked.connect(self.open_file_explorer)

        self.full_image_label = QLabel('', self)
        self.full_image_label.setScaledContents(False)

        self.timer_label = QLabel('0.0')

        self.invert_checkbox = QCheckBox('Invert Controls')
        self.invert_checkbox.stateChanged.connect(self.invert_controls)

        self.layout = QVBoxLayout()
        self.layout.addWidget(quit_button)

        self.file_box = QHBoxLayout()
        self.file_box.addWidget(self.file_button)
        self.file_box.addWidget(self.invert_checkbox)
        self.layout.addLayout(self.file_box)

        self.image_clock = QHBoxLayout()
        self.image_clock.addWidget(self.full_image_label)
        self.image_clock.addWidget(self.timer_label)
        self.timer_label.hide()

        self.layout.addLayout(self.image_clock)
        self.setLayout(self.layout)

        self.setFocusPolicy(Qt.StrongFocus)

        if file_path:
            self.load_image(file_path)
            self.add_start(file_path)

    def keyPressEvent(self, event):
        if not getattr(self, 'running', False):
            return
        
        o_index = self.game_list.index(0)

        if event.key() == Qt.Key_Left or event.key() == Qt.Key_A:
            if self.invert == True:
                if o_index == 2 or o_index == 5 or o_index == 8:
                    return
                else:
                    self.game_list[o_index], self.game_list[o_index + 1] = self.game_list[o_index + 1], self.game_list[o_index]
            else:
                if o_index == 0 or o_index == 3 or o_index == 6:
                    return
                else:
                    self.game_list[o_index], self.game_list[o_index - 1] = self.game_list[o_index - 1], self.game_list[o_index]
        elif event.key() == Qt.Key_Up or event.key() == Qt.Key_W:
            if self.invert == True:
                if o_index == 6 or o_index == 7 or o_index == 8:
                    return
                else:
                    self.game_list[o_index], self.game_list[o_index + 3] = self.game_list[o_index + 3], self.game_list[o_index]
            else:
                if o_index == 0 or o_index == 1 or o_index == 2:
                    return
                else:
                    self.game_list[o_index], self.game_list[o_index - 3] = self.game_list[o_index - 3], self.game_list[o_index]
        elif event.key() == Qt.Key_Down or event.key() == Qt.Key_S:
            if self.invert == True:
                if o_index == 0 or o_index == 1 or o_index == 2:
                    return
                else:
                    self.game_list[o_index], self.game_list[o_index - 3] = self.game_list[o_index - 3], self.game_list[o_index]
            else:
                if o_index == 6 or o_index == 7 or o_index == 8:
                    return
                else:
                    self.game_list[o_index], self.game_list[o_index + 3] = self.game_list[o_index + 3], self.game_list[o_index]
        elif event.key() == Qt.Key_Right or event.key() == Qt.Key_D:
            if self.invert == True:
                if o_index == 0 or o_index == 3 or o_index == 6:
                    return
                else:
                    self.game_list[o_index], self.game_list[o_index - 1] = self.game_list[o_index - 1], self.game_list[o_index]
            else:
                if o_index == 2 or o_index == 5 or o_index == 8:
                    return
                else:
                    self.game_list[o_index], self.game_list[o_index + 1] = self.game_list[o_index + 1], self.game_list[o_index]

        self.reload_tiles()
        self.check_over()

    def invert_controls(self, state):
        if state == Qt.Checked:
            self.invert = True
        else:
            self.invert = False

    def open_file_explorer(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select File')
        if file_path:
            print("File: ", file_path)
            self.load_image(file_path)
            self.add_start(file_path)

    def quit_ui(self):
        sys.exit()

    def load_image(self, file_path):
        if file_path:
            full_image = QPixmap(file_path)
            self.full_image_label.setPixmap(full_image)
            self.timer_label.show()

    def add_start(self, file_path):
        if file_path:
            self.file_path = file_path
            self.output_dir = os.path.join(os.path.dirname(file_path), "tiles")
            os.makedirs(self.output_dir, exist_ok=True)

            self.start_button = QPushButton('Start')
            self.start_button.clicked.connect(self.start_game)
            self.layout.addWidget(self.start_button)

    def update_time(self):
        if self.running:
            self.counter += 1
            seconds = self.counter / 10
            self.timer_label.setText(f"{seconds:.1f}")

    def add_restart(self):
        if self.running:
            self.start_button.hide()
            self.restart_button = QPushButton('Restart')
            self.restart_button.clicked.connect(self.restart_game)
            self.layout.addWidget(self.restart_button)

    def restart_game(self):
        self.restart_button.hide()
        self.start_button.show()
        self.timer.stop()
        self.timer_label.setText('0.0')
        
        self.tile0_label.hide()
        self.tile1_label.hide()
        self.tile2_label.hide()
        self.tile3_label.hide()
        self.tile4_label.hide()
        self.tile5_label.hide()
        self.tile6_label.hide()
        self.tile7_label.hide()
        self.tile8_label.hide()

        self.image_clock.insertWidget(0, self.full_image_label)
        self.full_image_label.show()

    def start_game(self):
        self.counter = 0
        self.running = True

        self.clear_tiles()

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_time)
        self.timer.start()

        self.add_restart()

        self.split_image(self.file_path, self.output_dir)

        self.game_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(self.game_list)
        self.image_list = [os.path.join(self.output_dir, f'tile_{i}.png') for i in range(9)]
        self.reload_tiles()

        self.load_tiles(self.image_list, self.game_list)

        self.image_clock.addWidget(self.timer_label)

    def load_tiles(self, image_list, game_list):
        split_image_v = QVBoxLayout()

        split_image_h1 = QHBoxLayout()
        self.tile0_label = QLabel('')
        tile0 = QPixmap(image_list[game_list[0]])
        self.tile0_label.setPixmap(tile0)
        split_image_h1.addWidget(self.tile0_label)
        self.tile1_label = QLabel('')
        tile1 = QPixmap(image_list[game_list[1]])
        self.tile1_label.setPixmap(tile1)
        split_image_h1.addWidget(self.tile1_label)
        self.tile2_label = QLabel('')
        tile2 = QPixmap(image_list[game_list[2]])
        self.tile2_label.setPixmap(tile2)
        split_image_h1.addWidget(self.tile2_label)
        split_image_v.addLayout(split_image_h1)

        split_image_h2 = QHBoxLayout()
        self.tile3_label = QLabel('') 
        tile3 = QPixmap(image_list[game_list[3]])
        self.tile3_label.setPixmap(tile3)
        split_image_h2.addWidget(self.tile3_label)
        self.tile4_label = QLabel('')
        tile4 = QPixmap(image_list[game_list[4]])
        self.tile4_label.setPixmap(tile4)
        split_image_h2.addWidget(self.tile4_label)
        self.tile5_label = QLabel('')
        tile5 = QPixmap(image_list[game_list[5]])
        self.tile5_label.setPixmap(tile5)
        split_image_h2.addWidget(self.tile5_label)
        split_image_v.addLayout(split_image_h2)

        split_image_h3 = QHBoxLayout()
        self.tile6_label = QLabel('')
        tile6 = QPixmap(image_list[game_list[6]])
        self.tile6_label.setPixmap(tile6)
        split_image_h3.addWidget(self.tile6_label)
        self.tile7_label = QLabel('')
        tile7 = QPixmap(image_list[game_list[7]])
        self.tile7_label.setPixmap(tile7)
        split_image_h3.addWidget(self.tile7_label)
        self.tile8_label = QLabel('')
        tile8 = QPixmap(image_list[game_list[8]])
        self.tile8_label.setPixmap(tile8)
        split_image_h3.addWidget(self.tile8_label)
        split_image_v.addLayout(split_image_h3)

        self.image_clock.addLayout(split_image_v)

    def reload_tiles(self):
        if hasattr(self, 'tile0_label'):
            self.tile0_label.setPixmap(QPixmap(self.image_list[self.game_list[0]]))
            self.tile1_label.setPixmap(QPixmap(self.image_list[self.game_list[1]]))
            self.tile2_label.setPixmap(QPixmap(self.image_list[self.game_list[2]]))
            self.tile3_label.setPixmap(QPixmap(self.image_list[self.game_list[3]]))
            self.tile4_label.setPixmap(QPixmap(self.image_list[self.game_list[4]]))
            self.tile5_label.setPixmap(QPixmap(self.image_list[self.game_list[5]]))
            self.tile6_label.setPixmap(QPixmap(self.image_list[self.game_list[6]]))
            self.tile7_label.setPixmap(QPixmap(self.image_list[self.game_list[7]]))
            self.tile8_label.setPixmap(QPixmap(self.image_list[self.game_list[8]]))

    def clear_tiles(self):
        number = self.image_clock.count()
        for i in reversed(range(number)):
            item = self.image_clock.itemAt(i)
            the_widget = item.widget()
            the_layout = item.layout()
            if the_widget and the_widget != self.timer_label:
                self.image_clock.removeWidget(the_widget)
                the_widget.setParent(None)
            elif the_layout:
                self.image_clock.removeItem(the_layout)

    def split_image(self, file_path, output_dir):
        image = QImage(file_path)
        image_width = image.width()
        image_height = image.height()

        tile_width = image_width // 3
        tile_height = image_height // 3

        count = 0
        for row in range(3):
            for col in range(3):
                x = col * tile_width
                y = row * tile_height
                tile = image.copy(x, y, tile_width, tile_height)

                if count == 0:
                    blank_tile = QImage(tile_width, tile_height, QImage.Format_ARGB32)
                    blank_tile.fill(Qt.transparent)
                    blank_tile.save(os.path.join(output_dir, f'tile_0.png'))
                else:
                    tile.save(os.path.join(output_dir, f'tile_{count}.png'))
                
                count += 1

    def check_over(self):
        self.check_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        if self.check_list == self.game_list:
            self.running = False
            self.timer.stop()
        else:
            pass

if __name__ == '__main__':
    ui = QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(ui.exec_())
