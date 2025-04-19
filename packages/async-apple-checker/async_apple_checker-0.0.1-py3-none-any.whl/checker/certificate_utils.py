import re
import plistlib
import contextlib
from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import pkcs12


def extract_cert_from_mobileprovision(mobileprovision: bytes):
    plist_match = re.search(rb'<\?xml.*?\</plist\>', mobileprovision, re.DOTALL) or re.search(rb'bplist00.*', mobileprovision, re.DOTALL)
    if not plist_match:
        raise ValueError("Plist data not found in the .mobileprovision file.")

    plist_data = plist_match.group()
    plist = plistlib.loads(plist_data)
    cert_data = plist['DeveloperCertificates'][0]
    cert = x509.load_der_x509_certificate(cert_data)
    return cert, {k: v for k, v in plist.get('Entitlements', {}).items() if v}


def extract_cert_from_p12(p12_data: bytes, password: str = ""):

    p12 = pkcs12.load_key_and_certificates(p12_data, password.encode() or None)
    if p12 is None:
        raise ValueError("Incorrect password or unable to load the p12 file.")
    return p12[1]


def get_certificate_info(cert: x509.Certificate) -> dict:
    def process_name(name):
        value = name.value
        return {"original": value, "truncated": value[:61] + "..."} if len(value) > 64 else value

    subject_details = {name.oid._name: process_name(name) for name in cert.subject}
    issuer_details = {name.oid._name: process_name(name) for name in cert.issuer}
    extensions = {ext.oid._name or "Unknown OID": str(ext.value) for ext in cert.extensions}

    return {
        "subject": ",".join([f"{key}={value['truncated'] if isinstance(value, dict) else value}" for key, value in subject_details.items()]),
        "issuer": ",".join([f"{key}={value['truncated'] if isinstance(value, dict) else value}" for key, value in issuer_details.items()]),
        "serial_number": cert.serial_number,
        "signature_algorithm": cert.signature_algorithm_oid._name,
        "valid_from": cert.not_valid_before_utc,
        "expiry_date": cert.not_valid_after_utc,
        "public_key_size": cert.public_key().key_size,
        "fingerprin56": cert.fingerprint(hashes.SHA256()).hex(),
        "ocsp_url": _get_ocsp_url(cert),
        "subject_details": subject_details,
        "issuer_details": issuer_details,
        "public_key_algorithm": cert.public_bytes(encoding=serialization.Encoding.PEM).decode('utf-8'),
        "fingerprint_md5": cert.fingerprint(hashes.MD5()).hex(),
        "fingerprint_sha1": cert.fingerprint(hashes.SHA1()).hex(),
        "signature_value": cert.signature.hex(),
        "extensions": extensions
    }


def _get_ocsp_url(cert: x509.Certificate) -> str:
    with contextlib.suppress(x509.ExtensionNotFound):
        aia = cert.extensions.get_extension_for_class(x509.AuthorityInformationAccess)
        for desc in aia.value:
            if desc.access_method == x509.OID_OCSP:
                return desc.access_location.value
    return None
