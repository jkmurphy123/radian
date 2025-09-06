import os
import sys
import json
import time
import glob
import itertools
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QScrollArea, QSizePolicy
)


CONFIG_FILE = "config.json"
LOGS_DIR = "logs"


class ChatBubble(QWidget):
    def __init__(self, speaker_name, text, avatar_path, color):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Avatar
        avatar_label = QLabel()
        pixmap = QPixmap(avatar_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        avatar_label.setPixmap(pixmap)
        avatar_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Text bubble
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                border-radius: 12px;
                padding: 8px;
                font-size: 14pt;
            }}
        """)
        bubble.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Speaker alignment (left/right)
        if hash(speaker_name) % 2 == 0:
            layout.addWidget(avatar_label)
            layout.addWidget(bubble)
        else:
            layout.addWidget(bubble)
            layout.addWidget(avatar_label)


class ChatWindow(QWidget):
    def __init__(self, config, logs):
        super().__init__()
        self.config = config
        self.logs = logs
        self.log_cycle = itertools.cycle(self.logs)  # loop forever
        self.current_messages = []
        self.current_log = None
        self.message_index = 0

        self.setWindowTitle("AI Chat Theater")
        self.resize(800, 600)

        # Scrollable area for chat
        self.chat_area = QVBoxLayout()
        scroll_content = QWidget()
        scroll_content.setLayout(self.chat_area)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

        # Timer for message playback
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_next_message)
        self.start_next_conversation()

    def keyPressEvent(self, event):
        """Stop on ESC key."""
        if event.key() == Qt.Key_Escape:
            QApplication.quit()

    def start_next_conversation(self):
        """Load next conversation log."""
        self.clear_chat()
        self.current_log = next(self.log_cycle)
        with open(self.current_log, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.current_messages = data["messages"]
        self.participants = {p["name"]: p for p in data["participants"]}
        self.message_index = 0
        self.timer.start(self.config["chat_delay_seconds"] * 1000)

    def clear_chat(self):
        """Clear chat bubbles from layout."""
        while self.chat_area.count():
            item = self.chat_area.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def show_next_message(self):
        if self.message_index < len(self.current_messages):
            msg = self.current_messages[self.message_index]
            p = self.participants[msg["speaker"]]
            bubble = ChatBubble(
                msg["speaker"],
                msg["text"],
                p["image"],
                p["color"]
            )
            self.chat_area.addWidget(bubble)
            self.message_index += 1
        else:
            # Conversation ended, start next after delay
            self.timer.stop()
            QTimer.singleShot(2000, self.start_next_conversation)  # 2 sec pause


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    config = load_config(CONFIG_FILE)
    logs = sorted(glob.glob(os.path.join(LOGS_DIR, "chat_*.json")))
    if not logs:
        print("❌ No chat logs found in logs/ folder.")
        sys.exit(1)

    app = QApplication(sys.argv)
    window = ChatWindow(config, logs)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
