# Maintainer: EchoGate Team

pkgname=echogate
pkgver=1.0.0
pkgrel=1
pkgdesc="Voice-based authentication using speech recognition"
arch=('any')
url="https://github.com/AG064/echogate"
license=('GPL3')
depends=('python' 'python-sounddevice' 'espeak-ng')
makedepends=('python-pip' 'unzip')
source=("echogate.py"
        "vosk-model-small-en-us-0.15.zip::https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip")
sha256sums=('SKIP'
            'SKIP')
noextract=('vosk-model-small-en-us-0.15.zip')

_vosk_model_name="vosk-model-small-en-us-0.15"

build() {
    # Install vosk to a local directory for packaging
    pip install --target="${srcdir}/vosk-libs" --no-deps vosk

    # Extract the vosk model
    unzip -q "${srcdir}/vosk-model-small-en-us-0.15.zip" -d "${srcdir}"
}

package() {
    # Create installation directories
    install -dm755 "${pkgdir}/opt/echogate/libs"
    install -dm755 "${pkgdir}/opt/echogate/model"
    install -dm755 "${pkgdir}/usr/bin"

    # Install vosk libraries
    cp -r "${srcdir}/vosk-libs"/* "${pkgdir}/opt/echogate/libs/"

    # Install vosk model
    cp -r "${srcdir}/${_vosk_model_name}"/* "${pkgdir}/opt/echogate/model/"

    # Install main script
    install -Dm755 "${srcdir}/echogate.py" "${pkgdir}/usr/bin/echogate"
}
