from .singleton import Singleton
from .buffer import Buffer
import math


class PyDOSIP(Singleton):
    r"""
    PyDOSIP is a Python library for detecting operating states in a system.
    

    Operating State Detection Algorithm:

    The detection of operating states in pipeline systems uses Z-Score analysis for both flow rate and pressure measurements:

    Z-Score Formula:
    Z = (X - μ)/σ
    Where:
    • X is the current value from the observation window
    • μ is the mean of the dataset
    • σ is the standard deviation of the dataset

    1. Flow Rate Analysis (Primary Check):
       Using Z-Score analysis on flow rate (Zf):
       • ShutIn State: Zf consistently near zero or negative
         (Indicates minimal or no active flow in the pipeline)
       • Active Flow: Zf significantly positive
         (Indicates active pumping operation)
       
       The flow Z-Score (Zf) helps to:
       • Detect subtle changes in flow patterns
       • Identify gradual transitions to/from ShutIn state
       • Provide more precise ShutIn detection than fixed thresholds

    2. Pressure State Analysis (Secondary Check):
       When active flow is confirmed, pressure Z-Score (Zp) determines:
       • Steady State: |Zp| < pressure_threshold
         (Pressure variations remain close to the mean)
       • Transient State:
         - Increasing pressure: Zp > pressure_threshold
         - Decreasing pressure: Zp < -pressure_threshold

    Operating States Classification:
    1. ShutIn State:
        • Primary indicator: Flow Z-Score (Zf) near zero or negative
        • Pressure analysis may still be monitored but is secondary

    2. Active Pipeline States:
        • Requires positive Flow Z-Score (Zf)
        • State determined by Pressure Z-Score (Zp)
        • Transitions between states can be tracked through Z-Score trends

    Advantages of Dual Z-Score Analysis:
    • More robust detection of operating states
    • Better handling of gradual transitions
    • Self-adjusting to system characteristics
    • Capable of detecting subtle operational changes
    • Consistent statistical approach across all measurements

    Note: The sensitivity of both flow and pressure state detection can be adjusted through their respective Z-Score thresholds based on operational requirements and system characteristics.

    """
    
    def __init__(
            self, 
            window_size: int = 10,
            threshold: float = 3.0,
            threshold_shutin: float = 0.0,
            buffer_type: str = 'forward',
            times_to_trigger: int = 5):

        self.threshold = threshold
        self.threshold_shutin = threshold_shutin
        self.__buffer_type_allowed = ['forward', 'backward']
        buffer_type = buffer_type.lower()
        if buffer_type not in self.__buffer_type_allowed:
            raise ValueError(f"Buffer type must be one of {self.__buffer_type_allowed}")
        self.times_to_trigger = times_to_trigger
        self.pbuffer = Buffer(size=window_size, roll=buffer_type)
        self.fbuffer = Buffer(size=window_size, roll=buffer_type)
        
        # Variables para el control de estados
        self.current_state = "SHUTIN"
        self.previous_state = "SHUTIN"
        self.state_counter = 0

    def calculate_z_score(self, buffer: Buffer) -> float:
        r"""
        Calculate the Z-Score for the current data point in the buffer.

        Parameters:
        -----------
        buffer : Buffer
            Buffer containing the historical data and current value.

        Returns:
        --------
        float
            The Z-Score of the current data point.

        Notes:
        ------
        The Z-Score is calculated using the formula:
        Z = (X - μ)/σ
        where:
        - X is the current value
        - μ is the mean of the dataset
        - σ is the standard deviation of the dataset

        A positive Z-Score indicates the value is above the mean,
        while a negative Z-Score indicates it's below the mean.
        """
        if not isinstance(buffer, Buffer):
            raise TypeError("buffer must be an instance of Buffer")
        
        current_value = buffer.current()
        historical_data = buffer  # All values except the current one
        
        if not historical_data:
            return 0.0  # If no historical data, consider it at the mean
        
        # Calculate mean
        mean = sum(historical_data) / len(historical_data)
        
        # Calculate standard deviation
        squared_diffs = [(x - mean) ** 2 for x in historical_data]
        variance = sum(squared_diffs) / len(historical_data)
        self.std = math.sqrt(variance)
        
        if self.std == 0:
            return 0.0  # If all values are the same, Z-Score is 0
        
        return (current_value - mean) / self.std

    def __call__(self, flow_value: float, pressure_value: float) -> str:
        r"""
        Execute the operating state detection algorithm.

        Parameters:
        -----------
        flow_value : float
            Current flow rate measurement.
        pressure_value : float
            Current pressure measurement.

        Returns:
        --------
        str
            Detected operating state. Possible values:
            - 'SHUTIN': Pipeline is not being actively pumped
            - 'STEADY': Pipeline is in steady state
            - 'TRANSIENT': Pipeline is in transient state
            - 'INSUFFICIENT_DATA': Not enough data points in buffers to perform analysis

        Notes:
        ------
        The algorithm first checks if there are enough data points in the buffers.
        Then it analyzes the flow rate to determine if the pipeline is in ShutIn state.
        If active flow is detected, it analyzes the pressure to determine if the system is
        in steady state or transient state.
        The state change is only triggered after the same state is detected times_to_trigger times.
        """
        # Update buffers with new values
        self.fbuffer(flow_value)
        self.pbuffer(pressure_value)

        # Check if buffers are full
        if len(self.fbuffer) < self.fbuffer.size or len(self.pbuffer) < self.pbuffer.size:

            return 'INSUFFICIENT_DATA'

        # Calculate Z-Scores
        # flow_z_score = self.calculate_z_score(self.fbuffer)
        pressure_z_score = self.calculate_z_score(self.pbuffer)

        # Determine new state
        if abs(flow_value) <= self.threshold_shutin:
            new_state = 'SHUTIN'
        elif abs(pressure_z_score) < self.threshold:
            new_state = 'STEADY'
        else:
            new_state = 'TRANSIENT'
        
        if new_state != self.previous_state:
            self.state_counter = 0
            self.previous_state = new_state
            return self.current_state

        self.state_counter += 1
        if self.state_counter >= self.times_to_trigger:
            self.current_state = new_state
            self.previous_state = new_state        
        return self.current_state
        
    def set_threshold(self, threshold: float):
        r"""
        Documentation here
        """
        self.threshold = threshold

    def set_threshold_shutin(self, threshold_shutin: float):
        r"""
        Set the threshold for determining ShutIn state based on flow Z-Score.

        Parameters:
        -----------
        threshold_shutin : float
            The Z-Score threshold below which the system is considered in ShutIn state.
            A value of 0.0 means the system is in ShutIn when flow Z-Score is zero or negative.
            A positive value allows for some tolerance in the ShutIn detection.
        """
        self.threshold_shutin = threshold_shutin

    def set_window_size(self, window_size: int):
        r"""
        Documentation here
        """
        self.pbuffer.size = window_size
        self.fbuffer.size = window_size

    def set_buffer_type(self, buffer_type: str):
        r"""
        Documentation here
        """
        buffer_type = buffer_type.lower()
        if buffer_type not in self.__buffer_type_allowed:
            raise ValueError(f"Buffer type must be one of {self.__buffer_type_allowed}")
        self.pbuffer.roll = buffer_type
        self.fbuffer.roll = buffer_type
        
    def set_times_to_trigger(self, times_to_trigger: int):
        r"""
        Documentation here
        """
        self.times_to_trigger = times_to_trigger
