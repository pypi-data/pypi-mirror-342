import aiohttp
from cryptography import x509
from cryptography.x509 import ocsp
from cryptography.hazmat.primitives import serialization


async def ocsp_check(p12_cert: x509.Certificate, ca_cert: x509.Certificate, ocsp_url: str) -> str:
    builder = ocsp.OCSPRequestBuilder().add_certificate(p12_cert, ca_cert, p12_cert.signature_hash_algorithm)
    req = builder.build()

    async with aiohttp.ClientSession() as session:
        async with session.post(
            ocsp_url,
            data=req.public_bytes(serialization.Encoding.DER),
            headers={'Content-Type': 'application/ocsp-request'}
        ) as response:
            if response.status != 200:
                return "OCSP request failed"

            response_data = await response.read()
    
    ocsp_response = ocsp.load_der_ocsp_response(response_data)

    if ocsp_response.response_status == ocsp.OCSPResponseStatus.SUCCESSFUL:
        status = ocsp_response.certificate_status
        return "ENABLED" if status == ocsp.OCSPCertStatus.GOOD else "REVOKED" if status == ocsp.OCSPCertStatus.REVOKED else "Unknown"
    else:
        return "OCSP check failed"
