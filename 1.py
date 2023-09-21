from abc import ABC, abstractmethod
import qrcode
import os
import requests
import itertools

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
    
    def __init__(self, generator):
        self.generator = generator
        
    def run(self):
        dangerous_domains = []
        self.generator.generate()
        
        for qrcode in self.generator.qrcodes:
            if 'http://' in qrcode or 'https://' in qrcode:
                if is_dangerous(qrcode):
                    print(f"{qrcode} is dangerous!")
                    dangerous_domains.append(qrcode)
        
        with open('dangerous.txt', 'w') as f:
            f.write('\n'.join(dangerous_domains))
            
        self.generator.qrcodes.clear()
            
def is_dangerous(qrcode):
    url = 'https://www.virustotal.com/vtapi/v2/url/report'
    params = {'apikey':'key', 'resource': qrcode}
    response = requests.get(url, params=params)
    return response.json()['positives'] > 0
            
if __name__ == '__main__':
    generator = BasicQRCodeGenerator()
    analyzer = QRCodeAnalyzer(generator)
    analyzer.run()
