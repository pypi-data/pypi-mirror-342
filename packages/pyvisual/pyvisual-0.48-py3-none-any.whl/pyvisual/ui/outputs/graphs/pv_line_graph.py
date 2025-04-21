from pyvisual.ui.outputs.graphs.pv_base_graph import PvBaseGraph
import pyqtgraph as pg
import numpy as np
from PySide6.QtCore import Qt

class PvLineGraph(PvBaseGraph):
    """
    A specialized graph class for line plots, inheriting from PvBaseGraph.
    """
    
    def __init__(self, container, x=100, y=100, width=400, height=300, 
                 title="", x_label="", y_label="", 
                 idle_color=(255, 255, 255, 1), axis_color=(0, 0, 0, 1),
                 grid=True, grid_color=(200, 200, 200, 1), grid_alpha=0.5,
                 legend=False, crosshair=False, 
                 x_range=None, y_range=None, log_x=False, log_y=False,
                 anti_aliasing=True, border_thickness=0, border_color=None, corner_radius=20,
                 is_visible=True, opacity=1.0, tag=None, default_buffer_size=None,
                 is_dynamic=True, update_interval=16, dummy_data=True, **kwargs):
        """
        Initialize a line graph with all base graph parameters plus line-specific options.
        
        Args:
            container: Parent widget
            x, y: Position of the widget
            width, height: Size of the widget
            title: Graph title
            x_label, y_label: Axis labels
            idle_color: Graph background color as RGBA tuple
            axis_color: Color of the axes as RGBA tuple
            grid: Whether to show grid lines
            grid_color: Color of grid lines as RGBA tuple
            grid_alpha: Grid transparency (0-1)
            legend: Whether to show the legend
            crosshair: Whether to show a crosshair cursor
            x_range, y_range: Initial axis ranges as (min, max) tuples or None for auto
            log_x, log_y: Whether to use logarithmic scaling for axes
            anti_aliasing: Whether to use anti-aliasing for smoother lines
            border_thickness: Border thickness of the graph widget
            border_color: Border color as RGBA tuple (if None, a darker shade of background color is used)
            corner_radius: Corner radius of the graph widget
            is_visible: Whether the widget is initially visible
            opacity: Widget opacity (0-1)
            tag: Optional user-defined tag for identification
            default_buffer_size: Default size for line data buffers (if None, no buffering)
            is_dynamic: Whether to use a background thread for graph updates
            update_interval: Interval between graph updates in milliseconds
            dummy_data: Whether to add some test data automatically (for testing purposes)
        """
        super().__init__(
            container, x, y, width, height, title, x_label, y_label,
            idle_color, axis_color, grid, grid_color, grid_alpha,
            legend, crosshair, x_range, y_range, log_x, log_y,
            anti_aliasing, border_thickness, corner_radius, border_color, is_visible, opacity,
            tag, is_dynamic=is_dynamic, update_interval=update_interval, **kwargs
        )
        
        # List to store internal data buffers for each line
        self._data_buffers = []
        self._buffer_sizes = []
        self._auto_x = []
        
        # Track how many valid points are in each buffer
        self._data_lengths = []
        
        # Default buffer size for all lines
        self._default_buffer_size = default_buffer_size
        
        # Add dummy data if requested (for testing purposes only)
        if dummy_data:
            self._add_dummy_data()
    
    def _add_dummy_data(self):
        """
        Add dummy data to the graph for testing purposes.
        This method is only called if dummy_data=True in __init__.
        """
        # Add a sine wave similar to the user's example
        # Generate 50 data points with scaled sine wave (sin(i*0.1)*50 + 50)
        x1 = np.arange(50)
        y1 = np.sin(x1 * 0.1) * 50 + 50
        self.add_line(
            x=x1, 
            y=y1,
            width=3,
       

                fill_color = (36, 152,243, 0.1),
    color = (36, 152,243, 1),
       
        )
        
    
        
        # Force redraw to ensure data is visible
        self.redraw()
    
    def add_line(self, x=None, y=None, name=None, color=(0, 0, 255, 1), width=1, 
                style='solid', symbol=None, symbol_size=10, symbol_color=None, 
                buffer_size=None, fill_color=None, fill_level=0):
        """
        Add a line plot to the graph.
        
        Args:
            x: X-axis data (array-like)
            y: Y-axis data (array-like)
            name: Name of the line (for legend)
            color: Line color as RGBA tuple
            width: Line width
            style: Line style ('solid', 'dash', 'dot', 'dashdot')
            symbol: Symbol type (None, 'o', 's', 't', 'd', '+', 'x')
            symbol_size: Size of symbols
            symbol_color: Symbol color as RGBA tuple (defaults to line color)
            buffer_size: Size of internal buffer (if None, uses default_buffer_size)
            fill_color: Color for the area below the curve as RGBA tuple (if None, no fill)
            fill_level: The y-level at which to fill to (default is 0)
            
        Returns:
            Plot item for further customization
        """
        # Use the default buffer size if not specified
        if buffer_size is None:
            buffer_size = self._default_buffer_size
        
        # Create default y values if not provided
        if y is None:
            if buffer_size is not None:
                # If buffer_size is specified but no y data, create a single zero
                # (not a full buffer of zeros)
                y = np.array([0.0])
            else:
                print("Error: No Y data provided for line plot")
                return None
            
        # Create default x values if not provided
        if x is None:
            x = np.arange(len(y))
            auto_x = True
        else:
            auto_x = False
        
        # Ensure data is properly formatted
        try:
            x = np.array(x, dtype=float)
            y = np.array(y, dtype=float)
            
            # Check for invalid data
            if np.isnan(x).any() or np.isnan(y).any():
                print("Warning: Data contains NaN values, which may prevent display")
            
            if len(x) != len(y):
                print(f"Warning: X and Y arrays have different lengths! X: {len(x)}, Y: {len(y)}")
                # Use the minimum length
                min_len = min(len(x), len(y))
                x = x[:min_len]
                y = y[:min_len]
                
            if len(x) == 0 or len(y) == 0:
                print("Error: Empty data arrays provided")
                return None
                
        except Exception as e:
            print(f"Error converting data to numpy arrays: {e}")
            return None
        
        # Make sure color is valid
        if len(color) < 3:
            print(f"Warning: Invalid color format: {color}. Using default blue.")
            color = (0, 0, 255, 1)
        elif len(color) == 3:
            # Add alpha if not provided
            color = (*color, 1)
            
        # Convert RGBA to PyQtGraph format
        plot_color = tuple(c/255.0 for c in color[:3])
        plot_alpha = color[3]
        
        # Create pen for the line
        color_obj = pg.mkColor(int(color[0]), int(color[1]), int(color[2]), int(plot_alpha*255))
        
        line_style_map = {
            'solid': Qt.SolidLine,
            'dash': Qt.DashLine,
            'dot': Qt.DotLine,
            'dashdot': Qt.DashDotLine
        }
        
        pen = pg.mkPen(color=color_obj, 
                      width=width, 
                      style=line_style_map.get(style, Qt.SolidLine))
        
        # Symbol settings
        symbol_map = {
            'o': 'o',  # circle
            's': 's',  # square
            't': 't',  # triangle
            'd': 'd',  # diamond
            '+': '+',  # plus
            'x': 'x'   # x
        }
        
        sym = symbol_map.get(symbol, None)
        
        # Symbol color
        if symbol_color is None:
            symbol_brush = pg.mkBrush(color_obj)
        else:
            # Make sure symbol color is valid
            if len(symbol_color) < 3:
                print(f"Warning: Invalid symbol color format: {symbol_color}. Using line color.")
                symbol_color = color
            elif len(symbol_color) == 3:
                # Add alpha if not provided
                symbol_color = (*symbol_color, 1)
                
            sym_color_obj = pg.mkColor(int(symbol_color[0]), int(symbol_color[1]), 
                                       int(symbol_color[2]), int(symbol_color[3]*255))
            symbol_brush = pg.mkBrush(sym_color_obj)
        
        # Fill settings
        fill_brush = None
        if fill_color is not None:
            # Make sure fill color is valid
            if len(fill_color) < 3:
                print(f"Warning: Invalid fill color format: {fill_color}.")
                # Use line color with reduced alpha
                fill_color = (*color[:3], 0.3 if len(color) == 4 else color[3] * 0.3)
            elif len(fill_color) == 3:
                # Add alpha if not provided (use 30% opacity by default)
                fill_color = (*fill_color, 0.3)
                
            fill_color_obj = pg.mkColor(
                int(fill_color[0]), 
                int(fill_color[1]), 
                int(fill_color[2]), 
                int(fill_color[3] * 255)
            )
            fill_brush = pg.mkBrush(fill_color_obj)
        
        # Try to add the plot
        try:
            # Important: Initially only plot the provided data, not a full buffer of zeros
            plot = self._plot_widget.plot(
                x=x, y=y, 
                pen=pen, 
                symbol=sym, 
                symbolSize=symbol_size, 
                symbolBrush=symbol_brush, 
                name=name,
                fillLevel=fill_level if fill_color is not None else None,
                fillBrush=fill_brush
            )
            
            # Store plot for later reference
            self._data_items.append(plot)
            
            # Set up internal buffer if buffer_size is provided
            if buffer_size is not None:
                # Create buffer of the right size but only filled with zeros
                x_buffer = np.zeros(buffer_size)
                y_buffer = np.zeros(buffer_size)
                
                # Store initial data in the buffer, but don't show the zeros
                data_len = len(y)
                if data_len > buffer_size:
                    # If we have more data than buffer size, use the most recent points
                    x_buffer[:] = x[-buffer_size:]
                    y_buffer[:] = y[-buffer_size:]
                else:
                    # If we have less data than buffer size, store at end of buffer
                    x_buffer[-data_len:] = x
                    y_buffer[-data_len:] = y
                
                self._data_buffers.append((x_buffer, y_buffer))
                self._buffer_sizes.append(buffer_size)
                
                # Store current valid data length (0 means empty)
                # This helps us track how much of the buffer is actually used
                if not hasattr(self, '_data_lengths'):
                    self._data_lengths = []
                self._data_lengths.append(min(data_len, buffer_size))
            else:
                # No internal buffering for this line
                self._data_buffers.append(None)
                self._buffer_sizes.append(None)
                if not hasattr(self, '_data_lengths'):
                    self._data_lengths = []
                self._data_lengths.append(0)
            
            # Store whether x is auto-generated
            self._auto_x.append(auto_x)
            
            # Auto range to show all data
            self._plot_item.enableAutoRange()
            
            # Force redraw to ensure data is visible
            self.redraw()
            
            return plot
            
        except Exception as e:
            print(f"Error creating line plot: {e}")
            
            # Try an alternative approach
            try:
                plot = self._plot_item.plot(
                    x=x, y=y, 
                    pen=pen, 
                    symbol=sym, 
                    symbolSize=symbol_size, 
                    symbolBrush=symbol_brush, 
                    name=name,
                    fillLevel=fill_level if fill_color is not None else None,
                    fillBrush=fill_brush
                )
                
                self._data_items.append(plot)
                self._data_buffers.append(None)
                self._buffer_sizes.append(None)
                if not hasattr(self, '_data_lengths'):
                    self._data_lengths = []
                self._data_lengths.append(0)
                self._auto_x.append(auto_x)
                self._plot_item.enableAutoRange()
                self.redraw()
                return plot
                
            except Exception as e2:
                print(f"Alternative plotting error: {e2}")
                return None
    
    def update_line(self, line_index, x=None, y=None, fill_color=None, fill_level=None):
        """
        Update an existing line's data completely.
        
        Args:
            line_index: Index of the line to update
            x: New x data
            y: New y data
            fill_color: New fill color as RGBA tuple (if None, doesn't change)
            fill_level: New y-level at which to fill to (if None, doesn't change)
            
        Returns:
            True if successful, False otherwise
        """
        if 0 <= line_index < len(self._data_items):
            if self._is_dynamic:
                # Queue the update to run in the background thread
                return self.queue_update(self._do_update_line, line_index, x, y, fill_color, fill_level)
            else:
                # Run immediately in the current thread
                return self._do_update_line(line_index, x, y, fill_color, fill_level)
        return False
        
    def _do_update_line(self, line_index, x=None, y=None, fill_color=None, fill_level=None):
        """Implementation of update_line that runs in UI thread"""
        line = self._data_items[line_index]
        
        # Update fill options if provided
        if fill_color is not None:
            # Make sure fill color is valid
            if len(fill_color) < 3:
                print(f"Warning: Invalid fill color format: {fill_color}.")
                return False
            elif len(fill_color) == 3:
                # Add alpha if not provided
                fill_color = (*fill_color, 0.3)
                
            fill_color_obj = pg.mkColor(
                int(fill_color[0]), 
                int(fill_color[1]), 
                int(fill_color[2]), 
                int(fill_color[3] * 255)
            )
            line.setFillBrush(fill_color_obj)
        
        if fill_level is not None:
            line.setFillLevel(fill_level)
        
        if y is not None:
            # Create default x values if not provided and originally auto-generated
            if x is None and self._auto_x[line_index]:
                x = np.arange(len(y))
                
            # Convert to numpy arrays if needed
            try:
                y = np.array(y, dtype=float)
                if x is not None:
                    x = np.array(x, dtype=float)
            except Exception as e:
                print(f"Error converting data to numpy arrays: {e}")
                return False
            
            # For lines without buffer, just update the plot directly
            if self._data_buffers[line_index] is None:
                # Update the plot with all new data
                line.setData(x=x, y=y)
                self._do_redraw()
                return True
            
            # For lines with buffer, update the buffer and display
            buffer_size = self._buffer_sizes[line_index]
            x_buffer, y_buffer = self._data_buffers[line_index]
            
            # Number of data points provided
            data_len = len(y)
            
            if data_len >= buffer_size:
                # If we have more data than buffer size, use the most recent points
                x_buffer[:] = x[-buffer_size:]
                y_buffer[:] = y[-buffer_size:]
                self._data_lengths[line_index] = buffer_size
            else:
                # If we have less data than buffer size, reset buffer and put data at start
                x_buffer.fill(0)
                y_buffer.fill(0)
                x_buffer[:data_len] = x
                y_buffer[:data_len] = y
                self._data_lengths[line_index] = data_len
            
            # Update the internal buffer
            self._data_buffers[line_index] = (x_buffer, y_buffer)
            
            # Only display the valid portion of the buffer
            display_length = self._data_lengths[line_index]
            line.setData(x=x_buffer[:display_length], y=y_buffer[:display_length])
            
            # Force redraw to ensure data is visible
            self._do_redraw()
            return True
        
        return True
    
    def add_point(self, line_index, y_value, x_value=None):
        """
        Add a single data point to a line's buffer and update the plot.
        
        Args:
            line_index: Index of the line to update
            y_value: New Y value to add
            x_value: New X value to add (if None and auto_x is True, will be auto-generated)
            
        Returns:
            True if successful, False otherwise
        """
        if 0 <= line_index < len(self._data_items):
            if self._is_dynamic:
                # Queue the point addition to run in the background thread
                return self.queue_update(self._do_add_point, line_index, y_value, x_value)
            else:
                # Run immediately in the current thread
                return self._do_add_point(line_index, y_value, x_value)
        return False
        
    def _do_add_point(self, line_index, y_value, x_value=None):
        """Implementation of add_point that runs in UI thread"""
        # Check if this line has a buffer
        if self._data_buffers[line_index] is None:
            print("Error: This line doesn't have an internal buffer. Use update_line() instead.")
            return False
        
        # Get current buffer
        x_buffer, y_buffer = self._data_buffers[line_index]
        buffer_size = self._buffer_sizes[line_index]
        current_length = self._data_lengths[line_index]
        
        # If buffer is not full yet, just add to the next position
        if current_length < buffer_size:
            # Add to next available position
            position = current_length
            
            # Set Y value
            y_buffer[position] = y_value
            
            # Set X value
            if x_value is None and self._auto_x[line_index]:
                # Auto-generate X value
                if position > 0:
                    # Increment from last X
                    x_buffer[position] = x_buffer[position-1] + 1
                else:
                    # Start at 0
                    x_buffer[position] = 0
            else:
                # Use provided X value
                x_buffer[position] = x_value if x_value is not None else position
                
            # Increment length
            self._data_lengths[line_index] = current_length + 1
        else:
            # Buffer is full, shift everything left
            # Shift data to the left (remove oldest point)
            x_buffer[:-1] = x_buffer[1:]
            y_buffer[:-1] = y_buffer[1:]
            
            # Add the new point at the end
            y_buffer[-1] = y_value
            
            # Handle x value
            if x_value is None and self._auto_x[line_index]:
                # Calculate next x value (increment from the last one)
                x_buffer[-1] = x_buffer[-2] + 1
            else:
                # Use provided x value
                x_buffer[-1] = x_value if x_value is not None else x_buffer[-1]
        
        # Update the internal buffer
        self._data_buffers[line_index] = (x_buffer, y_buffer)
        
        # Get the current length to determine how much data to display
        display_length = self._data_lengths[line_index]
        
        # Update the plot with only the valid portion of the buffer
        if display_length > 0:
            self._data_items[line_index].setData(
                x=x_buffer[:display_length], 
                y=y_buffer[:display_length]
            )
        
        # Force redraw to ensure data is visible
        self._do_redraw()
        return True
    
    def add_points(self, line_index, y_values, x_values=None):
        """
        Add multiple data points to a line's buffer and update the plot.
        
        Args:
            line_index: Index of the line to update
            y_values: Array of new Y values to add
            x_values: Array of new X values to add (if None and auto_x is True, will be auto-generated)
            
        Returns:
            True if successful, False otherwise
        """
        if 0 <= line_index < len(self._data_items):
            if self._is_dynamic:
                # Queue the points addition to run in the background thread
                return self.queue_update(self._do_add_points, line_index, y_values, x_values)
            else:
                # Run immediately in the current thread
                return self._do_add_points(line_index, y_values, x_values)
        return False
        
    def _do_add_points(self, line_index, y_values, x_values=None):
        """Implementation of add_points that runs in UI thread"""
        # Check if this line has a buffer
        if self._data_buffers[line_index] is None:
            print("Error: This line doesn't have an internal buffer. Use update_line() instead.")
            return False
        
        # Get current buffer
        x_buffer, y_buffer = self._data_buffers[line_index]
        buffer_size = self._buffer_sizes[line_index]
        current_length = self._data_lengths[line_index]
        
        # Convert input to numpy arrays if they aren't already
        try:
            y_values = np.array(y_values, dtype=float)
            if x_values is not None:
                x_values = np.array(x_values, dtype=float)
        except Exception as e:
            print(f"Error converting data to numpy arrays: {e}")
            return False
        
        # Number of new points
        num_new = len(y_values)
        
        # If no new points, nothing to do
        if num_new == 0:
            print("Warning: No new data points provided")
            return True
        
        # Space remaining in buffer
        space_remaining = buffer_size - current_length
        
        # If we have more points than space AND more points than buffer size
        if num_new > space_remaining and num_new > buffer_size:
            # If adding more points than buffer size, just use the latest ones
            # and completely replace the buffer
            new_y = y_values[-buffer_size:]
            
            if x_values is not None:
                new_x = x_values[-buffer_size:]
            else:
                # Auto-generate x if needed
                if self._auto_x[line_index]:
                    # Generate sequential x values
                    new_x = np.arange(len(new_y))
                else:
                    # Use existing x values pattern
                    new_x = np.arange(buffer_size)
            
            # Complete buffer replacement
            x_buffer[:] = new_x
            y_buffer[:] = new_y
            self._data_lengths[line_index] = buffer_size  # Buffer is now full
            
        elif num_new > space_remaining:
            # More new points than space but fewer than buffer size
            # Shift some data out to make room, keeping the most recent existing data
            # plus all the new data
            
            keep_existing = buffer_size - num_new  # How many existing points to keep
            if keep_existing > 0:
                # Move the most recent existing data to the start
                x_buffer[:keep_existing] = x_buffer[current_length-keep_existing:current_length]
                y_buffer[:keep_existing] = y_buffer[current_length-keep_existing:current_length]
            
            # Add new data after the kept existing data
            y_buffer[keep_existing:keep_existing+num_new] = y_values
            
            # Handle x values
            if x_values is not None:
                x_buffer[keep_existing:keep_existing+num_new] = x_values
            elif self._auto_x[line_index]:
                # Auto-generate x values continuing from the last value
                if keep_existing > 0:
                    start_x = x_buffer[keep_existing-1] + 1
                else:
                    start_x = 0
                x_buffer[keep_existing:keep_existing+num_new] = np.arange(start_x, start_x + num_new)
            
            # Update length - buffer is now full
            self._data_lengths[line_index] = buffer_size
        
        else:
            # Enough space for new points, just add them after existing ones
            y_buffer[current_length:current_length+num_new] = y_values
            
            # Handle x values
            if x_values is not None:
                x_buffer[current_length:current_length+num_new] = x_values
            elif self._auto_x[line_index]:
                # Auto-generate x values continuing from the last value
                if current_length > 0:
                    start_x = x_buffer[current_length-1] + 1
                else:
                    start_x = 0
                x_buffer[current_length:current_length+num_new] = np.arange(start_x, start_x + num_new)
            
            # Update length
            self._data_lengths[line_index] = current_length + num_new
        
        # Update the internal buffer
        self._data_buffers[line_index] = (x_buffer, y_buffer)
        
        # Get the current length to determine how much data to display
        display_length = self._data_lengths[line_index]
        
        # Update the plot with only the valid portion of the buffer
        if display_length > 0:
            self._data_items[line_index].setData(
                x=x_buffer[:display_length], 
                y=y_buffer[:display_length]
            )
        
        # Force redraw to ensure data is visible
        self._do_redraw()
        return True
    
    def get_buffer(self, line_index):
        """
        Get the current data buffer for a line.
        
        Args:
            line_index: Index of the line
            
        Returns:
            Tuple of (x_buffer, y_buffer) or None if no buffer exists
        """
        if 0 <= line_index < len(self._data_buffers):
            return self._data_buffers[line_index]
        return None
    
    def set_buffer_size(self, line_index, buffer_size):
        """
        Change the buffer size for a line.
        
        Args:
            line_index: Index of the line
            buffer_size: New buffer size
            
        Returns:
            True if successful, False otherwise
        """
        if 0 <= line_index < len(self._data_items):
            # Get current buffer
            current_buffer = self._data_buffers[line_index]
            
            # If line doesn't have a buffer yet, create one
            if current_buffer is None:
                x_buffer = np.zeros(buffer_size)
                y_buffer = np.zeros(buffer_size)
                self._data_buffers[line_index] = (x_buffer, y_buffer)
                self._buffer_sizes[line_index] = buffer_size
                return True
            
            # Resize existing buffer
            x_buffer, y_buffer = current_buffer
            old_size = len(x_buffer)
            
            if buffer_size > old_size:
                # New buffer is larger, pad with zeros
                new_x = np.zeros(buffer_size)
                new_y = np.zeros(buffer_size)
                new_x[-old_size:] = x_buffer
                new_y[-old_size:] = y_buffer
            else:
                # New buffer is smaller, keep most recent data
                new_x = x_buffer[-buffer_size:]
                new_y = y_buffer[-buffer_size:]
            
            self._data_buffers[line_index] = (new_x, new_y)
            self._buffer_sizes[line_index] = buffer_size
            
            # Update the plot
            self._data_items[line_index].setData(x=new_x, y=new_y)
            self.redraw()
            return True
        
        return False


