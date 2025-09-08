import os
import re
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

def split_message_into_chunks(text, max_len=200):
    """Split long text into smaller chunks at sentence boundaries."""
    # First, split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks, current = [], ""

    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= max_len:
            current += (" " if current else "") + sentence
        else:
            if current:
                chunks.append(current.strip())
            current = sentence

    if current:
        chunks.append(current.strip())

    return chunks

class TypingIndicator(QLabel):
    def __init__(self, speaker_name):
        super().__init__(f"{speaker_name} is typing...")
        self.setStyleSheet("font-style: italic; color: gray; padding: 5px;")

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

    def _show_chunks_with_delay(self, speaker, participant, chunks, idx, first_in_turn=True):
        """Show typing indicator + balloon for each chunk with natural delays."""
        if idx < len(chunks):
            # Show typing indicator
            indicator = TypingIndicator(speaker)
            self.chat_area.addWidget(indicator)

            # Decide typing delay
            if first_in_turn:
                typing_delay = 3000  # 3 seconds for first message
            else:
                length = len(chunks[idx])
                if length < 80:
                    typing_delay = 5000   # short message ~5s
                elif length < 200:
                    typing_delay = 8000   # medium ~8s
                else:
                    typing_delay = 12000  # long ~12s

            def show_balloon():
                # Remove typing indicator
                self.chat_area.removeWidget(indicator)
                indicator.deleteLater()

                # Add actual balloon
                bubble = ChatBubble(
                    speaker,
                    chunks[idx],
                    participant["image"],
                    participant["color"]
                )
                self.chat_area.addWidget(bubble)

                # Schedule next chunk (if any)
                QTimer.singleShot(
                    typing_delay,
                    lambda: self._show_chunks_with_delay(speaker, participant, chunks, idx + 1, first_in_turn=False)
                )

            # Show balloon after typing delay
            QTimer.singleShot(typing_delay, show_balloon)


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

            # Split into chunks
            chunks = split_message_into_chunks(msg["text"], max_len=200)

            # Start chunk display with special first-turn delay
            self._show_chunks_with_delay(msg["speaker"], p, chunks, 0, first_in_turn=True)

            self.message_index += 1
        else:
            # End of conversation
            self.timer.stop()
            QTimer.singleShot(2000, self.start_next_conversation)


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
