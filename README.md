# QR Code Generator and Malicious URL Checker

This Python application generates all possible QR codes of sizes from 2x2 to 164x164 and checks codes containing URLs for malicious content using VirusTotal API.

## What it does

- Generates all combinatinons of 0 and 1 for QR codes of given sizes
- Saves QR code images to `qrcode/` folder with indexed filenames 
- Checks codes containing URLs via VirusTotal API
- Prints and saves dangerous domains found to `dangerous.txt`

## Results

Total QR codes generated: 1,382,958  

Malicious URLs found: 298,593

Percent of malicious codes: 22% of all generated QR codes

## Usage

1. Clone repo
2. Get VirusTotal API key and add to code
3. Run `python3 qrcode_check.py`
4. Check output in terminal and dangerous.txt
