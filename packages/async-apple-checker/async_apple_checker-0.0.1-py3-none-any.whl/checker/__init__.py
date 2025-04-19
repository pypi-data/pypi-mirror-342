import aiohttp
from cryptography import x509
from async_lru import alru_cache
from checker.ocsp_utils import ocsp_check
from checker.entitlement_utils import check_entitlements
from checker.certificate_utils import extract_cert_from_mobileprovision, extract_cert_from_p12, get_certificate_info


@alru_cache(ttl=3600)
async def fetch_certificate(cert_name: str) -> x509.Certificate:
    """Fetch and cache Apple CA certificates."""

    if cert_name.endswith("A"):
        url = "https://developer.apple.com/certificationauthority/AppleWWDRCA.cer" 
    else:
        url = f"https://www.apple.com/certificateauthority/{cert_name}.cer"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch certificate: {cert_name}")

            cert_data = await response.read()
            cert = x509.load_der_x509_certificate(cert_data)

    return cert


async def check_p12(p12_bytes: bytes, password: str = "") -> dict:
    """Check a .p12 certificate."""
    p12_cert = extract_cert_from_p12(p12_bytes, password)
    cert_info = get_certificate_info(p12_cert)

    ocsp_status = "Unknown"
    ca_certs = ["AppleWWDRCA", "AppleWWDRCAG2", "AppleWWDRCAG3", "AppleWWDRCAG4", "AppleWWDRCAG5", "AppleWWDRCAG6"]

    for cert_name in ca_certs:
        try:
            ca_cert = await fetch_certificate(cert_name)
            ocsp_status = await ocsp_check(p12_cert, ca_cert, cert_info["ocsp_url"])

            if ocsp_status in ["ENABLED", "REVOKED"]:
                break
        except Exception as e:
            ocsp_status = f"OCSP check failed: {str(e)}"

    return {
        "certificate_info": cert_info,
        "certificate_status": ocsp_status,
        "entitlements": "Not applicable for p12 files"
    }


async def check_mobileprovision(mobileprovision_bytes: bytes) -> dict:
    """Check a .mobileprovision file."""
    p12_cert, entitlements = extract_cert_from_mobileprovision(mobileprovision_bytes)
    cert_info = get_certificate_info(p12_cert)
    entitlements_info = check_entitlements(entitlements)

    ocsp_status = "Unknown"
    ca_certs = ["AppleWWDRCA", "AppleWWDRCAG2", "AppleWWDRCAG3", "AppleWWDRCAG4", "AppleWWDRCAG5", "AppleWWDRCAG6"]

    for cert_name in ca_certs:
        try:
            ca_cert = await fetch_certificate(cert_name)
            ocsp_status = await ocsp_check(p12_cert, ca_cert, cert_info["ocsp_url"])

            if ocsp_status in ["ENABLED", "REVOKED"]:
                break
        except Exception as e:
            ocsp_status = f"OCSP check failed: {str(e)}"

    return {
        "certificate_info": cert_info,
        "certificate_status": ocsp_status,
        "entitlements": entitlements_info
    }
