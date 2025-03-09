# tymtUploader

## 📌 About

TymtUploader is a cross-platform game submission and torrent seeding tool for Tymt, allowing developers to submit games, generate metadata, and seed torrents.

---

## 🚀 Installation

### **1️⃣ Install Python** (if not installed)

- **Windows:** [Download Python](https://www.python.org/downloads/windows/) and check **Add Python to PATH** during installation.
- **MacOS:** Pre-installed, but you may need:
  ```sh
  brew install python
  ```
- **Linux:**
  ```sh
  sudo apt install python3 python3-pip -y
  ```

### **2️⃣ Clone the Repository**

```sh
git clone https://github.com/solarenterprises/tymtuploader.git
cd tymtUploader
```

### **3️⃣ Install Dependencies**

```sh
pip install -r requirements.txt
```

### **4️⃣ Install Transmission (for Torrenting)**

- **Windows:** Install [Transmission](https://transmissionbt.com/download/)
- **MacOS:**
  ```sh
  brew install transmission-cli
  ```
- **Linux:**
  ```sh
  sudo apt install transmission-cli -y
  ```

---

## 🎮 Running TymtUploader

```sh
python main.py
```

---

## 📷 Image Requirements

When uploading images for your game, please ensure they meet the following requirements:

- **Preview Image**: 
  - Format: `.webp`
  - Maximum Size: 100KB
  - Maximum Dimensions: 1600x900

- **Asset Images**: 
  - Format: `.webp`
  - Maximum Size: 100KB
  - Maximum Dimensions: 1600x900

- **Icon Image**: 
  - Format: `.webp`
  - Maximum Size: 25KB
  - Maximum Dimensions: 512x512

---

## 🔧 Building Executables

### **🖥 Windows (.exe)**

To build a Windows executable on macOS, you need to use a cross-compilation tool like `pyinstaller` with `wine`:

1. Install `wine`:
    ```sh
    brew install --cask wine-stable
    ```

2. Install `pyinstaller`:
    ```sh
    pip install pyinstaller
    ```

3. Build the executable:
    ```sh
    pyinstaller --onefile --windowed --name "TymtUploader" main.py
    ```

4. Build the executable directly from Windows:
    ```sh
    pyinstaller --clean --windowed --add-data "add-gamefolder-here;add-gamefolder-here" --add-data "menus;menus" --add-data "utils;utils" --add-data "README.md;." --add-data "requirements.txt;." --name "TymtUploader" --icon "icon.ico" main.py
    ```

### **🍏 macOS (.app)**

```sh
pyinstaller --onefile --windowed --name "TymtUploader" main.py
```

### **🐧 Linux (.AppImage)**

```sh
sudo apt install appimagetool
mkdir -p TymtUploader.AppDir/usr/bin
cp dist/TymtUploader TymtUploader.AppDir/usr/bin/
appimagetool TymtUploader.AppDir
```

---

## 🛠 Troubleshooting

- **PyInstaller not found?** Run:
  ```sh
  python3 -m pip install pyinstaller
  ```
- **Torrent trackers not included?** Update `torrent_manager.py` with the correct trackers.
- **Windows `.exe` doesn’t work?** Install the [VC++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe).

---

## 📜 License

This project is licensed under the MIT License.

---

## 📧 Contact

For questions, contact [**@NayiemWillems**](https://github.com/NayiemWillems) on GitHub.

---

Now you can run tymtUploader on any system! 🚀# tymtUploader
