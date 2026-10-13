import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

kivy.require('2.3.0')

# Set a background color for the window, suitable for a dark theme.
Window.clearcolor = (0.15, 0.15, 0.15, 1)

class CalculatorLayout(BoxLayout):
    """
    The root widget for the calculator. Its layout is defined in calculator.kv.
    This class contains the logic for the calculator's operations.
    """
    expression = ""

    def button_pressed(self, button):
        """
        Called when a number or operator button is pressed.
        Appends the button's text to the current expression.
        Adds some basic validation to prevent invalid expressions.
        """
        # Prevent starting with most operators
        if not self.expression and button.text in "*/+":
            return
            
        # Prevent multiple operators or decimals in a row
        if self.expression and self.expression and self.expression[-1] in "+-*/." and button.text in "+-*/.":
            return

        self.expression += str(button.text)
        self.update_display()

    def calculate(self):
        """
        Called when the '=' button is pressed.
        Evaluates the expression and updates the display with the result.
        """
        if not self.expression:
            return

        try:
            # Strip any trailing operators before evaluating to prevent errors
            safe_expression = self.expression.rstrip('+-*/.')
            if not safe_expression:
                self.clear_all()
                return

            result = str(eval(safe_expression))
            # Use scientific notation for very long numbers to prevent display overflow
            if len(result) > 15:
                result = f"{float(result):.9e}"
            self.expression = result
        except Exception:
            result = "Error"
            self.expression = ""

        self.ids.display.text = result

    def clear_all(self):
        """
        Called when the 'C' button is pressed.
        Clears the entire expression and resets the display.
        """
        self.expression = ""
        self.update_display()

    def backspace(self):
        """
        Called when the 'CE' (Clear Entry/Backspace) button is pressed.
        Removes the last character from the expression.
        """
        if self.expression:
            self.expression = self.expression[:-1]
        self.update_display()

    def update_display(self):
        """
        Updates the text of the display label.
        Shows '0' if the expression is empty, otherwise shows the expression.
        """
        if self.expression:
            self.ids.display.text = self.expression
        else:
            self.ids.display.text = "0"


class CalculatorApp(App):
    """
    The main Kivy application class. The 'build' method returns the root widget.
    Kivy automatically loads the 'calculator.kv' file because its name matches the app class name.
    """
    def build(self):
        self.title = "Calculator"
        return CalculatorLayout()

if __name__ == "__main__":
    CalculatorApp().run()
