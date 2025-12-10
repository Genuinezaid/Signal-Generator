import numpy as np

from typing import List, Tuple


class DigitalSignalGenerator:


    def __init__(self):
        self.bit_duration = 1.0
        self.sampling_rate = 100


    def pcm_encode(self, analog_signal: np.ndarray, n_bits: int = 8) -> str:

        if len(analog_signal) < 2:
            raise ValueError("Signal needs at least 2 samples")
        normalized = (analog_signal - np.min(analog_signal)) / (np.max(analog_signal) - np.min(analog_signal) + 1e-10)
        levels = 2 ** n_bits
        quantized = np.floor(normalized * (levels - 1)).astype(int)
        return ''.join([format(val, f'0{n_bits}b') for val in quantized])

    def delta_modulation(self, analog_signal: np.ndarray, step_size: float = 0.1) -> str:

        binary_output = []
        approximation = analog_signal[0]
        for sample in analog_signal:
            if sample > approximation:
                binary_output.append('1')
                approximation += step_size
            else:
                binary_output.append('0')
                approximation -= step_size
        return ''.join(binary_output)


    def longest_palindrome_manacher(self, data_stream: str) -> Tuple[str, int, int]:

        if not data_stream:
            return "", 0, 0

        t = '#'.join('^{}$'.format(data_stream))
        n = len(t)
        P = [0] * n
        center = right = 0

        for i in range(1, n - 1):
            mirror = 2 * center - i
            if i < right:
                P[i] = min(right - i, P[mirror])

            try:
                while t[i + 1 + P[i]] == t[i - 1 - P[i]]:
                    P[i] += 1
            except IndexError:
                pass

            if i + P[i] > right:
                center, right = i, i + P[i]

        max_len = max(P) if P else 0
        if max_len == 0:
            return "", 0, 0

        center_idx = P.index(max_len)
        start = (center_idx - max_len) // 2
        palindrome = data_stream[start:start + max_len]
        return palindrome, start, max_len


    def nrz_l(self, data: str) -> Tuple[np.ndarray, np.ndarray]:

        signal, time = [], []
        for i, bit in enumerate(data):
            t = np.linspace(i, i + 1, self.sampling_rate, endpoint=False)
            v = 1 if bit == '1' else -1
            signal.extend([v] * len(t))
            time.extend(t)
        return np.array(time), np.array(signal)

    def nrz_i(self, data: str) -> Tuple[np.ndarray, np.ndarray]:

        signal, time, level = [], [], -1
        for i, bit in enumerate(data):
            t = np.linspace(i, i + 1, self.sampling_rate, endpoint=False)
            if bit == '1':
                level *= -1
            signal.extend([level] * len(t))
            time.extend(t)
        return np.array(time), np.array(signal)

    def manchester(self, data: str) -> Tuple[np.ndarray, np.ndarray]:

        signal, time = [], []
        for i, bit in enumerate(data):
            t1 = np.linspace(i, i + 0.5, self.sampling_rate // 2, endpoint=False)
            t2 = np.linspace(i + 0.5, i + 1, self.sampling_rate // 2, endpoint=False)
            if bit == '1':
                signal.extend([-1] * len(t1) + [1] * len(t2))
            else:
                signal.extend([1] * len(t1) + [-1] * len(t2))
            time.extend(list(t1) + list(t2))
        return np.array(time), np.array(signal)

    def differential_manchester(self, data: str) -> Tuple[np.ndarray, np.ndarray]:

        signal, time, level = [], [], 1
        for i, bit in enumerate(data):
            t1 = np.linspace(i, i + 0.5, self.sampling_rate // 2, endpoint=False)
            t2 = np.linspace(i + 0.5, i + 1, self.sampling_rate // 2, endpoint=False)
            if bit == '0':
                level *= -1
            signal.extend([level] * len(t1))
            level *= -1
            signal.extend([level] * len(t2))
            time.extend(list(t1) + list(t2))
        return np.array(time), np.array(signal)

    def ami(self, data: str) -> Tuple[np.ndarray, np.ndarray]:

        signal, time, last_one = [], [], -1
        for i, bit in enumerate(data):
            t = np.linspace(i, i + 1, self.sampling_rate, endpoint=False)
            if bit == '0':
                v = 0
            else:
                last_one *= -1
                v = last_one
            signal.extend([v] * len(t))
            time.extend(t)
        return np.array(time), np.array(signal)


    def decode_nrz_l(self, signal: np.ndarray) -> str:

        bits = []
        samples_per_bit = self.sampling_rate
        for i in range(0, len(signal), samples_per_bit):
            bit_signal = signal[i:i + samples_per_bit]
            if len(bit_signal) < samples_per_bit // 2:
                break
            avg_voltage = np.mean(bit_signal)
            bits.append('1' if avg_voltage > 0 else '0')
        return ''.join(bits)

    def decode_nrz_i(self, signal: np.ndarray) -> str:

        bits = []
        samples_per_bit = self.sampling_rate
        last_level = signal[0]
        for i in range(0, len(signal), samples_per_bit):
            bit_signal = signal[i:i + samples_per_bit]
            if len(bit_signal) < samples_per_bit // 2:
                break
            avg_level = np.mean(bit_signal)
            bit = '1' if abs(avg_level - last_level) > 0.5 else '0'
            bits.append(bit)
            last_level = avg_level
        return ''.join(bits)

    def decode_manchester(self, signal: np.ndarray) -> str:

        bits = []
        samples_per_bit = self.sampling_rate
        for i in range(0, len(signal), samples_per_bit):
            bit_signal = signal[i:i + samples_per_bit]
            if len(bit_signal) < samples_per_bit // 2:
                break
            first_half = np.mean(bit_signal[:len(bit_signal) // 2])
            second_half = np.mean(bit_signal[len(bit_signal) // 2:])
            bits.append('1' if first_half < second_half else '0')
        return ''.join(bits)

    def decode_differential_manchester(self, signal: np.ndarray) -> str:

        bits = []
        samples_per_bit = self.sampling_rate
        for i in range(0, len(signal), samples_per_bit):
            bit_signal = signal[i:i + samples_per_bit]
            if len(bit_signal) < samples_per_bit // 2:
                break
            first_half = np.mean(bit_signal[:len(bit_signal) // 2])
            second_half = np.mean(bit_signal[len(bit_signal) // 2:])
            bits.append('1' if abs(first_half - second_half) > 0.5 else '0')
        return ''.join(bits)

    def decode_ami(self, signal: np.ndarray) -> str:

        bits = []
        samples_per_bit = self.sampling_rate
        for i in range(0, len(signal), samples_per_bit):
            bit_signal = signal[i:i + samples_per_bit]
            if len(bit_signal) < samples_per_bit // 2:
                break
            avg_voltage = np.mean(bit_signal)
            bits.append('1' if abs(avg_voltage) > 0.1 else '0')
        return ''.join(bits)


    def find_zero_sequences(self, data: str) -> List[Tuple[int, int]]:

        sequences, i = [], 0
        while i < len(data):
            if data[i] == '0':
                start, count = i, 0
                while i < len(data) and data[i] == '0':
                    count += 1;
                    i += 1
                sequences.append((start, count))
            else:
                i += 1
        return sequences

    def b8zs_scramble(self, data: str) -> str:

        result = list(data)
        sequences = self.find_zero_sequences(data)
        for start, length in sequences:
            if length >= 8:
                for j in range(start, start + length - 7, 8):
                    result[j:j + 8] = ['0', '0', '0', 'V', 'B', '0', 'V', 'B']
        return ''.join(result)

    def hdb3_scramble(self, data: str) -> str:

        result = list(data)
        sequences = self.find_zero_sequences(data)
        ones_count = 0
        for start, length in sequences:
            if length >= 4:
                for j in range(start, start + length - 3, 4):
                    if ones_count % 2 == 0:
                        result[j:j + 4] = ['0', '0', '0', 'V']
                    else:
                        result[j:j + 4] = ['B', '0', '0', 'V']
                    ones_count += 1
        return ''.join(result)


