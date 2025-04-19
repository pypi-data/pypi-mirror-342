import base64
import ast
import random

class NastarEncoder:
    def __init__(self, key: str = "nastar_default_key"):
        self.key = key
    
    def _xor_encrypt(self, code: str) -> bytes:
        """Enkripsi XOR dengan key."""
        key_bytes = self.key.encode()
        code_bytes = code.encode()
        return bytes([code_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(code_bytes))])
    
    def _obfuscate_names(self, code: str) -> str:
        """Ganti nama variabel/fungsi dengan karakter acak."""
        tree = ast.parse(code)
        # Generator nama acak (contoh: _x1, _y2)
        new_names = {f"var_{i}": f"_{chr(random.randint(97, 122))}{i}" 
                     for i in range(20)}
        # Manipulasi AST
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                node.id = new_names.get(node.id, node.id)
        return ast.unparse(tree)
    
    def protect(self, code: str) -> str:
        """Hasilkan kode Python terproteksi yang bisa dijalankan langsung."""
        # 1. Obfuscate AST
        obfuscated_code = self._obfuscate_names(code)
        # 2. Enkripsi XOR + Base85
        encrypted = self._xor_encrypt(obfuscated_code)
        encoded = base64.b85encode(encrypted).decode()
        # 3. Generate self-decoding script
        return f'''
import base64;exec(bytes([b^{ord(self.key[i % len(self.key)])} 
for i,b in enumerate(base64.b85decode("{encoded}"))]))
'''.strip()