# Example usage of the line graph class
if __name__ == "__main__":
    import pyvisual as pv
    from pyvisual.utils.pv_timer import PvTimer
    import random
    import time
    
    # Create app and window
    app = pv.PvApp()
    window = pv.PvWindow(title="Line Graph Examples", is_resizable=True)
    window.resize(1200, 800)

    #---------------------------------------------------------------------------
    # Example 1: Static Line Graph (No Buffer)
    #---------------------------------------------------------------------------
    line_graph = PvLineGraph(
        container=window,
        x=50, y=50,
        width=500, height=350,
        title="Static Line Graph Example",
        x_label="X-Axis", 
        y_label="Y-Axis",
        idle_color=(240, 240, 250, 1),  # Light blue background
        grid=True,
        legend=True,
        crosshair=True,
        corner_radius=5
    )
    
    # Example 1: Simple sine wave with default settings
    x1 = np.linspace(0, 10, 100)
    y1 = np.sin(x1)
    line_graph.add_line(
        x=x1, 
        y=y1,
        name="sin(x)",
        color=(255, 0, 0, 1),  # Red
        width=2
    )
    
    # Example 2: Cosine wave with symbols and custom style
    x2 = np.linspace(0, 10, 50)
    y2 = np.cos(x2)
    line_graph.add_line(
        x=x2, 
        y=y2,
        name="cos(x)",
        color=(0, 100, 255, 1),  # Blue
        width=2,
        style='dash',
        symbol='o',            # Circle symbols
        symbol_size=8,
        symbol_color=(0, 100, 255, 1)  # Same color as line
    )
    
    # Example 3: Exponential decay with different symbols
    x3 = np.linspace(0, 10, 30)
    y3 = np.exp(-0.5 * x3)
    line_graph.add_line(
        x=x3, 
        y=y3,
        name="exp(-0.5x)",
        color=(0, 180, 0, 1),  # Green
        width=2,
        style='solid',
        symbol='s',            # Square symbols
        symbol_size=10,
        symbol_color=(0, 120, 0, 1),  # Darker green for symbols
        fill_color=(0, 180, 0, 0.2),  # Light green fill with 20% opacity
        fill_level=0           # Fill down to y=0
    )
    
    #---------------------------------------------------------------------------
    # Example 2: Real-time updating with class-level default buffer
    #---------------------------------------------------------------------------
    
    # Define a default buffer size for the entire graph
    buffer_size = 100
    
    # Create a real-time graph with a default buffer size
    default_buffer_graph = PvLineGraph(
        container=window,
        x=600, y=50,
        width=550, height=350,
        title="Default Buffer Size Example",
        x_label="Time", 
        y_label="Value",
        idle_color=(245, 245, 245, 1),  # Light gray background
        grid=True,
        legend=True,
        crosshair=True,
        x_range=(0, 100),         # Fixed x-range for scrolling effect 
        y_range=(-1.5, 1.5),      # Fixed y-range
        default_buffer_size=buffer_size,  # Set default buffer size for all lines
        dummy_data=True
    )
    
    # Add lines without specifying buffer_size - will use default_buffer_size
    sine_line = default_buffer_graph.add_line(
        name="Sine Wave",
        color=(255, 0, 0, 1),     # Red
        width=2,
        fill_color=(255, 0, 0, 0.2)  # Light red fill
    )
    
    noise_line = default_buffer_graph.add_line(
        name="Noisy Data",
        color=(0, 0, 255, 1),     # Blue
        width=1,
        symbol='o',               # Circle symbols
        symbol_size=4
    )
    
    #---------------------------------------------------------------------------
    # Example 3: Filled Area Graph
    #---------------------------------------------------------------------------
    filled_graph = PvLineGraph(
        container=window,
        x=50, y=450,
        width=1100, height=300,
        title="Area Under Curve Example",
        x_label="X-Axis", 
        y_label="Y-Axis",
        idle_color=(250, 250, 250, 1),  # White background
        grid=True,
        legend=True
    )
    
    # Example with a filled area under the curve
    x4 = np.linspace(0, 20, 200)
    y4 = np.sin(x4) * np.exp(-0.2 * x4)
    
    filled_graph.add_line(
        x=x4, 
        y=y4,
        name="Damped Sine Wave",
        color=(100, 50, 200, 1),  # Purple
        width=3,
        fill_color=(100, 50, 200, 0.3),  # Light purple with 30% opacity
        fill_level=0  # Fill down to y=0
    )

    # Animation variables
    phase = 0
    
    # Update function that will be called by the timer
    def update_data():
        global phase
        
        # Update phase
        phase += 0.1
        
        # Calculate new values
        sine_value = np.sin(phase)
        noise_value = sine_value + random.uniform(-0.3, 0.3)
        default_value = np.sin(phase + 0.5)
        large_value = np.cos(phase * 0.5)
        
        # Example 2: Add points to default buffer graph
        default_buffer_graph.add_point(0, sine_value)
        default_buffer_graph.add_point(1, noise_value)

    # Create and start timer for real-time updates (50ms = 20fps)
    timer = PvTimer(interval=50, callback=update_data)
    timer.start()
    
    # Show the window and start the application
    window.show()
    app.run() 