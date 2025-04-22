import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import tldextract
from dotenv import load_dotenv
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer, util


class AIIA:
    def __init__(self, api_key: Optional[str] = None, client_secret: Optional[str] = None, ia_id: Optional[str] = None, endpoint: Optional[str] = None):
        load_dotenv()
        self.api_key = api_key or os.getenv("AIIA_API_KEY")
        client_secret = client_secret or os.getenv("AIIA_CLIENT_SECRET")
        self.client_secret = client_secret.encode() if client_secret is not None else None
        self.ia_id = ia_id or os.getenv("AIIA_IA_ID")
        self.endpoint = (endpoint or os.getenv("AIIA_ENDPOINT") or "https://api.aiiatrace.com/receive_log").rstrip('/')
        self.cache_file = Path(__file__).parent / "cache" / "actions_cache.json"
        self._init_cache()
        self._load_semantic_model()

    def _load_semantic_model(self):
        try:
            self.semantic_model = SentenceTransformer("all-MiniLM-L6-v2")
            actions_file = Path(__file__).parent / "aiia_actions_v1.0.json"
            with open(actions_file, "r") as f:
                actions_data = json.load(f).get("actions", [])
            self.semantic_actions = [
                {
                    "code": a["code"],
                    "text": f"{a['code']} - {a.get('description', '')}"
                } for a in actions_data
            ]
            self.semantic_embeddings = self.semantic_model.encode(
                [a["text"] for a in self.semantic_actions],
                convert_to_tensor=True
            )
        except Exception as e:
            print(f"Error cargando modelo semántico: {e}")
            self.semantic_model = None
            self.semantic_actions = []
            self.semantic_embeddings = []

    def _init_cache(self) -> None:
        self.cache_file.parent.mkdir(exist_ok=True)
        if not self.cache_file.exists():
            self.cache_file.write_text("{}")

    def _load_cache(self) -> Dict[str, Any]:
        try:
            return json.loads(self.cache_file.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_cache(self, data: Dict[str, Any]) -> None:
        self.cache_file.write_text(json.dumps(data))

    def _get_action_definition(self, action_code: str) -> Dict[str, Any]:
        cache = self._load_cache()
        if action_code in cache:
            return cache[action_code]

        try:
            response = requests.get(
                f"{self.endpoint}/actions/{action_code}",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=5
            )
            response.raise_for_status()
            action_data = response.json()
            cache[action_code] = action_data
            self._save_cache(cache)
            return action_data
        except requests.exceptions.RequestException:
            return {
                "code": action_code,
                "description": f"Acción {action_code}",
                "category": "general",
                "sensitive": False
            }

    def log_action(self, action_code: str, context: Optional[Dict[str, Any]] = None, registered: bool = True) -> bool:
        try:
            import hashlib
            if not hasattr(self, "_recent_logs"):
                self._recent_logs = set()

            # Crear un hash único del log basado en su contenido relevante
            log_fingerprint = hashlib.sha256(
                f"{action_code}|{json.dumps(context, sort_keys=True)}|{self.ia_id}".encode()
            ).hexdigest()

            if log_fingerprint in self._recent_logs:
                return False
            self._recent_logs.add(log_fingerprint)

            # Opcional: limpiar el set si se hace muy grande
            if len(self._recent_logs) > 10000:
                self._recent_logs = set(list(self._recent_logs)[-5000:])

            # Check if already logged (simple in-memory prevention, can be improved)
            if hasattr(self, "_logged_actions") and action_code in self._logged_actions:
                return False
            else:
                if not hasattr(self, "_logged_actions"):
                    self._logged_actions = set()
                self._logged_actions.add(action_code)

            action_def = self._get_action_definition(action_code)
            timestamp = datetime.now(timezone.utc).isoformat()
            data_to_sign = f"{timestamp}:{action_code}:{self.ia_id}"
            signature = hmac.new(
                self.client_secret,
                data_to_sign.encode(),
                hashlib.sha256
            ).hexdigest()

            context = context or {}
            encrypted_context = {}
            public_context = {}

            for key, value in context.items():
                if action_def.get("sensitive", False):
                    encrypted_context[key] = self._encrypt_value(value)
                else:
                    public_context[key] = value

            domain = None
            for key, value in context.items():
                if "email" in key and isinstance(value, str) and "@" in value:
                    domain_candidate = value.split("@")[1].lower()
                    extracted = tldextract.extract(domain_candidate)
                    if extracted.domain and extracted.suffix:
                        domain = f"{extracted.domain}.{extracted.suffix}"
                    else:
                        domain = None
                    break

            log_payload = {
                "timestamp": timestamp,
                "action": action_code,
                "ia_id": self.ia_id,
                "signature": signature,
                "context_encrypted": encrypted_context,
                "context_public": public_context,
                "encryption_metadata": {
                    "algorithm": "AES-256-GCM",
                    "key_derivation": "SHA-256",
                    "key_owner": "client"
                },
                "domain": domain,
                "registered": registered
            }

            response = requests.post(
                f"{self.endpoint}/receive_log",
                json=log_payload,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=5
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"❌ Error al registrar acción '{action_code}': {str(e)}")
            return False

    def validate_credentials(self) -> bool:
        try:
            response = requests.get(
                f"{self.endpoint}/validate_ia",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=3
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def _encrypt_value(self, plaintext: str) -> str:
        key = hashlib.sha256(self.client_secret).digest()
        nonce = os.urandom(12)
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(str(plaintext).encode()) + encryptor.finalize()
        return "aes256:" + base64.b64encode(nonce + encryptor.tag + ciphertext).decode()

    def semantic_detect_action(self, output_text: str) -> Optional[str]:
        try:
            if not self.semantic_model or not self.semantic_actions:
                print("⚠️ Modelo semántico no disponible.")
                return None

            output_embedding = self.semantic_model.encode(output_text, convert_to_tensor=True)
            scores = util.cos_sim(output_embedding, self.semantic_embeddings)[0]
            best_idx = scores.argmax().item()
            best_score = scores[best_idx].item()

            if best_score > 0.90:
                action_code = self.semantic_actions[best_idx]["code"]
                self.log_action(action_code, context={"output": output_text}, registered=False)
                return action_code
            return None
        except Exception as e:
            print(f"Error en semantic_detect_action: {e}")
            return None