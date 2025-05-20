from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
import os

# Папка для хранения сертификатов
cert_dir = "certs"
os.makedirs(cert_dir, exist_ok=True)

# Генерация ключа
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Параметры субъекта и издателя (они одинаковые для самоподписанного)
subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Moscow"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Moscow"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Sweet Treat"),
    x509.NameAttribute(NameOID.COMMON_NAME, "127.0.0.1"),
])

# Генерация сертификата
cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(subject)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.utcnow())
    .not_valid_after(datetime.utcnow() + timedelta(days=365))
    .add_extension(x509.SubjectAlternativeName([x509.DNSName("localhost"), x509.DNSName("127.0.0.1")]), critical=False)
    .sign(key, hashes.SHA256())
)

# Сохранение ключа
with open(os.path.join(cert_dir, "key.pem"), "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))

# Сохранение сертификата
with open(os.path.join(cert_dir, "cert.pem"), "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("✅ Сертификаты успешно сгенерированы в папке certs/")
