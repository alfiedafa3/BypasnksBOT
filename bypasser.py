"""
Main bypasser module untuk bypass link dan verifikasi
"""
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import json


class LinkBypassser:
    """Handle berbagai jenis link bypass"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
    
    def detect_link_type(self, url):
        """Deteksi tipe link yang diberikan"""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            if 'shortlink' in domain or 'short' in domain:
                return 'shortlink'
            elif 'bypass' in domain:
                return 'bypass'
            elif 'verify' in domain:
                return 'verify'
            elif 'google' in domain:
                return 'google'
            elif 'mega' in domain or 'mediafire' in domain or 'drive' in domain:
                return 'download'
            else:
                return 'unknown'
        except:
            return 'unknown'
    
    def bypass_shortlink(self, url):
        """Bypass shortlink service"""
        try:
            response = self.session.get(url, headers=self.headers, allow_redirects=False, timeout=10)
            
            # Check untuk redirect
            if response.status_code in [301, 302, 303, 307, 308]:
                redirect_url = response.headers.get('Location')
                if redirect_url:
                    return {
                        'success': True,
                        'type': 'shortlink',
                        'original_url': url,
                        'bypassed_url': redirect_url,
                        'method': 'redirect'
                    }
            
            # Check di content untuk hidden link
            content = response.text
            links = re.findall(r'href=["\']([^"\']+ )["\']', content)
            
            if links:
                return {
                    'success': True,
                    'type': 'shortlink',
                    'original_url': url,
                    'bypassed_url': links[0],
                    'method': 'html_parse'
                }
            
            return {
                'success': False,
                'type': 'shortlink',
                'error': 'Tidak bisa menemukan link tersembunyi'
            }
        
        except Exception as e:
            return {
                'success': False,
                'type': 'shortlink',
                'error': str(e)
            }
    
    def bypass_verify(self, url):
        """Bypass verification page"""
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cari button download atau link final
            download_buttons = soup.find_all('a', class_=re.compile(r'btn|button|download', re.I))
            
            if download_buttons:
                final_link = download_buttons[0].get('href')
                if final_link:
                    return {
                        'success': True,
                        'type': 'verify',
                        'original_url': url,
                        'download_link': final_link,
                        'method': 'button_found'
                    }
            
            # Cari iframe atau nested link
            iframes = soup.find_all('iframe')
            if iframes:
                iframe_src = iframes[0].get('src')
                if iframe_src:
                    return {
                        'success': True,
                        'type': 'verify',
                        'original_url': url,
                        'nested_link': iframe_src,
                        'method': 'iframe_found'
                    }
            
            return {
                'success': False,
                'type': 'verify',
                'error': 'Verification method tidak diketahui'
            }
        
        except Exception as e:
            return {
                'success': False,
                'type': 'verify',
                'error': str(e)
            }
    
    def bypass_link(self, url):
        """Main function untuk bypass link"""
        link_type = self.detect_link_type(url)
        
        if link_type == 'shortlink':
            return self.bypass_shortlink(url)
        elif link_type == 'verify':
            return self.bypass_verify(url)
        else:
            return {
                'success': False,
                'error': f'Link type {link_type} belum support',
                'original_url': url
            }


class DownloadManager:
    """Handle download file dari berbagai platform"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def download_file(self, url, filename):
        """Download file dari URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=30, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(filename, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress = (downloaded / total_size * 100) if total_size else 0
            
            return {
                'success': True,
                'filename': filename,
                'size': total_size,
                'message': f'Download selesai: {filename}'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Gagal download: {str(e)}'
            }
