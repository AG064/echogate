# Maintainer: EchoGate Team

pkgname=echogate
pkgver=1.0.0
pkgrel=1
pkgdesc="Voice-based authentication using speech recognition"
arch=('any')
url="https://github.com/AG064/echogate"
license=('GPL3')
depends=('python' 'python-sounddevice' 'espeak-ng')
makedepends=('python-pip' 'curl' 'unzip')
source=("echogate.py")
sha256sums=('SKIP')

# Vosk model URL (small English model)
_vosk_model_url="https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
_vosk_model_name="vosk-model-small-en-us-0.15"

package() {
    # Create installation directories
    install -dm755 "${pkgdir}/opt/echogate/libs"
    install -dm755 "${pkgdir}/opt/echogate/model"
    install -dm755 "${pkgdir}/usr/bin"

    # Install vosk to custom libs directory
    pip install --target="${pkgdir}/opt/echogate/libs" --no-deps vosk

    # Download and extract vosk model
    curl -L -o "${srcdir}/vosk-model.zip" "${_vosk_model_url}"
    unzip -q "${srcdir}/vosk-model.zip" -d "${srcdir}"
    cp -r "${srcdir}/${_vosk_model_name}"/* "${pkgdir}/opt/echogate/model/"

    # Install main script
    install -Dm755 "${srcdir}/echogate.py" "${pkgdir}/usr/bin/echogate"
}
