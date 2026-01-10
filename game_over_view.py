import arcade


# Конечный экран
class GameOverView(arcade.View):
    def __init__(self, score, high_score):
        super().__init__()
        self.score = score
        self.high_score = high_score

        # Вывод текста
        self.game_over_text = arcade.Text(
            "GAME OVER",
            self.window.width // 2,
            self.window.height // 2 + 80,
            arcade.color.WHITE,
            44,
            anchor_x="center",
            anchor_y="center"
        )

        self.score_text = arcade.Text(
            f"Score: {self.score}  High Score: {self.high_score}",
            self.window.width // 2,
            self.window.height // 2,
            arcade.color.WHITE,
            26,
            anchor_x="center",
            anchor_y="center",
            align="center"
        )

        self.restart_text = arcade.Text(
            "Press ENTER to return to menu",
            self.window.width // 2,
            self.window.height // 2 - 100,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            anchor_y="center"
        )

    def on_draw(self):
        self.clear()
        self.game_over_text.draw()
        self.score_text.draw()
        self.restart_text.draw()

    # Для возврата в меню
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            from game.menu_view import MenuView
            self.window.show_view(MenuView())
