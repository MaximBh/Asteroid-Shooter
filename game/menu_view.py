import arcade


# Начальный экран
class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        self.title_text = arcade.Text(
            "ASTEROID SHOOTER",
            self.window.width // 2,
            self.window.height // 2 + 60,
            arcade.color.WHITE,
            48,
            anchor_x="center",
            anchor_y="center"
        )

        self.start_text = arcade.Text(
            "Press ENTER to start",
            self.window.width // 2,
            self.window.height // 2 - 20,
            arcade.color.WHITE,
            24,
            anchor_x="center",
            anchor_y="center"
        )

    def on_draw(self):
        self.clear()
        self.title_text.draw()
        self.start_text.draw()

    # Запуск игры
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            from game.game_view import GameView
            self.window.show_view(GameView())
