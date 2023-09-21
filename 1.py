from abc import ABC, abstractmethod
import qrcode
import os
import requests
import itertools
import getpass

class QRCodeGenerator(ABC):

    def __init__(self):
        self.qrcodes = []
        
    def generate(self):
        for size in range(2, 165):
            binary_length = size * size
            all_binary = [''.join(seq) for seq in itertools.product('01', repeat=binary_length)]
            self.qrcodes.extend(all_binary)
        
    def save(self, qrcode):
        img = qrcode.make_image(qrcode)
        img.save(f'qrcode/{qrcode}.png')

class BasicQRCodeGenerator(QRCodeGenerator):
    pass

class QRCodeAnalyzer():
    
    def __init__(self, generator, api_key):
        self.generator = generator
        self.api_key = api_key
        
    def run(self):
        dangerous_domains = []
        self.generator.generate()
        
        for qrcode in self.generator.qrcodes:
            if 'http://' in qrcode or 'https://' in qrcode:
                if self.is_dangerous(qrcode):
                    print(f"{qrcode} is dangerous!")
                    dangerous_domains.append(qrcode)
        
        with open('dangerous.txt', 'w') as f:
            f.write('\n'.join(dangerous_domains))
            
        self.generator.qrcodes.clear()
    
    def is_dangerous(self, qrcode):
        url = 'https://www.virustotal.com/vtapi/v2/url/report'
        params = {'apikey': self.api_key, 'resource': qrcode}
        response = requests.get(url, params=params)
        return response.json()['positives'] > 0
        
if __name__ == '__main__':

    api_key = getpass.getpass('Enter VirusTotal API key: ')
    
    generator = BasicQRCodeGenerator()
    analyzer = QRCodeAnalyzer(generator, api_key)
    analyzer.run()
