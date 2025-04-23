from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QFont, QPainter, QColor, QPen
from PySide6.QtWidgets import QLabel, QCheckBox, QGraphicsOpacityEffect

class PvCheckbox(QCheckBox):
    def __init__(self, container, x=0, y=0, width=250, height=50, checkbox_size=30, padding=4,
                 checked_color=(76, 204, 76, 255), unchecked_color=(255, 255, 255, 255),
                 checkmark_color=(0, 0, 0, 255), checkmark_size=12, checkmark_type="✓",
                 border_color=(76, 76, 76, 255), border_thickness=1,
                 checkbox_border_color=(0, 0, 0, 255), checkbox_border_thickness=1,
                 is_checked=False, toggle_callback=None,
                 text="Option 1", text_position='right', text_alignment="left",
                 corner_radius=8, checkbox_corner_radius=0,
                 text_padding=5, spacing=10, font_name='Roboto',
                 font_color=(0, 0, 0, 255), font_size=14,
                 font_hover_color=None, bold=False, italic=False,
                 underline=False, strikeout=False,
                 is_visible=True, is_disabled=False, opacity=1, scale=1,
                 hover_color=None, clicked_color=None, idle_color=(255, 255, 255, 0),
                 border_hover_color=None, border_style="solid",
                 box_shadow=None, box_shadow_hover=None,
                 on_hover=None, on_click=None, on_release=None,
                 onChange=None, tag=None, variable_name=None, class_name="PvCheckbox",
                 z_index=0, id="", open_page=None, **kwargs):
        super().__init__(container)

        # ---------------------------------------------------------
        # Geometry and Basic Settings
        # ---------------------------------------------------------
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._checkbox_size = checkbox_size
        self._padding = padding
        self._spacing = spacing
        self._is_visible = is_visible
        self._is_disabled = is_disabled
        self._opacity = opacity
        self._scale = scale
        self._corner_radius = corner_radius
        self._checkbox_corner_radius = checkbox_corner_radius
        self._text_label = None
        self._hovered = False
        self._pressed = False

        # ---------------------------------------------------------
        # Checkbox State and Colors
        # ---------------------------------------------------------
        self._checked_color = QColor(
            checked_color[0],
            checked_color[1],
            checked_color[2],
            int(checked_color[3] * 255)
        )
        self._unchecked_color = QColor(
            unchecked_color[0],
            unchecked_color[1],
            unchecked_color[2],
            int(unchecked_color[3] * 255)
        )
        self._checkmark_size = checkmark_size
        self._checkmark_type = checkmark_type
        self._border_color = QColor(
            border_color[0],
            border_color[1],
            border_color[2],
            int(border_color[3] * 255)
        ) if border_color is not None else None
        self._original_border_color = border_color if border_color else (0, 0, 0, 0)
        self._border_thickness = border_thickness
        self._checkbox_border_color = QColor(
            checkbox_border_color[0],
            checkbox_border_color[1],
            checkbox_border_color[2],
            int(checkbox_border_color[3] * 255)
        ) if checkbox_border_color else None
        self._checkmark_color = QColor(
            checkmark_color[0],
            checkmark_color[1],
            checkmark_color[2],
            int(checkmark_color[3] * 255)
        ) if checkmark_color else QColor(0, 0, 0, 255)  # Default black

        # Store original checkbox border color for hover effects
        self._original_checkbox_border_color = self._checkbox_border_color

        self._checkbox_border_thickness = checkbox_border_thickness
        self._border_style = border_style
        self._border_hover_color = QColor(
            border_hover_color[0],
            border_hover_color[1],
            border_hover_color[2],
            int(border_hover_color[3] * 255)
        ) if border_hover_color is not None else None
        self._is_checked = is_checked

        # Background colors
        self._hover_color = QColor(
            hover_color[0],
            hover_color[1],
            hover_color[2],
            int(hover_color[3] * 255)
        ) if hover_color is not None else None
        self._clicked_color = QColor(
            clicked_color[0],
            clicked_color[1],
            clicked_color[2],
            int(clicked_color[3] * 255)
        ) if clicked_color is not None else None
        self._idle_color = QColor(
            idle_color[0],
            idle_color[1],
            idle_color[2],
            int(idle_color[3] * 255)
        ) if idle_color is not None else None
        self._current_bg_color = self._idle_color

        # Shadow effects
        self._box_shadow = box_shadow
        self._box_shadow_hover = box_shadow_hover

        # ---------------------------------------------------------
        # Text and Font Properties
        # ---------------------------------------------------------
        self._text = text
        self._text_position = text_position
        self._text_alignment = text_alignment
        self._text_padding = text_padding
        self._font_name = font_name
        self._font_color = QColor(
            font_color[0],
            font_color[1],
            font_color[2],
            int(font_color[3] * 255)
        )
        self._font_hover_color = QColor(
            font_hover_color[0],
            font_hover_color[1],
            font_hover_color[2],
            int(font_hover_color[3] * 255)
        ) if font_hover_color else QColor(
            font_color[0],
            font_color[1],
            font_color[2],
            int(font_color[3] * 255)
        )
        self._font_size = font_size
        self._bold = bold
        self._italic = italic
        self._underline = underline
        self._strikeout = strikeout

        # ---------------------------------------------------------
        # Callbacks and custom properties
        # ---------------------------------------------------------
        self._toggle_callback = toggle_callback
        self._on_hover = on_hover
        self._on_click = on_click
        self._on_release = on_release
        self._on_change = onChange
        self._tag = tag
        self._variable_name = variable_name
        self._class_name = class_name
        self._z_index = z_index
        self._id = id
        self._open_page = open_page

        # ---------------------------------------------------------
        # Initial Setup
        # ---------------------------------------------------------
        self.setDisabled(self._is_disabled)
        self.configure_style()
        self.setup_connections()
        super().setGeometry(x, y, width, height)

    # ---------------------------------------------------------
    # Create Layout
    # ---------------------------------------------------------

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setOpacity(self._opacity)

        # Get widget dimensions
        widget_height = super().height()
        widget_width = super().width()

        # Draw background (outside area)
        if self._current_bg_color and self._current_bg_color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._current_bg_color)
            painter.drawRoundedRect(0, 0, widget_width, widget_height,
                                    self._corner_radius, self._corner_radius)

        # Checkbox position (centered vertically)
        checkbox_y = (widget_height - self._checkbox_size) // 2
        checkbox_x = self._padding

        # Draw checkbox background (checked or unchecked)
        bg_color = self._checked_color if self.isChecked() else self._unchecked_color
        inner_padding = self._checkbox_border_thickness
        painter.setPen(Qt.NoPen)
        painter.setBrush(bg_color)
        painter.drawRoundedRect(checkbox_x + inner_padding, checkbox_y + inner_padding,
                                self._checkbox_size - 2 * inner_padding, self._checkbox_size - 2 * inner_padding,
                                self._checkbox_corner_radius, self._checkbox_corner_radius)

        # Draw outer border (around the whole widget)
        if self._border_color and self._border_thickness > 0:
            pen = QPen(self._border_color, self._border_thickness)
            if self._border_style == "dashed":
                pen.setStyle(Qt.DashLine)
            elif self._border_style == "dotted":
                pen.setStyle(Qt.DotLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(0, 0, widget_width, widget_height,
                                    self._corner_radius, self._corner_radius)

        # ✅ Draw checkbox border AFTER background
        if self._checkbox_border_color and self._checkbox_border_thickness > 0:
            pen = QPen(self._checkbox_border_color, self._checkbox_border_thickness)
            if self._border_style == "dashed":
                pen.setStyle(Qt.DashLine)
            elif self._border_style == "dotted":
                pen.setStyle(Qt.DotLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(
                checkbox_x, checkbox_y,
                self._checkbox_size, self._checkbox_size,
                self._checkbox_corner_radius,
                self._checkbox_corner_radius
            )

        # Draw checkmark if checked
        if self.isChecked():
            painter.setPen(QPen(self._checkmark_color, 2))
            font = QFont(self._font_name)
            font.setPixelSize(self._checkmark_size)
            painter.setFont(font)

            checkmark_rect = QRect(
                checkbox_x + (self._checkbox_size - self._checkmark_size) // 2,
                checkbox_y + (self._checkbox_size - self._checkmark_size) // 2,
                self._checkmark_size,
                self._checkmark_size
            )

            painter.drawText(checkmark_rect, Qt.AlignCenter, self._checkmark_type)

        painter.end()
        self._update_text_opacity()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self._is_disabled:
            # Toggle the checked state
            self.setChecked(not self.isChecked())

            # Update visual state
            if self._clicked_color:
                self._current_bg_color = self._clicked_color
                self.update()

            # Call callbacks
            if self._on_click:
                self._on_click(self)

            # Emit the signal manually since we're overriding
            self.stateChanged.emit(self.isChecked())

        super().mousePressEvent(event)

    # ---------------------------------------------------------
    # Configure Style
    # ---------------------------------------------------------

    def configure_style(self):
        """Initialize the checkbox UI components."""
        self.setStyleSheet("QCheckBox::indicator { width: 0; height: 0; }")
        super().setGeometry(self._x, self._y, self._width, self._height)
        self.setChecked(self._is_checked)
        self.setVisible(self._is_visible)

        # Initialize text label if text is provided
        if self._text:
            self._text_label = QLabel(self._text, self.parent())
            self._text_label.setVisible(self._is_visible)
            self._text_label.setCursor(Qt.PointingHandCursor)  # Add pointer cursor
            self._text_label.mousePressEvent = self._text_label_clicked  # Make text clickable

            if self._text_label.graphicsEffect() is None:
                self._text_label.setGraphicsEffect(QGraphicsOpacityEffect())

            self._apply_text_style(self._font_color)
            self._set_text_position()

    def _apply_text_style(self, color):
        """Apply all text styling properties to the label."""
        if hasattr(self, "_text_label"):
            font = QFont(self._font_name)
            font.setPixelSize(self._font_size)
            font.setBold(self._bold)
            font.setItalic(self._italic)
            font.setUnderline(self._underline)
            font.setStrikeOut(self._strikeout)
            self._text_label.setFont(font)

            self._text_label.setStyleSheet(
                f"color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()});"
                f"background-color: rgba({self._idle_color.red()}, {self._idle_color.green()}, "
                f"{self._idle_color.blue()}, {self._idle_color.alpha()});"
            )

            # Set text alignment
            alignment = Qt.AlignLeft
            if self._text_alignment == "center":
                alignment = Qt.AlignCenter
            elif self._text_alignment == "right":
                alignment = Qt.AlignRight
            self._text_label.setAlignment(alignment)

    def _get_checkmark_rect(self, x, y):
        """Calculate the rectangle for the checkmark based on size and position."""
        size = self._checkmark_size * 1.5  # Slightly larger area for the symbol
        return (x + (self._checkbox_size - size) // 2,
                y + (self._checkbox_size - size) // 2,
                size, size)

    def _update_text_opacity(self):
        """Update the text label's opacity."""
        if hasattr(self, "_text_label") and self._text_label is not None:
            effect = self._text_label.graphicsEffect()
            if effect is None:
                effect = QGraphicsOpacityEffect(self._text_label)
                self._text_label.setGraphicsEffect(effect)
            effect.setOpacity(self._opacity)

    # ---------------------------------------------------------
    # Event Handlers
    # ---------------------------------------------------------

    def setup_connections(self):
        self.stateChanged.connect(self._on_toggle)

    def mousePressEvent(self, event):
        self.setChecked(not self.isChecked())
        if event.button() == Qt.LeftButton and self._on_click:
            self._on_click(self)
        self.update()

    def enterEvent(self, event):
        self._hovered = True
        if not self._is_disabled:
            # Apply hover color overlay while preserving idle color
            if self._hover_color:
                # Create a composition of idle color and hover color
                hover_alpha = self._hover_color.alpha() / 255.0
                new_red = int(self._idle_color.red() * (1 - hover_alpha) + self._hover_color.red() * hover_alpha)
                new_green = int(self._idle_color.green() * (1 - hover_alpha) + self._hover_color.green() * hover_alpha)
                new_blue = int(self._idle_color.blue() * (1 - hover_alpha) + self._hover_color.blue() * hover_alpha)
                new_alpha = self._idle_color.alpha()  # Maintain original alpha
                self._current_bg_color = QColor(new_red, new_green, new_blue, new_alpha)
            else:
                self._current_bg_color = self._idle_color

            # Apply border hover color if specified
            if self._border_hover_color:
                self._border_color = self._border_hover_color

            # Apply text hover color if specified
            if self._text and hasattr(self, "_text_label"):
                if self._font_hover_color:
                    self._apply_text_style(self._font_hover_color)

            if self._on_hover:
                self._on_hover(self)

            self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        if not self._is_disabled:
            # Reset to idle state
            self._current_bg_color = self._idle_color
            if self._border_hover_color:
                self._border_color = QColor(*self._original_border_color)

            if self._text and hasattr(self, "_text_label"):
                self._apply_text_style(self._font_color)

            self.update()
        super().leaveEvent(event)

    def _on_toggle(self, state):
        self._is_checked = state == Qt.Checked
        self.update()
        if self._toggle_callback:
            self._toggle_callback(self)

    def _text_label_clicked(self, event):
        """Handle text label click event."""
        if event.button() == Qt.LeftButton and not self._is_disabled:
            # Toggle the checked state
            self.setChecked(not self.isChecked())

            # Update visual state
            if self._clicked_color:
                self._current_bg_color = self._clicked_color
                self.update()

            # Call callbacks
            if self._on_click:
                self._on_click(self)

            # Emit the signal manually since we're overriding
            self.stateChanged.emit(self.isChecked())

    def _set_text_position(self):
        if not hasattr(self, "_text_label"):
            return

        self._text_label.adjustSize()
        text_width = self._text_label.width()
        text_height = self._text_label.height()

        # Calculate the checkbox size including padding
        checkbox_size = self._checkbox_size + 2 * self._padding

        # Use the actual widget dimensions
        widget_height = super().height()
        widget_width = super().width()

        if self._text_position == 'left':
            self._text_label.setGeometry(
                self._x - text_width - self._text_padding,
                self._y + (widget_height - text_height) // 2,
                text_width,
                text_height
            )
        elif self._text_position == 'right':
            self._text_label.setGeometry(
                self._x + checkbox_size + self._text_padding + self._spacing,
                self._y + (widget_height - text_height) // 2,
                text_width,
                text_height
            )
        elif self._text_position == 'top':
            self._text_label.setGeometry(
                self._x + (widget_width - text_width) // 2,
                self._y - text_height - self._text_padding,
                text_width,
                text_height
            )
        elif self._text_position == 'bottom':
            self._text_label.setGeometry(
                self._x + (widget_width - text_width) // 2,
                self._y + widget_height + self._text_padding,
                text_width,
                text_height
            )

    # ---------------------------------------------------------
    # Property getters and setters
    # ---------------------------------------------------------

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self.setGeometry(self._x, self._y, self._width, self._height)
        if hasattr(self, "_text_label"):
            self._set_text_position()
        self.update()

    # In your property definitions, change:
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self.setGeometry(self._x, self._y, self._width, self._height)
        if hasattr(self, "_text_label"):
            self._set_text_position()
        self.update()

    @property
    def checkmark_color(self):
        return (
            self._checkmark_color.red(),
            self._checkmark_color.green(),
            self._checkmark_color.blue(),
            self._checkmark_color.alpha() / 255.0
        )

    @checkmark_color.setter
    def checkmark_color(self, value):
        self._checkmark_color = QColor(
            value[0],
            value[1],
            value[2],
            int(value[3] * 255)
        )
        self.update()

    @property
    def checkmark_size(self):
        return self._checkmark_size

    @checkmark_size.setter
    def checkmark_size(self, value):
        self._checkmark_size = value
        self.update()

    @property
    def is_disabled(self):
        return self._is_disabled

    @is_disabled.setter
    def is_disabled(self, value):
        self._is_disabled = value
        self.setDisabled(value)
        self.update()

    @property
    def hover_color(self):
        if self._hover_color:
            return (
                self._hover_color.red(),
                self._hover_color.green(),
                self._hover_color.blue(),
                self._hover_color.alpha() / 255.0
            )
        return None

    @hover_color.setter
    def hover_color(self, value):
        self._hover_color = QColor(
            value[0],
            value[1],
            value[2],
            int(value[3] * 255)
        ) if value else None
        self.update()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.setGeometry(self._x, self._y,
                         self._checkbox_size + self._padding * 2,
                         self._checkbox_size + self._padding * 2)
        if hasattr(self, "_text_label"):
            self._set_text_position()
        self.update()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.setGeometry(self._x, self._y,
                         self._checkbox_size + self._padding * 2,
                         self._checkbox_size + self._padding * 2)
        if hasattr(self, "_text_label"):
            self._set_text_position()
        self.update()

    @property
    def checkbox_size(self):
        return self._checkbox_size

    @checkbox_size.setter
    def checkbox_size(self, value):
        self._checkbox_size = value
        self.setGeometry(self._x, self._y,
                         self._checkbox_size + self._padding * 2,
                         self._checkbox_size + self._padding * 2)
        if hasattr(self, "_text_label"):
            self._set_text_position()
        self.update()

    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, value):
        self._padding = value
        self.setGeometry(self._x, self._y,
                         self._checkbox_size + self._padding * 2,
                         self._checkbox_size + self._padding * 2)
        if hasattr(self, "_text_label"):
            self._set_text_position()
        self.update()

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        """Set opacity for both checkbox and text label."""
        self._opacity = max(0.0, min(1.0, value))

        # Update checkbox opacity through painter in paintEvent
        self.update()

        # Update text label opacity if it exists
        if hasattr(self, "_text_label") and self._text_label:
            effect = self._text_label.graphicsEffect()
            if effect is None:
                effect = QGraphicsOpacityEffect(self._text_label)
                self._text_label.setGraphicsEffect(effect)
            effect.setOpacity(self._opacity)

    @property
    def is_visible(self):
        return self._is_visible

    @is_visible.setter
    def is_visible(self, value):
        """Set visibility for both checkbox and text label."""
        self._is_visible = value
        self.setVisible(value)

        if hasattr(self, "_text_label") and self._text_label:
            self._text_label.setVisible(value)

        self.update()

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value

    @property
    def on_hover(self):
        return self._on_hover

    @on_hover.setter
    def on_hover(self, callback):
        self._on_hover = callback

    @property
    def on_click(self):
        return self._on_click

    @on_click.setter
    def on_click(self, callback):
        self._on_click = callback

    @property
    def on_release(self):
        return self._on_release

    @on_release.setter
    def on_release(self, callback):
        self._on_release = callback

    @property
    def hovered(self):
        return self._hovered

    @property
    def checked_color(self):
        return (
            self._checked_color.red(),
            self._checked_color.green(),
            self._checked_color.blue(),
            self._checked_color.alpha() / 255.0
        )

    @checked_color.setter
    def checked_color(self, value):
        self._checked_color = QColor(
            value[0],
            value[1],
            value[2],
            int(value[3] * 255)
        )
        self.update()

    @property
    def unchecked_color(self):
        return (
            self._unchecked_color.red(),
            self._unchecked_color.green(),
            self._unchecked_color.blue(),
            self._unchecked_color.alpha() / 255.0
        )

    @unchecked_color.setter
    def unchecked_color(self, value):
        self._unchecked_color = QColor(
            value[0],
            value[1],
            value[2],
            int(value[3] * 255)
        )
        self.update()

    @property
    def border_color(self):
        if self._border_color:
            return (
                self._border_color.red(),
                self._border_color.green(),
                self._border_color.blue(),
                self._border_color.alpha() / 255.0
            )
        return None

    @border_color.setter
    def border_color(self, value):
        self._border_color = QColor(
            value[0],
            value[1],
            value[2],
            int(value[3] * 255)
        ) if value is not None else None
        self.update()

    @property
    def border_thickness(self):
        return self._border_thickness

    @border_thickness.setter
    def border_thickness(self, value):
        self._border_thickness = value
        self.update()

    @property
    def is_checked(self):
        return self._is_checked

    @is_checked.setter
    def is_checked(self, value):
        self._is_checked = value
        self.setChecked(value)
        self.update()

    @property
    def toggle_callback(self):
        return self._toggle_callback

    @toggle_callback.setter
    def toggle_callback(self, value):
        self._toggle_callback = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        if hasattr(self, "_text_label"):
            self._text_label.setText(value)
            self._set_text_position()
        else:
            self._text_label = QLabel(value, self.parent())
            self._apply_text_style(self._font_color)
            self._set_text_position()
        self.update()

    @property
    def text_position(self):
        return self._text_position

    @text_position.setter
    def text_position(self, value):
        self._text_position = value
        if hasattr(self, "_text_label"):
            self._set_text_position()
        self.update()

    @property
    def corner_radius(self):
        return self._corner_radius

    @corner_radius.setter
    def corner_radius(self, value):
        self._corner_radius = max(0, value)
        self.update()


    @property
    def checkbox_corner_radius(self):
        return self._checkbox_corner_radius

    @checkbox_corner_radius.setter
    def checkbox_corner_radius(self, value):
        self._checkbox_corner_radius = max(0, value)
        self.update()

    @property
    def text_padding(self):
        return self._text_padding

    @text_padding.setter
    def text_padding(self, value):
        self._text_padding = value
        if hasattr(self, "_text_label"):
            self._set_text_position()
        self.update()

    @property
    def font_name(self):
        return self._font_name

    @font_name.setter
    def font_name(self, value):
        self._font_name = value
        if hasattr(self, "_text_label"):
            self._apply_text_style(self._font_color)
        self.update()

    @property
    def font_color(self):
        return (
            self._font_color.red(),
            self._font_color.green(),
            self._font_color.blue(),
            self._font_color.alpha() / 255.0
        )

    @font_color.setter
    def font_color(self, value):
        self._font_color = QColor(
            value[0],
            value[1],
            value[2],
            int(value[3] * 255)
        )
        if hasattr(self, "_text_label"):
            self._apply_text_style(self._font_color)
        self.update()

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        self.font.setPixelSize(self._checkbox_size)
        self.setFont(self.font)
        self._adjust_height(self.text(), self.width(), self._paddings)
        if hasattr(self, "_text_label"):
            self._apply_text_style(self._font_color)
            self._set_text_position()
        self.update()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update()  # Trigger a redraw if needed

    @property
    def font_hover_color(self):
        if self._font_hover_color:
            return (
                self._font_hover_color.red(),
                self._font_hover_color.green(),
                self._font_hover_color.blue(),
                self._font_hover_color.alpha() / 255.0
            )
        return None

    @font_hover_color.setter
    def font_hover_color(self, value):
        self._font_hover_color = QColor(
            value[0],
            value[1],
            value[2],
            int(value[3] * 255)
        ) if value else None
        self.update()

    @property
    def checkmark_type(self):
        return self._checkmark_type

    @checkmark_type.setter
    def checkmark_type(self, value):
        self._checkmark_type = value
        self.update()  # Redraw the checkbox

    # Spacing
    @property
    def spacing(self):
        return self._spacing

    @spacing.setter
    def spacing(self, value):
        self._spacing = value
        self._set_text_position()
        self.update()

    # Border Hover Color
    @property
    def border_hover_color(self):
        if self._border_hover_color:
            return (
                self._border_hover_color.red(),
                self._border_hover_color.green(),
                self._border_hover_color.blue(),
                self._border_hover_color.alpha() / 255.0
            )
        return None

    @border_hover_color.setter
    def border_hover_color(self, value):
        self._border_hover_color = QColor(
            value[0],
            value[1],
            value[2],
            int(value[3] * 255)
        ) if value else None
        self.update()

    # Border Style
    @property
    def border_style(self):
        return self._border_style

    @border_style.setter
    def border_style(self, value):
        self._border_style = value
        self.update()

    # Checkbox Border Color
    @property
    def checkbox_border_color(self):
        if self._checkbox_border_color:
            return (
                self._checkbox_border_color.red(),
                self._checkbox_border_color.green(),
                self._checkbox_border_color.blue(),
                self._checkbox_border_color.alpha() / 255.0
            )
        return None

    @checkbox_border_color.setter
    def checkbox_border_color(self, value):
        self._checkbox_border_color = QColor(
            value[0],
            value[1],
            value[2],
            int(value[3] * 255)
        ) if value else None
        self.update()

    # Checkbox Border Thickness
    @property
    def checkbox_border_thickness(self):
        return self._checkbox_border_thickness

    @checkbox_border_thickness.setter
    def checkbox_border_thickness(self, value):
        self._checkbox_border_thickness = value
        self.update()

    # Clicked Color
    @property
    def clicked_color(self):
        if self._clicked_color:
            return (
                self._clicked_color.red(),
                self._clicked_color.green(),
                self._clicked_color.blue(),
                self._clicked_color.alpha() / 255.0
            )
        return None

    @clicked_color.setter
    def clicked_color(self, value):
        self._clicked_color = QColor(
            value[0],
            value[1],
            value[2],
            int(value[3] * 255)
        ) if value else None
        self.update()

    # Idle Color
    @property
    def idle_color(self):
        if self._idle_color:
            return (
                self._idle_color.red(),
                self._idle_color.green(),
                self._idle_color.blue(),
                self._idle_color.alpha() / 255.0
            )
        return None

    @idle_color.setter
    def idle_color(self, value):
        self._idle_color = QColor(
            value[0],
            value[1],
            value[2],
            int(value[3] * 255)
        ) if value else None
        self.update()

    # Text Alignment
    @property
    def text_alignment(self):
        return self._text_alignment

    @text_alignment.setter
    def text_alignment(self, value):
        self._text_alignment = value
        if hasattr(self, "_text_label"):
            self._apply_text_style(self._font_color)
        self.update()

    # Bold
    @property
    def bold(self):
        return self._bold

    @bold.setter
    def bold(self, value):
        self._bold = value
        if hasattr(self, "_text_label"):
            self._apply_text_style(self._font_color)
        self.update()

    # Italic
    @property
    def italic(self):
        return self._italic

    @italic.setter
    def italic(self, value):
        self._italic = value
        if hasattr(self, "_text_label"):
            self._apply_text_style(self._font_color)
        self.update()

    # Underline
    @property
    def underline(self):
        return self._underline

    @underline.setter
    def underline(self, value):
        self._underline = value
        if hasattr(self, "_text_label"):
            self._apply_text_style(self._font_color)
        self.update()

    # Strikeout
    @property
    def strikeout(self):
        return self._strikeout

    @strikeout.setter
    def strikeout(self, value):
        self._strikeout = value
        if hasattr(self, "_text_label"):
            self._apply_text_style(self._font_color)
        self.update()

    # On Change Callback
    @property
    def on_change(self):
        return self._on_change

    @on_change.setter
    def on_change(self, value):
        self._on_change = value

    # Variable Name
    @property
    def variable_name(self):
        return self._variable_name

    @variable_name.setter
    def variable_name(self, value):
        self._variable_name = value

    # Class Name
    @property
    def class_name(self):
        return self._class_name

    @class_name.setter
    def class_name(self, value):
        self._class_name = value

    # Z-Index
    @property
    def z_index(self):
        return self._z_index

    @z_index.setter
    def z_index(self, value):
        self._z_index = value
        if self.parent():
            self.parent().setZIndex(value)

    # ID
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def print_properties(self):
        """Print all current properties of the checkbox."""
        print(f"""
        PvCheckbox Properties:
        --------------------
        Position: ({self.x}, {self.y})
        Dimensions: {self.width}x{self.height}
        Size: {self.checkbox_size}
        Padding: {self.padding}
        Spacing: {self.spacing}
        Visibility: {self.is_visible}
        Disabled: {self.is_disabled}
        Opacity: {self.opacity}
        Scale: {self.scale}

        Checkbox Colors:
        - Checked: {self.checked_color}
        - Unchecked: {self.unchecked_color}
        - Checkmark: {self.checkmark_color}
        - Checkmark Size: {self.checkmark_size}
        - Checkmark Type: {self.checkmark_type}

        Borders:
        - Color: {self.border_color}
        - Thickness: {self.border_thickness}
        - Hover Color: {self.border_hover_color}
        - Style: {self.border_style}
        - Checkbox Border Color: {self.checkbox_border_color}
        - Checkbox Border Thickness: {self.checkbox_border_thickness}

        Background:
        - Hover: {self.hover_color}
        - Clicked: {self.clicked_color}
        - Idle: {self.idle_color}

        Text:
        - Content: {self.text}
        - Position: {self.text_position}
        - Alignment: {self.text_alignment}
        - Padding: {self.text_padding}
        - Font: {self.font_name}
        - Size: {self.font_size}
        - Color: {self.font_color}
        - Hover Color: {self.font_hover_color}
        - Bold: {self.bold}
        - Italic: {self.italic}
        - Underline: {self.underline}
        - Strikeout: {self.strikeout}

        State:
        - Checked: {self.is_checked}
        - Hovered: {self.hovered}
        - Pressed: {self._pressed}

        Callbacks:
        - Toggle: {self.toggle_callback is not None}
        - Hover: {self.on_hover is not None}
        - Click: {self.on_click is not None}
        - Release: {self.on_release is not None}
        - Change: {self.on_change is not None}

        Identifiers:
        - Tag: {self.tag}
        - Variable Name: {self.variable_name}
        - Class Name: {self.class_name}
        - Z-Index: {self.z_index}
        - ID: {self.id}
        """)


if __name__ == "__main__":
    import pyvisual as pv

    app = pv.PvApp()

    # Create a window
    window = pv.PvWindow(title="PvApp Example")

    Checkbox_1 = PvCheckbox(container=window, x=225, y=200, width=250,
                                          height=50, text='Accept our Terms',
                                          checked=False,
                                          checked_color=(239, 229, 229, 1),
                                          unchecked_color=(239, 229, 229, 1),
                                          checkmark_color=(20, 20, 23, 1),
                                          checkmark_size=10,
                                          checkbox_size=24,
                                          checkbox_corner_radius=25,
                                          checkmark_type='✓',
                                          checkbox_border_color=(0, 0, 0, 1),
                                          checkbox_border_thickness=1,
                                          font='assets/fonts/Poppins/Poppins.ttf', font_size=12,
                                          font_color=(101, 41, 41, 1), font_color_hover=None,
                                          bold=False, italic=False, underline=False, strikethrough=False,
                                          idle_color=(255, 255, 255, 1), hover_color=None, clicked_color=None,
                                          border_color=None,
                                          border_hover_color=None, border_thickness=10, corner_radius=10,
                                          border_style="solid",
                                          box_shadow=None, box_shadow_hover=None, paddings=(100, 0, 60, 50),
                                          is_visible=True,
                                          is_disabled=False, opacity=1, on_hover=None, on_click=None,
                                          on_release=None, tag=None)

    Checkbox_2 = PvCheckbox(container=window, x=144, y=100, width=260,
                                          height=50, text='Terms & conditions', checked=True,
                                          checked_color=(240, 103, 46, 1),
                                          unchecked_color=(255, 255, 255, 1),
                                          checkmark_color=(255, 255, 255, 1),
                                          checkmark_size=23, checkbox_size=25,
                                          checkbox_corner_radius=4, checkmark_type='✓',
                                          checkbox_border_color=(0, 0, 0, 1),
                                          checkbox_border_thickness=1,
                                          font='assets/fonts/Poppins/Poppins.ttf', font_size=18,
                                          font_color=(0, 0, 0, 1), font_color_hover=None,
                                          bold=False, italic=False, underline=False, strikethrough=False,
                                          idle_color=(255, 255, 255, 1), hover_color=None, clicked_color=None,
                                          border_color=(0,0,0,1),
                                          border_hover_color=None, border_thickness=2, corner_radius=10,
                                          border_style="solid",
                                          box_shadow=None, box_shadow_hover=None, paddings=(0, 0, 0, 50),
                                          is_visible=True,
                                          is_disabled=False, opacity=1, on_hover=None, on_click=None,
                                          on_release=None, tag=None)

    # checkbox.print_properties()

    # Show the window
    window.show()

    # Run the application
    app.run()
