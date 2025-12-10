# **Digital Signal Generator – README**

## **Overview**
This project provides a complete **Digital Signal Generator** with GUI support using **Tkinter**, enabling users to:
- Generate digital & analog signals  
- Encode signals using multiple line-coding schemes  
- Scramble AMI signals (B8ZS, HDB3)  
- Decode generated signals  
- Visualize signals using Matplotlib  
- Analyze longest palindromic subsequences using **Manacher’s Algorithm**

The project contains two major components:
1. **DigitalSignalGenerator** – backend logic  
2. **DigitalSignalGeneratorGUI** – graphical user interface  

---

# **Features**

## **1. Supported Line Encoding Schemes**
- **NRZ-L**  
- **NRZ-I**  
- **Manchester**  
- **Differential Manchester**  
- **AMI (Alternate Mark Inversion)**

## **2. Scrambling Techniques (AMI Only)**
- **B8ZS**
- **HDB3**

## **3. Analog Modulation**
- **PCM Encoding (8-bit)**
- **Delta Modulation**

## **4. Signal Analysis**
- Mean, Standard deviation  
- Longest palindrome detection using **Manacher’s algorithm**

## **5. Decoding Support**
Each encoding scheme includes a corresponding decoding function:
- NRZ-L decoder  
- NRZ-I decoder  
- Manchester decoder  
- Differential Manchester decoder  
- AMI decoder  

---

# **Project Structure**

## **DigitalSignalGenerator Class**
Handles all backend operations:
- PCM encoding  
- Delta modulation  
- Line encoding  
- Scrambling  
- Decoding  
- Zero-sequence detection  
- Manacher's longest palindrome algorithm  

### **Key Methods**
- `pcm_encode()`
- `delta_modulation()`
- `longest_palindrome_manacher()`
- `nrz_l()`, `nrz_i()`
- `manchester()`, `differential_manchester()`
- `ami()`
- `decode_*()` (for each scheme)
- `b8zs_scramble()`
- `hdb3_scramble()`

---

# **Graphical User Interface**

## **DigitalSignalGeneratorGUI**
Provides an intuitive interface with:
- Input panels  
- Encoding/scrambling options  
- Signal plot window  
- Output and analysis box  
- Decoding button  

### **Main GUI Features**
- Input selection (digital/analog)
- Real-time signal plotting
- Scrambling toggle
- Signal decoding
- Error detection and GUI messages

---

# **How to Run**
Ensure Python packages are installed:

```bash
pip install numpy matplotlib
